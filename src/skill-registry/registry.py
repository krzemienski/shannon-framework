"""
Shannon Framework v4 - Skill Registry

Central registry for skill management, discovery, and activation.
"""

from typing import Dict, List, Optional, Set
from pathlib import Path
from .models import Skill, LoadLevel, SkillMetadata
from .loader import SkillLoader, SkillLoadError


class SkillRegistryError(Exception):
    """Exception raised for registry operations."""
    pass


class SkillRegistry:
    """
    Central registry for managing skills.

    Responsibilities:
    - Discover and register skills from skills/ directory
    - Manage skill lifecycle (load, unload, reload)
    - Provide skill lookup and query
    - Handle auto-activation based on context
    - Validate skill dependencies
    """

    def __init__(self, skills_dir: Path):
        """
        Initialize skill registry.

        Args:
            skills_dir: Directory containing skill definitions
        """
        self.skills_dir = Path(skills_dir)
        self.loader = SkillLoader(skills_dir)

        # Skill storage
        self._skills: Dict[str, Skill] = {}  # name -> Skill
        self._skills_by_type: Dict[str, List[str]] = {}  # type -> [names]
        self._auto_activate_skills: Set[str] = set()  # Skills with auto-activation

        # Dependency graph
        self._dependency_graph: Dict[str, Set[str]] = {}  # skill -> dependencies

    def initialize(self):
        """
        Discover and register all skills at Level 1 (frontmatter only).

        This loads all skills to frontmatter level (~50 tokens each).
        For 13 skills, this is ~650 tokens total.
        """
        skill_files = self.loader.discover_skills()

        if not skill_files:
            raise SkillRegistryError(f"No skills found in {self.skills_dir}")

        # Load all skills to frontmatter level
        for skill_file in skill_files:
            try:
                skill = self.loader.load_skill(skill_file, LoadLevel.FRONTMATTER)
                self.register_skill(skill)
            except SkillLoadError as e:
                print(f"Warning: Failed to load skill {skill_file}: {e}")

        # Build dependency graph
        self._build_dependency_graph()

        # Validate all dependencies
        self._validate_dependencies()

    def register_skill(self, skill: Skill):
        """
        Register a skill in the registry.

        Args:
            skill: Skill to register
        """
        name = skill.metadata.name

        if name in self._skills:
            raise SkillRegistryError(f"Skill '{name}' already registered")

        self._skills[name] = skill

        # Index by type
        skill_type = skill.metadata.skill_type.value
        if skill_type not in self._skills_by_type:
            self._skills_by_type[skill_type] = []
        self._skills_by_type[skill_type].append(name)

        # Track auto-activate skills
        if skill.metadata.auto_activate:
            self._auto_activate_skills.add(name)

    def unregister_skill(self, name: str):
        """
        Unregister a skill from the registry.

        Args:
            name: Skill name to unregister
        """
        if name not in self._skills:
            raise SkillRegistryError(f"Skill '{name}' not registered")

        skill = self._skills[name]

        # Remove from type index
        skill_type = skill.metadata.skill_type.value
        self._skills_by_type[skill_type].remove(name)

        # Remove from auto-activate set
        self._auto_activate_skills.discard(name)

        # Remove from skills
        del self._skills[name]

    def get_skill(self, name: str, load_level: LoadLevel = None) -> Optional[Skill]:
        """
        Get skill by name, optionally loading to specified level.

        Args:
            name: Skill name
            load_level: Optional load level to ensure

        Returns:
            Skill instance or None if not found
        """
        if name not in self._skills:
            return None

        skill = self._skills[name]

        # Upgrade load level if requested
        if load_level and skill.requires_loading(load_level):
            skill = self.loader.upgrade_skill_load(skill, load_level)
            self._skills[name] = skill  # Update registry

        return skill

    def load_skill(self, name: str, level: LoadLevel = LoadLevel.SKILL_BODY) -> Skill:
        """
        Load skill to specified level.

        Args:
            name: Skill name
            level: Target load level

        Returns:
            Loaded skill

        Raises:
            SkillRegistryError: If skill not found
        """
        skill = self.get_skill(name, load_level=level)
        if not skill:
            raise SkillRegistryError(f"Skill '{name}' not found")
        return skill

    def list_skills(self, skill_type: str = None, auto_activate_only: bool = False) -> List[str]:
        """
        List registered skills.

        Args:
            skill_type: Optional filter by skill type
            auto_activate_only: Only include auto-activating skills

        Returns:
            List of skill names
        """
        if skill_type:
            skills = self._skills_by_type.get(skill_type, [])
        else:
            skills = list(self._skills.keys())

        if auto_activate_only:
            skills = [s for s in skills if s in self._auto_activate_skills]

        return sorted(skills)

    def get_skills_by_type(self, skill_type: str) -> List[Skill]:
        """
        Get all skills of a specific type.

        Args:
            skill_type: Skill type (QUANTITATIVE, RIGID, PROTOCOL, FLEXIBLE)

        Returns:
            List of skills
        """
        skill_names = self._skills_by_type.get(skill_type, [])
        return [self._skills[name] for name in skill_names]

    def check_auto_activation(self, context: Dict) -> List[str]:
        """
        Check which skills should auto-activate given context.

        Args:
            context: Context dictionary with complexity, text, domain info

        Returns:
            List of skill names that should activate
        """
        activated = []

        for skill_name in self._auto_activate_skills:
            skill = self._skills[skill_name]
            if skill.metadata.activation_triggers:
                if skill.metadata.activation_triggers.matches(context):
                    activated.append(skill_name)

        return activated

    def get_dependency_chain(self, skill_name: str) -> List[str]:
        """
        Get complete dependency chain for a skill.

        Args:
            skill_name: Skill name

        Returns:
            List of skill names in dependency order (dependencies first)
        """
        if skill_name not in self._skills:
            raise SkillRegistryError(f"Skill '{skill_name}' not found")

        visited = set()
        chain = []

        def _visit(name):
            if name in visited:
                return
            visited.add(name)

            # Visit dependencies first
            for dep in self._dependency_graph.get(name, set()):
                _visit(dep)

            chain.append(name)

        _visit(skill_name)
        return chain

    def validate_skill(self, skill_name: str) -> List[str]:
        """
        Validate skill and its dependencies.

        Args:
            skill_name: Skill to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        if skill_name not in self._skills:
            return [f"Skill '{skill_name}' not registered"]

        skill = self._skills[skill_name]

        # Check required sub-skills exist
        for sub_skill in skill.metadata.required_sub_skills:
            if sub_skill.name not in self._skills:
                errors.append(f"Required sub-skill '{sub_skill.name}' not found")

        # Check for circular dependencies
        try:
            chain = self.get_dependency_chain(skill_name)
        except RecursionError:
            errors.append(f"Circular dependency detected for '{skill_name}'")

        return errors

    def get_registry_stats(self) -> Dict:
        """
        Get registry statistics.

        Returns:
            Dictionary with registry metrics
        """
        total_skills = len(self._skills)
        skills_by_type = {
            skill_type: len(skills)
            for skill_type, skills in self._skills_by_type.items()
        }

        # Count load levels
        load_levels = {
            'frontmatter': 0,
            'skill_body': 0,
            'references': 0,
        }
        for skill in self._skills.values():
            if skill.loaded_level == LoadLevel.FRONTMATTER:
                load_levels['frontmatter'] += 1
            elif skill.loaded_level == LoadLevel.SKILL_BODY:
                load_levels['skill_body'] += 1
            elif skill.loaded_level == LoadLevel.REFERENCES:
                load_levels['references'] += 1

        # Token usage estimate
        total_tokens = sum(skill.get_token_estimate() for skill in self._skills.values())

        return {
            'total_skills': total_skills,
            'auto_activate_count': len(self._auto_activate_skills),
            'skills_by_type': skills_by_type,
            'load_levels': load_levels,
            'estimated_tokens': total_tokens,
            'skills_dir': str(self.skills_dir),
        }

    def reload_skill(self, skill_name: str):
        """
        Reload skill from disk.

        Args:
            skill_name: Skill to reload
        """
        if skill_name not in self._skills:
            raise SkillRegistryError(f"Skill '{skill_name}' not found")

        old_skill = self._skills[skill_name]
        old_level = old_skill.loaded_level

        # Unregister and re-register
        self.unregister_skill(skill_name)

        try:
            new_skill = self.loader.load_skill(old_skill.metadata.skill_file, old_level)
            self.register_skill(new_skill)
        except Exception as e:
            # Re-register old skill if reload fails
            self.register_skill(old_skill)
            raise SkillRegistryError(f"Failed to reload skill '{skill_name}': {e}")

    def _build_dependency_graph(self):
        """Build dependency graph for all skills."""
        self._dependency_graph = {}

        for skill_name, skill in self._skills.items():
            deps = set()
            for sub_skill in skill.metadata.required_sub_skills:
                deps.add(sub_skill.name)
            self._dependency_graph[skill_name] = deps

    def _validate_dependencies(self):
        """Validate all skill dependencies."""
        errors = []

        for skill_name in self._skills:
            skill_errors = self.validate_skill(skill_name)
            if skill_errors:
                errors.extend([f"{skill_name}: {err}" for err in skill_errors])

        if errors:
            print("Warning: Dependency validation errors:")
            for error in errors:
                print(f"  - {error}")

    def export_metadata(self) -> Dict:
        """
        Export all skill metadata (Level 1 only).

        Returns:
            Dictionary with all skill metadata
        """
        return {
            skill_name: skill.to_dict()
            for skill_name, skill in self._skills.items()
        }

    def search_skills(
        self,
        query: str = None,
        tags: List[str] = None,
        skill_type: str = None
    ) -> List[str]:
        """
        Search skills by various criteria.

        Args:
            query: Text query (searches name and description)
            tags: Required tags
            skill_type: Skill type filter

        Returns:
            List of matching skill names
        """
        results = list(self._skills.keys())

        # Filter by skill type
        if skill_type:
            results = [s for s in results if s in self._skills_by_type.get(skill_type, [])]

        # Filter by tags
        if tags:
            results = [
                s for s in results
                if any(tag in self._skills[s].metadata.tags for tag in tags)
            ]

        # Filter by query
        if query:
            query_lower = query.lower()
            results = [
                s for s in results
                if query_lower in s.lower() or
                   query_lower in self._skills[s].metadata.description.lower()
            ]

        return sorted(results)
