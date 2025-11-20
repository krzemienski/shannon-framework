"""
Shannon Framework v4 - Skill Registry Models

Data structures for skills and skill metadata.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class SkillType(Enum):
    """Skill execution types."""
    QUANTITATIVE = "QUANTITATIVE"  # Algorithmic, deterministic
    RIGID = "RIGID"  # Protocol-based, strict steps
    PROTOCOL = "PROTOCOL"  # Standardized format
    FLEXIBLE = "FLEXIBLE"  # Creative, adaptive


class LoadLevel(Enum):
    """Progressive disclosure load levels."""
    FRONTMATTER = 1  # Only metadata (~50 tokens)
    SKILL_BODY = 2   # Full SKILL.md (~500 lines)
    REFERENCES = 3   # All references/* (unlimited)


@dataclass
class ActivationTrigger:
    """Skill auto-activation trigger conditions."""
    complexity: Optional[str] = None  # e.g., ">= 0.60"
    keywords: List[str] = field(default_factory=list)
    context_patterns: List[str] = field(default_factory=list)
    domain_types: List[str] = field(default_factory=list)

    def matches(self, context: Dict[str, Any]) -> bool:
        """
        Check if context matches trigger conditions.

        Args:
            context: Context dictionary with complexity, text, domain info

        Returns:
            True if any trigger condition matches
        """
        # Complexity-based trigger
        if self.complexity and 'complexity' in context:
            complexity_value = context['complexity']
            if self._evaluate_complexity(complexity_value):
                return True

        # Keyword-based trigger
        if self.keywords and 'text' in context:
            text_lower = context['text'].lower()
            if any(keyword.lower() in text_lower for keyword in self.keywords):
                return True

        # Context pattern trigger
        if self.context_patterns and 'text' in context:
            text_lower = context['text'].lower()
            if any(pattern.lower() in text_lower for pattern in self.context_patterns):
                return True

        # Domain-based trigger
        if self.domain_types and 'domain' in context:
            domain = context['domain']
            if domain in self.domain_types:
                return True

        return False

    def _evaluate_complexity(self, value: float) -> bool:
        """Evaluate complexity comparison expression."""
        if not self.complexity:
            return False

        # Parse expressions like ">= 0.60", "< 0.30"
        import re
        match = re.match(r'([><=]+)\s*([\d.]+)', self.complexity)
        if not match:
            return False

        operator, threshold = match.groups()
        threshold = float(threshold)

        if operator == '>=':
            return value >= threshold
        elif operator == '>':
            return value > threshold
        elif operator == '<=':
            return value <= threshold
        elif operator == '<':
            return value < threshold
        elif operator == '==':
            return abs(value - threshold) < 0.01

        return False


@dataclass
class MCPDependency:
    """MCP server dependency specification."""
    name: str
    version: str = "*"  # Semantic version or "*"
    required: bool = True
    fallback: Optional[str] = None  # Fallback strategy if unavailable


@dataclass
class SubSkillRequirement:
    """Required sub-skill specification."""
    name: str
    version: str = "*"
    load_level: LoadLevel = LoadLevel.SKILL_BODY


@dataclass
class SkillMetadata:
    """
    Skill metadata from frontmatter (Level 1).

    This is the minimal information loaded for ALL skills (~50 tokens each).
    """
    name: str
    description: str
    skill_type: SkillType
    version: str = "1.0.0"

    # Auto-activation
    auto_activate: bool = False
    activation_triggers: Optional[ActivationTrigger] = None

    # Dependencies
    required_sub_skills: List[SubSkillRequirement] = field(default_factory=list)
    mcp_dependencies: List[MCPDependency] = field(default_factory=list)

    # File paths
    skill_file: Optional[Path] = None
    references_dir: Optional[Path] = None

    # Additional metadata
    author: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    estimated_tokens: int = 500  # Estimated size when fully loaded

    @classmethod
    def from_frontmatter(cls, frontmatter: Dict[str, Any], skill_path: Path) -> 'SkillMetadata':
        """
        Create SkillMetadata from parsed frontmatter.

        Args:
            frontmatter: Parsed YAML frontmatter
            skill_path: Path to SKILL.md file

        Returns:
            SkillMetadata instance
        """
        # Parse activation triggers
        triggers = None
        if frontmatter.get('auto_activate') and 'activation_triggers' in frontmatter:
            trigger_data = frontmatter['activation_triggers']
            triggers = ActivationTrigger(
                complexity=trigger_data.get('complexity'),
                keywords=trigger_data.get('keywords', []),
                context_patterns=trigger_data.get('context_patterns', []),
                domain_types=trigger_data.get('domain_types', [])
            )

        # Parse sub-skill requirements
        sub_skills = []
        for sub_skill in frontmatter.get('required-sub-skills', []):
            if isinstance(sub_skill, str):
                sub_skills.append(SubSkillRequirement(name=sub_skill))
            elif isinstance(sub_skill, dict):
                sub_skills.append(SubSkillRequirement(
                    name=sub_skill['name'],
                    version=sub_skill.get('version', '*'),
                    load_level=LoadLevel[sub_skill.get('load_level', 'SKILL_BODY')]
                ))

        # Parse MCP dependencies
        mcp_deps = []
        for mcp_category in ['required', 'recommended', 'optional']:
            for mcp in frontmatter.get('mcp-dependencies', {}).get(mcp_category, []):
                if isinstance(mcp, str):
                    mcp_deps.append(MCPDependency(
                        name=mcp,
                        required=(mcp_category == 'required')
                    ))
                elif isinstance(mcp, dict):
                    mcp_deps.append(MCPDependency(
                        name=mcp['name'],
                        version=mcp.get('version', '*'),
                        required=(mcp_category == 'required'),
                        fallback=mcp.get('fallback')
                    ))

        # Determine file paths
        references_dir = skill_path.parent / 'references'
        if not references_dir.exists():
            references_dir = None

        return cls(
            name=frontmatter['name'],
            description=frontmatter['description'],
            skill_type=SkillType[frontmatter['skill-type']],
            version=frontmatter.get('version', '1.0.0'),
            auto_activate=frontmatter.get('auto_activate', False),
            activation_triggers=triggers,
            required_sub_skills=sub_skills,
            mcp_dependencies=mcp_deps,
            skill_file=skill_path,
            references_dir=references_dir,
            author=frontmatter.get('author'),
            tags=frontmatter.get('tags', []),
            estimated_tokens=frontmatter.get('estimated_tokens', 500)
        )


@dataclass
class SkillContent:
    """
    Full skill content (Level 2).

    Loaded on-demand when skill is invoked.
    """
    metadata: SkillMetadata
    body: str  # Full SKILL.md content
    sections: Dict[str, str] = field(default_factory=dict)  # Parsed sections
    examples: List[str] = field(default_factory=list)
    load_level: LoadLevel = LoadLevel.SKILL_BODY


@dataclass
class SkillReferences:
    """
    Skill references (Level 3).

    Loaded only when explicitly mentioned in conversation.
    """
    skill_name: str
    references: Dict[str, str] = field(default_factory=dict)  # filename -> content
    load_level: LoadLevel = LoadLevel.REFERENCES


@dataclass
class Skill:
    """
    Complete skill representation with progressive loading.

    Supports 3-level loading:
    - Level 1: metadata only (~50 tokens)
    - Level 2: + full SKILL.md body (~500 lines)
    - Level 3: + all references/* (unlimited)
    """
    metadata: SkillMetadata
    content: Optional[SkillContent] = None
    references: Optional[SkillReferences] = None
    loaded_level: LoadLevel = LoadLevel.FRONTMATTER

    def is_loaded(self, level: LoadLevel) -> bool:
        """Check if skill is loaded to specified level."""
        return self.loaded_level.value >= level.value

    def requires_loading(self, level: LoadLevel) -> bool:
        """Check if skill needs to be loaded to specified level."""
        return self.loaded_level.value < level.value

    def get_token_estimate(self) -> int:
        """Estimate token count for current load level."""
        if self.loaded_level == LoadLevel.FRONTMATTER:
            return 50
        elif self.loaded_level == LoadLevel.SKILL_BODY:
            return self.metadata.estimated_tokens
        else:  # REFERENCES
            # Rough estimate: 1 token ≈ 4 chars
            ref_chars = sum(len(content) for content in self.references.references.values())
            return self.metadata.estimated_tokens + (ref_chars // 4)

    def to_dict(self) -> Dict[str, Any]:
        """Convert skill to dictionary representation."""
        result = {
            'name': self.metadata.name,
            'description': self.metadata.description,
            'skill_type': self.metadata.skill_type.value,
            'version': self.metadata.version,
            'auto_activate': self.metadata.auto_activate,
            'loaded_level': self.loaded_level.value,
            'estimated_tokens': self.get_token_estimate(),
        }

        if self.metadata.activation_triggers:
            result['activation_triggers'] = {
                'complexity': self.metadata.activation_triggers.complexity,
                'keywords': self.metadata.activation_triggers.keywords,
                'context_patterns': self.metadata.activation_triggers.context_patterns,
                'domain_types': self.metadata.activation_triggers.domain_types,
            }

        if self.metadata.required_sub_skills:
            result['required_sub_skills'] = [
                {'name': sub.name, 'version': sub.version}
                for sub in self.metadata.required_sub_skills
            ]

        if self.metadata.mcp_dependencies:
            result['mcp_dependencies'] = [
                {
                    'name': mcp.name,
                    'version': mcp.version,
                    'required': mcp.required,
                    'fallback': mcp.fallback
                }
                for mcp in self.metadata.mcp_dependencies
            ]

        return result
