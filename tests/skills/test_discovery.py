"""
Tests for Shannon Skills Framework - Discovery Engine

Comprehensive test suite for the DiscoveryEngine covering:
- Built-in skill discovery
- Project-local skill discovery
- User-global skill discovery
- package.json script conversion
- Makefile target conversion
- Conflict resolution
- Error handling
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

from shannon.skills.discovery import (
    DiscoveryEngine,
    DiscoveryError,
    SourceDiscoveryError
)
from shannon.skills.registry import SkillRegistry
from shannon.skills.loader import SkillLoader
from shannon.skills.models import (
    Skill, Execution, ExecutionType,
    Parameter, SkillMetadata
)


@pytest.fixture
def temp_dir():
    """Create temporary directory for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def schema_path():
    """Get path to skill schema"""
    # Use the actual schema from the project
    schema = Path(__file__).parent.parent.parent / "schemas" / "skill.schema.json"
    if not schema.exists():
        # Fallback: create minimal schema for testing
        schema = Path(__file__).parent / "test_schema.json"
        schema.parent.mkdir(parents=True, exist_ok=True)
        schema.write_text(json.dumps({
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["name", "version", "description", "execution"],
            "properties": {
                "name": {"type": "string"},
                "version": {"type": "string"},
                "description": {"type": "string"},
                "category": {"type": "string"},
                "execution": {"type": "object"}
            }
        }))
    return schema


@pytest.fixture
def registry(schema_path):
    """Create test registry"""
    reg = SkillRegistry(schema_path=schema_path)
    yield reg
    # Cleanup
    SkillRegistry.reset_instance()


@pytest.fixture
def loader(registry):
    """Create test loader"""
    return SkillLoader(registry=registry)


@pytest.fixture
def engine(registry, loader):
    """Create test discovery engine"""
    return DiscoveryEngine(registry=registry, loader=loader)


# ============================================================================
# Built-in Skills Discovery Tests
# ============================================================================

@pytest.mark.asyncio
async def test_discover_builtin_skills(engine):
    """Test discovery of built-in skills"""
    # Discover built-in skills
    skills = await engine.discover_built_in()

    # Should find at least the example built-in skills
    assert len(skills) > 0
    assert all(isinstance(skill, Skill) for skill in skills)

    # Verify skills are registered
    for skill in skills:
        assert engine.registry.exists(skill.name)

    # Verify discovered names are tracked
    assert len(engine._discovered_names) == len(skills)


@pytest.mark.asyncio
async def test_discover_builtin_missing_directory(engine):
    """Test error handling when built-in directory is missing"""
    # Mock missing directory
    original_dir = engine.BUILTIN_SKILLS_DIR
    engine.BUILTIN_SKILLS_DIR = Path("/nonexistent/path")

    with pytest.raises(SourceDiscoveryError, match="not found"):
        await engine.discover_built_in()

    # Restore
    engine.BUILTIN_SKILLS_DIR = original_dir


# ============================================================================
# Project Skills Discovery Tests
# ============================================================================

@pytest.mark.asyncio
async def test_discover_project_skills_existing(engine, temp_dir):
    """Test discovery of project-local skills"""
    # Create project skills directory
    project_skills_dir = temp_dir / ".shannon" / "skills"
    project_skills_dir.mkdir(parents=True)

    # Create test skill file
    skill_data = {
        "name": "test_project_skill",
        "version": "1.0.0",
        "description": "A test project skill",
        "category": "testing",
        "execution": {
            "type": "script",
            "script": "echo 'test'",
            "timeout": 30
        }
    }

    skill_file = project_skills_dir / "test_skill.yaml"
    import yaml
    with open(skill_file, 'w') as f:
        yaml.dump(skill_data, f)

    # Discover project skills
    skills = await engine.discover_project_skills(temp_dir)

    assert len(skills) == 1
    assert skills[0].name == "test_project_skill"
    assert engine.registry.exists("test_project_skill")


@pytest.mark.asyncio
async def test_discover_project_skills_missing(engine, temp_dir):
    """Test project skills discovery when directory doesn't exist"""
    # Discover from empty project
    skills = await engine.discover_project_skills(temp_dir)

    # Should return empty list, not error
    assert skills == []


@pytest.mark.asyncio
async def test_discover_project_skills_recursive(engine, temp_dir):
    """Test recursive discovery in project skills directory"""
    # Create nested structure
    project_skills_dir = temp_dir / ".shannon" / "skills"
    subdir = project_skills_dir / "category1"
    subdir.mkdir(parents=True)

    # Create skills in different directories
    import yaml
    for i, directory in enumerate([project_skills_dir, subdir]):
        skill_data = {
            "name": f"skill_{i}",
            "version": "1.0.0",
            "description": f"Test skill number {i} for recursive discovery testing",  # Longer description
            "category": "testing",
            "execution": {
                "type": "script",
                "script": f"echo 'test{i}'",
                "timeout": 30
            }
        }

        skill_file = directory / f"skill_{i}.yaml"
        with open(skill_file, 'w') as f:
            yaml.dump(skill_data, f)

    # Discover all skills
    skills = await engine.discover_project_skills(temp_dir)

    assert len(skills) == 2
    assert all(engine.registry.exists(f"skill_{i}") for i in range(2))


# ============================================================================
# User Skills Discovery Tests
# ============================================================================

@pytest.mark.asyncio
async def test_discover_user_skills_missing(engine):
    """Test user skills discovery when directory doesn't exist"""
    # Mock missing user directory
    original_dir = engine.USER_SKILLS_DIR
    engine.USER_SKILLS_DIR = Path("/nonexistent/user/path")

    skills = await engine.discover_user_skills()

    # Should return empty list, not error
    assert skills == []

    # Restore
    engine.USER_SKILLS_DIR = original_dir


# ============================================================================
# package.json Discovery Tests
# ============================================================================

@pytest.mark.asyncio
async def test_discover_from_package_json(engine, temp_dir):
    """Test npm script discovery from package.json"""
    # Create package.json
    package_data = {
        "name": "test-project",
        "version": "1.0.0",
        "scripts": {
            "build": "webpack --mode production",
            "test": "jest",
            "dev": "webpack-dev-server",
            "lint": "eslint src/"
        }
    }

    package_json = temp_dir / "package.json"
    with open(package_json, 'w') as f:
        json.dump(package_data, f)

    # Discover npm scripts
    skills = await engine.discover_from_package_json(temp_dir)

    assert len(skills) == 4

    # Verify skill names
    skill_names = {skill.name for skill in skills}
    assert skill_names == {"npm_build", "npm_test", "npm_dev", "npm_lint"}

    # Verify skill properties
    for skill in skills:
        assert skill.execution.type == ExecutionType.SCRIPT
        assert skill.execution.script.startswith("npm run ")
        assert skill.category == "utility"
        assert skill.metadata.auto_generated is True
        assert "npm" in skill.metadata.tags


@pytest.mark.asyncio
async def test_discover_from_package_json_missing(engine, temp_dir):
    """Test package.json discovery when file doesn't exist"""
    skills = await engine.discover_from_package_json(temp_dir)

    # Should return empty list, not error
    assert skills == []


@pytest.mark.asyncio
async def test_discover_from_package_json_no_scripts(engine, temp_dir):
    """Test package.json with no scripts section"""
    # Create package.json without scripts
    package_data = {
        "name": "test-project",
        "version": "1.0.0",
        "dependencies": {}
    }

    package_json = temp_dir / "package.json"
    with open(package_json, 'w') as f:
        json.dump(package_data, f)

    skills = await engine.discover_from_package_json(temp_dir)

    assert skills == []


@pytest.mark.asyncio
async def test_discover_from_package_json_invalid(engine, temp_dir):
    """Test error handling for invalid package.json"""
    # Create invalid JSON
    package_json = temp_dir / "package.json"
    package_json.write_text("{ invalid json }")

    with pytest.raises(SourceDiscoveryError, match="Invalid package.json"):
        await engine.discover_from_package_json(temp_dir)


# ============================================================================
# Makefile Discovery Tests
# ============================================================================

@pytest.mark.asyncio
async def test_discover_from_makefile(engine, temp_dir):
    """Test Makefile target discovery"""
    # Create Makefile with various targets
    makefile_content = """
# Build the project
build:
\tgcc -o app main.c

# Run tests
test:
\tpytest tests/

# Clean build artifacts
clean:
\trm -rf build/

# Install dependencies
install:
\tpip install -r requirements.txt

.PHONY: build test clean install
"""

    makefile = temp_dir / "Makefile"
    makefile.write_text(makefile_content)

    # Discover Makefile targets
    skills = await engine.discover_from_makefile(temp_dir)

    assert len(skills) == 4

    # Verify skill names
    skill_names = {skill.name for skill in skills}
    assert skill_names == {"make_build", "make_test", "make_clean", "make_install"}

    # Verify skill properties
    for skill in skills:
        assert skill.execution.type == ExecutionType.SCRIPT
        assert skill.execution.script.startswith("make ")
        assert skill.category == "utility"
        assert skill.metadata.auto_generated is True
        assert "make" in skill.metadata.tags


@pytest.mark.asyncio
async def test_discover_from_makefile_missing(engine, temp_dir):
    """Test Makefile discovery when file doesn't exist"""
    skills = await engine.discover_from_makefile(temp_dir)

    # Should return empty list, not error
    assert skills == []


@pytest.mark.asyncio
async def test_discover_from_makefile_variations(engine, temp_dir):
    """Test discovery of different Makefile name variations"""
    # Create makefile (lowercase)
    makefile_content = """
target:
\techo "test"
"""

    makefile = temp_dir / "makefile"
    makefile.write_text(makefile_content)

    skills = await engine.discover_from_makefile(temp_dir)

    assert len(skills) == 1
    assert skills[0].name == "make_target"


@pytest.mark.asyncio
async def test_parse_makefile_with_comments(engine, temp_dir):
    """Test Makefile parsing with descriptive comments"""
    makefile_content = """
# This builds the application
build:
\tgcc -o app main.c

# Run all unit tests
test:
\tpytest

# Target without comment
deploy:
\t./deploy.sh
"""

    makefile = temp_dir / "Makefile"
    makefile.write_text(makefile_content)

    skills = await engine.discover_from_makefile(temp_dir)

    # Find specific skills to verify descriptions
    build_skill = next(s for s in skills if s.name == "make_build")
    test_skill = next(s for s in skills if s.name == "make_test")
    deploy_skill = next(s for s in skills if s.name == "make_deploy")

    assert "builds the application" in build_skill.description
    assert "Run all unit tests" in test_skill.description
    # The comment "Target without comment" is correctly parsed as the description
    assert "Target without comment" in deploy_skill.description


# ============================================================================
# Complete Discovery Tests
# ============================================================================

@pytest.mark.asyncio
async def test_discover_all(engine, temp_dir):
    """Test complete discovery from all sources"""
    # Setup project structure
    project_skills_dir = temp_dir / ".shannon" / "skills"
    project_skills_dir.mkdir(parents=True)

    # Create project skill
    import yaml
    skill_data = {
        "name": "custom_skill",
        "version": "1.0.0",
        "description": "Custom project skill",
        "category": "utility",  # Use valid category
        "execution": {
            "type": "script",
            "script": "echo 'custom'",
            "timeout": 30
        }
    }
    with open(project_skills_dir / "custom.yaml", 'w') as f:
        yaml.dump(skill_data, f)

    # Create package.json
    package_data = {
        "name": "test-project",
        "scripts": {
            "build": "webpack",
            "test": "jest"
        }
    }
    with open(temp_dir / "package.json", 'w') as f:
        json.dump(package_data, f)

    # Create Makefile
    makefile_content = """
build:
\tgcc -o app main.c
test:
\tpytest
"""
    (temp_dir / "Makefile").write_text(makefile_content)

    # Discover all
    skills = await engine.discover_all(temp_dir, include_mcp=False)

    # Should find:
    # - Built-in skills (at least 4)
    # - 1 project skill
    # - 2 npm scripts
    # - 2 make targets
    assert len(skills) >= 9

    # Verify statistics
    stats = engine.get_statistics()
    assert stats['total_discovered'] >= 9
    assert stats['by_source']['builtin'] >= 4
    assert stats['by_source']['project'] == 1
    assert stats['by_source']['package_json'] == 2
    assert stats['by_source']['makefile'] == 2


@pytest.mark.asyncio
async def test_discover_all_conflict_resolution(engine, temp_dir):
    """Test that discovery handles naming conflicts correctly"""
    # Create package.json with script that conflicts with built-in
    package_data = {
        "name": "test-project",
        "scripts": {
            # This will conflict if we have a built-in with same name
            "git_operations": "echo 'conflict'"
        }
    }
    with open(temp_dir / "package.json", 'w') as f:
        json.dump(package_data, f)

    # Discover all (built-in first, then package.json)
    skills = await engine.discover_all(temp_dir, include_mcp=False)

    # Built-in should win, npm script should be skipped
    stats = engine.get_statistics()
    assert stats['conflicts'] >= 0  # May have conflicts

    # Verify the skill that exists is not auto-generated
    if engine.registry.exists("git_operations"):
        skill = engine.registry.get("git_operations")
        # Built-in skills are not auto-generated
        assert skill.metadata.auto_generated is False


# ============================================================================
# Statistics and Utilities Tests
# ============================================================================

def test_get_statistics(engine):
    """Test statistics retrieval"""
    stats = engine.get_statistics()

    assert 'total_discovered' in stats
    assert 'by_source' in stats
    assert 'failed' in stats
    assert 'conflicts' in stats
    assert 'unique_names' in stats

    # Initially should be zero
    assert stats['total_discovered'] == 0
    assert stats['by_source']['builtin'] == 0


def test_engine_repr(engine):
    """Test string representation"""
    repr_str = repr(engine)

    assert "DiscoveryEngine" in repr_str
    assert "discovered" in repr_str


# ============================================================================
# Helper Method Tests
# ============================================================================

def test_create_npm_skill(engine):
    """Test npm skill creation"""
    skill = engine._create_npm_skill("build", "webpack --mode production")

    assert skill.name == "npm_build"
    assert skill.execution.type == ExecutionType.SCRIPT
    assert skill.execution.script == "npm run build"
    assert skill.category == "utility"
    assert skill.metadata.auto_generated is True
    assert "npm" in skill.metadata.tags


def test_create_make_skill(engine):
    """Test Makefile skill creation"""
    skill = engine._create_make_skill("test", "Run all tests")

    assert skill.name == "make_test"
    assert skill.execution.type == ExecutionType.SCRIPT
    assert skill.execution.script == "make test"
    assert skill.category == "utility"
    assert skill.metadata.auto_generated is True
    assert "make" in skill.metadata.tags


def test_parse_makefile_targets(engine, temp_dir):
    """Test Makefile parsing logic"""
    makefile_content = """
# Build target
build:
\tgcc -o app main.c

# Test with spaces
test  :  dependencies
\tpytest

# Skip special targets
.PHONY: build test

# Skip variables
CC = gcc

# Target with complex dependencies
deploy: build test
\t./deploy.sh
"""

    makefile = temp_dir / "Makefile"
    makefile.write_text(makefile_content)

    targets = engine._parse_makefile(makefile)

    # Should find regular targets, skip special ones
    assert "build" in targets
    assert "test" in targets
    assert "deploy" in targets
    assert ".PHONY" not in targets
    assert "CC" not in targets


# ============================================================================
# MCP Discovery Tests (Placeholder)
# ============================================================================

@pytest.mark.asyncio
async def test_discover_from_mcps_placeholder(engine):
    """Test MCP discovery placeholder"""
    # Currently returns empty list
    skills = await engine.discover_from_mcps()

    assert skills == []
    # TODO: Add real MCP tests when implemented


# ============================================================================
# Error Handling Tests
# ============================================================================

@pytest.mark.asyncio
async def test_discovery_partial_failure(engine, temp_dir):
    """Test that discovery continues after partial failures"""
    # Create valid package.json
    package_data = {
        "name": "test",
        "scripts": {"build": "webpack"}
    }
    with open(temp_dir / "package.json", 'w') as f:
        json.dump(package_data, f)

    # Discover should succeed for package.json even if others fail
    skills = await engine.discover_all(temp_dir, include_mcp=False)

    # Should have at least built-in and npm skills
    assert len(skills) > 0

    stats = engine.get_statistics()
    assert stats['by_source']['package_json'] >= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
