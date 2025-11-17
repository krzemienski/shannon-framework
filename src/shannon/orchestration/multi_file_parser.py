"""Shannon Orchestration - Multi-File Parser

Detects and parses multi-file requests from natural language task descriptions.

A multi-file request is a task that specifies creation of multiple files in a single
command. Patterns include:
- "create auth: tokens.py, middleware.py, __init__.py"
- "generate database models: user.py, post.py, comment.py"
- "build api endpoints: users.py, auth.py, posts.py"

The parser extracts:
- Directory/module name (e.g., "auth")
- List of file names (e.g., ["tokens.py", "middleware.py", "__init__.py"])
- Base task description (e.g., "create authentication")

Example:
    parser = MultiFileParser()

    if parser.is_multi_file("create auth: tokens.py, middleware.py, __init__.py"):
        result = parser.parse("create auth: tokens.py, middleware.py, __init__.py")
        # MultiFileRequest(
        #     directory="auth",
        #     files=["tokens.py", "middleware.py", "__init__.py"],
        #     base_task="create auth"
        # )
"""

import re
import logging
from dataclasses import dataclass
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class MultiFileRequest:
    """Structured representation of a multi-file creation request"""
    directory: str                 # Target directory/module name
    files: List[str]               # List of file names to create
    base_task: str                 # Base task description without file list
    raw_task: str                  # Original task string

    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            'directory': self.directory,
            'files': self.files,
            'base_task': self.base_task,
            'raw_task': self.raw_task
        }


class MultiFileParser:
    """
    Parser for detecting and extracting multi-file creation requests.

    Supports patterns like:
    - "create auth: tokens.py, middleware.py, __init__.py"
    - "generate models: user.py, post.py"
    - "build api: users.py, posts.py, auth.py"

    The parser looks for:
    1. Action verb (create, generate, build, etc.)
    2. Directory/module name
    3. Colon separator
    4. Comma-separated list of file names
    """

    # Pattern: <action> <directory>: <file1>, <file2>, <file3>
    # Captures: directory name and comma-separated file list
    MULTI_FILE_PATTERN = re.compile(
        r'^(?:create|generate|build|add|implement)\s+'  # Action verb
        r'([a-zA-Z0-9_-]+)\s*:\s*'                      # Directory name + colon
        r'([a-zA-Z0-9_.,\s-]+)$',                       # Comma-separated files
        re.IGNORECASE
    )

    def is_multi_file(self, task: str) -> bool:
        """
        Check if task is a multi-file creation request.

        Args:
            task: Task description string

        Returns:
            True if task matches multi-file pattern, False otherwise

        Example:
            >>> parser = MultiFileParser()
            >>> parser.is_multi_file("create auth: tokens.py, middleware.py")
            True
            >>> parser.is_multi_file("create authentication system")
            False
        """
        task_normalized = task.strip()
        match = self.MULTI_FILE_PATTERN.match(task_normalized)

        if not match:
            return False

        # Verify we have at least 2 comma-separated files
        file_list_str = match.group(2)
        files = [f.strip() for f in file_list_str.split(',')]

        # Must have at least 2 files to be considered multi-file
        valid_files = [f for f in files if f]
        return len(valid_files) >= 2

    def parse(self, task: str) -> Optional[MultiFileRequest]:
        """
        Parse multi-file request into structured format.

        Args:
            task: Task description string

        Returns:
            MultiFileRequest if task is valid multi-file request, None otherwise

        Example:
            >>> parser = MultiFileParser()
            >>> result = parser.parse("create auth: tokens.py, middleware.py, __init__.py")
            >>> result.directory
            'auth'
            >>> result.files
            ['tokens.py', 'middleware.py', '__init__.py']
        """
        task_normalized = task.strip()
        match = self.MULTI_FILE_PATTERN.match(task_normalized)

        if not match:
            logger.debug(f"Task does not match multi-file pattern: {task}")
            return None

        directory = match.group(1)
        file_list_str = match.group(2)

        # Split and clean file names
        files = [f.strip() for f in file_list_str.split(',')]
        files = [f for f in files if f]  # Remove empty strings

        # Must have at least 2 files
        if len(files) < 2:
            logger.debug(f"Insufficient files ({len(files)}) in multi-file request: {task}")
            return None

        # Extract base task (action + directory)
        # Example: "create auth: tokens.py, ..." -> "create auth"
        action = task_normalized.split()[0]  # "create", "generate", etc.
        base_task = f"{action} {directory}"

        logger.info(f"Parsed multi-file request: directory={directory}, files={len(files)}")

        return MultiFileRequest(
            directory=directory,
            files=files,
            base_task=base_task,
            raw_task=task
        )

    def validate_file_names(self, files: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate that file names are reasonable (basic sanity checks).

        Args:
            files: List of file names to validate

        Returns:
            Tuple of (all_valid, list_of_errors)

        Example:
            >>> parser = MultiFileParser()
            >>> valid, errors = parser.validate_file_names(["tokens.py", "middleware.py"])
            >>> valid
            True
            >>> errors
            []
        """
        errors = []

        for file_name in files:
            # Check for empty
            if not file_name or not file_name.strip():
                errors.append("Empty file name found")
                continue

            # Check for reasonable characters
            if not re.match(r'^[a-zA-Z0-9_.-]+$', file_name):
                errors.append(f"Invalid characters in file name: {file_name}")

            # Check for extension (should have one)
            if '.' not in file_name:
                errors.append(f"File name missing extension: {file_name}")

            # Check for path separators (should not have any)
            if '/' in file_name or '\\' in file_name:
                errors.append(f"File name should not contain path separators: {file_name}")

        return (len(errors) == 0, errors)
