"""
Shannon Framework v4 - Skill Manager

High-level skill lifecycle management and orchestration.
"""

from typing import List, Dict, Optional, Any
from pathlib import Path
from .registry import SkillRegistry, SkillRegistryError
from .models import Skill, LoadLevel


class SkillManager:
    """
    High-level manager for skill operations.

    Provides simplified interface for:
    - Initialization and discovery
    - Context-based activation
    - Dependency resolution
    - MCP compatibility checking
    - Skill invocation orchestration
    """

    def __init__(self, skills_dir: Path):
        """
        Initialize skill manager.

        Args:
            skills_dir: Directory containing skill definitions
        """
        self.registry = SkillRegistry(skills_dir)
        self.active_skills: Dict[str, Skill] = {}  # Currently active skills
        self.execution_history: List[Dict[str, Any]] = []

    def initialize(self):
        """
        Initialize skill registry and load all skills to Level 1.

        This performs initial discovery and validation.
        """
        self.registry.initialize()

    def activate_for_context(self, context: Dict[str, Any]) -> List[str]:
        """
        Activate skills based on context.

        This checks auto-activation triggers and loads appropriate skills.

        Args:
            context: Context dictionary with complexity, text, domain, etc.

        Returns:
            List of activated skill names
        """
        # Check which skills should auto-activate
        candidates = self.registry.check_auto_activation(context)

        activated = []
        for skill_name in candidates:
            try:
                # Load skill to Level 2 (SKILL_BODY)
                skill = self.registry.load_skill(skill_name, LoadLevel.SKILL_BODY)

                # Resolve and load dependencies
                self._load_dependencies(skill_name)

                # Mark as active
                self.active_skills[skill_name] = skill
                activated.append(skill_name)

            except Exception as e:
                print(f"Warning: Failed to activate skill '{skill_name}': {e}")

        # Record activation
        if activated:
            self.execution_history.append({
                'action': 'auto_activate',
                'skills': activated,
                'context': context,
            })

        return activated

    def invoke_skill(
        self,
        skill_name: str,
        context: Dict[str, Any],
        load_references: bool = False
    ) -> Skill:
        """
        Invoke a specific skill.

        Args:
            skill_name: Name of skill to invoke
            context: Execution context
            load_references: Whether to load Level 3 (references)

        Returns:
            Loaded and activated skill

        Raises:
            SkillRegistryError: If skill not found or dependencies missing
        """
        # Determine load level
        load_level = LoadLevel.REFERENCES if load_references else LoadLevel.SKILL_BODY

        # Load skill
        skill = self.registry.load_skill(skill_name, load_level)

        # Validate skill
        errors = self.registry.validate_skill(skill_name)
        if errors:
            raise SkillRegistryError(f"Skill validation failed: {'; '.join(errors)}")

        # Load dependencies
        self._load_dependencies(skill_name, load_level)

        # Mark as active
        self.active_skills[skill_name] = skill

        # Record invocation
        self.execution_history.append({
            'action': 'invoke',
            'skill': skill_name,
            'context': context,
            'load_level': load_level.value,
        })

        return skill

    def deactivate_skill(self, skill_name: str):
        """
        Deactivate a skill (unload from memory but keep in registry).

        Args:
            skill_name: Skill to deactivate
        """
        if skill_name in self.active_skills:
            del self.active_skills[skill_name]

            # Record deactivation
            self.execution_history.append({
                'action': 'deactivate',
                'skill': skill_name,
            })

    def get_skill_recommendations(
        self,
        context: Dict[str, Any],
        max_recommendations: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get skill recommendations based on context.

        Args:
            context: Context dictionary
            max_recommendations: Maximum number to return

        Returns:
            List of recommendations with relevance scores
        """
        recommendations = []

        # Get auto-activation candidates
        candidates = self.registry.check_auto_activation(context)

        for skill_name in candidates:
            skill = self.registry.get_skill(skill_name)
            if not skill:
                continue

            # Calculate relevance score
            score = self._calculate_relevance_score(skill, context)

            recommendations.append({
                'skill_name': skill_name,
                'description': skill.metadata.description,
                'relevance_score': score,
                'auto_activate': skill.metadata.auto_activate,
                'skill_type': skill.metadata.skill_type.value,
            })

        # Sort by relevance
        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)

        return recommendations[:max_recommendations]

    def check_mcp_compatibility(self, skill_name: str, available_mcps: List[str]) -> Dict[str, Any]:
        """
        Check MCP compatibility for a skill.

        Args:
            skill_name: Skill to check
            available_mcps: List of available MCP server names

        Returns:
            Dictionary with compatibility status
        """
        skill = self.registry.get_skill(skill_name)
        if not skill:
            raise SkillRegistryError(f"Skill '{skill_name}' not found")

        available_set = set(mcp.lower() for mcp in available_mcps)

        required_missing = []
        recommended_missing = []
        optional_missing = []

        for mcp_dep in skill.metadata.mcp_dependencies:
            mcp_name = mcp_dep.name.lower()

            if mcp_name not in available_set:
                if mcp_dep.required:
                    required_missing.append(mcp_dep.name)
                else:
                    # Assume recommended if not required
                    recommended_missing.append(mcp_dep.name)

        # Calculate compatibility score
        total_deps = len(skill.metadata.mcp_dependencies)
        missing_count = len(required_missing) + len(recommended_missing)

        if total_deps == 0:
            compatibility_score = 1.0
        else:
            compatibility_score = 1.0 - (missing_count / total_deps)

        # Determine status
        if required_missing:
            status = 'incompatible'
        elif recommended_missing:
            status = 'partial'
        else:
            status = 'compatible'

        return {
            'skill_name': skill_name,
            'status': status,
            'compatibility_score': compatibility_score,
            'required_missing': required_missing,
            'recommended_missing': recommended_missing,
            'has_fallback': any(
                mcp.fallback for mcp in skill.metadata.mcp_dependencies
                if mcp.name in required_missing + recommended_missing
            ),
        }

    def get_execution_summary(self) -> Dict[str, Any]:
        """
        Get summary of skill execution history.

        Returns:
            Summary statistics
        """
        total_invocations = sum(
            1 for event in self.execution_history
            if event['action'] == 'invoke'
        )

        total_activations = sum(
            len(event.get('skills', []))
            for event in self.execution_history
            if event['action'] == 'auto_activate'
        )

        skill_usage = {}
        for event in self.execution_history:
            if event['action'] == 'invoke':
                skill_name = event['skill']
                skill_usage[skill_name] = skill_usage.get(skill_name, 0) + 1
            elif event['action'] == 'auto_activate':
                for skill_name in event.get('skills', []):
                    skill_usage[skill_name] = skill_usage.get(skill_name, 0) + 1

        return {
            'total_invocations': total_invocations,
            'total_auto_activations': total_activations,
            'active_skill_count': len(self.active_skills),
            'skill_usage': skill_usage,
            'most_used_skills': sorted(
                skill_usage.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
        }

    def generate_skill_report(self) -> str:
        """
        Generate human-readable skill report.

        Returns:
            Formatted report string
        """
        stats = self.registry.get_registry_stats()
        exec_summary = self.get_execution_summary()

        report = f"""
Shannon Framework v4 - Skill Registry Report
============================================

Registry Statistics:
  Total Skills: {stats['total_skills']}
  Auto-Activate: {stats['auto_activate_count']}
  Estimated Tokens: {stats['estimated_tokens']:,}

Skills by Type:
"""
        for skill_type, count in stats['skills_by_type'].items():
            report += f"  {skill_type}: {count}\n"

        report += f"""
Load Levels:
  Frontmatter Only: {stats['load_levels']['frontmatter']}
  Full Body Loaded: {stats['load_levels']['skill_body']}
  References Loaded: {stats['load_levels']['references']}

Execution Summary:
  Total Invocations: {exec_summary['total_invocations']}
  Auto-Activations: {exec_summary['total_auto_activations']}
  Currently Active: {exec_summary['active_skill_count']}

Most Used Skills:
"""
        for skill_name, count in exec_summary['most_used_skills']:
            report += f"  {skill_name}: {count} times\n"

        report += f"""
Active Skills:
"""
        for skill_name in sorted(self.active_skills.keys()):
            skill = self.active_skills[skill_name]
            report += f"  - {skill_name} [{skill.loaded_level.name}]\n"

        return report.strip()

    def _load_dependencies(self, skill_name: str, load_level: LoadLevel = LoadLevel.SKILL_BODY):
        """
        Load all dependencies for a skill.

        Args:
            skill_name: Skill whose dependencies to load
            load_level: Load level for dependencies
        """
        # Get dependency chain
        dependency_chain = self.registry.get_dependency_chain(skill_name)

        # Load each dependency (excluding the skill itself)
        for dep_name in dependency_chain[:-1]:
            if dep_name not in self.active_skills:
                try:
                    skill = self.registry.load_skill(dep_name, load_level)
                    self.active_skills[dep_name] = skill
                except Exception as e:
                    print(f"Warning: Failed to load dependency '{dep_name}': {e}")

    def _calculate_relevance_score(self, skill: Skill, context: Dict[str, Any]) -> float:
        """
        Calculate relevance score for skill given context.

        Args:
            skill: Skill to score
            context: Context dictionary

        Returns:
            Relevance score (0.0 to 1.0)
        """
        score = 0.0

        # Base score for auto-activation match
        if skill.metadata.activation_triggers:
            if skill.metadata.activation_triggers.matches(context):
                score += 0.5

        # Bonus for keyword matches in description
        if 'text' in context:
            text_lower = context['text'].lower()
            desc_lower = skill.metadata.description.lower()

            # Count keyword overlaps
            text_words = set(text_lower.split())
            desc_words = set(desc_lower.split())
            overlap = len(text_words & desc_words)

            if overlap > 0:
                score += min(0.3, overlap * 0.05)

        # Bonus for complexity match
        if 'complexity' in context and skill.metadata.activation_triggers:
            if skill.metadata.activation_triggers.complexity:
                score += 0.2

        return min(1.0, score)

    def reset(self):
        """Reset manager state (clear active skills and history)."""
        self.active_skills = {}
        self.execution_history = []
