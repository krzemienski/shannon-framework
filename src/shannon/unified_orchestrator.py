"""UnifiedOrchestrator - V5 Consolidation Layer

Consolidates V3 (ContextAwareOrchestrator) and V4 (orchestration.Orchestrator)
into a unified interface while maintaining both systems' integrity.

Architecture: Facade pattern with subsystem sharing
- Delegates to existing orchestrators (no reimplementation)
- Shares subsystems: cache, context, analytics, cost optimization
- Provides unified interface for all commands

Created for: Shannon CLI V5
Design: docs/design/UNIFIED_ORCHESTRATOR_DESIGN.md
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

# V3 Orchestrator and subsystems
from shannon.orchestrator import ContextAwareOrchestrator
from shannon.cache.manager import CacheManager
from shannon.context.manager import ContextManager
from shannon.analytics.database import AnalyticsDatabase
from shannon.optimization.model_selector import ModelSelector
from shannon.optimization.cost_estimator import CostEstimator
from shannon.optimization.budget_enforcer import BudgetEnforcer
from shannon.mcp.manager import MCPManager
from shannon.agents.state_tracker import AgentStateTracker
from shannon.agents.controller import AgentController

# V4 Orchestration and subsystems
from shannon.orchestration.orchestrator import Orchestrator as V4Orchestrator
from shannon.orchestration.planner import ExecutionPlanner
from shannon.orchestration.state_manager import StateManager
from shannon.orchestration.agent_pool import AgentPool
from shannon.skills.registry import SkillRegistry
from shannon.skills.executor import SkillExecutor
from shannon.skills.hooks import HookManager

# Shared infrastructure
from shannon.config import ShannonConfig
from shannon.sdk.client import ShannonSDKClient

logger = logging.getLogger(__name__)


class UnifiedOrchestrator:
    """Unified orchestration layer consolidating V3 and V4 capabilities.

    The UnifiedOrchestrator provides a single interface for all Shannon CLI
    operations while maintaining the separation between V3 (intelligence/analysis)
    and V4 (skills/execution) systems.

    Architecture:
        - V3 Path: execute_analysis() → ContextAwareOrchestrator (context-aware analysis)
        - V4 Path: execute_skills() → orchestration.Orchestrator (skills execution)
        - Unified: execute_unified() → Both V3 + V4 (analysis then execution)

    Shared Subsystems (available to both V3 and V4):
        - CacheManager: Multi-tier caching
        - ContextManager: Project context loading
        - AnalyticsDatabase: Session recording
        - CostEstimator/BudgetEnforcer: Cost optimization
        - AgentPool: Parallel execution management

    Usage:
        orchestrator = UnifiedOrchestrator()

        # V3 analysis
        result = await orchestrator.execute_analysis(spec_text)

        # V4 execution
        result = await orchestrator.execute_skills(task)

        # Combined
        result = await orchestrator.execute_unified(spec_text, auto_execute=True)
    """

    def __init__(self, config: Optional[ShannonConfig] = None):
        """Initialize unified orchestrator with shared subsystems.

        Args:
            config: Optional ShannonConfig (creates default if not provided)
        """
        self.config = config or ShannonConfig()

        # Thread safety for shared mutable state
        self._budget_lock = asyncio.Lock()

        # Initialize shared subsystems (available to both V3 and V4)
        self._initialize_shared_subsystems()

        # Initialize V3-specific components
        self._initialize_v3_components()

        # Initialize V4-specific components
        self._initialize_v4_components()

        logger.info("UnifiedOrchestrator initialized: V3+V4 consolidated")

    def _initialize_shared_subsystems(self):
        """Initialize subsystems shared between V3 and V4 flows."""

        # Cache: Shared analysis and skill result caching
        try:
            cache_dir = self.config.config_dir / 'cache'
            self.cache = CacheManager(base_dir=cache_dir)
            logger.info("✓ Shared CacheManager initialized")
        except Exception as e:
            logger.warning(f"CacheManager initialization failed: {e}")
            self.cache = None

        # Context: Shared project context loading
        try:
            self.context = ContextManager()
            logger.info("✓ Shared ContextManager initialized")
        except Exception as e:
            logger.warning(f"ContextManager initialization failed: {e}")
            self.context = None

        # Analytics: Shared session and performance recording
        try:
            analytics_db_path = self.config.config_dir / 'analytics.db'
            self.analytics_db = AnalyticsDatabase(db_path=analytics_db_path)
            logger.info("✓ Shared AnalyticsDatabase initialized")
        except Exception as e:
            logger.warning(f"AnalyticsDatabase initialization failed: {e}")
            self.analytics_db = None

        # Cost Optimization: Shared model selection and budget enforcement
        try:
            self.model_selector = ModelSelector()
            self.cost_estimator = CostEstimator()
            self.budget_enforcer = BudgetEnforcer()
            logger.info("✓ Shared cost optimization initialized")
        except Exception as e:
            logger.warning(f"Cost optimization initialization failed: {e}")
            self.model_selector = None
            self.cost_estimator = None
            self.budget_enforcer = None

        # Agent Pool: Shared parallel agent execution
        try:
            self.agent_pool = AgentPool(max_active=8, max_total=50)
            logger.info("✓ Shared AgentPool initialized (8 active / 50 max)")
        except Exception as e:
            logger.warning(f"AgentPool initialization failed: {e}")
            self.agent_pool = None

        # SDK Client: Shared Shannon Framework interface
        try:
            self.sdk_client = ShannonSDKClient()
            logger.info("✓ Shared SDK client initialized")
        except Exception as e:
            logger.error(f"SDK client initialization failed: {e}")
            self.sdk_client = None

    def _initialize_v3_components(self):
        """Initialize V3-specific components."""

        # MCP Manager (V3 feature)
        try:
            self.mcp = MCPManager()
            logger.info("✓ V3 MCPManager initialized")
        except Exception as e:
            logger.warning(f"MCPManager initialization failed: {e}")
            self.mcp = None

        # Agent State Tracker (V3 wave monitoring)
        try:
            self.agent_tracker = AgentStateTracker()
            self.agent_controller = AgentController(self.agent_tracker)
            logger.info("✓ V3 Agent tracking initialized")
        except Exception as e:
            logger.warning(f"Agent tracking initialization failed: {e}")
            self.agent_tracker = None
            self.agent_controller = None

        # Create V3 orchestrator instance with shared subsystems
        try:
            self.v3_orchestrator = ContextAwareOrchestrator(self.config)

            # Inject shared subsystems (override V3's own instances)
            self.v3_orchestrator.cache = self.cache
            self.v3_orchestrator.context = self.context
            self.v3_orchestrator.analytics_db = self.analytics_db
            self.v3_orchestrator.model_selector = self.model_selector
            self.v3_orchestrator.cost_estimator = self.cost_estimator
            self.v3_orchestrator.budget_enforcer = self.budget_enforcer
            self.v3_orchestrator.sdk_client = self.sdk_client
            self.v3_orchestrator.agent_pool = self.agent_pool

            logger.info("✓ V3 ContextAwareOrchestrator created with shared subsystems")
        except Exception as e:
            logger.error(f"V3 orchestrator initialization failed: {e}")
            self.v3_orchestrator = None

    def _initialize_v4_components(self):
        """Initialize V4-specific components."""

        # Skills Registry (V4 feature) - requires schema_path
        try:
            # Schema is in project root /schemas/skill.schema.json
            schema_path = Path(__file__).parent.parent.parent / "schemas" / "skill.schema.json"

            if schema_path.exists():
                self.skills_registry = SkillRegistry(schema_path=schema_path)
                logger.info(f"✓ V4 SkillRegistry initialized (schema: {schema_path})")
            else:
                logger.warning(f"Skill schema not found at {schema_path}, SkillRegistry unavailable")
                self.skills_registry = None
        except Exception as e:
            logger.warning(f"SkillRegistry initialization failed: {e}")
            self.skills_registry = None

        # Hook Manager (V4 feature) - requires registry
        try:
            if self.skills_registry is not None:
                self.hook_manager = HookManager(registry=self.skills_registry)
                logger.info("✓ V4 HookManager initialized")
            else:
                logger.warning("HookManager skipped (no registry)")
                self.hook_manager = None
        except Exception as e:
            logger.warning(f"HookManager initialization failed: {e}")
            self.hook_manager = None

        # Execution Planner (V4 feature) - requires registry
        try:
            if self.skills_registry is not None:
                self.planner = ExecutionPlanner(registry=self.skills_registry)
                logger.info("✓ V4 ExecutionPlanner initialized")
            else:
                logger.warning("ExecutionPlanner skipped (no registry)")
                self.planner = None
        except Exception as e:
            logger.warning(f"ExecutionPlanner initialization failed: {e}")
            self.planner = None

        # State Manager (V4 feature) - requires project_root
        try:
            # Use config directory as project root for state management
            project_root = self.config.config_dir / "execution_state"
            project_root.mkdir(parents=True, exist_ok=True)

            self.state_manager = StateManager(project_root=project_root)
            logger.info(f"✓ V4 StateManager initialized (root: {project_root})")
        except Exception as e:
            logger.warning(f"StateManager initialization failed: {e}")
            self.state_manager = None

        # Skill Executor (V4 feature) - requires registry and hook_manager
        try:
            if self.skills_registry is not None and self.hook_manager is not None:
                self.v4_executor = SkillExecutor(
                    registry=self.skills_registry,
                    hook_manager=self.hook_manager,
                    dashboard_client=None  # Will be set per-execution
                )
                logger.info("✓ V4 SkillExecutor initialized")
            else:
                logger.warning("SkillExecutor skipped (missing registry or hook_manager)")
                self.v4_executor = None
        except Exception as e:
            logger.warning(f"SkillExecutor initialization failed: {e}")
            self.v4_executor = None

    async def execute_analysis(
        self,
        spec_text: str,
        project_id: Optional[str] = None,
        use_cache: bool = True,
        show_metrics: bool = True,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute specification analysis via V3 ContextAwareOrchestrator.

        This method delegates to the V3 orchestrator which provides:
        - Context-aware analysis
        - Multi-tier caching
        - Cost optimization
        - MCP recommendations
        - Analytics recording

        Args:
            spec_text: Specification text to analyze
            project_id: Optional project ID for context-aware analysis
            use_cache: Whether to check/use cache (default: True)
            show_metrics: Whether to show live metrics dashboard (default: True)
            session_id: Optional session ID for tracking

        Returns:
            Analysis result dictionary with complexity scores, domains, recommendations

        Raises:
            RuntimeError: If V3 orchestrator not available
        """
        if not self.v3_orchestrator:
            raise RuntimeError("V3 orchestrator not available")

        logger.info(f"Delegating to V3 analysis: project={project_id}, cache={use_cache}")

        # Delegate to V3 ContextAwareOrchestrator
        # Shared subsystems already injected during initialization
        result = await self.v3_orchestrator.execute_analyze(
            spec_text=spec_text,
            project_id=project_id,
            use_cache=use_cache,
            show_metrics=show_metrics,
            session_id=session_id
        )

        logger.info("V3 analysis complete")
        return result

    async def execute_wave(
        self,
        wave_request: str,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Execute wave-based implementation via V3 ContextAwareOrchestrator.

        Args:
            wave_request: Wave execution request
            project_id: Optional project ID for context
            session_id: Session ID for tracking
            use_cache: Whether to use cached results

        Returns:
            Wave execution results
        """
        if not self.v3_orchestrator:
            raise RuntimeError("V3 orchestrator not available")

        logger.info(f"Delegating to V3 wave: {wave_request}")

        result = await self.v3_orchestrator.execute_wave(
            wave_request=wave_request,
            project_id=project_id,
            session_id=session_id,
            use_cache=use_cache
        )

        logger.info("V3 wave complete")
        return result

    async def execute_task(
        self,
        spec_or_request: str,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute combined analyze + wave via V3 ContextAwareOrchestrator.

        Args:
            spec_or_request: Specification text or task request
            project_id: Optional project ID
            session_id: Session ID for tracking

        Returns:
            Combined analysis and wave results
        """
        if not self.v3_orchestrator:
            raise RuntimeError("V3 orchestrator not available")

        logger.info(f"Delegating to V3 task: {spec_or_request}")

        result = await self.v3_orchestrator.execute_task(
            spec_or_request=spec_or_request,
            project_id=project_id,
            session_id=session_id
        )

        logger.info("V3 task complete")
        return result

    async def execute_skills(
        self,
        task: str,
        dashboard_client: Optional[Any] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute skills-based task via V4 orchestration with multi-agent support.

        This method provides V4 skills-based execution with:
        - Skills framework (auto-discovery, dependencies)
        - Interactive controls (halt, resume, rollback)
        - Real-time dashboard streaming
        - Multi-agent parallel execution via AgentPool

        Args:
            task: Natural language task description
            dashboard_client: Optional DashboardEventClient for real-time updates
            session_id: Optional session ID for tracking

        Returns:
            Execution result dictionary

        Raises:
            RuntimeError: If V4 components not available
        """
        if not self.planner or not self.v4_executor or not self.state_manager:
            raise RuntimeError("V4 orchestration components not available")

        logger.info(f"Executing V4 skills-based task: {task}")

        # Create execution plan
        plan = await self.planner.create_plan(task)
        logger.info(f"Plan created: {len(plan.steps)} steps")

        # Set dashboard client on executor if provided
        if dashboard_client:
            self.v4_executor.dashboard_client = dashboard_client

        # V5: Agent spawning and tracking for each skill step
        if self.agent_pool and self.agent_tracker:
            logger.info(f"Agent spawning enabled: {len(plan.steps)} skills")

            # Import AgentTask and AgentRole for agent creation
            from shannon.orchestration.agent_pool import AgentTask, AgentRole

            for i, skill_step in enumerate(plan.steps):
                # Create agent task for each skill
                agent_task = AgentTask(
                    task_id=f"task-{skill_step.skill_name}-{i}",
                    description=skill_step.description or f"Execute {skill_step.skill_name}",
                    role=AgentRole.GENERIC
                )

                # Submit to pool (spawns agent infrastructure)
                await self.agent_pool.submit_task(agent_task)
                logger.info(f"Agent task submitted: {agent_task.task_id}")

                # Register with tracker for monitoring
                agent_id = f"agent-{agent_task.task_id}"
                self.agent_tracker.register_agent(
                    agent_id=agent_id,
                    wave_number=1,  # TODO: Track wave counter
                    agent_type=skill_step.skill_name,
                    task_description=skill_step.description or skill_step.skill_name
                )
                self.agent_tracker.mark_started(agent_id)
                logger.info(f"Agent registered and started: {agent_id}")

                # Emit agent:started event
                if dashboard_client:
                    await dashboard_client.emit_event('agent:started', {
                        'agent_id': agent_id,
                        'skill_name': skill_step.skill_name,
                        'step_index': i
                    })

            # Get agent pool stats for logging
            pool_stats = self.agent_pool.get_agent_stats()
            logger.info(f"AgentPool stats: {pool_stats}")

        # Create V4 orchestrator for execution
        # Note: Created per-execution to avoid state conflicts
        v4_orchestrator = V4Orchestrator(
            plan=plan,
            executor=self.v4_executor,
            state_manager=self.state_manager,
            session_id=session_id
        )

        # Inject shared subsystems into V4 orchestrator
        # This gives V4 access to V3's intelligence features
        v4_orchestrator.cache = self.cache
        v4_orchestrator.analytics_db = self.analytics_db
        v4_orchestrator.context = self.context
        v4_orchestrator.agent_pool = self.agent_pool

        # Execute via V4 orchestrator
        result = await v4_orchestrator.execute()

        # V5: Mark agents complete after execution
        if self.agent_tracker:
            # Mark all registered agents as complete
            all_states = self.agent_tracker.get_all_states()
            for agent_state in all_states:
                if agent_state.status == 'active':
                    self.agent_tracker.mark_complete(agent_state.agent_id)
                    logger.info(f"Agent marked complete: {agent_state.agent_id}")

                    # Emit agent:completed event
                    if dashboard_client:
                        await dashboard_client.emit_event('agent:completed', {
                            'agent_id': agent_state.agent_id,
                            'status': 'complete'
                        })

        logger.info(f"V4 execution complete: {result.success}")

        # Convert OrchestratorResult to dict
        return result.to_dict()

    async def execute_unified(
        self,
        spec_text: str,
        auto_execute: bool = True,
        project_id: Optional[str] = None,
        session_id: Optional[str] = None,
        dashboard_client: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Execute unified workflow: V3 analysis → V4 execution.

        This is the "full Shannon" experience:
        1. Analyze spec with V3 (complexity, domains, recommendations)
        2. Generate implementation plan
        3. Execute via V4 skills (with multi-agent, dashboard, controls)

        Args:
            spec_text: Specification text
            auto_execute: Whether to automatically execute after analysis
            project_id: Optional project ID for context
            session_id: Session ID for tracking
            dashboard_client: Optional dashboard client for real-time updates

        Returns:
            Combined analysis and execution results
        """
        logger.info("Starting unified V3→V4 workflow")

        # Step 1: V3 Analysis
        analysis_result = await self.execute_analysis(
            spec_text=spec_text,
            project_id=project_id,
            session_id=session_id,
            use_cache=True,
            show_metrics=True
        )

        logger.info("Analysis complete, proceeding to execution")

        # Step 2: V4 Execution (if auto_execute)
        execution_result = None
        if auto_execute:
            # Convert analysis to implementation task
            task = f"Implement: {spec_text}"

            execution_result = await self.execute_skills(
                task=task,
                dashboard_client=dashboard_client,
                session_id=session_id
            )

        # Return combined results
        return {
            'analysis': analysis_result,
            'execution': execution_result,
            'unified': True
        }

    def get_status(self) -> Dict[str, Any]:
        """Get status of all subsystems and orchestrators.

        Returns:
            Status dictionary with health of all components
        """
        return {
            'unified': {
                'version': '5.0.0',
                'mode': 'unified'
            },
            'shared_subsystems': {
                'cache': self.cache is not None,
                'context': self.context is not None,
                'analytics': self.analytics_db is not None,
                'cost_optimization': all([
                    self.model_selector is not None,
                    self.cost_estimator is not None,
                    self.budget_enforcer is not None
                ]),
                'agent_pool': self.agent_pool is not None,
                'sdk_client': self.sdk_client is not None
            },
            'v3_components': {
                'orchestrator': self.v3_orchestrator is not None,
                'mcp_manager': self.mcp is not None,
                'agent_tracker': self.agent_tracker is not None,
                'agent_controller': self.agent_controller is not None
            },
            'v4_components': {
                'skills_registry': self.skills_registry is not None,
                'planner': self.planner is not None,
                'state_manager': self.state_manager is not None,
                'executor': self.v4_executor is not None,
                'hook_manager': self.hook_manager is not None
            }
        }

    async def get_budget_status(self) -> Dict[str, Any]:
        """Get current budget status (thread-safe).

        Returns:
            Budget status dictionary
        """
        if not self.budget_enforcer:
            return {'available': False}

        async with self._budget_lock:
            status = self.budget_enforcer.get_status()
            return {
                'limit': status.limit,
                'spent': status.spent,
                'remaining': status.remaining,
                'available': True
            }

    async def check_budget(self, estimated_cost: float) -> bool:
        """Check if budget allows estimated cost (thread-safe).

        Args:
            estimated_cost: Estimated cost in USD

        Returns:
            True if budget allows, False otherwise
        """
        if not self.budget_enforcer:
            return True  # No enforcement if not available

        async with self._budget_lock:
            return self.budget_enforcer.check_available(estimated_cost)


# Convenience function for easy access
def create_unified_orchestrator(config: Optional[ShannonConfig] = None) -> UnifiedOrchestrator:
    """Create and return a UnifiedOrchestrator instance.

    Args:
        config: Optional configuration

    Returns:
        Configured unified orchestrator instance
    """
    return UnifiedOrchestrator(config)
