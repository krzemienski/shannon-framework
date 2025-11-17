"""Integration Tests for Multi-File Generation

GATE 1.4: Playwright-style Functional Validation
These tests verify the complete multi-file workflow end-to-end with real CLI execution.

This is SHANNON NO MOCKS functional testing - we test the actual CLI with real file creation.
"""

import pytest
import subprocess
import tempfile
import shutil
from pathlib import Path


class TestMultiFileIntegration:
    """Functional tests for multi-file generation feature (NO MOCKS)"""

    def setup_method(self):
        """Create temporary test directory for each test"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = Path.cwd()

    def teardown_method(self):
        """Clean up temporary directory and restore cwd"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def run_shannon_do(self, command: str) -> tuple[int, str, str]:
        """
        Run shannon do command and return (return_code, stdout, stderr).
        This is FUNCTIONAL testing - we actually run the CLI.
        """
        result = subprocess.run(
            ["shannon", "do", command],
            cwd=self.test_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode, result.stdout, result.stderr

    def test_creates_three_python_files(self):
        """
        CRITERION 1-3: Verify 3/3 Python files created
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create auth: tokens.py, middleware.py, __init__.py"
        )

        # Verify command succeeded
        assert returncode == 0, f"Command failed: {stderr}"

        # Verify all 3 files exist
        auth_dir = self.test_dir / "auth"
        assert auth_dir.exists(), "auth directory not created"
        assert (auth_dir / "tokens.py").exists(), "tokens.py not created"
        assert (auth_dir / "middleware.py").exists(), "middleware.py not created"
        assert (auth_dir / "__init__.py").exists(), "__init__.py not created"

    def test_creates_two_javascript_files(self):
        """
        CRITERION 4-5: Verify JavaScript file generation
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create utils: helpers.js, constants.js"
        )

        assert returncode == 0
        utils_dir = self.test_dir / "utils"
        assert (utils_dir / "helpers.js").exists()
        assert (utils_dir / "constants.js").exists()

    def test_creates_nested_directory_structure(self):
        """
        CRITERION 6: Verify nested directory creation
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create api/routes: users.py, posts.py"
        )

        assert returncode == 0
        nested_dir = self.test_dir / "api" / "routes"
        assert nested_dir.exists(), "Nested directory not created"
        assert (nested_dir / "users.py").exists()
        assert (nested_dir / "posts.py").exists()

    def test_python_files_have_docstrings(self):
        """
        CRITERION 7-9: Verify Python file content has proper docstrings
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create models: user.py, post.py, comment.py"
        )

        assert returncode == 0

        # Check each file has docstring
        user_content = (self.test_dir / "models" / "user.py").read_text()
        assert '"""' in user_content, "user.py missing docstring"
        assert "models.user" in user_content

        post_content = (self.test_dir / "models" / "post.py").read_text()
        assert '"""' in post_content, "post.py missing docstring"

        comment_content = (self.test_dir / "models" / "comment.py").read_text()
        assert '"""' in comment_content, "comment.py missing docstring"

    def test_init_file_has_module_initialization(self):
        """
        CRITERION 10: Verify __init__.py has proper module docstring
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create database: __init__.py, models.py"
        )

        assert returncode == 0

        init_content = (self.test_dir / "database" / "__init__.py").read_text()
        assert '"""database module' in init_content
        assert "Module initialization" in init_content

    def test_cli_output_shows_multi_file_detection(self):
        """
        CRITERION 11: Verify CLI output indicates multi-file detection
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create api: routes.py, handlers.py"
        )

        assert returncode == 0
        assert "Multi-file request detected" in stdout or "⚡" in stdout

    def test_cli_output_shows_all_files_created(self):
        """
        CRITERION 12-14: Verify CLI output lists all created files
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create services: auth.py, payment.py, email.py"
        )

        assert returncode == 0
        # Verify each file is mentioned in output
        assert "auth.py" in stdout
        assert "payment.py" in stdout
        assert "email.py" in stdout

    def test_cli_output_shows_success_message(self):
        """
        CRITERION 15: Verify success message displayed
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create utils: math.py, string.py"
        )

        assert returncode == 0
        assert ("Multi-File Creation Complete" in stdout or
                "✓" in stdout or
                "Files created" in stdout)

    def test_cli_output_shows_file_count(self):
        """
        CRITERION 16: Verify file count displayed (N/N format)
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create controllers: user.py, post.py"
        )

        assert returncode == 0
        # Should show "2/2" somewhere
        assert "2/2" in stdout

    def test_javascript_files_have_export_statements(self):
        """
        CRITERION 17-18: Verify JavaScript files have proper structure
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create lib: utils.js, helpers.js"
        )

        assert returncode == 0

        utils_content = (self.test_dir / "lib" / "utils.js").read_text()
        assert "export" in utils_content or "function" in utils_content

        helpers_content = (self.test_dir / "lib" / "helpers.js").read_text()
        assert "export" in helpers_content or "function" in helpers_content

    def test_handles_four_files(self):
        """
        CRITERION 19: Verify handles 4+ files correctly
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create models: user.py, post.py, comment.py, like.py"
        )

        assert returncode == 0

        models_dir = self.test_dir / "models"
        assert (models_dir / "user.py").exists()
        assert (models_dir / "post.py").exists()
        assert (models_dir / "comment.py").exists()
        assert (models_dir / "like.py").exists()

    def test_handles_five_files(self):
        """
        CRITERION 20: Verify handles 5+ files correctly
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create api: users.py, posts.py, comments.py, auth.py, health.py"
        )

        assert returncode == 0

        api_dir = self.test_dir / "api"
        assert len(list(api_dir.glob("*.py"))) == 5

    def test_files_have_task_context_in_comments(self):
        """
        CRITERION 21: Verify files reference the base task
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create auth: tokens.py, middleware.py"
        )

        assert returncode == 0

        tokens_content = (self.test_dir / "auth" / "tokens.py").read_text()
        # Should mention the task or module somewhere
        assert "auth" in tokens_content.lower()

    def test_files_have_related_files_context(self):
        """
        CRITERION 22: Verify files know about related files
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create database: models.py, queries.py"
        )

        assert returncode == 0

        models_content = (self.test_dir / "database" / "models.py").read_text()
        # Should mention related files in comments
        assert "queries.py" in models_content or "Related files" in models_content

    def test_directory_created_if_not_exists(self):
        """
        CRITERION 23: Verify directory auto-creation
        """
        # Verify directory doesn't exist before
        new_dir = self.test_dir / "newmodule"
        assert not new_dir.exists()

        returncode, stdout, stderr = self.run_shannon_do(
            "create newmodule: a.py, b.py"
        )

        assert returncode == 0
        assert new_dir.exists()

    def test_execution_completes_quickly(self):
        """
        CRITERION 24: Verify reasonable execution time (< 5 seconds)
        """
        import time
        start_time = time.time()

        returncode, stdout, stderr = self.run_shannon_do(
            "create fast: a.py, b.py, c.py"
        )

        duration = time.time() - start_time

        assert returncode == 0
        assert duration < 5.0, f"Execution took {duration:.1f}s, expected < 5s"

    def test_single_file_bypasses_multifile(self):
        """
        CRITERION 25: Verify single-file requests bypass multi-file detection
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create hello.py"
        )

        # Single file should NOT trigger multi-file detection
        # It may fail due to other reasons (out of scope for this agent)
        # but should not show "Multi-file request detected"
        assert "Multi-file request detected" not in stdout
        assert "⚡" not in stdout or "multi-file" not in stdout.lower()

    def test_cli_exit_code_zero_on_success(self):
        """
        CRITERION 26: Verify exit code 0 on success
        """
        returncode, stdout, stderr = self.run_shannon_do(
            "create final: test.py, demo.py"
        )

        assert returncode == 0, f"Expected exit code 0, got {returncode}"
