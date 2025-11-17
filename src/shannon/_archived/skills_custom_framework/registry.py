"""
Shannon Skills Framework - Central Skill Registry

The SkillRegistry is the central component for managing all skills in Shannon v4.0.
It provides thread-safe registration, validation, querying, and lifecycle management
for all discovered and loaded skills.

Features:
- Singleton pattern for global access
- JSON Schema validation for all skills
- Conflict detection and duplicate prevention
- Thread-safe async operations with asyncio.Lock
- Rich query API (by name, category, domain, tags)
- Metadata tracking and usage statistics
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime
import logging

from jsonschema import validate, ValidationError as JSONValidationError

from shannon.skills.models import Skill, ExecutionType

logger = logging.getLogger(__name__)


class SkillRegistrationError(Exception):
    """Raised when skill registration fails"""
    pass


class SkillConflictError(SkillRegistrationError):
    """Raised when attempting to register a duplicate skill"""
    pass


class SkillValidationError(SkillRegistrationError):
    """Raised when skill validation fails"""
    pass


class SkillNotFoundError(Exception):
    """Raised when attempting to access a non-existent skill"""
    pass


class SkillRegistry:
    """
    Central registry for all discovered and loaded skills.

    This is the primary interface for skill management in Shannon v4.0.
    It maintains a thread-safe collection of validated skills and provides
    rich query capabilities for skill discovery and orchestration.

    Thread Safety:
        All mutating operations (register, unregister) use asyncio.Lock
        to ensure thread-safe concurrent access. Read operations are
        lock-free for performance.

    Schema Validation:
        All skills are validated against the JSON Schema before registration.
        Invalid skills are rejected with detailed error messages.

    Usage:
        registry = SkillRegistry(schema_path=Path("schemas/skill.schema.json"))

        # Register a skill
        await registry.register(skill)

        # Query skills
        skill = registry.get("my_skill")
        all_skills = registry.list_all()
        testing_skills = registry.find_by_category("testing")
        ios_skills = registry.find_for_domain("iOS")
    """

    _instance: Optional['SkillRegistry'] = None
    _lock_instance: asyncio.Lock = asyncio.Lock()

    def __init__(self, schema_path: Path):
        """
        Initialize the skill registry.

        Args:
            schema_path: Path to the skill.schema.json file for validation

        Raises:
            FileNotFoundError: If schema file doesn't exist
            json.JSONDecodeError: If schema file is invalid JSON
        """
        self.schema_path = schema_path
        self.schema = self._load_schema(schema_path)
        self.skills: Dict[str, Skill] = {}
        self._lock = asyncio.Lock()

        # Indexes for efficient querying
        self._category_index: Dict[str, Set[str]] = {}
        self._domain_index: Dict[str, Set[str]] = {}
        self._tag_index: Dict[str, Set[str]] = {}

        logger.info(f"SkillRegistry initialized with schema from {schema_path}")

    @classmethod
    async def get_instance(cls, schema_path: Optional[Path] = None) -> 'SkillRegistry':
        """
        Get or create the singleton registry instance.

        Args:
            schema_path: Path to schema (required for first call)

        Returns:
            The singleton SkillRegistry instance

        Raises:
            ValueError: If schema_path not provided on first call
        """
        async with cls._lock_instance:
            if cls._instance is None:
                if schema_path is None:
                    raise ValueError("schema_path required for first registry initialization")
                cls._instance = cls(schema_path)
            return cls._instance

    @classmethod
    def reset_instance(cls):
        """Reset singleton instance (primarily for testing)"""
        cls._instance = None

    def _load_schema(self, schema_path: Path) -> Dict:
        """
        Load and parse the JSON Schema file.

        Args:
            schema_path: Path to schema file

        Returns:
            Parsed JSON schema dictionary

        Raises:
            FileNotFoundError: If schema file doesn't exist
            json.JSONDecodeError: If schema is invalid JSON
        """
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        try:
            with open(schema_path, 'r') as f:
                schema = json.load(f)
            logger.debug(f"Loaded schema from {schema_path}")
            return schema
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in schema file: {e}")
            raise

    def _clean_dict_for_validation(self, data: Dict) -> Dict:
        """
        Recursively remove None values from dictionary for schema validation.

        The JSON Schema doesn't allow null values, only missing keys.
        This helper cleans the dictionary to ensure validation passes.

        Args:
            data: Dictionary to clean

        Returns:
            Cleaned dictionary without None values
        """
        if not isinstance(data, dict):
            return data

        cleaned = {}
        for key, value in data.items():
            if value is None:
                continue  # Skip None values
            elif isinstance(value, dict):
                cleaned[key] = self._clean_dict_for_validation(value)
            elif isinstance(value, list):
                cleaned[key] = [
                    self._clean_dict_for_validation(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                cleaned[key] = value

        return cleaned

    def _validate_skill(self, skill: Skill) -> None:
        """
        Validate skill against JSON Schema.

        Args:
            skill: Skill to validate

        Raises:
            SkillValidationError: If validation fails
        """
        try:
            # Convert skill to dict for validation
            skill_dict = skill.to_dict()

            # Remove None values for schema validation
            # The schema doesn't allow null values, only missing keys
            cleaned_dict = self._clean_dict_for_validation(skill_dict)

            validate(instance=cleaned_dict, schema=self.schema)
            logger.debug(f"Skill '{skill.name}' passed schema validation")
        except JSONValidationError as e:
            error_msg = f"Skill validation failed for '{skill.name}': {e.message}"
            logger.error(error_msg)
            raise SkillValidationError(error_msg) from e

    def _check_conflicts(self, skill: Skill) -> None:
        """
        Check for naming conflicts with existing skills.

        Args:
            skill: Skill to check

        Raises:
            SkillConflictError: If skill with same name already exists
        """
        if skill.name in self.skills:
            existing = self.skills[skill.name]
            error_msg = (
                f"Skill conflict: '{skill.name}' already registered "
                f"(version {existing.version})"
            )
            logger.error(error_msg)
            raise SkillConflictError(error_msg)

    def _update_indexes(self, skill: Skill) -> None:
        """
        Update internal indexes for efficient querying.

        Args:
            skill: Skill to index
        """
        # Category index
        if skill.category not in self._category_index:
            self._category_index[skill.category] = set()
        self._category_index[skill.category].add(skill.name)

        # Domain index (from tags)
        for tag in skill.metadata.tags:
            if tag not in self._domain_index:
                self._domain_index[tag] = set()
            self._domain_index[tag].add(skill.name)

        # Tag index
        for tag in skill.metadata.tags:
            if tag not in self._tag_index:
                self._tag_index[tag] = set()
            self._tag_index[tag].add(skill.name)

        logger.debug(f"Updated indexes for skill '{skill.name}'")

    def _remove_from_indexes(self, skill: Skill) -> None:
        """
        Remove skill from internal indexes.

        Args:
            skill: Skill to remove from indexes
        """
        # Remove from category index
        if skill.category in self._category_index:
            self._category_index[skill.category].discard(skill.name)
            if not self._category_index[skill.category]:
                del self._category_index[skill.category]

        # Remove from domain and tag indexes
        for tag in skill.metadata.tags:
            if tag in self._domain_index:
                self._domain_index[tag].discard(skill.name)
                if not self._domain_index[tag]:
                    del self._domain_index[tag]

            if tag in self._tag_index:
                self._tag_index[tag].discard(skill.name)
                if not self._tag_index[tag]:
                    del self._tag_index[tag]

        logger.debug(f"Removed '{skill.name}' from indexes")

    async def register(self, skill: Skill) -> None:
        """
        Register a new skill with validation and conflict checking.

        This is the primary method for adding skills to the registry.
        It performs comprehensive validation and ensures no conflicts
        with existing skills.

        Args:
            skill: Skill instance to register

        Raises:
            SkillValidationError: If skill fails schema validation
            SkillConflictError: If skill name already exists

        Example:
            skill = Skill.from_dict(skill_data)
            await registry.register(skill)
        """
        async with self._lock:
            # Validate against schema
            self._validate_skill(skill)

            # Check for conflicts
            self._check_conflicts(skill)

            # Update metadata
            if skill.metadata.created is None:
                skill.metadata.created = datetime.now()
            skill.metadata.updated = datetime.now()

            # Register the skill
            self.skills[skill.name] = skill
            self._update_indexes(skill)

            logger.info(
                f"Registered skill '{skill.name}' v{skill.version} "
                f"(category: {skill.category}, type: {skill.execution.type.value})"
            )

    async def unregister(self, name: str) -> bool:
        """
        Unregister a skill by name.

        Args:
            name: Name of skill to unregister

        Returns:
            True if skill was unregistered, False if not found

        Example:
            success = await registry.unregister("my_skill")
        """
        async with self._lock:
            if name not in self.skills:
                logger.warning(f"Attempted to unregister non-existent skill: {name}")
                return False

            skill = self.skills[name]
            self._remove_from_indexes(skill)
            del self.skills[name]

            logger.info(f"Unregistered skill '{name}'")
            return True

    def get(self, name: str) -> Optional[Skill]:
        """
        Get a skill by name.

        Args:
            name: Name of skill to retrieve

        Returns:
            Skill instance if found, None otherwise

        Example:
            skill = registry.get("my_skill")
            if skill:
                print(f"Found: {skill.description}")
        """
        return self.skills.get(name)

    def exists(self, name: str) -> bool:
        """
        Check if a skill exists in the registry.

        Args:
            name: Name of skill to check

        Returns:
            True if skill exists, False otherwise

        Example:
            if registry.exists("my_skill"):
                print("Skill is registered")
        """
        return name in self.skills

    def list_all(self) -> List[Skill]:
        """
        Get all registered skills.

        Returns:
            List of all registered skills (sorted by name)

        Example:
            for skill in registry.list_all():
                print(f"{skill.name}: {skill.description}")
        """
        return sorted(self.skills.values(), key=lambda s: s.name)

    def find_by_category(self, category: str) -> List[Skill]:
        """
        Find all skills in a specific category.

        Args:
            category: Category to search for

        Returns:
            List of skills in the category (sorted by name)

        Example:
            testing_skills = registry.find_by_category("testing")
        """
        skill_names = self._category_index.get(category, set())
        skills = [self.skills[name] for name in skill_names if name in self.skills]
        return sorted(skills, key=lambda s: s.name)

    def find_for_domain(self, domain: str) -> List[Skill]:
        """
        Find skills relevant to a specific domain (iOS, React, Python, etc.).

        Searches through skill tags to find domain-relevant skills.
        Domain matching is case-insensitive.

        Args:
            domain: Domain to search for (e.g., "iOS", "React", "Python")

        Returns:
            List of skills relevant to the domain (sorted by name)

        Example:
            ios_skills = registry.find_for_domain("iOS")
            react_skills = registry.find_for_domain("react")
        """
        domain_lower = domain.lower()
        matching_skills = []

        for skill in self.skills.values():
            # Check tags for domain match (case-insensitive)
            for tag in skill.metadata.tags:
                if domain_lower in tag.lower():
                    matching_skills.append(skill)
                    break

        return sorted(matching_skills, key=lambda s: s.name)

    def find_by_tag(self, tag: str) -> List[Skill]:
        """
        Find skills with a specific tag.

        Args:
            tag: Tag to search for (case-insensitive)

        Returns:
            List of skills with the tag (sorted by name)

        Example:
            swift_skills = registry.find_by_tag("swift")
        """
        tag_lower = tag.lower()
        skill_names = set()

        for idx_tag, names in self._tag_index.items():
            if tag_lower == idx_tag.lower():
                skill_names.update(names)

        skills = [self.skills[name] for name in skill_names if name in self.skills]
        return sorted(skills, key=lambda s: s.name)

    def find_by_execution_type(self, exec_type: ExecutionType) -> List[Skill]:
        """
        Find skills with a specific execution type.

        Args:
            exec_type: Execution type to filter by

        Returns:
            List of skills with the execution type (sorted by name)

        Example:
            native_skills = registry.find_by_execution_type(ExecutionType.NATIVE)
            mcp_skills = registry.find_by_execution_type(ExecutionType.MCP)
        """
        matching_skills = [
            skill for skill in self.skills.values()
            if skill.execution.type == exec_type
        ]
        return sorted(matching_skills, key=lambda s: s.name)

    def get_statistics(self) -> Dict:
        """
        Get registry statistics and metrics.

        Returns:
            Dictionary containing registry statistics

        Example:
            stats = registry.get_statistics()
            print(f"Total skills: {stats['total_skills']}")
        """
        stats = {
            'total_skills': len(self.skills),
            'categories': {},
            'execution_types': {},
            'domains': {},
            'avg_parameters': 0,
            'skills_with_dependencies': 0,
            'skills_with_hooks': 0,
        }

        param_count = 0

        for skill in self.skills.values():
            # Category count
            stats['categories'][skill.category] = \
                stats['categories'].get(skill.category, 0) + 1

            # Execution type count
            exec_type = skill.execution.type.value
            stats['execution_types'][exec_type] = \
                stats['execution_types'].get(exec_type, 0) + 1

            # Parameter count
            param_count += len(skill.parameters)

            # Dependencies
            if skill.dependencies:
                stats['skills_with_dependencies'] += 1

            # Hooks
            if skill.hooks.pre or skill.hooks.post or skill.hooks.error:
                stats['skills_with_hooks'] += 1

        # Calculate averages
        if self.skills:
            stats['avg_parameters'] = param_count / len(self.skills)

        # Domain statistics from tags
        for skill in self.skills.values():
            for tag in skill.metadata.tags:
                stats['domains'][tag] = stats['domains'].get(tag, 0) + 1

        return stats

    def __len__(self) -> int:
        """Return number of registered skills"""
        return len(self.skills)

    def __contains__(self, name: str) -> bool:
        """Check if skill exists using 'in' operator"""
        return name in self.skills

    def __repr__(self) -> str:
        """String representation of registry"""
        return f"<SkillRegistry: {len(self.skills)} skills registered>"
