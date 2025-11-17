"""
Shannon Skills Framework - Skill Loader

The SkillLoader is responsible for reading skill definitions from YAML/JSON files,
validating them against the JSON Schema, and creating Skill objects for registration.

Features:
- Load from YAML (.yaml, .yml) and JSON (.json) files
- Automatic format detection based on file extension
- JSON Schema validation via SkillRegistry
- Batch loading from directories (recursive)
- Comprehensive error handling and logging
- Graceful handling of malformed files
- Skip non-skill files (.md, .txt, etc.)

Usage:
    registry = SkillRegistry(schema_path=Path("schemas/skill.schema.json"))
    loader = SkillLoader(registry)

    # Load single skill
    skill = await loader.load_from_file(Path("skills/my_skill.yaml"))

    # Load all skills from directory
    skills = await loader.load_from_directory(Path("skills/"))
"""

import asyncio
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

from shannon.skills.models import Skill
from shannon.skills.registry import SkillRegistry, SkillValidationError, SkillConflictError

logger = logging.getLogger(__name__)


class SkillLoadError(Exception):
    """Base exception for skill loading errors"""
    pass


class SkillParseError(SkillLoadError):
    """Raised when skill file cannot be parsed"""
    pass


class SkillFileError(SkillLoadError):
    """Raised when skill file cannot be read"""
    pass


class SkillLoader:
    """
    Load skills from YAML/JSON files with validation and error handling.

    The loader handles:
    1. Reading skill definitions from disk
    2. Parsing YAML/JSON content
    3. Validation against JSON Schema (via SkillRegistry)
    4. Creating Skill objects from validated data
    5. Automatic registration in the provided registry
    6. Batch loading with error recovery

    Design Principles:
    - Fail gracefully: Invalid files are logged but don't stop batch loads
    - Validate early: Schema validation happens before Skill creation
    - Clear errors: Detailed error messages for debugging
    - Performance: Async I/O for parallel file loading

    Thread Safety:
        The loader itself is not thread-safe, but it delegates to
        SkillRegistry which handles thread-safe registration.
    """

    # Supported file extensions
    YAML_EXTENSIONS = {'.yaml', '.yml'}
    JSON_EXTENSIONS = {'.json'}
    SUPPORTED_EXTENSIONS = YAML_EXTENSIONS | JSON_EXTENSIONS

    # File patterns to skip during directory scanning
    SKIP_PATTERNS = {
        '.md', '.txt', '.py', '.pyc', '.git', '.DS_Store',
        '__pycache__', '__init__', 'README', 'LICENSE'
    }

    def __init__(self, registry: SkillRegistry):
        """
        Initialize the skill loader.

        Args:
            registry: SkillRegistry instance for validation and registration

        Example:
            registry = SkillRegistry(schema_path=Path("schemas/skill.schema.json"))
            loader = SkillLoader(registry)
        """
        self.registry = registry
        logger.info("SkillLoader initialized")

    def _should_process_file(self, file_path: Path) -> bool:
        """
        Check if a file should be processed as a skill definition.

        Filters out:
        - Non-skill files (.md, .txt, .py, etc.)
        - Hidden files and system files
        - Directories

        Args:
            file_path: Path to check

        Returns:
            True if file should be processed, False otherwise
        """
        # Must be a file
        if not file_path.is_file():
            return False

        # Check file extension
        if file_path.suffix not in self.SUPPORTED_EXTENSIONS:
            return False

        # Skip hidden files
        if file_path.name.startswith('.'):
            return False

        # Skip files matching skip patterns
        for pattern in self.SKIP_PATTERNS:
            if pattern in file_path.name:
                return False

        return True

    def _read_file_content(self, file_path: Path) -> str:
        """
        Read file content with error handling.

        Args:
            file_path: Path to file

        Returns:
            File content as string

        Raises:
            SkillFileError: If file cannot be read
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.debug(f"Read {len(content)} bytes from {file_path}")
            return content
        except FileNotFoundError:
            raise SkillFileError(f"Skill file not found: {file_path}")
        except PermissionError:
            raise SkillFileError(f"Permission denied reading: {file_path}")
        except UnicodeDecodeError as e:
            raise SkillFileError(f"Invalid UTF-8 encoding in {file_path}: {e}")
        except Exception as e:
            raise SkillFileError(f"Error reading {file_path}: {e}")

    def _parse_yaml(self, content: str, file_path: Path) -> Dict[str, Any]:
        """
        Parse YAML content into dictionary.

        Args:
            content: YAML content string
            file_path: Path to file (for error messages)

        Returns:
            Parsed dictionary

        Raises:
            SkillParseError: If YAML is invalid
        """
        try:
            data = yaml.safe_load(content)
            if not isinstance(data, dict):
                raise SkillParseError(
                    f"YAML content must be a dictionary, got {type(data).__name__}: {file_path}"
                )
            logger.debug(f"Parsed YAML from {file_path}")
            return data
        except yaml.YAMLError as e:
            error_msg = f"Invalid YAML syntax in {file_path}: {e}"
            logger.error(error_msg)
            raise SkillParseError(error_msg) from e
        except Exception as e:
            error_msg = f"Error parsing YAML from {file_path}: {e}"
            logger.error(error_msg)
            raise SkillParseError(error_msg) from e

    def _parse_json(self, content: str, file_path: Path) -> Dict[str, Any]:
        """
        Parse JSON content into dictionary.

        Args:
            content: JSON content string
            file_path: Path to file (for error messages)

        Returns:
            Parsed dictionary

        Raises:
            SkillParseError: If JSON is invalid
        """
        try:
            data = json.loads(content)
            if not isinstance(data, dict):
                raise SkillParseError(
                    f"JSON content must be an object, got {type(data).__name__}: {file_path}"
                )
            logger.debug(f"Parsed JSON from {file_path}")
            return data
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON syntax in {file_path} at line {e.lineno}, col {e.colno}: {e.msg}"
            logger.error(error_msg)
            raise SkillParseError(error_msg) from e
        except Exception as e:
            error_msg = f"Error parsing JSON from {file_path}: {e}"
            logger.error(error_msg)
            raise SkillParseError(error_msg) from e

    def _parse_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse skill file based on extension.

        Automatically detects format (YAML/JSON) and uses appropriate parser.

        Args:
            file_path: Path to skill definition file

        Returns:
            Parsed skill definition dictionary

        Raises:
            SkillFileError: If file cannot be read
            SkillParseError: If content cannot be parsed
        """
        # Read file content
        content = self._read_file_content(file_path)

        # Parse based on extension
        if file_path.suffix in self.YAML_EXTENSIONS:
            return self._parse_yaml(content, file_path)
        elif file_path.suffix in self.JSON_EXTENSIONS:
            return self._parse_json(content, file_path)
        else:
            raise SkillParseError(
                f"Unsupported file extension: {file_path.suffix}. "
                f"Supported: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )

    def _validate_skill_definition(self, skill_def: Dict[str, Any], file_path: Path) -> None:
        """
        Validate skill definition dictionary against JSON Schema.

        This delegates to SkillRegistry for validation, which uses jsonschema.

        Args:
            skill_def: Skill definition dictionary
            file_path: Path to file (for error messages)

        Raises:
            SkillValidationError: If validation fails
        """
        try:
            # Create temporary Skill object for validation
            skill = Skill.from_dict(skill_def)

            # Validate via registry (which validates against schema)
            self.registry._validate_skill(skill)

            logger.debug(f"Validated skill definition from {file_path}")
        except SkillValidationError:
            # Re-raise validation errors as-is
            raise
        except Exception as e:
            error_msg = f"Error validating skill from {file_path}: {e}"
            logger.error(error_msg)
            raise SkillValidationError(error_msg) from e

    async def load_from_file(self, skill_file: Path, register: bool = True) -> Skill:
        """
        Load a single skill from YAML/JSON file.

        This is the main entry point for loading individual skills.
        It handles the complete pipeline:
        1. Read and parse file
        2. Validate against schema
        3. Create Skill object
        4. Register in registry (optional)

        Args:
            skill_file: Path to skill definition file (.yaml/.yml/.json)
            register: Whether to register skill in registry (default: True)

        Returns:
            Loaded and validated Skill instance

        Raises:
            SkillFileError: If file cannot be read
            SkillParseError: If content cannot be parsed
            SkillValidationError: If validation fails
            SkillConflictError: If skill name conflicts (when register=True)

        Example:
            # Load and register
            skill = await loader.load_from_file(Path("skills/my_skill.yaml"))

            # Load without registering
            skill = await loader.load_from_file(
                Path("skills/my_skill.yaml"),
                register=False
            )
        """
        logger.info(f"Loading skill from {skill_file}")

        try:
            # Parse file
            skill_def = self._parse_file(skill_file)

            # Validate definition
            self._validate_skill_definition(skill_def, skill_file)

            # Create Skill object
            skill = Skill.from_dict(skill_def)

            # Register if requested
            if register:
                await self.registry.register(skill)
                logger.info(
                    f"Successfully loaded and registered skill '{skill.name}' "
                    f"from {skill_file}"
                )
            else:
                logger.info(
                    f"Successfully loaded skill '{skill.name}' from {skill_file} "
                    f"(not registered)"
                )

            return skill

        except (SkillFileError, SkillParseError, SkillValidationError) as e:
            # Re-raise known errors
            logger.error(f"Failed to load skill from {skill_file}: {e}")
            raise
        except SkillConflictError:
            # Re-raise conflict errors as-is (from registry)
            raise
        except Exception as e:
            # Wrap unexpected errors
            error_msg = f"Unexpected error loading skill from {skill_file}: {e}"
            logger.error(error_msg)
            raise SkillLoadError(error_msg) from e

    async def load_from_directory(
        self,
        skills_dir: Path,
        recursive: bool = True,
        register: bool = True
    ) -> List[Skill]:
        """
        Load all skills from a directory.

        This method provides batch loading with:
        - Recursive directory traversal (optional)
        - Graceful error handling (invalid files are logged but don't stop the process)
        - Parallel loading for performance
        - Comprehensive error reporting

        Args:
            skills_dir: Directory containing skill files
            recursive: Whether to search subdirectories (default: True)
            register: Whether to register skills in registry (default: True)

        Returns:
            List of successfully loaded Skill instances

        Example:
            # Load all skills recursively
            skills = await loader.load_from_directory(Path("skills/"))

            # Load only from top-level directory
            skills = await loader.load_from_directory(
                Path("skills/"),
                recursive=False
            )

        Note:
            Invalid files are logged as warnings but don't prevent other files
            from being loaded. Check logs for details on any failed loads.
        """
        logger.info(
            f"Loading skills from {skills_dir} "
            f"(recursive={recursive}, register={register})"
        )

        # Verify directory exists
        if not skills_dir.exists():
            raise SkillFileError(f"Directory not found: {skills_dir}")

        if not skills_dir.is_dir():
            raise SkillFileError(f"Not a directory: {skills_dir}")

        # Find all skill files
        skill_files = []

        if recursive:
            # Recursive search
            for file_path in skills_dir.rglob('*'):
                if self._should_process_file(file_path):
                    skill_files.append(file_path)
        else:
            # Top-level only
            for file_path in skills_dir.iterdir():
                if self._should_process_file(file_path):
                    skill_files.append(file_path)

        logger.info(f"Found {len(skill_files)} skill files to process")

        if not skill_files:
            logger.warning(f"No skill files found in {skills_dir}")
            return []

        # Load all skills
        loaded_skills = []
        failed_files = []

        for file_path in skill_files:
            try:
                skill = await self.load_from_file(file_path, register=register)
                loaded_skills.append(skill)
            except (SkillFileError, SkillParseError, SkillValidationError) as e:
                # Log error but continue processing
                logger.warning(f"Skipping {file_path}: {e}")
                failed_files.append((file_path, str(e)))
            except Exception as e:
                # Log unexpected errors but continue
                logger.warning(f"Unexpected error loading {file_path}: {e}")
                failed_files.append((file_path, f"Unexpected error: {e}"))

        # Summary logging
        logger.info(
            f"Batch load complete: {len(loaded_skills)} skills loaded, "
            f"{len(failed_files)} failed"
        )

        if failed_files:
            logger.warning("Failed files:")
            for file_path, error in failed_files:
                logger.warning(f"  - {file_path}: {error}")

        return loaded_skills

    async def reload_skill(self, skill_file: Path) -> Skill:
        """
        Reload a skill from file, replacing existing registration.

        This is useful for:
        - Hot-reloading skills during development
        - Updating skills without restart
        - Refreshing skills from disk

        Args:
            skill_file: Path to skill file

        Returns:
            Reloaded Skill instance

        Raises:
            SkillFileError: If file cannot be read
            SkillParseError: If content cannot be parsed
            SkillValidationError: If validation fails

        Example:
            # Reload a skill
            skill = await loader.reload_skill(Path("skills/my_skill.yaml"))
        """
        logger.info(f"Reloading skill from {skill_file}")

        # Parse to get skill name
        skill_def = self._parse_file(skill_file)
        skill_name = skill_def.get('name')

        # Unregister if exists
        if skill_name and self.registry.exists(skill_name):
            await self.registry.unregister(skill_name)
            logger.debug(f"Unregistered existing skill '{skill_name}'")

        # Load and register
        return await self.load_from_file(skill_file, register=True)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get loader statistics.

        Returns:
            Dictionary with loader statistics

        Example:
            stats = loader.get_statistics()
            print(f"Supported formats: {stats['supported_formats']}")
        """
        return {
            'supported_formats': list(self.SUPPORTED_EXTENSIONS),
            'yaml_extensions': list(self.YAML_EXTENSIONS),
            'json_extensions': list(self.JSON_EXTENSIONS),
            'skip_patterns': list(self.SKIP_PATTERNS),
            'registry_skill_count': len(self.registry),
        }

    def __repr__(self) -> str:
        """String representation of loader"""
        return f"<SkillLoader: registry={len(self.registry)} skills>"
