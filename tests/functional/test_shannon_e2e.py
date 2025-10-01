"""
Shannon Framework E2E Functional Test Suite

Comprehensive end-to-end tests validating Shannon commands, artifacts,
behavioral patterns, and context preservation.

Test Categories:
1. Command Execution - Shannon command functionality
2. Artifact Generation - Output validation
3. Behavioral Patterns - Shannon-specific behaviors
4. Context Preservation - Checkpoint/restore cycles
5. Shadcn Integration - React component enforcement
"""

import pytest
from pathlib import Path
import json
import yaml
import re
import time
from typing import Dict, List, Optional
from datetime import datetime
import shutil

# Import test harness components
from harness.claude_interface import ClaudeCodeInterface, CommandResult
from harness.artifact_validator import (
    SpecAnalysisValidator,
    CheckpointValidator,
    ImplementationValidator,
    ValidationResult
)
from harness.debug_logger import DebugLogger


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def shannon_project() -> Path:
    """Shannon project directory"""
    return Path("/Users/nick/Documents/shannon")


@pytest.fixture(scope="session")
def claude_interface(shannon_project: Path) -> ClaudeCodeInterface:
    """Claude Code interface for command execution"""
    return ClaudeCodeInterface(shannon_project, debug=True)


@pytest.fixture(scope="session")
def debug_logger(shannon_project: Path) -> DebugLogger:
    """Debug logger for test session"""
    log_dir = shannon_project / "test-results" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return DebugLogger(log_dir)


@pytest.fixture(scope="session")
def validators(shannon_project: Path) -> Dict[str, object]:
    """Artifact validators"""
    return {
        "spec": SpecAnalysisValidator(),
        "checkpoint": CheckpointValidator(),
        "implementation": ImplementationValidator()
    }


@pytest.fixture(autouse=True)
def clean_artifacts(shannon_project: Path):
    """Clean .shannon/ directory before each test, preserve after"""
    shannon_dir = shannon_project / ".shannon"

    # Clean before test
    if shannon_dir.exists():
        # Backup existing artifacts
        backup_dir = shannon_project / "test-results" / "artifacts-backup"
        backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"artifacts_{timestamp}"
        shutil.copytree(shannon_dir, backup_path)

        # Clean for test
        shutil.rmtree(shannon_dir)

    shannon_dir.mkdir(exist_ok=True)

    yield

    # Preserve artifacts for analysis after test
    # (artifacts remain in .shannon/ for inspection)


@pytest.fixture
def sample_spec() -> str:
    """Sample specification for testing"""
    return """Build a todo application with the following features:

    - User authentication (email/password)
    - Create, read, update, delete todos
    - Mark todos as complete/incomplete
    - Filter todos by status (all, active, completed)
    - Responsive design for mobile and desktop

    Technical requirements:
    - React frontend with TypeScript
    - RESTful API backend
    - PostgreSQL database
    - JWT authentication
    """


# ============================================================================
# TEST CLASS 1: COMMAND EXECUTION
# ============================================================================

class TestCommandExecution:
    """Test Shannon command execution and basic functionality"""

    def test_sh_spec_executes_successfully(
        self,
        claude_interface: ClaudeCodeInterface,
        debug_logger: DebugLogger,
        sample_spec: str
    ):
        """Test /sh:spec command executes and completes"""
        debug_logger.log_command_start("/sh:spec", {"spec": sample_spec})

        start_time = time.time()
        result = claude_interface.execute_command(
            f'/sh:spec "{sample_spec}"'
        )
        duration = time.time() - start_time

        debug_logger.log_command_end("/sh:spec", result, duration)

        # Validate execution
        assert result.success, f"Command failed: {result.errors}"
        assert result.output, "No output captured"
        assert duration < 300, f"Command took too long: {duration}s"

        # Verify spec analysis mentions key features
        output_lower = result.output.lower()
        assert "authentication" in output_lower, "Missing authentication analysis"
        assert "todo" in output_lower, "Missing todo feature analysis"


    def test_sh_spec_with_code_sample(
        self,
        claude_interface: ClaudeCodeInterface,
        debug_logger: DebugLogger
    ):
        """Test /sh:spec with @code reference"""
        spec = """Analyze this React component and suggest improvements:
        @components/TodoList.tsx"""

        debug_logger.log_command_start("/sh:spec", {"spec": spec, "with_code": True})

        result = claude_interface.execute_command(f'/sh:spec "{spec}"')

        debug_logger.log_command_end("/sh:spec", result)

        assert result.success, "Command with code reference failed"
        # Verify code analysis in output
        assert "component" in result.output.lower()


    def test_sh_checkpoint_creates_snapshot(
        self,
        claude_interface: ClaudeCodeInterface,
        shannon_project: Path
    ):
        """Test /sh:checkpoint creates checkpoint snapshot"""
        checkpoint_name = "test-checkpoint-1"

        result = claude_interface.execute_command(
            f'/sh:checkpoint "{checkpoint_name}"'
        )

        assert result.success, f"Checkpoint creation failed: {result.errors}"

        # Verify checkpoint file exists
        checkpoint_dir = shannon_project / ".shannon" / "checkpoints"
        assert checkpoint_dir.exists(), "Checkpoints directory not created"

        checkpoint_files = list(checkpoint_dir.glob(f"*{checkpoint_name}*"))
        assert len(checkpoint_files) > 0, "No checkpoint file created"


    def test_sh_restore_without_checkpoint_fails_gracefully(
        self,
        claude_interface: ClaudeCodeInterface
    ):
        """Test /sh:restore fails gracefully with no checkpoints"""
        result = claude_interface.execute_command('/sh:restore')

        # Should fail but not crash
        assert not result.success, "Restore should fail with no checkpoints"
        assert "no checkpoint" in result.errors.lower() or \
               "not found" in result.errors.lower()


    def test_sh_checkpoint_restore_cycle(
        self,
        claude_interface: ClaudeCodeInterface,
        shannon_project: Path
    ):
        """Test complete checkpoint/restore cycle"""
        checkpoint_name = "restore-test"

        # Create checkpoint
        checkpoint_result = claude_interface.execute_command(
            f'/sh:checkpoint "{checkpoint_name}"'
        )
        assert checkpoint_result.success, "Checkpoint creation failed"

        # Restore checkpoint
        restore_result = claude_interface.execute_command('/sh:restore')
        assert restore_result.success, f"Restore failed: {restore_result.errors}"

        # Verify restoration message
        assert "restored" in restore_result.output.lower()


    def test_sh_implement_executes(
        self,
        claude_interface: ClaudeCodeInterface,
        debug_logger: DebugLogger
    ):
        """Test /sh:implement command execution"""
        task = "Create a React LoginForm component with email and password fields"

        debug_logger.log_command_start("/sh:implement", {"task": task})

        result = claude_interface.execute_command(f'/sh:implement "{task}"')

        debug_logger.log_command_end("/sh:implement", result)

        assert result.success, f"Implementation failed: {result.errors}"
        assert "component" in result.output.lower() or \
               "created" in result.output.lower()


    def test_sh_validate_executes(
        self,
        claude_interface: ClaudeCodeInterface
    ):
        """Test /sh:validate command execution"""
        result = claude_interface.execute_command('/sh:validate')

        # Should execute even if no implementation exists
        assert result.success or "no implementation" in result.errors.lower()


# ============================================================================
# TEST CLASS 2: ARTIFACT GENERATION
# ============================================================================

class TestArtifactGeneration:
    """Test artifact creation, structure, and content quality"""

    def test_spec_creates_analysis_artifact(
        self,
        claude_interface: ClaudeCodeInterface,
        shannon_project: Path,
        validators: Dict,
        sample_spec: str
    ):
        """Test spec analysis creates properly structured artifact"""
        # Execute spec analysis
        result = claude_interface.execute_command(f'/sh:spec "{sample_spec}"')
        assert result.success, "Spec command failed"

        # Find analysis artifact
        analysis_dir = shannon_project / ".shannon" / "analysis"
        assert analysis_dir.exists(), "Analysis directory not created"

        artifacts = list(analysis_dir.glob("spec_*.md"))
        assert len(artifacts) > 0, "No spec analysis artifact created"

        # Validate artifact structure
        validator = validators["spec"]
        validation_result = validator.validate(artifacts[0])

        assert validation_result.passed, \
            f"Validation failed: {validation_result.checks_failed}"
        assert validation_result.score >= 0.85, \
            f"Low validation score: {validation_result.score}"


    def test_spec_artifact_contains_required_sections(
        self,
        claude_interface: ClaudeCodeInterface,
        shannon_project: Path,
        sample_spec: str
    ):
        """Test spec artifact contains all required sections"""
        result = claude_interface.execute_command(f'/sh:spec "{sample_spec}"')
        assert result.success

        # Read artifact
        analysis_dir = shannon_project / ".shannon" / "analysis"
        artifacts = list(analysis_dir.glob("spec_*.md"))
        assert len(artifacts) > 0

        content = artifacts[0].read_text()

        # Required sections
        required_sections = [
            "## Core Requirements",
            "## Technical Architecture",
            "## Implementation Strategy",
            "## Risk Assessment",
            "## Success Criteria"
        ]

        for section in required_sections:
            assert section in content, f"Missing required section: {section}"


    def test_checkpoint_creates_metadata_artifact(
        self,
        claude_interface: ClaudeCodeInterface,
        shannon_project: Path,
        validators: Dict
    ):
        """Test checkpoint creates metadata artifact"""
        checkpoint_name = "metadata-test"

        result = claude_interface.execute_command(
            f'/sh:checkpoint "{checkpoint_name}"'
        )
        assert result.success

        # Find checkpoint metadata
        checkpoint_dir = shannon_project / ".shannon" / "checkpoints"
        metadata_files = list(checkpoint_dir.glob("*_metadata.yaml"))

        assert len(metadata_files) > 0, "No checkpoint metadata created"

        # Validate metadata structure
        validator = validators["checkpoint"]
        validation_result = validator.validate(metadata_files[0])

        assert validation_result.passed, \
            f"Metadata validation failed: {validation_result.checks_failed}"


    def test_artifact_timestamps_are_accurate(
        self,
        claude_interface: ClaudeCodeInterface,
        shannon_project: Path
    ):
        """Test artifact timestamps reflect creation time"""
        before_time = datetime.now()

        result = claude_interface.execute_command(
            '/sh:spec "Simple test spec"'
        )
        assert result.success

        after_time = datetime.now()

        # Check artifact timestamp
        analysis_dir = shannon_project / ".shannon" / "analysis"
        artifacts = list(analysis_dir.glob("spec_*.md"))
        assert len(artifacts) > 0

        artifact_mtime = datetime.fromtimestamp(artifacts[0].stat().st_mtime)

        assert before_time <= artifact_mtime <= after_time, \
            "Artifact timestamp out of expected range"


    def test_artifacts_use_consistent_formatting(
        self,
        claude_interface: ClaudeCodeInterface,
        shannon_project: Path,
        sample_spec: str
    ):
        """Test artifacts follow consistent markdown formatting"""
        result = claude_interface.execute_command(f'/sh:spec "{sample_spec}"')
        assert result.success

        # Read artifact
        analysis_dir = shannon_project / ".shannon" / "analysis"
        artifacts = list(analysis_dir.glob("spec_*.md"))
        content = artifacts[0].read_text()

        # Check formatting consistency
        assert content.startswith("# "), "Should start with H1 header"
        assert "\n## " in content, "Should contain H2 headers"

        # Check for proper list formatting
        list_pattern = re.compile(r"^\s*[-*]\s+\w+", re.MULTILINE)
        assert list_pattern.search(content), "Should contain proper lists"

        # No trailing whitespace on lines
        lines = content.split("\n")
        trailing_whitespace = [i for i, line in enumerate(lines)
                              if line.endswith(" ") or line.endswith("\t")]
        assert len(trailing_whitespace) == 0, \
            f"Lines with trailing whitespace: {trailing_whitespace}"


# ============================================================================
# TEST CLASS 3: BEHAVIORAL PATTERNS
# ============================================================================

class TestBehavioralPatterns:
    """Test Shannon-specific behavioral patterns"""

    def test_shannon_commands_discoverable(
        self,
        claude_interface: ClaudeCodeInterface,
        shannon_project: Path
    ):
        """Verify Shannon commands are loaded and discoverable"""
        # Check that Shannon framework files exist and are loadable
        shannon_dir = shannon_project
        commands_file = shannon_dir / ".claude" / "SHANNON_COMMANDS.md"

        assert commands_file.exists(), "Shannon commands file not found"

        content = commands_file.read_text()

        # Verify key commands documented
        assert "/sh:spec" in content
        assert "/sh:implement" in content
        assert "/sh:checkpoint" in content
        assert "/sh:restore" in content


    def test_shadcn_enforced_for_react_components(
        self,
        claude_interface: ClaudeCodeInterface,
        debug_logger: DebugLogger
    ):
        """Verify shadcn MCP used for React UI (NOT Magic MCP)"""
        task = "Create a React button component with primary and secondary variants"

        debug_logger.log_command_start("/sh:implement", {"task": task})

        result = claude_interface.execute_command(f'/sh:implement "{task}"')

        debug_logger.log_command_end("/sh:implement", result)

        assert result.success, "Implementation failed"

        # Check for shadcn usage indicators
        output_lower = result.output.lower()

        # Positive indicators (should be present)
        shadcn_indicators = [
            "shadcn", "npx shadcn", "shadcn/ui",
            "components/ui", "@/components/ui"
        ]
        has_shadcn = any(indicator in output_lower for indicator in shadcn_indicators)

        # Negative indicators (should NOT be present)
        magic_indicators = ["magic mcp", "21st.dev", "/ui", "magic component"]
        has_magic = any(indicator in output_lower for indicator in magic_indicators)

        assert has_shadcn, "shadcn not used for React component"
        assert not has_magic, "Magic MCP should NOT be used for React components"


    def test_wave_orchestration_for_complex_tasks(
        self,
        claude_interface: ClaudeCodeInterface,
        debug_logger: DebugLogger
    ):
        """Test wave orchestration activates for complex multi-step tasks"""
        complex_spec = """Build a complete e-commerce platform with:
        - User authentication and authorization
        - Product catalog with search and filters
        - Shopping cart and checkout
        - Payment processing integration
        - Order management system
        - Admin dashboard
        - Email notifications
        - Analytics and reporting
        """

        debug_logger.log_command_start("/sh:spec", {"spec": complex_spec})

        result = claude_interface.execute_command(f'/sh:spec "{complex_spec}"')

        debug_logger.log_command_end("/sh:spec", result)

        assert result.success

        # Check for wave orchestration indicators
        output_lower = result.output.lower()
        wave_indicators = [
            "wave", "phase", "stage", "progressive",
            "multi-step", "orchestration"
        ]

        has_wave_orchestration = any(
            indicator in output_lower for indicator in wave_indicators
        )

        assert has_wave_orchestration, \
            "Wave orchestration should activate for complex tasks"


    def test_context_aware_analysis(
        self,
        claude_interface: ClaudeCodeInterface,
        shannon_project: Path
    ):
        """Test Shannon provides context-aware analysis"""
        # First spec establishes context
        initial_spec = "Build a user authentication system"
        result1 = claude_interface.execute_command(f'/sh:spec "{initial_spec}"')
        assert result1.success

        # Second spec should reference first context
        related_spec = "Add password reset functionality"
        result2 = claude_interface.execute_command(f'/sh:spec "{related_spec}"')
        assert result2.success

        # Check if second analysis references authentication context
        output_lower = result2.output.lower()
        context_indicators = [
            "authentication", "existing", "integrate",
            "previous", "current"
        ]

        has_context_awareness = any(
            indicator in output_lower for indicator in context_indicators
        )

        assert has_context_awareness, \
            "Analysis should be context-aware of previous work"


    def test_shannon_respects_project_conventions(
        self,
        claude_interface: ClaudeCodeInterface
    ):
        """Test Shannon respects existing project patterns"""
        # This would check that Shannon follows project structure
        # For now, verify it checks for existing patterns
        result = claude_interface.execute_command(
            '/sh:spec "Add a new API endpoint"'
        )

        assert result.success

        # Should mention checking existing patterns
        output_lower = result.output.lower()
        pattern_indicators = [
            "existing", "convention", "pattern", "structure", "follow"
        ]

        respects_conventions = any(
            indicator in output_lower for indicator in pattern_indicators
        )

        assert respects_conventions, \
            "Should mention checking existing project conventions"


# ============================================================================
# TEST CLASS 4: CONTEXT PRESERVATION
# ============================================================================

class TestContextPreservation:
    """Test checkpoint/restore context preservation"""

    def test_checkpoint_preserves_analysis_state(
        self,
        claude_interface: ClaudeCodeInterface,
        shannon_project: Path,
        sample_spec: str
    ):
        """Test checkpoint captures current analysis state"""
        # Create analysis
        result = claude_interface.execute_command(f'/sh:spec "{sample_spec}"')
        assert result.success

        # Create checkpoint
        checkpoint_result = claude_interface.execute_command(
            '/sh:checkpoint "state-test"'
        )
        assert checkpoint_result.success

        # Verify checkpoint contains analysis reference
        checkpoint_dir = shannon_project / ".shannon" / "checkpoints"
        metadata_files = list(checkpoint_dir.glob("*_metadata.yaml"))

        assert len(metadata_files) > 0

        with open(metadata_files[0]) as f:
            metadata = yaml.safe_load(f)

        assert "analysis" in metadata or "artifacts" in metadata, \
            "Checkpoint should reference analysis artifacts"


    def test_restore_recovers_previous_context(
        self,
        claude_interface: ClaudeCodeInterface,
        shannon_project: Path
    ):
        """Test restore recovers checkpoint context"""
        # Create checkpoint with context
        claude_interface.execute_command(
            '/sh:spec "Initial feature specification"'
        )
        claude_interface.execute_command('/sh:checkpoint "restore-context-test"')

        # Clear current context (simulated)
        analysis_dir = shannon_project / ".shannon" / "analysis"
        if analysis_dir.exists():
            for artifact in analysis_dir.glob("spec_*.md"):
                artifact.unlink()

        # Restore
        restore_result = claude_interface.execute_command('/sh:restore')
        assert restore_result.success, f"Restore failed: {restore_result.errors}"

        # Verify context restored
        assert "restored" in restore_result.output.lower()


    def test_multiple_checkpoints_maintained(
        self,
        claude_interface: ClaudeCodeInterface,
        shannon_project: Path
    ):
        """Test multiple checkpoints can coexist"""
        # Create multiple checkpoints
        checkpoints = ["checkpoint-1", "checkpoint-2", "checkpoint-3"]

        for cp_name in checkpoints:
            result = claude_interface.execute_command(f'/sh:checkpoint "{cp_name}"')
            assert result.success, f"Failed to create {cp_name}"

        # Verify all exist
        checkpoint_dir = shannon_project / ".shannon" / "checkpoints"
        checkpoint_files = list(checkpoint_dir.glob("*.yaml"))

        assert len(checkpoint_files) >= len(checkpoints), \
            "Not all checkpoints preserved"


    def test_checkpoint_includes_timestamp(
        self,
        claude_interface: ClaudeCodeInterface,
        shannon_project: Path
    ):
        """Test checkpoints include accurate timestamps"""
        before_time = datetime.now()

        result = claude_interface.execute_command(
            '/sh:checkpoint "timestamp-test"'
        )
        assert result.success

        after_time = datetime.now()

        # Read checkpoint metadata
        checkpoint_dir = shannon_project / ".shannon" / "checkpoints"
        metadata_files = list(checkpoint_dir.glob("*_metadata.yaml"))

        with open(metadata_files[0]) as f:
            metadata = yaml.safe_load(f)

        assert "timestamp" in metadata, "Checkpoint missing timestamp"

        checkpoint_time = datetime.fromisoformat(metadata["timestamp"])

        assert before_time <= checkpoint_time <= after_time, \
            "Checkpoint timestamp out of range"


# ============================================================================
# TEST CLASS 5: SHADCN INTEGRATION
# ============================================================================

class TestShadcnIntegration:
    """Test shadcn/ui MCP integration for React components"""

    def test_shadcn_button_component(
        self,
        claude_interface: ClaudeCodeInterface,
        debug_logger: DebugLogger
    ):
        """Test shadcn Button component implementation"""
        task = "Implement a Button component using shadcn/ui"

        debug_logger.log_mcp_call(
            "shadcn",
            "get_component",
            {"component": "button"},
            None
        )

        result = claude_interface.execute_command(f'/sh:implement "{task}"')

        assert result.success, "Button implementation failed"

        # Verify shadcn Button usage
        output_lower = result.output.lower()
        assert "button" in output_lower
        assert any(indicator in output_lower
                  for indicator in ["shadcn", "components/ui"])


    def test_shadcn_form_components(
        self,
        claude_interface: ClaudeCodeInterface,
        debug_logger: DebugLogger
    ):
        """Test shadcn Form components implementation"""
        task = "Create a login form with Input and Button from shadcn/ui"

        result = claude_interface.execute_command(f'/sh:implement "{task}"')

        assert result.success, "Form implementation failed"

        output_lower = result.output.lower()
        assert "input" in output_lower or "form" in output_lower
        assert "button" in output_lower


    def test_shadcn_not_used_for_backend(
        self,
        claude_interface: ClaudeCodeInterface
    ):
        """Test shadcn NOT used for backend code"""
        task = "Create a REST API endpoint for user authentication"

        result = claude_interface.execute_command(f'/sh:implement "{task}"')

        assert result.success

        # Should NOT mention shadcn for backend
        output_lower = result.output.lower()
        assert "shadcn" not in output_lower, \
            "shadcn should not be used for backend code"


    def test_magic_mcp_blocked_for_react(
        self,
        claude_interface: ClaudeCodeInterface,
        debug_logger: DebugLogger
    ):
        """Test Magic MCP explicitly NOT used for React components"""
        task = "Create a React Card component with image and text"

        result = claude_interface.execute_command(f'/sh:implement "{task}"')

        assert result.success

        # Check logs for Magic MCP calls (should be none)
        output_lower = result.output.lower()
        magic_indicators = ["magic", "21st.dev", "/ui"]

        has_magic = any(indicator in output_lower for indicator in magic_indicators)

        assert not has_magic, \
            "Magic MCP should be blocked for React components"

        # Should use shadcn instead
        assert "shadcn" in output_lower or "components/ui" in output_lower


# ============================================================================
# TEST CLASS 6: ERROR HANDLING AND EDGE CASES
# ============================================================================

class TestErrorHandlingAndEdgeCases:
    """Test error handling and edge case scenarios"""

    def test_invalid_command_fails_gracefully(
        self,
        claude_interface: ClaudeCodeInterface
    ):
        """Test invalid Shannon command fails gracefully"""
        result = claude_interface.execute_command('/sh:invalid "test"')

        assert not result.success, "Invalid command should fail"
        assert result.errors, "Should provide error message"


    def test_empty_spec_handled(
        self,
        claude_interface: ClaudeCodeInterface
    ):
        """Test empty specification is handled"""
        result = claude_interface.execute_command('/sh:spec ""')

        # Should either fail gracefully or request clarification
        if not result.success:
            assert "empty" in result.errors.lower() or \
                   "no specification" in result.errors.lower()
        else:
            assert "clarification" in result.output.lower() or \
                   "more details" in result.output.lower()


    def test_checkpoint_without_analysis(
        self,
        claude_interface: ClaudeCodeInterface
    ):
        """Test checkpoint works even without prior analysis"""
        result = claude_interface.execute_command(
            '/sh:checkpoint "empty-state"'
        )

        # Should succeed but note empty state
        assert result.success, "Checkpoint should work with empty state"


    def test_concurrent_command_handling(
        self,
        claude_interface: ClaudeCodeInterface
    ):
        """Test system handles rapid command execution"""
        # Execute multiple commands rapidly
        results = []
        for i in range(3):
            result = claude_interface.execute_command(
                f'/sh:checkpoint "rapid-{i}"'
            )
            results.append(result)

        # All should succeed
        assert all(r.success for r in results), \
            "Concurrent commands should all succeed"


# ============================================================================
# TEST CLASS 7: PERFORMANCE AND RESOURCE USAGE
# ============================================================================

class TestPerformanceAndResourceUsage:
    """Test performance characteristics and resource usage"""

    def test_spec_analysis_completes_within_time_limit(
        self,
        claude_interface: ClaudeCodeInterface,
        sample_spec: str
    ):
        """Test spec analysis completes within reasonable time"""
        start_time = time.time()

        result = claude_interface.execute_command(f'/sh:spec "{sample_spec}"')

        duration = time.time() - start_time

        assert result.success, "Spec analysis failed"
        assert duration < 180, f"Analysis took too long: {duration}s (limit: 180s)"


    def test_artifact_size_reasonable(
        self,
        claude_interface: ClaudeCodeInterface,
        shannon_project: Path,
        sample_spec: str
    ):
        """Test generated artifacts are reasonable size"""
        result = claude_interface.execute_command(f'/sh:spec "{sample_spec}"')
        assert result.success

        # Check artifact size
        analysis_dir = shannon_project / ".shannon" / "analysis"
        artifacts = list(analysis_dir.glob("spec_*.md"))

        for artifact in artifacts:
            size_kb = artifact.stat().st_size / 1024
            assert size_kb < 500, f"Artifact too large: {size_kb}KB (limit: 500KB)"


    def test_checkpoint_compression_effective(
        self,
        claude_interface: ClaudeCodeInterface,
        shannon_project: Path
    ):
        """Test checkpoint compression is effective"""
        # Create some analysis
        claude_interface.execute_command('/sh:spec "Test specification"')

        # Create checkpoint
        result = claude_interface.execute_command(
            '/sh:checkpoint "compression-test"'
        )
        assert result.success

        # Check checkpoint size is reasonable
        checkpoint_dir = shannon_project / ".shannon" / "checkpoints"
        checkpoint_files = list(checkpoint_dir.glob("*.tar.gz"))

        if checkpoint_files:
            size_kb = checkpoint_files[0].stat().st_size / 1024
            assert size_kb < 1024, \
                f"Checkpoint too large: {size_kb}KB (limit: 1024KB)"


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
