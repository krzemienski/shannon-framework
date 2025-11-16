"""
Tests for Shannon Skills Catalog - Persistent Skill Caching

Tests the SkillCatalog's ability to save and load skill catalogs from Memory MCP
with proper TTL handling and graceful degradation.

Test Coverage:
- Save catalog to Memory MCP (with mock)
- Load catalog from Memory MCP (with mock)
- Cache freshness validation
- Graceful failure when Memory MCP unavailable
- Cache invalidation
- Statistics reporting
"""

import pytest
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch, Mock

from shannon.skills.catalog import SkillCatalog, SkillCatalogError
from shannon.skills.models import (
    Skill,
    Execution,
    ExecutionType,
    SkillMetadata,
    Parameter
)
from shannon.skills.registry import SkillRegistry


# Create mock MCP module for testing
class MockMCP:
    """Mock MCP module for testing"""
    create_entities = AsyncMock()
    search_nodes = AsyncMock()
    delete_entities = AsyncMock()
    add_observations = AsyncMock()


@pytest.fixture
def mock_schema_path(tmp_path):
    """Create a mock schema file"""
    schema_path = tmp_path / "skill.schema.json"
    schema_path.write_text(json.dumps({
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "version": {"type": "string"},
            "description": {"type": "string"},
            "category": {"type": "string"},
            "execution": {"type": "object"}
        },
        "required": ["name", "version", "description", "execution"]
    }))
    return schema_path


@pytest.fixture
def registry(mock_schema_path):
    """Create a SkillRegistry instance"""
    return SkillRegistry(schema_path=mock_schema_path)


@pytest.fixture
def catalog(registry):
    """Create a SkillCatalog instance"""
    return SkillCatalog(registry=registry, cache_ttl_days=7)


@pytest.fixture
def sample_skills():
    """Create sample skills for testing"""
    return [
        Skill(
            name="skill_one",
            version="1.0.0",
            description="First test skill",
            category="testing",
            execution=Execution(
                type=ExecutionType.NATIVE,
                module="test.module",
                method="execute"
            ),
            metadata=SkillMetadata(
                tags=["test", "sample"]
            )
        ),
        Skill(
            name="skill_two",
            version="2.0.0",
            description="Second test skill",
            category="validation",
            execution=Execution(
                type=ExecutionType.SCRIPT,
                script="/usr/bin/test.sh"
            ),
            parameters=[
                Parameter(
                    name="param1",
                    type="string",
                    required=True,
                    description="Test parameter"
                )
            ],
            metadata=SkillMetadata(
                tags=["test", "script"]
            )
        )
    ]


@pytest.fixture
def project_root(tmp_path):
    """Create a temporary project root"""
    return tmp_path / "test_project"


class TestCatalogInitialization:
    """Test catalog initialization and configuration"""

    def test_catalog_init(self, catalog):
        """Test catalog initializes correctly"""
        assert catalog.cache_ttl_days == 7
        assert catalog._memory_mcp_available is None
        assert catalog._lock is not None

    def test_catalog_custom_ttl(self, registry):
        """Test catalog with custom TTL"""
        catalog = SkillCatalog(registry=registry, cache_ttl_days=14)
        assert catalog.cache_ttl_days == 14

    def test_catalog_repr(self, catalog):
        """Test catalog string representation"""
        repr_str = repr(catalog)
        assert "SkillCatalog" in repr_str
        assert "TTL=7d" in repr_str


class TestCacheFreshness:
    """Test cache freshness validation"""

    def test_is_cache_fresh_recent(self, catalog):
        """Test fresh cache (< TTL)"""
        recent_time = datetime.now() - timedelta(days=3)
        assert catalog.is_cache_fresh(recent_time.isoformat()) is True

    def test_is_cache_fresh_boundary(self, catalog):
        """Test cache at TTL boundary"""
        boundary_time = datetime.now() - timedelta(days=6, hours=23)
        assert catalog.is_cache_fresh(boundary_time.isoformat()) is True

    def test_is_cache_stale(self, catalog):
        """Test stale cache (> TTL)"""
        stale_time = datetime.now() - timedelta(days=8)
        assert catalog.is_cache_fresh(stale_time.isoformat()) is False

    def test_is_cache_fresh_invalid_timestamp(self, catalog):
        """Test with invalid timestamp"""
        assert catalog.is_cache_fresh("invalid-timestamp") is False
        assert catalog.is_cache_fresh("") is False

    def test_is_cache_fresh_none(self, catalog):
        """Test with None timestamp"""
        assert catalog.is_cache_fresh(None) is False


class TestCatalogStatistics:
    """Test catalog statistics"""

    def test_get_stats_initial(self, catalog):
        """Test statistics when no operations performed"""
        stats = catalog.get_stats()

        assert stats['cache_ttl_days'] == 7
        assert stats['memory_mcp_available'] is None
        assert stats['registry_skill_count'] == 0


class TestParseSearchResult:
    """Test search result parsing"""

    def test_parse_dict_with_nodes(self, catalog):
        """Test parsing dict with 'nodes' key"""
        result = {'nodes': [{'id': 1}, {'id': 2}]}
        nodes = catalog._parse_search_result(result)
        assert len(nodes) == 2
        assert nodes[0]['id'] == 1

    def test_parse_list(self, catalog):
        """Test parsing list directly"""
        result = [{'id': 1}, {'id': 2}]
        nodes = catalog._parse_search_result(result)
        assert len(nodes) == 2

    def test_parse_unexpected_format(self, catalog):
        """Test parsing unexpected format"""
        result = "unexpected"
        nodes = catalog._parse_search_result(result)
        assert nodes == []


class TestMemoryMCPOperations:
    """Test Memory MCP integration with mocks"""

    @pytest.mark.asyncio
    async def test_save_catalog_when_mcp_available(self, catalog, sample_skills, project_root):
        """Test successful catalog save when MCP is available"""
        # Create mock MCP module
        mock_mcp = MockMCP()
        mock_mcp.create_entities = AsyncMock()

        # Inject mock into sys.modules before operation
        sys.modules['mcp'] = mock_mcp

        try:
            # Reset cached availability state
            catalog._memory_mcp_available = None

            result = await catalog.save_to_memory(sample_skills, project_root)

            assert result is True
            assert mock_mcp.create_entities.called

            # Verify the call structure
            call_args = mock_mcp.create_entities.call_args[0][0]
            assert 'entities' in call_args
            assert len(call_args['entities']) == 1

            entity = call_args['entities'][0]
            assert entity['entityType'] == 'SkillCatalog'
            assert entity['name'] == f"skill_catalog_{project_root.name}"

            # Verify catalog data
            catalog_data = json.loads(entity['observations'][0])
            assert catalog_data['skill_count'] == 2
            assert len(catalog_data['skills']) == 2

        finally:
            # Clean up mock module
            if 'mcp' in sys.modules:
                del sys.modules['mcp']
            catalog._memory_mcp_available = None

    @pytest.mark.asyncio
    async def test_save_catalog_when_mcp_unavailable(self, catalog, sample_skills, project_root):
        """Test save when Memory MCP unavailable"""
        # Ensure mcp is not importable
        if 'mcp' in sys.modules:
            del sys.modules['mcp']

        # Reset cached state
        catalog._memory_mcp_available = None

        result = await catalog.save_to_memory(sample_skills, project_root)
        assert result is False
        assert catalog._memory_mcp_available is False

    @pytest.mark.asyncio
    async def test_load_catalog_when_mcp_available(self, catalog, sample_skills, project_root):
        """Test successful catalog load when MCP is available"""
        # Create mock MCP module
        mock_mcp = MockMCP()

        # Prepare mock search result
        catalog_data = {
            'skills': [s.to_dict() for s in sample_skills],
            'discovered_at': datetime.now().isoformat(),
            'project_root': str(project_root.resolve()),
            'skill_count': len(sample_skills),
            'cache_version': '1.0',
            'ttl_days': 7
        }

        mock_search_result = {
            'nodes': [{
                'name': f"skill_catalog_{project_root.name}",
                'entityType': 'SkillCatalog',
                'observations': [json.dumps(catalog_data)]
            }]
        }

        mock_mcp.search_nodes = AsyncMock(return_value=mock_search_result)
        sys.modules['mcp'] = mock_mcp

        try:
            catalog._memory_mcp_available = None

            skills = await catalog.load_from_memory(project_root)

            assert skills is not None
            assert len(skills) == 2
            assert skills[0].name == "skill_one"
            assert skills[1].name == "skill_two"

        finally:
            if 'mcp' in sys.modules:
                del sys.modules['mcp']
            catalog._memory_mcp_available = None

    @pytest.mark.asyncio
    async def test_load_catalog_stale_cache(self, catalog, sample_skills, project_root):
        """Test load with stale cache (> TTL)"""
        mock_mcp = MockMCP()

        # Create stale timestamp (8 days old, TTL is 7)
        stale_time = datetime.now() - timedelta(days=8)

        catalog_data = {
            'skills': [s.to_dict() for s in sample_skills],
            'discovered_at': stale_time.isoformat(),
            'project_root': str(project_root.resolve()),
            'skill_count': len(sample_skills)
        }

        mock_search_result = {
            'nodes': [{
                'observations': [json.dumps(catalog_data)]
            }]
        }

        mock_mcp.search_nodes = AsyncMock(return_value=mock_search_result)
        sys.modules['mcp'] = mock_mcp

        try:
            catalog._memory_mcp_available = None
            skills = await catalog.load_from_memory(project_root)
            assert skills is None  # Stale cache returns None

        finally:
            if 'mcp' in sys.modules:
                del sys.modules['mcp']
            catalog._memory_mcp_available = None

    @pytest.mark.asyncio
    async def test_invalidate_cache_when_mcp_available(self, catalog, project_root):
        """Test cache invalidation when MCP is available"""
        mock_mcp = MockMCP()
        mock_mcp.delete_entities = AsyncMock()
        sys.modules['mcp'] = mock_mcp

        try:
            catalog._memory_mcp_available = None

            result = await catalog.invalidate_cache(project_root)

            assert result is True
            assert mock_mcp.delete_entities.called

            call_args = mock_mcp.delete_entities.call_args[0][0]
            assert 'entityNames' in call_args
            assert call_args['entityNames'] == [f"skill_catalog_{project_root.name}"]

        finally:
            if 'mcp' in sys.modules:
                del sys.modules['mcp']
            catalog._memory_mcp_available = None


class TestGracefulDegradation:
    """Test graceful degradation when MCP unavailable"""

    @pytest.mark.asyncio
    async def test_all_operations_fail_gracefully(self, catalog, sample_skills, project_root):
        """Test all operations handle MCP unavailability gracefully"""
        # Ensure mcp is not available
        if 'mcp' in sys.modules:
            del sys.modules['mcp']
        catalog._memory_mcp_available = None

        # All operations should return False/None without raising
        save_result = await catalog.save_to_memory(sample_skills, project_root)
        assert save_result is False

        load_result = await catalog.load_from_memory(project_root)
        assert load_result is None

        invalidate_result = await catalog.invalidate_cache(project_root)
        assert invalidate_result is False

        # MCP should be marked as unavailable
        assert catalog._memory_mcp_available is False
