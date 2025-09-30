#!/usr/bin/env python3
"""
Shannon V3 Test Suite

Comprehensive functional tests for Shannon V3 markdown-based framework.
Tests validate markdown structure, hook functionality, and installation.

Following Shannon's NO MOCKS philosophy:
- Real file operations (no filesystem mocks)
- Real hook execution (no process mocks)
- Real YAML parsing (no parser mocks)
- Real JSON I/O (no data mocks)

Author: Shannon Framework
Version: 1.0.0
License: MIT
"""

import pytest
import os
import json
import subprocess
import tempfile
import shutil
import yaml
from pathlib import Path
from typing import Dict, Any, List


# =============================================================================
# Test Configuration & Fixtures
# =============================================================================

@pytest.fixture
def shannon_root():
    """Return path to Shannon framework root directory"""
    current_file = Path(__file__).resolve()
    return current_file.parent.parent / "Shannon"


@pytest.fixture
def hooks_dir(shannon_root):
    """Return path to Shannon hooks directory"""
    return shannon_root / "Hooks"


@pytest.fixture
def commands_dir(shannon_root):
    """Return path to Shannon commands directory"""
    return shannon_root / "Commands"


@pytest.fixture
def agents_dir(shannon_root):
    """Return path to Shannon agents directory"""
    return shannon_root / "Agents"


@pytest.fixture
def modes_dir(shannon_root):
    """Return path to Shannon modes directory"""
    return shannon_root / "Modes"


@pytest.fixture
def temp_dir():
    """Create temporary directory for test operations"""
    temp = tempfile.mkdtemp(prefix="shannon_test_")
    yield Path(temp)
    shutil.rmtree(temp, ignore_errors=True)


# =============================================================================
# Markdown Structure Tests
# =============================================================================

class TestMarkdownStructure:
    """Test markdown file structure and YAML frontmatter validation"""

    def test_all_commands_have_yaml_frontmatter(self, commands_dir):
        """Verify all command files have valid YAML frontmatter"""
        command_files = list(commands_dir.glob("sc_*.md"))
        assert len(command_files) > 0, "No command files found"

        for cmd_file in command_files:
            content = cmd_file.read_text()
            assert content.startswith("---\n"), f"{cmd_file.name} missing YAML frontmatter start"
            assert "\n---\n" in content[4:], f"{cmd_file.name} missing YAML frontmatter end"

    def test_command_yaml_required_fields(self, commands_dir):
        """Verify command YAML contains required fields"""
        required_fields = ["name", "description", "category"]
        command_files = list(commands_dir.glob("sc_*.md"))

        for cmd_file in command_files:
            content = cmd_file.read_text()
            yaml_end = content.find("\n---\n", 4)
            yaml_content = content[4:yaml_end]

            data = yaml.safe_load(yaml_content)
            assert data is not None, f"{cmd_file.name} has empty YAML"

            for field in required_fields:
                assert field in data, f"{cmd_file.name} missing required field: {field}"
                assert data[field], f"{cmd_file.name} has empty {field}"

    def test_command_category_validation(self, commands_dir):
        """Verify command category is 'command'"""
        command_files = list(commands_dir.glob("sc_*.md"))

        for cmd_file in command_files:
            content = cmd_file.read_text()
            yaml_end = content.find("\n---\n", 4)
            yaml_content = content[4:yaml_end]
            data = yaml.safe_load(yaml_content)

            assert data["category"] == "command", \
                f"{cmd_file.name} has invalid category: {data['category']}"

    def test_all_agents_have_yaml_frontmatter(self, agents_dir):
        """Verify all agent files have valid YAML frontmatter"""
        agent_files = list(agents_dir.glob("*.md"))
        assert len(agent_files) > 0, "No agent files found"

        for agent_file in agent_files:
            content = agent_file.read_text()
            assert content.startswith("---\n"), f"{agent_file.name} missing YAML frontmatter"
            assert "\n---\n" in content[4:], f"{agent_file.name} missing YAML end"

    def test_agent_yaml_required_fields(self, agents_dir):
        """Verify agent YAML contains required fields"""
        required_fields = ["name", "description", "category"]
        agent_files = list(agents_dir.glob("*.md"))

        for agent_file in agent_files:
            content = agent_file.read_text()
            yaml_end = content.find("\n---\n", 4)
            yaml_content = content[4:yaml_end]

            data = yaml.safe_load(yaml_content)
            assert data is not None, f"{agent_file.name} has empty YAML"

            for field in required_fields:
                assert field in data, f"{agent_file.name} missing {field}"

    def test_mode_yaml_structure(self, modes_dir):
        """Verify mode files have valid YAML frontmatter"""
        mode_files = list(modes_dir.glob("*.md"))
        assert len(mode_files) > 0, "No mode files found"

        for mode_file in mode_files:
            content = mode_file.read_text()
            assert content.startswith("---\n"), f"{mode_file.name} missing YAML frontmatter"

            yaml_end = content.find("\n---\n", 4)
            yaml_content = content[4:yaml_end]
            data = yaml.safe_load(yaml_content)

            assert "name" in data, f"{mode_file.name} missing name field"
            assert "category" in data, f"{mode_file.name} missing category field"

    def test_yaml_parsing_validity(self, shannon_root):
        """Verify all markdown files have parseable YAML"""
        md_files = list(shannon_root.rglob("*.md"))
        assert len(md_files) > 0, "No markdown files found"

        errors = []
        for md_file in md_files:
            try:
                content = md_file.read_text()
                if content.startswith("---\n"):
                    yaml_end = content.find("\n---\n", 4)
                    if yaml_end > 0:
                        yaml_content = content[4:yaml_end]
                        yaml.safe_load(yaml_content)
            except yaml.YAMLError as e:
                errors.append(f"{md_file.name}: {str(e)}")

        assert len(errors) == 0, f"YAML parsing errors:\n" + "\n".join(errors)


# =============================================================================
# Hook Tests - Real Execution
# =============================================================================

class TestPreCompactHook:
    """Test PreCompact hook with real execution (NO MOCKS)"""

    def test_hook_executable_exists(self, hooks_dir):
        """Verify precompact.py exists and is executable"""
        hook_file = hooks_dir / "precompact.py"
        assert hook_file.exists(), "precompact.py not found"
        assert os.access(hook_file, os.X_OK), "precompact.py not executable"

    def test_hook_shebang_valid(self, hooks_dir):
        """Verify hook has proper Python shebang"""
        hook_file = hooks_dir / "precompact.py"
        first_line = hook_file.read_text().split("\n")[0]
        assert first_line.startswith("#!"), "Missing shebang"
        assert "python" in first_line.lower(), "Invalid shebang (not Python)"

    def test_hook_executes_with_valid_json(self, hooks_dir, temp_dir):
        """Test hook execution with real JSON input"""
        hook_file = hooks_dir / "precompact.py"

        # Real input JSON
        input_data = {
            "event": "PreCompact",
            "context": {
                "projectDir": str(temp_dir)
            }
        }

        # Real subprocess execution
        result = subprocess.run(
            [str(hook_file)],
            input=json.dumps(input_data),
            capture_output=True,
            text=True,
            timeout=5
        )

        assert result.returncode == 0, f"Hook failed: {result.stderr}"
        assert result.stdout, "Hook produced no output"

    def test_hook_output_json_valid(self, hooks_dir, temp_dir):
        """Verify hook outputs valid JSON structure"""
        hook_file = hooks_dir / "precompact.py"

        input_data = {
            "event": "PreCompact",
            "context": {"projectDir": str(temp_dir)}
        }

        result = subprocess.run(
            [str(hook_file)],
            input=json.dumps(input_data),
            capture_output=True,
            text=True,
            timeout=5
        )

        # Parse real JSON output
        output = json.loads(result.stdout)

        # Validate structure
        assert "hookSpecificOutput" in output, "Missing hookSpecificOutput"
        hook_output = output["hookSpecificOutput"]
        assert "hookEventName" in hook_output
        assert hook_output["hookEventName"] == "PreCompact"
        assert "version" in hook_output
        assert "checkpointKey" in hook_output

    def test_hook_generates_checkpoint_instructions(self, hooks_dir, temp_dir):
        """Verify hook generates valid checkpoint instructions"""
        hook_file = hooks_dir / "precompact.py"

        input_data = {
            "event": "PreCompact",
            "context": {"projectDir": str(temp_dir)}
        }

        result = subprocess.run(
            [str(hook_file)],
            input=json.dumps(input_data),
            capture_output=True,
            text=True,
            timeout=5
        )

        output = json.loads(result.stdout)
        hook_output = output["hookSpecificOutput"]

        # Verify checkpoint instructions present
        assert "additionalContext" in hook_output
        instructions = hook_output["additionalContext"]
        assert "CONTEXT_GUARDIAN" in instructions
        assert "write_memory" in instructions
        assert "checkpoint_key" in instructions

    def test_hook_handles_invalid_json_gracefully(self, hooks_dir):
        """Verify hook handles malformed JSON without crashing"""
        hook_file = hooks_dir / "precompact.py"

        # Invalid JSON input
        result = subprocess.run(
            [str(hook_file)],
            input="invalid json {{{",
            capture_output=True,
            text=True,
            timeout=5
        )

        # Should exit 0 (non-blocking) even with bad input
        assert result.returncode == 0, "Hook should not block on error"

        # Should return error JSON
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output
        assert "error" in output["hookSpecificOutput"]

    def test_hook_timeout_compliance(self, hooks_dir, temp_dir):
        """Verify hook executes within 5000ms timeout"""
        import time
        hook_file = hooks_dir / "precompact.py"

        input_data = {"event": "PreCompact", "context": {"projectDir": str(temp_dir)}}

        start_time = time.time()
        result = subprocess.run(
            [str(hook_file)],
            input=json.dumps(input_data),
            capture_output=True,
            text=True,
            timeout=5
        )
        execution_time = (time.time() - start_time) * 1000  # Convert to ms

        assert result.returncode == 0
        assert execution_time < 5000, f"Hook took {execution_time}ms (limit: 5000ms)"


# =============================================================================
# Installation Tests - Real File Operations
# =============================================================================

class TestInstallation:
    """Test installation functionality with real file operations (NO MOCKS)"""

    def test_shannon_directory_structure(self, shannon_root):
        """Verify Shannon has required directory structure"""
        required_dirs = ["Commands", "Agents", "Modes", "Core", "Hooks"]

        for dir_name in required_dirs:
            dir_path = shannon_root / dir_name
            assert dir_path.exists(), f"Missing directory: {dir_name}"
            assert dir_path.is_dir(), f"{dir_name} is not a directory"

    def test_commands_directory_not_empty(self, commands_dir):
        """Verify Commands directory contains command files"""
        command_files = list(commands_dir.glob("sc_*.md"))
        assert len(command_files) > 0, "Commands directory is empty"

    def test_agents_directory_not_empty(self, agents_dir):
        """Verify Agents directory contains agent files"""
        agent_files = list(agents_dir.glob("*.md"))
        assert len(agent_files) > 0, "Agents directory is empty"

    def test_hooks_directory_contains_precompact(self, hooks_dir):
        """Verify Hooks directory contains precompact.py"""
        hook_file = hooks_dir / "precompact.py"
        assert hook_file.exists(), "precompact.py not found in Hooks"

    def test_file_copy_operation(self, temp_dir, shannon_root):
        """Test real file copying from Shannon to temp directory"""
        # Real file from Shannon
        source_file = shannon_root / "Commands" / "sc_help.md"
        assert source_file.exists(), "Source file not found"

        # Real copy operation
        dest_file = temp_dir / "test_copy.md"
        shutil.copy2(source_file, dest_file)

        # Verify real copy
        assert dest_file.exists(), "File copy failed"
        assert dest_file.stat().st_size > 0, "Copied file is empty"

        # Verify content matches
        assert dest_file.read_text() == source_file.read_text()


# =============================================================================
# Integration Tests - Framework Structure
# =============================================================================

class TestFrameworkIntegration:
    """Test Shannon framework integration and structure"""

    def test_command_agent_mode_relationship(self, shannon_root):
        """Verify commands, agents, and modes form coherent structure"""
        commands = list((shannon_root / "Commands").glob("sc_*.md"))
        agents = list((shannon_root / "Agents").glob("*.md"))
        modes = list((shannon_root / "Modes").glob("*.md"))

        assert len(commands) > 0, "No commands found"
        assert len(agents) > 0, "No agents found"
        assert len(modes) > 0, "No modes found"

    def test_command_names_follow_convention(self, commands_dir):
        """Verify command file names follow sc_* or sh_* convention"""
        command_files = list(commands_dir.glob("*.md"))

        for cmd_file in command_files:
            assert cmd_file.name.startswith("sc_") or cmd_file.name.startswith("sh_"), \
                f"Command file {cmd_file.name} doesn't follow sc_* or sh_* convention"

    def test_yaml_name_matches_filename(self, commands_dir):
        """Verify YAML name field matches filename convention"""
        command_files = list(commands_dir.glob("sc_*.md"))

        for cmd_file in command_files:
            content = cmd_file.read_text()
            yaml_end = content.find("\n---\n", 4)
            yaml_content = content[4:yaml_end]
            data = yaml.safe_load(yaml_content)

            # Extract expected name from filename
            # sc_analyze.md -> sc:analyze
            # Allow both underscore and hyphen in names
            expected_name = "sc:" + cmd_file.stem.replace("sc_", "")
            expected_name_hyphen = expected_name.replace("_", "-")

            assert data["name"] == expected_name or data["name"] == expected_name_hyphen, \
                f"{cmd_file.name} YAML name mismatch: {data['name']} != {expected_name} or {expected_name_hyphen}"


# =============================================================================
# Test Fixtures and Sample Data
# =============================================================================

@pytest.fixture
def sample_command_yaml():
    """Sample valid command YAML for testing"""
    return """---
name: sc:test
description: Test command for validation
category: command
base: SuperClaude test
complexity: low
wave-enabled: false
---

# Test Command

This is a test command for validation purposes.
"""


@pytest.fixture
def sample_agent_yaml():
    """Sample valid agent YAML for testing"""
    return """---
name: TEST_AGENT
description: Test agent for validation
category: agent
specialization: testing
---

# Test Agent

This is a test agent for validation purposes.
"""


@pytest.fixture
def sample_hook_input():
    """Sample hook input JSON for testing"""
    return {
        "event": "PreCompact",
        "context": {
            "projectDir": "/tmp/test",
            "sessionId": "test_session_123"
        },
        "metadata": {
            "timestamp": "2024-01-01T00:00:00Z"
        }
    }


# =============================================================================
# Test Runner Configuration
# =============================================================================

def pytest_configure(config):
    """Pytest configuration - register custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


if __name__ == "__main__":
    """Run tests directly with python test_shannon.py"""
    pytest.main([__file__, "-v", "--tb=short"])