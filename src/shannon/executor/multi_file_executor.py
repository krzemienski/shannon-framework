"""Shannon Executor - Multi-File Executor

Executes multi-file creation requests by iterating through files and creating
each one individually with appropriate context.

For a request like "create auth: tokens.py, middleware.py, __init__.py", this executor:
1. Validates the multi-file request structure
2. Creates the target directory if needed
3. Iterates through each file
4. Generates appropriate content for each file with context about the module
5. Writes files to disk
6. Reports progress and errors

Example:
    executor = MultiFileExecutor(project_root=Path.cwd())

    result = await executor.execute(
        directory="auth",
        files=["tokens.py", "middleware.py", "__init__.py"],
        base_task="create authentication"
    )

    # result.success = True
    # result.files_created = ["auth/tokens.py", "auth/middleware.py", "auth/__init__.py"]
"""

import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class MultiFileExecutionResult:
    """Result of multi-file execution"""
    success: bool
    directory: str
    files_created: List[str] = field(default_factory=list)
    files_failed: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    total_files: int = 0
    duration_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'success': self.success,
            'directory': self.directory,
            'files_created': self.files_created,
            'files_failed': self.files_failed,
            'errors': self.errors,
            'total_files': self.total_files,
            'duration_seconds': self.duration_seconds
        }


class MultiFileExecutor:
    """
    Executor for multi-file creation requests.

    Handles the complexity of creating multiple related files by:
    1. Creating the target directory structure
    2. Iterating through each file in the request
    3. Generating appropriate content for each file
    4. Maintaining context about the overall module being created
    5. Handling errors gracefully (partial success possible)

    Thread-safe and designed for async execution.
    """

    def __init__(self, project_root: Path):
        """
        Initialize multi-file executor.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root)
        logger.info(f"MultiFileExecutor initialized with project_root: {self.project_root}")

    async def execute(
        self,
        directory: str,
        files: List[str],
        base_task: str,
        context: Optional[Dict[str, Any]] = None
    ) -> MultiFileExecutionResult:
        """
        Execute multi-file creation request.

        Args:
            directory: Target directory name (e.g., "auth")
            files: List of file names to create (e.g., ["tokens.py", "middleware.py"])
            base_task: Base task description (e.g., "create authentication")
            context: Optional execution context

        Returns:
            MultiFileExecutionResult with success status and created files

        Example:
            result = await executor.execute(
                directory="auth",
                files=["tokens.py", "middleware.py", "__init__.py"],
                base_task="create authentication"
            )
        """
        import time
        start_time = time.time()

        logger.info(f"Starting multi-file execution: {directory} with {len(files)} files")

        result = MultiFileExecutionResult(
            success=False,
            directory=directory,
            total_files=len(files)
        )

        try:
            # Step 1: Validate inputs
            if not directory or not files:
                result.errors.append("Invalid directory or files list")
                return result

            if len(files) < 2:
                result.errors.append(f"Multi-file request requires at least 2 files, got {len(files)}")
                return result

            # Step 2: Create target directory
            target_dir = self.project_root / directory
            try:
                target_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {target_dir}")
            except Exception as e:
                result.errors.append(f"Failed to create directory {target_dir}: {e}")
                return result

            # Step 3: Iterate through files and create each one
            for file_name in files:
                try:
                    file_path = target_dir / file_name
                    success = await self._create_file(
                        file_path=file_path,
                        file_name=file_name,
                        directory=directory,
                        base_task=base_task,
                        all_files=files,
                        context=context or {}
                    )

                    if success:
                        # Store relative path from project root
                        relative_path = file_path.relative_to(self.project_root)
                        result.files_created.append(str(relative_path))
                        logger.info(f"Created file: {relative_path}")
                    else:
                        result.files_failed.append(file_name)
                        result.errors.append(f"Failed to create {file_name}")

                except Exception as e:
                    result.files_failed.append(file_name)
                    result.errors.append(f"Error creating {file_name}: {e}")
                    logger.error(f"Error creating {file_name}: {e}")

            # Step 4: Determine overall success
            # Success if at least some files created (partial success allowed)
            result.success = len(result.files_created) > 0

            result.duration_seconds = time.time() - start_time

            logger.info(
                f"Multi-file execution complete: "
                f"{len(result.files_created)}/{result.total_files} files created, "
                f"duration: {result.duration_seconds:.2f}s"
            )

            return result

        except Exception as e:
            result.errors.append(f"Execution failed: {e}")
            result.duration_seconds = time.time() - start_time
            logger.error(f"Multi-file execution failed: {e}")
            return result

    async def _create_file(
        self,
        file_path: Path,
        file_name: str,
        directory: str,
        base_task: str,
        all_files: List[str],
        context: Dict[str, Any]
    ) -> bool:
        """
        Create a single file with appropriate content.

        Args:
            file_path: Full path where file should be created
            file_name: Name of the file (e.g., "tokens.py")
            directory: Directory name (e.g., "auth")
            base_task: Base task description
            all_files: List of all files in this multi-file request
            context: Execution context

        Returns:
            True if file created successfully, False otherwise
        """
        try:
            # Generate appropriate file content
            content = self._generate_file_content(
                file_name=file_name,
                directory=directory,
                base_task=base_task,
                all_files=all_files,
                context=context
            )

            # Write file to disk
            file_path.write_text(content, encoding='utf-8')

            logger.debug(f"Wrote {len(content)} bytes to {file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to create file {file_path}: {e}")
            return False

    def _generate_file_content(
        self,
        file_name: str,
        directory: str,
        base_task: str,
        all_files: List[str],
        context: Dict[str, Any]
    ) -> str:
        """
        Generate appropriate content for a file.

        For now, this creates placeholder content with proper structure.
        In a full implementation, this would use Claude SDK to generate
        real code based on the task and file context.

        Args:
            file_name: Name of the file
            directory: Directory name
            base_task: Base task description
            all_files: All files in this multi-file request
            context: Execution context

        Returns:
            File content as string
        """
        # Detect file type from extension
        extension = Path(file_name).suffix

        # Build context comment about the module
        module_context = f"Part of {directory} module\n"
        module_context += f"Task: {base_task}\n"
        module_context += f"Related files: {', '.join(all_files)}"

        # Generate content based on file type
        if extension == ".py":
            return self._generate_python_content(file_name, module_context, directory)
        elif extension == ".js" or extension == ".ts":
            return self._generate_javascript_content(file_name, module_context, directory)
        elif extension == ".java":
            return self._generate_java_content(file_name, module_context, directory)
        else:
            # Generic placeholder
            return f"# {file_name}\n# {module_context}\n\n# TODO: Implement {file_name}\n"

    def _generate_python_content(self, file_name: str, context: str, directory: str) -> str:
        """Generate Python file content"""
        base_name = Path(file_name).stem

        if file_name == "__init__.py":
            return f'"""{directory} module\n\n{context}\n"""\n\n# Module initialization\n'

        return f'''"""{directory}.{base_name}

{context}
"""


def placeholder():
    """Placeholder function - implement actual functionality"""
    pass
'''

    def _generate_javascript_content(self, file_name: str, context: str, directory: str) -> str:
        """Generate JavaScript/TypeScript file content"""
        base_name = Path(file_name).stem

        return f'''/**
 * {directory}/{file_name}
 *
 * {context}
 */

// TODO: Implement {base_name} functionality
export function placeholder() {{
  // Placeholder function
}}
'''

    def _generate_java_content(self, file_name: str, context: str, directory: str) -> str:
        """Generate Java file content"""
        base_name = Path(file_name).stem
        class_name = base_name.capitalize()

        return f'''/**
 * {directory}/{file_name}
 *
 * {context}
 */

public class {class_name} {{
    // TODO: Implement {class_name} functionality
}}
'''
