"""Shannon Orchestration - Execution Planner

Creates detailed execution plans from parsed tasks by:
- Selecting appropriate skills from candidates
- Resolving dependencies and determining execution order
- Adding checkpoint locations before critical skills
- Detecting decision points where human input may be needed
- Estimating execution duration

The ExecutionPlanner produces a comprehensive ExecutionPlan that the Orchestrator
uses to execute skills in the correct order with proper checkpointing.

Example:
    planner = ExecutionPlanner(registry, dependency_resolver)

    plan = await planner.create_plan(parsed_task)
    # ExecutionPlan with ordered skills, checkpoints, decision points
"""

import logging
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Set
from datetime import datetime, timedelta

from shannon.skills.registry import SkillRegistry, SkillNotFoundError
from shannon.skills.dependencies import DependencyResolver, ResolvedDependencies
from shannon.skills.models import Skill
from shannon.orchestration.task_parser import ParsedTask, TaskIntent

logger = logging.getLogger(__name__)


@dataclass
class CheckpointPlan:
    """Plan for creating a checkpoint"""
    id: str
    label: str
    before_skill: str  # Skill name to checkpoint before
    reason: str        # Why checkpoint here
    priority: int = 1  # Priority (1=critical, 2=important, 3=nice-to-have)


@dataclass
class DecisionPoint:
    """Point where execution may need human decision"""
    id: str
    question: str              # Question to ask
    options: List[str]         # Available options
    after_skill: Optional[str] # Skill after which to ask
    default: Optional[str]     # Default choice if auto-mode
    timeout_seconds: int = 300 # How long to wait


@dataclass
class SkillStep:
    """A single skill execution step in the plan"""
    skill_name: str
    parameters: Dict[str, Any]
    estimated_duration: float  # seconds
    critical: bool = False     # If true, failure stops execution
    retries: int = 0           # Number of retries on failure
    checkpoint_before: bool = False  # Create checkpoint before this step


@dataclass
class ExecutionPlan:
    """Complete execution plan for a task"""
    plan_id: str
    task: str                           # Original task description
    intent: TaskIntent                  # Parsed intent
    steps: List[SkillStep]              # Ordered execution steps
    checkpoints: List[CheckpointPlan]   # Checkpoint locations
    decision_points: List[DecisionPoint] # Decision points
    estimated_duration: float           # Total estimated duration (seconds)
    complexity: float                   # 0.0-1.0
    parallel_opportunities: List[List[str]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'plan_id': self.plan_id,
            'task': self.task,
            'intent': self.intent.to_dict(),
            'steps': [
                {
                    'skill_name': step.skill_name,
                    'parameters': step.parameters,
                    'estimated_duration': step.estimated_duration,
                    'critical': step.critical,
                    'retries': step.retries,
                    'checkpoint_before': step.checkpoint_before
                }
                for step in self.steps
            ],
            'checkpoints': [
                {
                    'id': cp.id,
                    'label': cp.label,
                    'before_skill': cp.before_skill,
                    'reason': cp.reason,
                    'priority': cp.priority
                }
                for cp in self.checkpoints
            ],
            'decision_points': [
                {
                    'id': dp.id,
                    'question': dp.question,
                    'options': dp.options,
                    'after_skill': dp.after_skill,
                    'default': dp.default,
                    'timeout_seconds': dp.timeout_seconds
                }
                for dp in self.decision_points
            ],
            'estimated_duration': self.estimated_duration,
            'complexity': self.complexity,
            'parallel_opportunities': self.parallel_opportunities,
            'metadata': self.metadata
        }


class PlanningError(Exception):
    """Raised when planning fails"""
    pass


class ExecutionPlanner:
    """
    Creates execution plans from parsed tasks.

    The planner takes parsed task intent and candidate skills, then:
    1. Validates and selects skills from candidates
    2. Resolves dependencies using DependencyResolver
    3. Orders skills in safe execution sequence
    4. Adds checkpoints before critical operations
    5. Detects decision points for human input
    6. Estimates total execution time
    7. Identifies parallel execution opportunities

    Critical Skills (checkpoint before):
    - code_generation: Changes files
    - git_operations: Commits changes
    - deployment: Deploys to production
    - database_migration: Modifies database schema

    Decision Points:
    - After library_discovery: Which library to use?
    - After analysis: Which approach to take?
    - Before deployment: Ready to deploy?
    """

    # Skills that are critical and need checkpoints
    CRITICAL_SKILLS = {
        'code_generation': 'Modifies code files',
        'git_operations': 'Commits changes to git',
        'deployment': 'Deploys to production',
        'database_migration': 'Modifies database schema',
        'refactoring': 'Large code changes',
    }

    # Skills that may need human decisions
    DECISION_SKILLS = {
        'library_discovery': 'Which library should be used?',
        'analysis': 'Which approach should be taken?',
        'validation': 'Are the results acceptable?',
    }

    # Average duration estimates by skill type (seconds)
    DURATION_ESTIMATES = {
        'library_discovery': 30,
        'prompt_enhancement': 10,
        'analysis': 45,
        'code_generation': 60,
        'validation': 30,
        'test_generation': 45,
        'git_operations': 15,
        'deployment': 120,
        'refactoring': 90,
        'documentation_generation': 40,
    }

    def __init__(
        self,
        registry: SkillRegistry,
        dependency_resolver: Optional[DependencyResolver] = None
    ):
        """
        Initialize execution planner.

        Args:
            registry: SkillRegistry for skill lookup
            dependency_resolver: Optional DependencyResolver (creates if not provided)
        """
        self.registry = registry
        self.resolver = dependency_resolver or DependencyResolver(registry)
        logger.info("ExecutionPlanner initialized")

    async def create_plan(
        self,
        parsed_task: ParsedTask,
        auto_mode: bool = False,
        context: Optional[Dict[str, Any]] = None
    ) -> ExecutionPlan:
        """
        Create execution plan from parsed task.

        Args:
            parsed_task: Parsed task with intent and candidates
            auto_mode: If True, include default decisions for auto-execution
            context: Optional execution context (e.g., project_root, variables)

        Returns:
            ExecutionPlan ready for orchestrator execution

        Raises:
            PlanningError: If planning fails
        """
        logger.info(f"Creating execution plan for: {parsed_task.raw_task}")

        # Initialize context if not provided
        context = context or {}

        # Add raw task to context for parameter extraction
        context['raw_task'] = parsed_task.raw_task

        # Step 1: Select and validate skills
        selected_skills = await self._select_skills(parsed_task.candidate_skills)

        # Step 2: Resolve dependencies and order skills
        resolved = await self._resolve_dependencies(selected_skills)

        # Step 3: Create skill steps with parameters
        steps = await self._create_steps(
            resolved.execution_order,
            parsed_task.intent,
            context
        )

        # Step 4: Add checkpoints
        checkpoints = self._plan_checkpoints(steps)

        # Step 5: Detect decision points
        decision_points = self._detect_decision_points(steps, auto_mode)

        # Step 6: Estimate duration
        total_duration = self._estimate_duration(steps)

        # Step 7: Mark checkpoint locations in steps
        self._mark_checkpoint_steps(steps, checkpoints)

        # Build plan
        plan = ExecutionPlan(
            plan_id=str(uuid.uuid4()),
            task=parsed_task.raw_task,
            intent=parsed_task.intent,
            steps=steps,
            checkpoints=checkpoints,
            decision_points=decision_points,
            estimated_duration=total_duration,
            complexity=parsed_task.intent.complexity_estimate,
            parallel_opportunities=resolved.parallel_groups,
            metadata={
                'created_at': datetime.now().isoformat(),
                'auto_mode': auto_mode,
                'skill_count': len(steps),
                'dependency_levels': resolved.dependency_levels
            }
        )

        logger.info(
            f"Plan created: {len(steps)} steps, {len(checkpoints)} checkpoints, "
            f"{len(decision_points)} decisions, ~{total_duration:.0f}s"
        )

        return plan

    async def _select_skills(self, candidates: List[str]) -> List[Skill]:
        """
        Select and validate skills from candidates.

        Args:
            candidates: List of candidate skill names

        Returns:
            List of valid Skill objects

        Raises:
            PlanningError: If no valid skills found
        """
        skills = []
        missing = []

        for skill_name in candidates:
            try:
                skill = self.registry.get(skill_name)
                if skill is None:
                    raise SkillNotFoundError(f"Skill not found: {skill_name}")
                skills.append(skill)
            except SkillNotFoundError:
                logger.warning(f"Candidate skill not found: {skill_name}")
                missing.append(skill_name)

        if not skills:
            raise PlanningError(
                f"No valid skills found from candidates: {candidates}\n"
                f"Missing: {missing}"
            )

        if missing:
            logger.info(f"Selected {len(skills)} skills, {len(missing)} missing: {missing}")

        return skills

    async def _resolve_dependencies(self, skills: List[Skill]) -> ResolvedDependencies:
        """
        Resolve skill dependencies and determine execution order.

        Args:
            skills: List of skills to order

        Returns:
            ResolvedDependencies with execution order

        Raises:
            PlanningError: If dependency resolution fails
        """
        try:
            resolved = self.resolver.resolve_dependencies(skills)
            logger.debug(
                f"Dependencies resolved: {len(resolved.execution_order)} skills, "
                f"{resolved.dependency_levels} levels"
            )
            return resolved
        except Exception as e:
            raise PlanningError(f"Dependency resolution failed: {e}") from e

    async def _create_steps(
        self,
        skill_order: List[str],
        intent: TaskIntent,
        context: Optional[Dict[str, Any]] = None
    ) -> List[SkillStep]:
        """
        Create skill steps with parameters.

        Args:
            skill_order: Ordered list of skill names
            intent: Task intent for parameter population
            context: Optional execution context for parameter extraction

        Returns:
            List of SkillStep objects
        """
        steps = []
        context = context or {}

        for skill_name in skill_order:
            try:
                skill = self.registry.get(skill_name)
                if skill is None:
                    raise SkillNotFoundError(f"Skill not found: {skill_name}")

                # Extract parameters intelligently from intent and context
                parameters = self._extract_parameters_for_skill(skill, intent, context)

                # Estimate duration
                duration = self._estimate_skill_duration(skill_name)

                # Determine if critical
                critical = skill_name in self.CRITICAL_SKILLS

                # Determine retries
                retries = 2 if critical else 0

                step = SkillStep(
                    skill_name=skill_name,
                    parameters=parameters,
                    estimated_duration=duration,
                    critical=critical,
                    retries=retries,
                    checkpoint_before=False  # Set later
                )

                steps.append(step)

            except SkillNotFoundError:
                logger.warning(f"Skill not found during step creation: {skill_name}")
                continue

        return steps

    def _extract_parameters_for_skill(
        self,
        skill: Skill,
        intent: TaskIntent,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Intelligently extract parameters for skill from task intent and context.

        Maps skill parameter requirements to available data sources:
        - Task intent (goal, domain, keywords, entities)
        - Execution context variables (project_root, previous results)
        - Skill-specific patterns and defaults

        Args:
            skill: Skill to extract parameters for
            intent: Task intent with extracted information
            context: Optional execution context variables

        Returns:
            Dictionary of parameters with all required fields populated
        """
        params = {}
        context = context or {}

        for param in skill.parameters:
            # Skip if optional and has default (will use default)
            if not param.required and param.default is not None:
                continue

            # Common parameter patterns
            if param.name == 'project_root':
                # Get from context or use current directory
                params['project_root'] = str(context.get('project_root', '.'))

            elif param.name == 'task':
                # Use raw task from context if available, otherwise build from intent
                params['task'] = context.get('raw_task', f"{intent.goal} {intent.domain}").strip()

            elif param.name == 'feature_description':
                # Extract from task keywords or goal
                feature_desc = ' '.join(intent.keywords) if intent.keywords else intent.goal
                params['feature_description'] = feature_desc

            elif param.name == 'category':
                # Use domain as category
                params['category'] = intent.domain or 'general'

            elif param.name == 'domain':
                params['domain'] = intent.domain

            elif param.name == 'goal':
                params['goal'] = intent.goal

            elif param.name == 'keywords':
                params['keywords'] = intent.keywords

            elif param.name == 'changes':
                # Get from context if available
                params['changes'] = context.get('changes', {})

            elif param.name == 'check_tests':
                params['check_tests'] = True

            elif param.name == 'check_types':
                params['check_types'] = True

            elif param.name == 'auto_commit':
                params['auto_commit'] = True

            elif param.name == 'message':
                # Build commit message from intent
                params['message'] = f"{intent.goal}: {intent.domain}"

            # If parameter is required but not mapped, try to use intent.goal
            elif param.required and param.name not in params:
                logger.warning(
                    f"Required parameter '{param.name}' for skill '{skill.name}' "
                    f"not explicitly mapped, using intent.goal as fallback"
                )
                params[param.name] = intent.goal

        # Add any explicit defaults for optional parameters
        for param in skill.parameters:
            if param.name not in params and param.default is not None:
                params[param.name] = param.default

        logger.debug(f"Extracted parameters for {skill.name}: {list(params.keys())}")
        return params

    def _build_parameters(self, skill: Skill, intent: TaskIntent) -> Dict[str, Any]:
        """
        Build skill parameters from task intent (legacy method).

        DEPRECATED: Use _extract_parameters_for_skill instead.
        Kept for backward compatibility.

        Args:
            skill: Skill to build parameters for
            intent: Task intent with extracted information

        Returns:
            Dictionary of parameters
        """
        # Delegate to new intelligent extraction method
        return self._extract_parameters_for_skill(skill, intent)

    def _estimate_skill_duration(self, skill_name: str) -> float:
        """
        Estimate skill execution duration.

        Args:
            skill_name: Name of skill

        Returns:
            Estimated duration in seconds
        """
        return self.DURATION_ESTIMATES.get(skill_name, 30.0)

    def _plan_checkpoints(self, steps: List[SkillStep]) -> List[CheckpointPlan]:
        """
        Plan checkpoint locations.

        Args:
            steps: List of skill steps

        Returns:
            List of checkpoint plans
        """
        checkpoints = []

        for step in steps:
            if step.skill_name in self.CRITICAL_SKILLS:
                reason = self.CRITICAL_SKILLS[step.skill_name]
                checkpoint = CheckpointPlan(
                    id=str(uuid.uuid4()),
                    label=f"before_{step.skill_name}",
                    before_skill=step.skill_name,
                    reason=reason,
                    priority=1  # Critical checkpoints have priority 1
                )
                checkpoints.append(checkpoint)

        # Add checkpoint at the beginning
        if steps:
            checkpoints.insert(0, CheckpointPlan(
                id=str(uuid.uuid4()),
                label="initial_state",
                before_skill=steps[0].skill_name,
                reason="Initial state before execution",
                priority=1
            ))

        return checkpoints

    def _detect_decision_points(
        self,
        steps: List[SkillStep],
        auto_mode: bool
    ) -> List[DecisionPoint]:
        """
        Detect decision points in execution.

        Args:
            steps: List of skill steps
            auto_mode: If True, provide defaults for auto-execution

        Returns:
            List of decision points
        """
        decision_points = []

        for i, step in enumerate(steps):
            if step.skill_name in self.DECISION_SKILLS:
                question = self.DECISION_SKILLS[step.skill_name]

                # Build options based on skill type
                options = []
                default = None

                if step.skill_name == 'library_discovery':
                    options = ['Use top recommendation', 'Show alternatives', 'Skip library']
                    default = 'Use top recommendation' if auto_mode else None

                elif step.skill_name == 'analysis':
                    options = ['Proceed with plan', 'Modify approach', 'Cancel']
                    default = 'Proceed with plan' if auto_mode else None

                elif step.skill_name == 'validation':
                    options = ['Accept results', 'Retry', 'Manual review']
                    default = 'Accept results' if auto_mode else None

                decision = DecisionPoint(
                    id=str(uuid.uuid4()),
                    question=question,
                    options=options,
                    after_skill=step.skill_name,
                    default=default,
                    timeout_seconds=300
                )

                decision_points.append(decision)

        return decision_points

    def _estimate_duration(self, steps: List[SkillStep]) -> float:
        """
        Estimate total execution duration.

        Args:
            steps: List of skill steps

        Returns:
            Total estimated duration in seconds
        """
        return sum(step.estimated_duration for step in steps)

    def _mark_checkpoint_steps(
        self,
        steps: List[SkillStep],
        checkpoints: List[CheckpointPlan]
    ):
        """
        Mark which steps need checkpoints.

        Args:
            steps: List of skill steps (modified in-place)
            checkpoints: List of checkpoint plans
        """
        for checkpoint in checkpoints:
            for step in steps:
                if step.skill_name == checkpoint.before_skill:
                    step.checkpoint_before = True
                    break
