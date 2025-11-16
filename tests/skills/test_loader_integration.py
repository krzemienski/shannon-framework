"""
Integration test for SkillLoader demonstrating complete workflow
"""

import pytest
import tempfile
import yaml
from pathlib import Path

from shannon.skills import (
    SkillRegistry,
    SkillLoader,
    Skill,
    ExecutionType,
)


@pytest.mark.asyncio
async def test_complete_workflow():
    """
    Integration test demonstrating complete skill loading workflow:
    1. Create registry
    2. Create loader
    3. Load skills from YAML/JSON
    4. Query loaded skills
    """
    # Get schema path
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "skill.schema.json"

    # Reset and create fresh registry
    SkillRegistry.reset_instance()
    registry = SkillRegistry(schema_path=schema_path)
    loader = SkillLoader(registry)

    # Create temporary directory with test skills
    with tempfile.TemporaryDirectory() as tmpdir:
        skills_dir = Path(tmpdir)

        # Create a testing skill
        test_skill = {
            "name": "run_tests",
            "version": "1.0.0",
            "description": "Execute test suite with coverage",
            "category": "testing",
            "parameters": [
                {
                    "name": "coverage",
                    "type": "boolean",
                    "required": False,
                    "default": True,
                    "description": "Generate coverage report"
                }
            ],
            "execution": {
                "type": "script",
                "script": "pytest",
                "timeout": 300
            },
            "metadata": {
                "tags": ["testing", "pytest", "coverage"]
            }
        }
        (skills_dir / "run_tests.yaml").write_text(yaml.dump(test_skill))

        # Create a git skill
        git_skill = {
            "name": "git_commit",
            "version": "1.0.0",
            "description": "Create git commit with message",
            "category": "git",
            "parameters": [
                {
                    "name": "message",
                    "type": "string",
                    "required": True,
                    "description": "Commit message"
                }
            ],
            "execution": {
                "type": "native",
                "module": "shannon.skills.git",
                "class": "GitSkills",
                "method": "commit"
            }
        }
        (skills_dir / "git_commit.yaml").write_text(yaml.dump(git_skill))

        # Load all skills
        loaded_skills = await loader.load_from_directory(skills_dir)

        # Verify loading
        assert len(loaded_skills) == 2
        assert registry.exists("run_tests")
        assert registry.exists("git_commit")

        # Query by category
        testing_skills = registry.find_by_category("testing")
        assert len(testing_skills) == 1
        assert testing_skills[0].name == "run_tests"

        git_skills = registry.find_by_category("git")
        assert len(git_skills) == 1
        assert git_skills[0].name == "git_commit"

        # Query by execution type
        script_skills = registry.find_by_execution_type(ExecutionType.SCRIPT)
        assert len(script_skills) == 1
        assert script_skills[0].name == "run_tests"

        native_skills = registry.find_by_execution_type(ExecutionType.NATIVE)
        assert len(native_skills) == 1
        assert native_skills[0].name == "git_commit"

        # Query by tag
        pytest_skills = registry.find_by_tag("pytest")
        assert len(pytest_skills) == 1
        assert pytest_skills[0].name == "run_tests"

        # Get statistics
        stats = registry.get_statistics()
        assert stats['total_skills'] == 2
        assert stats['categories']['testing'] == 1
        assert stats['categories']['git'] == 1
        assert stats['execution_types']['script'] == 1
        assert stats['execution_types']['native'] == 1

        print("\n=== Integration Test Success ===")
        print(f"Loaded {len(loaded_skills)} skills")
        print(f"Registry contains {len(registry)} skills")
        print(f"Categories: {list(stats['categories'].keys())}")
        print(f"Execution types: {list(stats['execution_types'].keys())}")
