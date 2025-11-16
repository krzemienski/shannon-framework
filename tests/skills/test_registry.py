"""
Tests for Shannon Skills Framework - SkillRegistry

Comprehensive test suite covering:
- Basic registration and retrieval
- Schema validation
- Conflict detection
- Query methods (by category, domain, tags, execution type)
- Thread safety and async operations
- Index management
- Statistics and metrics
- Singleton pattern
"""

import pytest
import asyncio
from pathlib import Path
from datetime import datetime

from shannon.skills.registry import (
    SkillRegistry,
    SkillRegistrationError,
    SkillConflictError,
    SkillValidationError,
    SkillNotFoundError,
)
from shannon.skills.models import (
    Skill,
    Execution,
    ExecutionType,
    Parameter,
    Hooks,
    SkillMetadata,
)


@pytest.fixture
def schema_path():
    """Path to skill schema"""
    return Path(__file__).parent.parent.parent / "schemas" / "skill.schema.json"


@pytest.fixture
def registry(schema_path):
    """Create a fresh registry for each test"""
    SkillRegistry.reset_instance()
    return SkillRegistry(schema_path)


@pytest.fixture
def sample_skill():
    """Create a sample valid skill"""
    return Skill(
        name="test_skill",
        version="1.0.0",
        description="A test skill for unit testing",
        category="testing",
        execution=Execution(
            type=ExecutionType.NATIVE,
            module="shannon.skills.test",
            class_name="TestSkill",
            method="execute"
        ),
        parameters=[
            Parameter(
                name="input_path",
                type="string",
                required=True,
                description="Path to input file"
            )
        ],
        dependencies=["dependency_skill"],
        hooks=Hooks(
            pre=["pre_hook"],
            post=["post_hook"],
            error=["error_hook"]
        ),
        metadata=SkillMetadata(
            author="Test Author",
            tags=["test", "iOS", "swift"]
        )
    )


@pytest.fixture
def another_skill():
    """Create another valid skill with different properties"""
    return Skill(
        name="another_skill",
        version="2.0.0",
        description="Another test skill for testing purposes",
        category="research",
        execution=Execution(
            type=ExecutionType.MCP,
            mcp_server="test_server",
            mcp_tool="test_tool"
        ),
        metadata=SkillMetadata(
            tags=["research", "python", "data"]
        )
    )


class TestRegistryInitialization:
    """Tests for registry initialization"""

    def test_init_success(self, schema_path):
        """Test successful registry initialization"""
        registry = SkillRegistry(schema_path)
        assert registry is not None
        assert len(registry) == 0
        assert registry.schema is not None

    def test_init_missing_schema(self):
        """Test initialization with missing schema file"""
        with pytest.raises(FileNotFoundError):
            SkillRegistry(Path("/nonexistent/schema.json"))

    def test_init_invalid_schema(self, tmp_path):
        """Test initialization with invalid JSON schema"""
        invalid_schema = tmp_path / "invalid.json"
        invalid_schema.write_text("{ invalid json")

        with pytest.raises(Exception):  # Will raise JSONDecodeError
            SkillRegistry(invalid_schema)

    @pytest.mark.asyncio
    async def test_singleton_pattern(self, schema_path):
        """Test singleton pattern for registry"""
        SkillRegistry.reset_instance()

        registry1 = await SkillRegistry.get_instance(schema_path)
        registry2 = await SkillRegistry.get_instance()

        assert registry1 is registry2

    @pytest.mark.asyncio
    async def test_singleton_requires_schema_on_first_call(self):
        """Test that singleton requires schema_path on first call"""
        SkillRegistry.reset_instance()

        with pytest.raises(ValueError, match="schema_path required"):
            await SkillRegistry.get_instance()


class TestSkillRegistration:
    """Tests for skill registration"""

    @pytest.mark.asyncio
    async def test_register_valid_skill(self, registry, sample_skill):
        """Test registering a valid skill"""
        await registry.register(sample_skill)

        assert len(registry) == 1
        assert "test_skill" in registry
        assert registry.exists("test_skill")

        retrieved = registry.get("test_skill")
        assert retrieved is not None
        assert retrieved.name == "test_skill"
        assert retrieved.version == "1.0.0"

    @pytest.mark.asyncio
    async def test_register_updates_metadata(self, registry, sample_skill):
        """Test that registration updates skill metadata timestamps"""
        assert sample_skill.metadata.created is None

        await registry.register(sample_skill)

        registered = registry.get("test_skill")
        assert registered.metadata.created is not None
        assert registered.metadata.updated is not None

    @pytest.mark.asyncio
    async def test_register_multiple_skills(self, registry, sample_skill, another_skill):
        """Test registering multiple skills"""
        await registry.register(sample_skill)
        await registry.register(another_skill)

        assert len(registry) == 2
        assert registry.exists("test_skill")
        assert registry.exists("another_skill")

    @pytest.mark.asyncio
    async def test_register_duplicate_raises_conflict(self, registry, sample_skill):
        """Test that registering duplicate skill raises conflict error"""
        await registry.register(sample_skill)

        # Try to register again
        duplicate = Skill(
            name="test_skill",  # Same name
            version="2.0.0",
            description="A duplicate skill",
            execution=Execution(type=ExecutionType.NATIVE, module="test", class_name="Test", method="run")
        )

        with pytest.raises(SkillConflictError, match="already registered"):
            await registry.register(duplicate)

    @pytest.mark.asyncio
    async def test_register_invalid_skill_raises_validation_error(self, registry):
        """Test that registering invalid skill raises validation error"""
        # Create skill with invalid name (contains uppercase)
        invalid_skill = Skill(
            name="InvalidName",  # Should be snake_case
            version="1.0.0",
            description="Invalid skill",
            execution=Execution(type=ExecutionType.NATIVE, module="test", class_name="Test", method="run")
        )

        with pytest.raises(SkillValidationError):
            await registry.register(invalid_skill)

    @pytest.mark.asyncio
    async def test_register_skill_with_missing_required_field(self, registry):
        """Test that skill missing required fields fails validation"""
        # Create skill without description (required field)
        invalid_skill = Skill(
            name="test_skill",
            version="1.0.0",
            description="",  # Too short, minimum 10 chars
            execution=Execution(type=ExecutionType.NATIVE, module="test", class_name="Test", method="run")
        )

        with pytest.raises(SkillValidationError):
            await registry.register(invalid_skill)


class TestSkillUnregistration:
    """Tests for skill unregistration"""

    @pytest.mark.asyncio
    async def test_unregister_existing_skill(self, registry, sample_skill):
        """Test unregistering an existing skill"""
        await registry.register(sample_skill)
        assert len(registry) == 1

        result = await registry.unregister("test_skill")
        assert result is True
        assert len(registry) == 0
        assert not registry.exists("test_skill")

    @pytest.mark.asyncio
    async def test_unregister_nonexistent_skill(self, registry):
        """Test unregistering a non-existent skill"""
        result = await registry.unregister("nonexistent")
        assert result is False

    @pytest.mark.asyncio
    async def test_unregister_removes_from_indexes(self, registry, sample_skill):
        """Test that unregistration removes skill from indexes"""
        await registry.register(sample_skill)

        # Verify skill is in indexes
        assert len(registry.find_by_category("testing")) == 1
        assert len(registry.find_for_domain("iOS")) == 1

        await registry.unregister("test_skill")

        # Verify skill is removed from indexes
        assert len(registry.find_by_category("testing")) == 0
        assert len(registry.find_for_domain("iOS")) == 0


class TestSkillRetrieval:
    """Tests for skill retrieval and querying"""

    @pytest.mark.asyncio
    async def test_get_existing_skill(self, registry, sample_skill):
        """Test getting an existing skill"""
        await registry.register(sample_skill)

        skill = registry.get("test_skill")
        assert skill is not None
        assert skill.name == "test_skill"

    def test_get_nonexistent_skill(self, registry):
        """Test getting a non-existent skill returns None"""
        skill = registry.get("nonexistent")
        assert skill is None

    @pytest.mark.asyncio
    async def test_exists_method(self, registry, sample_skill):
        """Test exists method"""
        assert not registry.exists("test_skill")

        await registry.register(sample_skill)
        assert registry.exists("test_skill")

    @pytest.mark.asyncio
    async def test_contains_operator(self, registry, sample_skill):
        """Test 'in' operator"""
        assert "test_skill" not in registry

        await registry.register(sample_skill)
        assert "test_skill" in registry

    @pytest.mark.asyncio
    async def test_list_all_empty(self, registry):
        """Test list_all on empty registry"""
        skills = registry.list_all()
        assert len(skills) == 0

    @pytest.mark.asyncio
    async def test_list_all_with_skills(self, registry, sample_skill, another_skill):
        """Test list_all returns all skills sorted by name"""
        await registry.register(sample_skill)
        await registry.register(another_skill)

        skills = registry.list_all()
        assert len(skills) == 2
        # Should be sorted alphabetically
        assert skills[0].name == "another_skill"
        assert skills[1].name == "test_skill"


class TestCategoryQueries:
    """Tests for category-based queries"""

    @pytest.mark.asyncio
    async def test_find_by_category(self, registry, sample_skill, another_skill):
        """Test finding skills by category"""
        await registry.register(sample_skill)  # category: testing
        await registry.register(another_skill)  # category: research

        testing_skills = registry.find_by_category("testing")
        assert len(testing_skills) == 1
        assert testing_skills[0].name == "test_skill"

        research_skills = registry.find_by_category("research")
        assert len(research_skills) == 1
        assert research_skills[0].name == "another_skill"

    @pytest.mark.asyncio
    async def test_find_by_nonexistent_category(self, registry):
        """Test finding skills in non-existent category"""
        skills = registry.find_by_category("nonexistent")
        assert len(skills) == 0

    @pytest.mark.asyncio
    async def test_find_by_category_multiple_skills(self, registry):
        """Test finding multiple skills in same category"""
        skill1 = Skill(
            name="skill1",
            version="1.0.0",
            description="First testing skill",
            category="testing",
            execution=Execution(type=ExecutionType.NATIVE, module="test", class_name="Test", method="run")
        )
        skill2 = Skill(
            name="skill2",
            version="1.0.0",
            description="Second testing skill",
            category="testing",
            execution=Execution(type=ExecutionType.NATIVE, module="test", class_name="Test", method="run")
        )

        await registry.register(skill1)
        await registry.register(skill2)

        testing_skills = registry.find_by_category("testing")
        assert len(testing_skills) == 2
        # Should be sorted
        assert testing_skills[0].name == "skill1"
        assert testing_skills[1].name == "skill2"


class TestDomainQueries:
    """Tests for domain-based queries"""

    @pytest.mark.asyncio
    async def test_find_for_domain(self, registry, sample_skill):
        """Test finding skills for specific domain"""
        await registry.register(sample_skill)  # tags: ["test", "iOS", "swift"]

        ios_skills = registry.find_for_domain("iOS")
        assert len(ios_skills) == 1
        assert ios_skills[0].name == "test_skill"

    @pytest.mark.asyncio
    async def test_find_for_domain_case_insensitive(self, registry, sample_skill):
        """Test domain search is case-insensitive"""
        await registry.register(sample_skill)

        # Should match "iOS" tag regardless of case
        assert len(registry.find_for_domain("ios")) == 1
        assert len(registry.find_for_domain("IOS")) == 1
        assert len(registry.find_for_domain("iOS")) == 1

    @pytest.mark.asyncio
    async def test_find_for_domain_partial_match(self, registry, sample_skill):
        """Test domain search with partial matches"""
        await registry.register(sample_skill)  # tags include "swift"

        # Should match tags containing "swift"
        swift_skills = registry.find_for_domain("swift")
        assert len(swift_skills) == 1

    @pytest.mark.asyncio
    async def test_find_for_nonexistent_domain(self, registry, sample_skill):
        """Test finding skills for non-existent domain"""
        await registry.register(sample_skill)

        android_skills = registry.find_for_domain("Android")
        assert len(android_skills) == 0


class TestTagQueries:
    """Tests for tag-based queries"""

    @pytest.mark.asyncio
    async def test_find_by_tag(self, registry, sample_skill):
        """Test finding skills by tag"""
        await registry.register(sample_skill)  # tags: ["test", "iOS", "swift"]

        test_skills = registry.find_by_tag("test")
        assert len(test_skills) == 1
        assert test_skills[0].name == "test_skill"

    @pytest.mark.asyncio
    async def test_find_by_tag_case_insensitive(self, registry, sample_skill):
        """Test tag search is case-insensitive"""
        await registry.register(sample_skill)

        assert len(registry.find_by_tag("test")) == 1
        assert len(registry.find_by_tag("TEST")) == 1
        assert len(registry.find_by_tag("Test")) == 1

    @pytest.mark.asyncio
    async def test_find_by_nonexistent_tag(self, registry):
        """Test finding skills by non-existent tag"""
        skills = registry.find_by_tag("nonexistent")
        assert len(skills) == 0


class TestExecutionTypeQueries:
    """Tests for execution type queries"""

    @pytest.mark.asyncio
    async def test_find_by_execution_type(self, registry, sample_skill, another_skill):
        """Test finding skills by execution type"""
        await registry.register(sample_skill)  # ExecutionType.NATIVE
        await registry.register(another_skill)  # ExecutionType.MCP

        native_skills = registry.find_by_execution_type(ExecutionType.NATIVE)
        assert len(native_skills) == 1
        assert native_skills[0].name == "test_skill"

        mcp_skills = registry.find_by_execution_type(ExecutionType.MCP)
        assert len(mcp_skills) == 1
        assert mcp_skills[0].name == "another_skill"

    @pytest.mark.asyncio
    async def test_find_by_execution_type_none_found(self, registry, sample_skill):
        """Test finding skills by execution type with no matches"""
        await registry.register(sample_skill)  # ExecutionType.NATIVE

        script_skills = registry.find_by_execution_type(ExecutionType.SCRIPT)
        assert len(script_skills) == 0


class TestStatistics:
    """Tests for registry statistics"""

    @pytest.mark.asyncio
    async def test_statistics_empty_registry(self, registry):
        """Test statistics on empty registry"""
        stats = registry.get_statistics()

        assert stats['total_skills'] == 0
        assert stats['avg_parameters'] == 0
        assert stats['skills_with_dependencies'] == 0
        assert stats['skills_with_hooks'] == 0

    @pytest.mark.asyncio
    async def test_statistics_with_skills(self, registry, sample_skill, another_skill):
        """Test statistics with registered skills"""
        await registry.register(sample_skill)
        await registry.register(another_skill)

        stats = registry.get_statistics()

        assert stats['total_skills'] == 2
        assert stats['categories']['testing'] == 1
        assert stats['categories']['research'] == 1
        assert stats['execution_types']['native'] == 1
        assert stats['execution_types']['mcp'] == 1
        assert stats['skills_with_dependencies'] == 1  # sample_skill has dependency
        assert stats['skills_with_hooks'] == 1  # sample_skill has hooks
        assert 'domains' in stats

    @pytest.mark.asyncio
    async def test_statistics_average_parameters(self, registry):
        """Test average parameters calculation"""
        skill1 = Skill(
            name="skill1",
            version="1.0.0",
            description="Skill with 2 parameters",
            execution=Execution(type=ExecutionType.NATIVE, module="test", class_name="Test", method="run"),
            parameters=[
                Parameter(name="param1", type="string"),
                Parameter(name="param2", type="integer")
            ]
        )
        skill2 = Skill(
            name="skill2",
            version="1.0.0",
            description="Skill with 0 parameters",
            execution=Execution(type=ExecutionType.NATIVE, module="test", class_name="Test", method="run")
        )

        await registry.register(skill1)
        await registry.register(skill2)

        stats = registry.get_statistics()
        assert stats['avg_parameters'] == 1.0  # (2 + 0) / 2


class TestThreadSafety:
    """Tests for thread safety and concurrent access"""

    @pytest.mark.asyncio
    async def test_concurrent_registration(self, registry):
        """Test concurrent skill registration is thread-safe"""
        skills = [
            Skill(
                name=f"skill_{i}",
                version="1.0.0",
                description=f"Concurrent test skill number {i}",
                execution=Execution(type=ExecutionType.NATIVE, module="test", class_name="Test", method="run")
            )
            for i in range(10)
        ]

        # Register all skills concurrently
        await asyncio.gather(*[registry.register(skill) for skill in skills])

        # All should be registered
        assert len(registry) == 10
        for i in range(10):
            assert registry.exists(f"skill_{i}")

    @pytest.mark.asyncio
    async def test_concurrent_registration_and_unregistration(self, registry):
        """Test concurrent registration and unregistration"""
        # Register initial skills
        initial_skills = [
            Skill(
                name=f"skill_{i}",
                version="1.0.0",
                description=f"Test skill {i}",
                execution=Execution(type=ExecutionType.NATIVE, module="test", class_name="Test", method="run")
            )
            for i in range(5)
        ]

        for skill in initial_skills:
            await registry.register(skill)

        # Mix of registration and unregistration
        async def register_skill(i):
            skill = Skill(
                name=f"new_skill_{i}",
                version="1.0.0",
                description=f"New skill {i}",
                execution=Execution(type=ExecutionType.NATIVE, module="test", class_name="Test", method="run")
            )
            await registry.register(skill)

        async def unregister_skill(i):
            await registry.unregister(f"skill_{i}")

        # Execute concurrently
        tasks = []
        for i in range(5):
            tasks.append(register_skill(i))
            tasks.append(unregister_skill(i))

        await asyncio.gather(*tasks)

        # Should have 5 new skills, 0 old skills
        assert len(registry) == 5
        for i in range(5):
            assert registry.exists(f"new_skill_{i}")
            assert not registry.exists(f"skill_{i}")

    @pytest.mark.asyncio
    async def test_concurrent_reads_during_writes(self, registry, sample_skill):
        """Test that concurrent reads work during writes"""
        await registry.register(sample_skill)

        # Concurrent readers
        async def read_skill():
            return registry.get("test_skill")

        # Concurrent writer
        async def write_skill(i):
            skill = Skill(
                name=f"concurrent_{i}",
                version="1.0.0",
                description=f"Concurrent skill {i}",
                execution=Execution(type=ExecutionType.NATIVE, module="test", class_name="Test", method="run")
            )
            await registry.register(skill)

        # Mix reads and writes
        tasks = [read_skill() for _ in range(20)] + [write_skill(i) for i in range(5)]

        results = await asyncio.gather(*tasks)

        # All read operations should have succeeded
        read_results = results[:20]
        for result in read_results:
            assert result is not None
            assert result.name == "test_skill"


class TestMagicMethods:
    """Tests for magic methods and operators"""

    @pytest.mark.asyncio
    async def test_len_operator(self, registry, sample_skill, another_skill):
        """Test len() operator"""
        assert len(registry) == 0

        await registry.register(sample_skill)
        assert len(registry) == 1

        await registry.register(another_skill)
        assert len(registry) == 2

    @pytest.mark.asyncio
    async def test_repr(self, registry, sample_skill):
        """Test string representation"""
        repr_str = repr(registry)
        assert "SkillRegistry" in repr_str
        assert "0 skills" in repr_str

        await registry.register(sample_skill)
        repr_str = repr(registry)
        assert "1 skills" in repr_str


class TestIndexManagement:
    """Tests for internal index management"""

    @pytest.mark.asyncio
    async def test_indexes_updated_on_registration(self, registry, sample_skill):
        """Test that indexes are updated when skill is registered"""
        await registry.register(sample_skill)

        # Check internal indexes (accessing private attributes for testing)
        assert "testing" in registry._category_index
        assert "test_skill" in registry._category_index["testing"]

        for tag in sample_skill.metadata.tags:
            assert tag in registry._tag_index
            assert "test_skill" in registry._tag_index[tag]

    @pytest.mark.asyncio
    async def test_indexes_cleaned_on_unregistration(self, registry, sample_skill):
        """Test that indexes are cleaned when skill is unregistered"""
        await registry.register(sample_skill)
        await registry.unregister("test_skill")

        # Empty indexes should be removed
        assert "testing" not in registry._category_index or not registry._category_index["testing"]

        for tag in sample_skill.metadata.tags:
            assert tag not in registry._tag_index or not registry._tag_index[tag]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
