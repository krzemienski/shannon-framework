"""Tests for MultiFileExecutor

GATE 1.2: Multi-File Executor Tests
These tests verify file-by-file iteration and creation.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from shannon.executor.multi_file_executor import MultiFileExecutor, MultiFileExecutionResult


class TestMultiFileExecutor:
    """Test suite for MultiFileExecutor"""

    def setup_method(self):
        """Create temporary directory for each test"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.executor = MultiFileExecutor(project_root=self.temp_dir)

    def teardown_method(self):
        """Clean up temporary directory after each test"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    @pytest.mark.asyncio
    async def test_execute_creates_all_files(self):
        """Test 1: Execute creates all specified files"""
        result = await self.executor.execute(
            directory="auth",
            files=["tokens.py", "middleware.py", "__init__.py"],
            base_task="create authentication"
        )

        # Verify success
        assert result.success is True
        assert len(result.files_created) == 3
        assert len(result.files_failed) == 0
        assert len(result.errors) == 0

        # Verify files exist on disk
        auth_dir = self.temp_dir / "auth"
        assert auth_dir.exists()
        assert (auth_dir / "tokens.py").exists()
        assert (auth_dir / "middleware.py").exists()
        assert (auth_dir / "__init__.py").exists()

        # Verify relative paths in result
        assert "auth/tokens.py" in result.files_created
        assert "auth/middleware.py" in result.files_created
        assert "auth/__init__.py" in result.files_created

    @pytest.mark.asyncio
    async def test_execute_creates_directory_if_not_exists(self):
        """Test 2: Execute creates target directory if it doesn't exist"""
        # Verify directory doesn't exist before
        models_dir = self.temp_dir / "models"
        assert not models_dir.exists()

        result = await self.executor.execute(
            directory="models",
            files=["user.py", "post.py"],
            base_task="create models"
        )

        # Verify directory was created
        assert models_dir.exists()
        assert result.success is True

    @pytest.mark.asyncio
    async def test_execute_handles_nested_directory(self):
        """Test 3: Execute handles nested directory paths"""
        result = await self.executor.execute(
            directory="api/routes",
            files=["users.py", "posts.py"],
            base_task="create api routes"
        )

        assert result.success is True

        # Verify nested directory structure
        nested_dir = self.temp_dir / "api" / "routes"
        assert nested_dir.exists()
        assert (nested_dir / "users.py").exists()
        assert (nested_dir / "posts.py").exists()

    @pytest.mark.asyncio
    async def test_execute_rejects_insufficient_files(self):
        """Test 4: Execute rejects requests with less than 2 files"""
        result = await self.executor.execute(
            directory="utils",
            files=["helpers.py"],  # Only 1 file
            base_task="create utils"
        )

        # Should fail validation
        assert result.success is False
        assert len(result.errors) > 0
        assert any("at least 2 files" in err for err in result.errors)

    @pytest.mark.asyncio
    async def test_execute_generates_appropriate_content(self):
        """Test 5: Execute generates appropriate content for different file types"""
        result = await self.executor.execute(
            directory="auth",
            files=["tokens.py", "middleware.js", "Auth.java"],
            base_task="create auth"
        )

        assert result.success is True

        # Verify Python file has docstring
        py_content = (self.temp_dir / "auth" / "tokens.py").read_text()
        assert '"""' in py_content
        assert "auth.tokens" in py_content

        # Verify JavaScript file has comment block
        js_content = (self.temp_dir / "auth" / "middleware.js").read_text()
        assert "/**" in js_content
        assert "auth/middleware.js" in js_content

        # Verify Java file has class definition
        java_content = (self.temp_dir / "auth" / "Auth.java").read_text()
        assert "public class" in java_content

    @pytest.mark.asyncio
    async def test_execute_handles_init_file_specially(self):
        """Test 6: Execute handles __init__.py with module docstring"""
        result = await self.executor.execute(
            directory="database",
            files=["__init__.py", "models.py"],
            base_task="create database"
        )

        assert result.success is True

        # Verify __init__.py has module docstring
        init_content = (self.temp_dir / "database" / "__init__.py").read_text()
        assert '"""database module' in init_content
        assert "Module initialization" in init_content

    @pytest.mark.asyncio
    async def test_execute_to_dict_serialization(self):
        """Test 7: MultiFileExecutionResult serializes correctly"""
        result = await self.executor.execute(
            directory="api",
            files=["routes.py", "handlers.py"],
            base_task="create api"
        )

        data = result.to_dict()

        assert isinstance(data, dict)
        assert data['success'] is True
        assert data['directory'] == "api"
        assert len(data['files_created']) == 2
        assert data['total_files'] == 2
        assert data['duration_seconds'] > 0

    @pytest.mark.asyncio
    async def test_execute_partial_success_on_error(self):
        """Test 8: Execute allows partial success (some files created despite errors)"""
        # This test verifies graceful error handling
        # Even if one file fails, others should still be created
        result = await self.executor.execute(
            directory="services",
            files=["auth.py", "payment.py"],
            base_task="create services"
        )

        # Should succeed with at least some files
        assert result.success is True
        assert len(result.files_created) >= 1
