"""Shannon Orchestration - Task Parser

Parses natural language task descriptions into structured intent that can be
mapped to skills for execution planning.

The TaskParser extracts:
- Goal: What the user wants to accomplish (create, update, fix, analyze, test)
- Domain: Area of work (auth, database, API, frontend, testing)
- Type: Category of task (feature, bugfix, refactor, test, documentation)
- Keywords: Important terms for skill matching
- Constraints: Limitations or requirements (time, complexity, dependencies)

Example:
    parser = TaskParser(registry)

    parsed = await parser.parse("create authentication system with JWT")
    # ParsedTask(
    #     raw_task="create authentication system with JWT",
    #     intent=TaskIntent(
    #         goal="create",
    #         domain="authentication",
    #         type="feature",
    #         keywords=["auth", "jwt", "token", "security"]
    #     ),
    #     candidate_skills=["library_discovery", "prompt_enhancement", ...]
    # )
"""

import re
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Any
from enum import Enum

from shannon.skills.registry import SkillRegistry
from shannon.skills.models import Skill

logger = logging.getLogger(__name__)


class GoalType(Enum):
    """High-level goal types"""
    CREATE = "create"      # Build new functionality
    UPDATE = "update"      # Modify existing code
    FIX = "fix"           # Fix bugs or issues
    ANALYZE = "analyze"    # Analyze code or system
    TEST = "test"         # Add or run tests
    REFACTOR = "refactor" # Improve code structure
    DOCUMENT = "document"  # Add documentation
    OPTIMIZE = "optimize"  # Performance improvements
    DEPLOY = "deploy"      # Deployment tasks
    CONFIGURE = "configure" # Configuration changes


class DomainType(Enum):
    """Domain/area of work"""
    AUTHENTICATION = "authentication"
    DATABASE = "database"
    API = "api"
    FRONTEND = "frontend"
    BACKEND = "backend"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    SECURITY = "security"
    PERFORMANCE = "performance"
    INFRASTRUCTURE = "infrastructure"
    DOCUMENTATION = "documentation"
    INTEGRATION = "integration"
    GENERIC = "generic"


class TaskType(Enum):
    """Type of task"""
    FEATURE = "feature"           # New feature implementation
    BUGFIX = "bugfix"             # Bug fix
    REFACTOR = "refactor"         # Code refactoring
    TEST = "test"                 # Testing
    DOCUMENTATION = "documentation" # Documentation
    OPTIMIZATION = "optimization"  # Performance optimization
    SECURITY = "security"          # Security enhancement
    MAINTENANCE = "maintenance"    # Maintenance work


@dataclass
class TaskIntent:
    """Structured representation of task intent"""
    goal: str                          # Primary goal (create, update, fix, etc.)
    domain: str                        # Domain/area (auth, database, API, etc.)
    type: str                          # Task type (feature, bugfix, etc.)
    keywords: List[str] = field(default_factory=list)  # Important keywords
    constraints: List[str] = field(default_factory=list)  # Constraints
    priority: str = "normal"           # Priority level
    complexity_estimate: float = 0.5   # 0.0-1.0 complexity estimate

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'goal': self.goal,
            'domain': self.domain,
            'type': self.type,
            'keywords': self.keywords,
            'constraints': self.constraints,
            'priority': self.priority,
            'complexity_estimate': self.complexity_estimate
        }


@dataclass
class ParsedTask:
    """Complete parsed task representation"""
    raw_task: str                      # Original task description
    intent: TaskIntent                 # Extracted intent
    candidate_skills: List[str]        # Potential skills to use
    confidence: float = 0.0            # Parsing confidence (0.0-1.0)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'raw_task': self.raw_task,
            'intent': self.intent.to_dict(),
            'candidate_skills': self.candidate_skills,
            'confidence': self.confidence,
            'metadata': self.metadata
        }


class TaskParser:
    """
    Parses natural language tasks into structured intent and maps to skills.

    The parser uses rule-based NLP techniques to extract:
    1. Goal: What action to take (create, fix, update, etc.)
    2. Domain: What area is affected (auth, database, API, etc.)
    3. Type: What kind of task (feature, bugfix, refactor, etc.)
    4. Keywords: Important terms for skill matching

    Then maps intent to candidate skills based on:
    - Skill categories matching domain
    - Skill descriptions matching keywords
    - Common skill patterns for task types

    Thread-safe and designed for async execution.
    """

    # Goal keywords mapping
    GOAL_KEYWORDS = {
        GoalType.CREATE: ['create', 'add', 'implement', 'build', 'generate', 'new'],
        GoalType.UPDATE: ['update', 'modify', 'change', 'edit', 'revise'],
        GoalType.FIX: ['fix', 'repair', 'resolve', 'correct', 'debug', 'solve'],
        GoalType.ANALYZE: ['analyze', 'review', 'inspect', 'examine', 'audit'],
        GoalType.TEST: ['test', 'verify', 'validate', 'check', 'ensure'],
        GoalType.REFACTOR: ['refactor', 'restructure', 'reorganize', 'clean up'],
        GoalType.DOCUMENT: ['document', 'write docs', 'add documentation'],
        GoalType.OPTIMIZE: ['optimize', 'improve performance', 'speed up'],
        GoalType.DEPLOY: ['deploy', 'release', 'publish', 'ship'],
        GoalType.CONFIGURE: ['configure', 'setup', 'initialize', 'set up']
    }

    # Domain keywords mapping
    DOMAIN_KEYWORDS = {
        DomainType.AUTHENTICATION: ['auth', 'authentication', 'login', 'user', 'jwt', 'oauth', 'session', 'token'],
        DomainType.DATABASE: ['database', 'db', 'sql', 'postgres', 'mysql', 'mongo', 'schema', 'migration'],
        DomainType.API: ['api', 'endpoint', 'rest', 'graphql', 'route', 'handler'],
        DomainType.FRONTEND: ['frontend', 'ui', 'interface', 'component', 'react', 'vue', 'angular'],
        DomainType.BACKEND: ['backend', 'server', 'service', 'microservice'],
        DomainType.TESTING: ['test', 'testing', 'spec', 'unit test', 'integration test'],
        DomainType.DEPLOYMENT: ['deployment', 'deploy', 'ci/cd', 'pipeline', 'docker'],
        DomainType.SECURITY: ['security', 'vulnerability', 'xss', 'csrf', 'encryption'],
        DomainType.PERFORMANCE: ['performance', 'speed', 'optimization', 'caching', 'latency'],
        DomainType.INFRASTRUCTURE: ['infrastructure', 'aws', 'cloud', 'kubernetes', 'terraform'],
        DomainType.DOCUMENTATION: ['documentation', 'docs', 'readme', 'guide'],
        DomainType.INTEGRATION: ['integration', 'third-party', 'external', 'webhook']
    }

    # Skill mapping patterns - maps domains/goals to typical skill sequences
    # NOTE: Only using skills that currently exist in built-in directory
    SKILL_PATTERNS = {
        ('create', 'authentication'): ['code_generation', 'library_discovery', 'prompt_enhancement'],
        ('create', 'api'): ['code_generation', 'library_discovery', 'prompt_enhancement'],
        ('fix', 'generic'): ['library_discovery', 'prompt_enhancement'],
        ('test', 'generic'): ['library_discovery', 'prompt_enhancement'],
        ('refactor', 'generic'): ['library_discovery', 'prompt_enhancement'],
        ('document', 'generic'): ['library_discovery', 'prompt_enhancement'],
        ('create', 'generic'): ['code_generation', 'library_discovery', 'prompt_enhancement'],
    }

    def __init__(self, registry: SkillRegistry):
        """
        Initialize task parser with skill registry.

        Args:
            registry: SkillRegistry for skill lookup and matching
        """
        self.registry = registry
        logger.info("TaskParser initialized")

    async def parse(self, task: str) -> ParsedTask:
        """
        Parse natural language task into structured intent and map to skills.

        Args:
            task: Natural language task description

        Returns:
            ParsedTask with extracted intent and candidate skills

        Example:
            parsed = await parser.parse("create authentication system with JWT")
        """
        logger.info(f"Parsing task: {task}")

        # Normalize task
        normalized = task.lower().strip()

        # Extract intent components
        goal = self._extract_goal(normalized)
        domain = self._extract_domain(normalized)
        task_type = self._infer_type(goal, domain)
        keywords = self._extract_keywords(normalized, domain)
        constraints = self._extract_constraints(normalized)

        # Build intent
        intent = TaskIntent(
            goal=goal,
            domain=domain,
            type=task_type,
            keywords=keywords,
            constraints=constraints,
            complexity_estimate=self._estimate_complexity(normalized, keywords)
        )

        # Map to candidate skills
        candidate_skills = await self._map_to_skills(intent, normalized)

        # Calculate confidence
        confidence = self._calculate_confidence(intent, candidate_skills)

        parsed = ParsedTask(
            raw_task=task,
            intent=intent,
            candidate_skills=candidate_skills,
            confidence=confidence,
            metadata={
                'normalized_task': normalized,
                'parsing_method': 'rule-based',
                'timestamp': None  # Would use datetime.now() in production
            }
        )

        logger.info(f"Parsed task: goal={goal}, domain={domain}, type={task_type}, "
                   f"skills={len(candidate_skills)}, confidence={confidence:.2f}")

        return parsed

    def _extract_goal(self, task: str) -> str:
        """
        Extract primary goal from task.

        Args:
            task: Normalized task string

        Returns:
            Goal type as string
        """
        # Check each goal type for keyword matches
        for goal_type, keywords in self.GOAL_KEYWORDS.items():
            for keyword in keywords:
                if keyword in task:
                    return goal_type.value

        # Default to create if no clear goal
        return GoalType.CREATE.value

    def _extract_domain(self, task: str) -> str:
        """
        Extract domain/area from task.

        Args:
            task: Normalized task string

        Returns:
            Domain type as string
        """
        # Check each domain for keyword matches
        domain_scores = {}
        for domain_type, keywords in self.DOMAIN_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in task)
            if score > 0:
                domain_scores[domain_type] = score

        # Return domain with highest score
        if domain_scores:
            best_domain = max(domain_scores.items(), key=lambda x: x[1])[0]
            return best_domain.value

        # Default to generic if no clear domain
        return DomainType.GENERIC.value

    def _infer_type(self, goal: str, domain: str) -> str:
        """
        Infer task type from goal and domain.

        Args:
            goal: Extracted goal
            domain: Extracted domain

        Returns:
            Task type as string
        """
        # Map goals to task types
        if goal == GoalType.CREATE.value:
            return TaskType.FEATURE.value
        elif goal == GoalType.FIX.value:
            return TaskType.BUGFIX.value
        elif goal == GoalType.REFACTOR.value:
            return TaskType.REFACTOR.value
        elif goal == GoalType.TEST.value:
            return TaskType.TEST.value
        elif goal == GoalType.DOCUMENT.value:
            return TaskType.DOCUMENTATION.value
        elif goal == GoalType.OPTIMIZE.value:
            return TaskType.OPTIMIZATION.value
        elif domain == DomainType.SECURITY.value:
            return TaskType.SECURITY.value
        else:
            return TaskType.FEATURE.value

    def _extract_keywords(self, task: str, domain: str) -> List[str]:
        """
        Extract important keywords from task.

        Args:
            task: Normalized task string
            domain: Extracted domain

        Returns:
            List of keywords
        """
        keywords = []

        # Add domain keywords that appear in task
        if domain in [d.value for d in DomainType]:
            domain_enum = DomainType(domain)
            if domain_enum in self.DOMAIN_KEYWORDS:
                domain_kws = self.DOMAIN_KEYWORDS[domain_enum]
                keywords.extend([kw for kw in domain_kws if kw in task])

        # Extract technical terms (words with specific patterns)
        # - Technology names (e.g., jwt, oauth, postgres)
        # - Framework names (e.g., react, vue, django)
        tech_pattern = r'\b(jwt|oauth|sql|postgres|mysql|mongo|redis|docker|kubernetes|aws|react|vue|angular|django|flask|express)\b'
        tech_matches = re.findall(tech_pattern, task)
        keywords.extend(tech_matches)

        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen:
                seen.add(kw)
                unique_keywords.append(kw)

        return unique_keywords

    def _extract_constraints(self, task: str) -> List[str]:
        """
        Extract constraints from task.

        Args:
            task: Normalized task string

        Returns:
            List of constraints
        """
        constraints = []

        # Time constraints
        if any(word in task for word in ['quickly', 'fast', 'urgent', 'asap']):
            constraints.append('time_sensitive')

        # Complexity constraints
        if any(word in task for word in ['simple', 'basic', 'minimal']):
            constraints.append('low_complexity')
        elif any(word in task for word in ['complex', 'advanced', 'sophisticated']):
            constraints.append('high_complexity')

        # Dependency constraints
        if 'without' in task or 'no dependencies' in task:
            constraints.append('no_dependencies')

        return constraints

    def _estimate_complexity(self, task: str, keywords: List[str]) -> float:
        """
        Estimate task complexity (0.0-1.0).

        Args:
            task: Normalized task string
            keywords: Extracted keywords

        Returns:
            Complexity estimate (0.0 = simple, 1.0 = very complex)
        """
        complexity = 0.5  # Base complexity

        # Increase for multiple keywords (indicates scope)
        complexity += len(keywords) * 0.05

        # Increase for complex words
        complex_words = ['sophisticated', 'advanced', 'complex', 'comprehensive', 'enterprise']
        if any(word in task for word in complex_words):
            complexity += 0.2

        # Decrease for simple words
        simple_words = ['simple', 'basic', 'minimal', 'small']
        if any(word in task for word in simple_words):
            complexity -= 0.2

        # Clamp to [0.1, 0.9] range
        return max(0.1, min(0.9, complexity))

    async def _map_to_skills(self, intent: TaskIntent, task: str) -> List[str]:
        """
        Map task intent to candidate skills.

        Args:
            intent: Extracted task intent
            task: Normalized task string

        Returns:
            List of candidate skill names in suggested execution order
        """
        # Check for predefined patterns first
        pattern_key = (intent.goal, intent.domain)
        if pattern_key in self.SKILL_PATTERNS:
            logger.debug(f"Using predefined pattern for {pattern_key}")
            return self.SKILL_PATTERNS[pattern_key].copy()

        # Fallback pattern for generic goal + generic domain
        generic_key = (intent.goal, 'generic')
        if generic_key in self.SKILL_PATTERNS:
            logger.debug(f"Using generic pattern for goal={intent.goal}")
            return self.SKILL_PATTERNS[generic_key].copy()

        # Build skill list dynamically by querying registry
        skills = []

        # If creating/generating code, include code_generation skill
        if intent.goal in ['create', 'implement', 'build']:
            skills.append('code_generation')

        # Query skills by category matching domain
        try:
            domain_skills = self.registry.find_by_category(intent.domain)
            skills.extend([s.name for s in domain_skills])
        except Exception as e:
            logger.debug(f"No skills found for category {intent.domain}: {e}")

        # Query skills with keywords in description
        for keyword in intent.keywords:
            try:
                # This would search skill descriptions for keyword
                # For now, we'll skip this as it requires registry enhancement
                pass
            except Exception as e:
                logger.debug(f"Error searching for keyword {keyword}: {e}")

        # Always include library_discovery and prompt_enhancement for code tasks
        if 'code_generation' in skills:
            if 'library_discovery' not in skills:
                skills.append('library_discovery')
            if 'prompt_enhancement' not in skills:
                skills.append('prompt_enhancement')

        # If no skills found, use default sequence (only existing skills)
        if not skills:
            logger.debug("Using default skill sequence")
            skills = ['library_discovery', 'prompt_enhancement']

        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in skills:
            if skill not in seen:
                seen.add(skill)
                unique_skills.append(skill)

        return unique_skills

    def _calculate_confidence(self, intent: TaskIntent, skills: List[str]) -> float:
        """
        Calculate confidence in parsing result.

        Args:
            intent: Extracted intent
            skills: Candidate skills

        Returns:
            Confidence score (0.0-1.0)
        """
        confidence = 0.5  # Base confidence

        # Increase for specific domain (not generic)
        if intent.domain != DomainType.GENERIC.value:
            confidence += 0.2

        # Increase for keywords found
        confidence += min(0.2, len(intent.keywords) * 0.05)

        # Increase for skills mapped
        if len(skills) > 0:
            confidence += 0.1

        # Clamp to [0.0, 1.0]
        return max(0.0, min(1.0, confidence))
