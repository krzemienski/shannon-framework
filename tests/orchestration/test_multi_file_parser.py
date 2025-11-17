"""Tests for MultiFileParser

GATE 1.1: Backend Unit Tests
These tests verify multi-file pattern detection and parsing.
"""

import pytest
from shannon.orchestration.multi_file_parser import MultiFileParser, MultiFileRequest


class TestMultiFileParser:
    """Test suite for MultiFileParser"""

    def setup_method(self):
        """Create parser instance for each test"""
        self.parser = MultiFileParser()

    def test_is_multi_file_valid_patterns(self):
        """Test 1: Detect valid multi-file patterns"""
        # Valid patterns with 2+ files
        valid_tasks = [
            "create auth: tokens.py, middleware.py, __init__.py",
            "generate models: user.py, post.py",
            "build api: users.py, posts.py, auth.py",
            "create utils: helpers.py, constants.py",
        ]

        for task in valid_tasks:
            assert self.parser.is_multi_file(task), f"Should detect multi-file: {task}"

    def test_is_multi_file_invalid_patterns(self):
        """Test 2: Reject invalid patterns"""
        # Invalid patterns
        invalid_tasks = [
            "create authentication system",  # No colon + file list
            "create auth: tokens.py",        # Only 1 file (not multi)
            "create auth",                   # No file list
            "tokens.py, middleware.py",      # No action + directory
            "",                              # Empty
        ]

        for task in invalid_tasks:
            assert not self.parser.is_multi_file(task), f"Should NOT detect multi-file: {task}"

    def test_parse_extracts_correct_structure(self):
        """Test 3: Parse extracts directory, files, and base task correctly"""
        task = "create auth: tokens.py, middleware.py, __init__.py"
        result = self.parser.parse(task)

        assert result is not None, "Should successfully parse valid multi-file task"
        assert isinstance(result, MultiFileRequest)

        # Verify extracted fields
        assert result.directory == "auth"
        assert result.files == ["tokens.py", "middleware.py", "__init__.py"]
        assert result.base_task == "create auth"
        assert result.raw_task == task

    def test_parse_handles_whitespace(self):
        """Test 4: Parse handles extra whitespace in file list"""
        task = "create models: user.py,  post.py  , comment.py"
        result = self.parser.parse(task)

        assert result is not None
        # Files should be trimmed
        assert result.files == ["user.py", "post.py", "comment.py"]

    def test_parse_returns_none_for_invalid(self):
        """Test 5: Parse returns None for invalid patterns"""
        invalid_tasks = [
            "create authentication system",
            "not a multi-file request",
            "",
        ]

        for task in invalid_tasks:
            result = self.parser.parse(task)
            assert result is None, f"Should return None for invalid: {task}"

    def test_validate_file_names_accepts_valid(self):
        """Test 6: Validate accepts valid file names"""
        valid_files = ["tokens.py", "middleware.py", "__init__.py", "utils_v2.py"]
        is_valid, errors = self.parser.validate_file_names(valid_files)

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_file_names_rejects_invalid(self):
        """Test 7: Validate rejects invalid file names"""
        # Missing extension
        invalid_files = ["noextension"]
        is_valid, errors = self.parser.validate_file_names(invalid_files)
        assert is_valid is False
        assert any("extension" in err.lower() for err in errors)

        # Path separator
        invalid_files = ["path/to/file.py"]
        is_valid, errors = self.parser.validate_file_names(invalid_files)
        assert is_valid is False
        assert any("separator" in err.lower() for err in errors)

        # Invalid characters
        invalid_files = ["file@#$.py"]
        is_valid, errors = self.parser.validate_file_names(invalid_files)
        assert is_valid is False
        assert any("character" in err.lower() for err in errors)

    def test_to_dict_serialization(self):
        """Test 8: MultiFileRequest serializes to dict correctly"""
        task = "create auth: tokens.py, middleware.py"
        result = self.parser.parse(task)

        assert result is not None
        data = result.to_dict()

        assert isinstance(data, dict)
        assert data['directory'] == "auth"
        assert data['files'] == ["tokens.py", "middleware.py"]
        assert data['base_task'] == "create auth"
        assert data['raw_task'] == task
