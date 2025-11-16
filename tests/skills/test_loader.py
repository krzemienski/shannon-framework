"""
Tests for Shannon Skills Framework - SkillLoader

Comprehensive test suite covering:
- Loading from YAML files
- Loading from JSON files
- Schema validation (valid and invalid skills)
- Batch loading from directories
- Error handling for malformed files
- Edge cases and error recovery
"""

import pytest
import asyncio
import tempfile
import json
import yaml
from pathlib import Path
from typing import Dict, Any

from shannon.skills.loader import (
    SkillLoader,
    SkillLoadError,
    SkillParseError,
    SkillFileError,
)
from shannon.skills.registry import (
    SkillRegistry,
    SkillValidationError,
    SkillConflictError,
)
from shannon.skills.models import Skill, ExecutionType


# Sample valid skill definition for testing
VALID_SKILL_YAML = """
name: test_skill
version: 1.0.0
description: A test skill for unit testing the loader
category: testing
parameters:
  - name: test_param
    type: string
    required: true
    description: A test parameter
execution:
  type: native
  module: shannon.skills.test
  class: TestSkill
  method: execute
  timeout: 60
  retry: 1
metadata:
  author: Test Suite
  tags:
    - testing
    - unit-test
"""

# Same skill as JSON
VALID_SKILL_JSON = {
    "name": "test_skill",
    "version": "1.0.0",
    "description": "A test skill for unit testing the loader",
    "category": "testing",
    "parameters": [
        {
            "name": "test_param",
            "type": "string",
            "required": True,
            "description": "A test parameter"
        }
    ],
    "execution": {
        "type": "native",
        "module": "shannon.skills.test",
        "class": "TestSkill",
        "method": "execute",
        "timeout": 60,
        "retry": 1
    },
    "metadata": {
        "author": "Test Suite",
        "tags": ["testing", "unit-test"]
    }
}

# Invalid skill - missing required fields
INVALID_SKILL_MISSING_FIELDS = """
name: invalid_skill
description: Missing version and execution
"""

# Invalid skill - wrong data types
INVALID_SKILL_WRONG_TYPES = """
name: invalid_skill
version: 1.0.0
description: Invalid skill with wrong types
execution:
  type: native
  module: test
  class: TestSkill
  method: execute
  timeout: "not_a_number"
"""

# Invalid skill - bad name pattern
INVALID_SKILL_BAD_NAME = """
name: Invalid-Skill-Name
version: 1.0.0
description: Skill with invalid name pattern
execution:
  type: native
  module: test
  class: TestSkill
  method: execute
"""

# Malformed YAML
MALFORMED_YAML = """
name: test
  bad_indent: value
version: 1.0.0
"""

# Malformed JSON
MALFORMED_JSON = '{"name": "test", "version": 1.0.0,}'  # Trailing comma


@pytest.fixture
def schema_path():
    """Get path to skill schema"""
    return Path(__file__).parent.parent.parent / "schemas" / "skill.schema.json"


@pytest.fixture
def registry(schema_path):
    """Create fresh registry for each test"""
    SkillRegistry.reset_instance()
    return SkillRegistry(schema_path=schema_path)


@pytest.fixture
def loader(registry):
    """Create loader with fresh registry"""
    return SkillLoader(registry)


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestSkillLoaderInit:
    """Test SkillLoader initialization"""

    def test_init_with_registry(self, loader, registry):
        """Test loader initialization with registry"""
        assert loader.registry is registry
        assert isinstance(loader.registry, SkillRegistry)

    def test_supported_extensions(self, loader):
        """Test supported file extensions"""
        assert '.yaml' in loader.SUPPORTED_EXTENSIONS
        assert '.yml' in loader.SUPPORTED_EXTENSIONS
        assert '.json' in loader.SUPPORTED_EXTENSIONS


class TestFileFiltering:
    """Test file filtering logic"""

    def test_should_process_yaml_file(self, loader, temp_dir):
        """Test YAML files are processed"""
        yaml_file = temp_dir / "skill.yaml"
        yaml_file.touch()
        assert loader._should_process_file(yaml_file)

    def test_should_process_yml_file(self, loader, temp_dir):
        """Test .yml files are processed"""
        yml_file = temp_dir / "skill.yml"
        yml_file.touch()
        assert loader._should_process_file(yml_file)

    def test_should_process_json_file(self, loader, temp_dir):
        """Test JSON files are processed"""
        json_file = temp_dir / "skill.json"
        json_file.touch()
        assert loader._should_process_file(json_file)

    def test_should_skip_markdown(self, loader, temp_dir):
        """Test markdown files are skipped"""
        md_file = temp_dir / "README.md"
        md_file.touch()
        assert not loader._should_process_file(md_file)

    def test_should_skip_python(self, loader, temp_dir):
        """Test Python files are skipped"""
        py_file = temp_dir / "test.py"
        py_file.touch()
        assert not loader._should_process_file(py_file)

    def test_should_skip_hidden_files(self, loader, temp_dir):
        """Test hidden files are skipped"""
        hidden_file = temp_dir / ".hidden.yaml"
        hidden_file.touch()
        assert not loader._should_process_file(hidden_file)

    def test_should_skip_directories(self, loader, temp_dir):
        """Test directories are skipped"""
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        assert not loader._should_process_file(subdir)


class TestLoadFromYAML:
    """Test loading skills from YAML files"""

    @pytest.mark.asyncio
    async def test_load_valid_yaml(self, loader, temp_dir):
        """Test loading valid YAML skill"""
        yaml_file = temp_dir / "test_skill.yaml"
        yaml_file.write_text(VALID_SKILL_YAML)

        skill = await loader.load_from_file(yaml_file)

        assert skill.name == "test_skill"
        assert skill.version == "1.0.0"
        assert skill.description == "A test skill for unit testing the loader"
        assert skill.category == "testing"
        assert len(skill.parameters) == 1
        assert skill.parameters[0].name == "test_param"
        assert skill.execution.type == ExecutionType.NATIVE

    @pytest.mark.asyncio
    async def test_load_yaml_registers_skill(self, loader, registry, temp_dir):
        """Test loading YAML automatically registers skill"""
        yaml_file = temp_dir / "test_skill.yaml"
        yaml_file.write_text(VALID_SKILL_YAML)

        skill = await loader.load_from_file(yaml_file)

        assert registry.exists("test_skill")
        assert registry.get("test_skill") == skill

    @pytest.mark.asyncio
    async def test_load_yaml_without_register(self, loader, registry, temp_dir):
        """Test loading YAML without registering"""
        yaml_file = temp_dir / "test_skill.yaml"
        yaml_file.write_text(VALID_SKILL_YAML)

        skill = await loader.load_from_file(yaml_file, register=False)

        assert skill.name == "test_skill"
        assert not registry.exists("test_skill")

    @pytest.mark.asyncio
    async def test_load_yml_extension(self, loader, temp_dir):
        """Test loading .yml extension"""
        yml_file = temp_dir / "test_skill.yml"
        yml_file.write_text(VALID_SKILL_YAML)

        skill = await loader.load_from_file(yml_file)
        assert skill.name == "test_skill"


class TestLoadFromJSON:
    """Test loading skills from JSON files"""

    @pytest.mark.asyncio
    async def test_load_valid_json(self, loader, temp_dir):
        """Test loading valid JSON skill"""
        json_file = temp_dir / "test_skill.json"
        json_file.write_text(json.dumps(VALID_SKILL_JSON, indent=2))

        skill = await loader.load_from_file(json_file)

        assert skill.name == "test_skill"
        assert skill.version == "1.0.0"
        assert skill.execution.type == ExecutionType.NATIVE

    @pytest.mark.asyncio
    async def test_load_json_registers_skill(self, loader, registry, temp_dir):
        """Test loading JSON automatically registers skill"""
        json_file = temp_dir / "test_skill.json"
        json_file.write_text(json.dumps(VALID_SKILL_JSON))

        await loader.load_from_file(json_file)

        assert registry.exists("test_skill")


class TestSchemaValidation:
    """Test schema validation with invalid skills"""

    @pytest.mark.asyncio
    async def test_reject_missing_required_fields(self, loader, temp_dir):
        """Test rejection of skills missing required fields"""
        yaml_file = temp_dir / "invalid.yaml"
        yaml_file.write_text(INVALID_SKILL_MISSING_FIELDS)

        with pytest.raises(SkillValidationError):
            await loader.load_from_file(yaml_file)

    @pytest.mark.asyncio
    async def test_reject_wrong_data_types(self, loader, temp_dir):
        """Test rejection of skills with wrong data types"""
        yaml_file = temp_dir / "invalid.yaml"
        yaml_file.write_text(INVALID_SKILL_WRONG_TYPES)

        with pytest.raises(SkillValidationError):
            await loader.load_from_file(yaml_file)

    @pytest.mark.asyncio
    async def test_reject_bad_name_pattern(self, loader, temp_dir):
        """Test rejection of skills with invalid name patterns"""
        yaml_file = temp_dir / "invalid.yaml"
        yaml_file.write_text(INVALID_SKILL_BAD_NAME)

        with pytest.raises(SkillValidationError):
            await loader.load_from_file(yaml_file)

    @pytest.mark.asyncio
    async def test_invalid_skill_not_registered(self, loader, registry, temp_dir):
        """Test invalid skills are not registered"""
        yaml_file = temp_dir / "invalid.yaml"
        yaml_file.write_text(INVALID_SKILL_MISSING_FIELDS)

        try:
            await loader.load_from_file(yaml_file)
        except SkillValidationError:
            pass

        # Should not be registered
        assert not registry.exists("invalid_skill")


class TestMalformedFiles:
    """Test handling of malformed files"""

    @pytest.mark.asyncio
    async def test_malformed_yaml(self, loader, temp_dir):
        """Test handling of malformed YAML"""
        yaml_file = temp_dir / "malformed.yaml"
        yaml_file.write_text(MALFORMED_YAML)

        with pytest.raises(SkillParseError):
            await loader.load_from_file(yaml_file)

    @pytest.mark.asyncio
    async def test_malformed_json(self, loader, temp_dir):
        """Test handling of malformed JSON"""
        json_file = temp_dir / "malformed.json"
        json_file.write_text(MALFORMED_JSON)

        with pytest.raises(SkillParseError):
            await loader.load_from_file(json_file)

    @pytest.mark.asyncio
    async def test_nonexistent_file(self, loader, temp_dir):
        """Test handling of non-existent file"""
        missing_file = temp_dir / "missing.yaml"

        with pytest.raises(SkillFileError):
            await loader.load_from_file(missing_file)

    @pytest.mark.asyncio
    async def test_yaml_with_non_dict_content(self, loader, temp_dir):
        """Test YAML file with non-dictionary content"""
        yaml_file = temp_dir / "bad_content.yaml"
        yaml_file.write_text("- item1\n- item2\n")  # List, not dict

        with pytest.raises(SkillParseError):
            await loader.load_from_file(yaml_file)

    @pytest.mark.asyncio
    async def test_json_with_non_object_content(self, loader, temp_dir):
        """Test JSON file with non-object content"""
        json_file = temp_dir / "bad_content.json"
        json_file.write_text('["item1", "item2"]')  # Array, not object

        with pytest.raises(SkillParseError):
            await loader.load_from_file(json_file)


class TestBatchLoading:
    """Test batch loading from directories"""

    @pytest.mark.asyncio
    async def test_load_from_directory(self, loader, temp_dir):
        """Test loading multiple skills from directory"""
        # Create multiple skill files
        for i in range(3):
            skill_def = VALID_SKILL_JSON.copy()
            skill_def['name'] = f"test_skill_{i}"
            skill_file = temp_dir / f"skill_{i}.yaml"
            skill_file.write_text(yaml.dump(skill_def))

        skills = await loader.load_from_directory(temp_dir)

        assert len(skills) == 3
        skill_names = {s.name for s in skills}
        assert skill_names == {"test_skill_0", "test_skill_1", "test_skill_2"}

    @pytest.mark.asyncio
    async def test_load_from_directory_recursive(self, loader, temp_dir):
        """Test recursive directory loading"""
        # Create nested structure
        subdir = temp_dir / "subdir"
        subdir.mkdir()

        # Top-level skill
        skill1 = VALID_SKILL_JSON.copy()
        skill1['name'] = "skill_top"
        (temp_dir / "skill_top.yaml").write_text(yaml.dump(skill1))

        # Subdirectory skill
        skill2 = VALID_SKILL_JSON.copy()
        skill2['name'] = "skill_sub"
        (subdir / "skill_sub.yaml").write_text(yaml.dump(skill2))

        skills = await loader.load_from_directory(temp_dir, recursive=True)

        assert len(skills) == 2
        skill_names = {s.name for s in skills}
        assert skill_names == {"skill_top", "skill_sub"}

    @pytest.mark.asyncio
    async def test_load_from_directory_non_recursive(self, loader, temp_dir):
        """Test non-recursive directory loading"""
        subdir = temp_dir / "subdir"
        subdir.mkdir()

        # Top-level skill
        skill1 = VALID_SKILL_JSON.copy()
        skill1['name'] = "skill_top"
        (temp_dir / "skill_top.yaml").write_text(yaml.dump(skill1))

        # Subdirectory skill (should be ignored)
        skill2 = VALID_SKILL_JSON.copy()
        skill2['name'] = "skill_sub"
        (subdir / "skill_sub.yaml").write_text(yaml.dump(skill2))

        skills = await loader.load_from_directory(temp_dir, recursive=False)

        assert len(skills) == 1
        assert skills[0].name == "skill_top"

    @pytest.mark.asyncio
    async def test_load_mixed_yaml_json(self, loader, temp_dir):
        """Test loading both YAML and JSON files"""
        # YAML skill
        (temp_dir / "skill1.yaml").write_text(VALID_SKILL_YAML)

        # JSON skill
        skill2 = VALID_SKILL_JSON.copy()
        skill2['name'] = "skill2"
        (temp_dir / "skill2.json").write_text(json.dumps(skill2))

        skills = await loader.load_from_directory(temp_dir)

        assert len(skills) == 2
        skill_names = {s.name for s in skills}
        assert skill_names == {"test_skill", "skill2"}

    @pytest.mark.asyncio
    async def test_batch_load_skips_invalid_files(self, loader, temp_dir):
        """Test batch loading continues despite invalid files"""
        # Valid skill
        (temp_dir / "valid.yaml").write_text(VALID_SKILL_YAML)

        # Invalid skill
        (temp_dir / "invalid.yaml").write_text(INVALID_SKILL_MISSING_FIELDS)

        # Malformed skill
        (temp_dir / "malformed.yaml").write_text(MALFORMED_YAML)

        skills = await loader.load_from_directory(temp_dir)

        # Should load only the valid skill
        assert len(skills) == 1
        assert skills[0].name == "test_skill"

    @pytest.mark.asyncio
    async def test_batch_load_skips_non_skill_files(self, loader, temp_dir):
        """Test batch loading ignores non-skill files"""
        # Valid skill
        (temp_dir / "skill.yaml").write_text(VALID_SKILL_YAML)

        # Non-skill files (should be ignored)
        (temp_dir / "README.md").write_text("# README")
        (temp_dir / "config.txt").write_text("config")
        (temp_dir / ".hidden.yaml").write_text("hidden")

        skills = await loader.load_from_directory(temp_dir)

        assert len(skills) == 1
        assert skills[0].name == "test_skill"

    @pytest.mark.asyncio
    async def test_load_from_empty_directory(self, loader, temp_dir):
        """Test loading from empty directory"""
        skills = await loader.load_from_directory(temp_dir)
        assert len(skills) == 0

    @pytest.mark.asyncio
    async def test_load_from_nonexistent_directory(self, loader, temp_dir):
        """Test loading from non-existent directory"""
        missing_dir = temp_dir / "missing"

        with pytest.raises(SkillFileError):
            await loader.load_from_directory(missing_dir)


class TestConflictHandling:
    """Test handling of skill name conflicts"""

    @pytest.mark.asyncio
    async def test_duplicate_name_in_registry(self, schema_path, temp_dir):
        """Test loading duplicate skill name fails"""
        # Create fresh registry and loader for this test
        SkillRegistry.reset_instance()
        registry = SkillRegistry(schema_path=schema_path)
        loader = SkillLoader(registry)

        yaml_file = temp_dir / "skill.yaml"
        yaml_file.write_text(VALID_SKILL_YAML)

        # Load first time (success)
        await loader.load_from_file(yaml_file)

        # Load second time (should fail)
        with pytest.raises(SkillConflictError):
            await loader.load_from_file(yaml_file)


class TestReloadSkill:
    """Test skill reloading functionality"""

    @pytest.mark.asyncio
    async def test_reload_updates_skill(self, loader, registry, temp_dir):
        """Test reloading updates an existing skill"""
        yaml_file = temp_dir / "skill.yaml"

        # Initial load
        yaml_file.write_text(VALID_SKILL_YAML)
        skill1 = await loader.load_from_file(yaml_file)

        # Modify skill
        modified_yaml = VALID_SKILL_YAML.replace("1.0.0", "2.0.0")
        yaml_file.write_text(modified_yaml)

        # Reload
        skill2 = await loader.reload_skill(yaml_file)

        assert skill2.version == "2.0.0"
        assert registry.get("test_skill").version == "2.0.0"


class TestLoaderStatistics:
    """Test loader statistics"""

    def test_get_statistics(self, loader):
        """Test getting loader statistics"""
        stats = loader.get_statistics()

        assert 'supported_formats' in stats
        assert 'yaml_extensions' in stats
        assert 'json_extensions' in stats
        assert 'skip_patterns' in stats
        assert 'registry_skill_count' in stats

        assert '.yaml' in stats['supported_formats']
        assert '.json' in stats['supported_formats']


class TestEdgeCases:
    """Test edge cases and error scenarios"""

    @pytest.mark.asyncio
    async def test_empty_yaml_file(self, loader, temp_dir):
        """Test handling of empty YAML file"""
        yaml_file = temp_dir / "empty.yaml"
        yaml_file.write_text("")

        with pytest.raises((SkillParseError, SkillValidationError)):
            await loader.load_from_file(yaml_file)

    @pytest.mark.asyncio
    async def test_empty_json_file(self, loader, temp_dir):
        """Test handling of empty JSON file"""
        json_file = temp_dir / "empty.json"
        json_file.write_text("")

        with pytest.raises(SkillParseError):
            await loader.load_from_file(json_file)

    @pytest.mark.asyncio
    async def test_binary_file(self, loader, temp_dir):
        """Test handling of binary file"""
        binary_file = temp_dir / "binary.yaml"
        binary_file.write_bytes(b'\x00\x01\x02\x03\x04')

        # Binary data causes either file read error or YAML parse error
        with pytest.raises((SkillFileError, SkillParseError)):
            await loader.load_from_file(binary_file)
