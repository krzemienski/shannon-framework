"""
Shannon Framework v4 - Specification Models

Data structures for specifications and related objects.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class SpecificationFormat(Enum):
    """Supported specification input formats."""
    TEXT = "text"
    JSON = "json"
    YAML = "yaml"
    MARKDOWN = "markdown"


class DomainType(Enum):
    """Project domain types."""
    FRONTEND = "frontend"
    BACKEND = "backend"
    MOBILE = "mobile"
    DATA = "data"
    DEVOPS = "devops"
    SECURITY = "security"


@dataclass
class Requirement:
    """Single requirement from specification."""
    id: str
    text: str
    priority: str  # high, medium, low
    category: str  # functional, non-functional, technical
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TechStack:
    """Technology stack specification."""
    languages: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    databases: List[str] = field(default_factory=list)
    infrastructure: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)


@dataclass
class ComplexityScores:
    """8-Dimensional complexity scores."""
    structural: float = 0.0
    cognitive: float = 0.0
    coordination: float = 0.0
    temporal: float = 0.0
    technical: float = 0.0
    scale: float = 0.0
    uncertainty: float = 0.0
    dependencies: float = 0.0
    overall: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {
            'structural': self.structural,
            'cognitive': self.cognitive,
            'coordination': self.coordination,
            'temporal': self.temporal,
            'technical': self.technical,
            'scale': self.scale,
            'uncertainty': self.uncertainty,
            'dependencies': self.dependencies,
            'overall': self.overall,
        }


@dataclass
class DomainPercentages:
    """Domain breakdown percentages."""
    frontend: float = 0.0
    backend: float = 0.0
    mobile: float = 0.0
    data: float = 0.0
    devops: float = 0.0
    security: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {
            'frontend': self.frontend,
            'backend': self.backend,
            'mobile': self.mobile,
            'data': self.data,
            'devops': self.devops,
            'security': self.security,
        }

    def validate(self) -> bool:
        """Validate that percentages sum to 100 (within tolerance)."""
        total = sum(self.to_dict().values())
        return abs(total - 100.0) < 0.1


@dataclass
class MCPRequirements:
    """MCP server requirements extracted from specification."""
    required: List[str] = field(default_factory=list)
    recommended: List[str] = field(default_factory=list)
    optional: List[str] = field(default_factory=list)


@dataclass
class SkillRequirements:
    """Skills required for this specification."""
    required_skills: List[str] = field(default_factory=list)
    optional_skills: List[str] = field(default_factory=list)
    estimated_skill_count: int = 0


@dataclass
class SpecificationObject:
    """Complete specification object."""

    # Core fields
    raw_input: str
    title: str
    description: str
    requirements: List[Requirement] = field(default_factory=list)

    # Technical details
    tech_stack: TechStack = field(default_factory=TechStack)
    architecture_pattern: Optional[str] = None
    deployment_target: Optional[str] = None

    # Analysis results (populated by spec-analysis skill)
    complexity_scores: ComplexityScores = field(default_factory=ComplexityScores)
    domain_percentages: DomainPercentages = field(default_factory=DomainPercentages)
    mcp_requirements: MCPRequirements = field(default_factory=MCPRequirements)
    skill_requirements: SkillRequirements = field(default_factory=SkillRequirements)

    # Metadata
    format: SpecificationFormat = SpecificationFormat.TEXT
    confidence: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert specification to dictionary."""
        return {
            'title': self.title,
            'description': self.description,
            'requirements': [
                {
                    'id': req.id,
                    'text': req.text,
                    'priority': req.priority,
                    'category': req.category,
                    'dependencies': req.dependencies,
                    'metadata': req.metadata,
                }
                for req in self.requirements
            ],
            'tech_stack': {
                'languages': self.tech_stack.languages,
                'frameworks': self.tech_stack.frameworks,
                'databases': self.tech_stack.databases,
                'infrastructure': self.tech_stack.infrastructure,
                'tools': self.tech_stack.tools,
            },
            'architecture_pattern': self.architecture_pattern,
            'deployment_target': self.deployment_target,
            'complexity_scores': self.complexity_scores.to_dict(),
            'domain_percentages': self.domain_percentages.to_dict(),
            'mcp_requirements': {
                'required': self.mcp_requirements.required,
                'recommended': self.mcp_requirements.recommended,
                'optional': self.mcp_requirements.optional,
            },
            'skill_requirements': {
                'required_skills': self.skill_requirements.required_skills,
                'optional_skills': self.skill_requirements.optional_skills,
                'estimated_skill_count': self.skill_requirements.estimated_skill_count,
            },
            'confidence': self.confidence,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'version': self.version,
            'metadata': self.metadata,
        }


# Type alias for backward compatibility
Specification = SpecificationObject
