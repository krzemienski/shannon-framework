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

# V5 Infrastructure (not custom skills framework)
from shannon.orchestration.state_manager import StateManager
from shannon.orchestration.agent_pool import AgentPool

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
        """Initialize infrastructure components (not custom skills framework).

        V5: Removed custom skills framework (SkillRegistry, Planner, Executor).
        Shannon V5 uses Shannon Framework Claude Code skills instead.

        Keeping only:
        - StateManager: For execution checkpoints
        """

        # State Manager - for checkpoints and rollback
        try:
            # Use config directory as project root for state management
            project_root = self.config.config_dir / "execution_state"
            project_root.mkdir(parents=True, exist_ok=True)

            self.state_manager = StateManager(project_root=project_root)
            logger.info(f"✓ StateManager initialized (root: {project_root})")
        except Exception as e:
            logger.warning(f"StateManager initialization failed: {e}")
            self.state_manager = None

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

    async def execute_task(
        self,
        task: str,
        dashboard_client: Optional[Any] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute task via Shannon Framework task-automation Claude Code skill.

        V5: Invokes Shannon Framework's task-automation skill and wraps with
        V3 intelligence (cache, analytics, cost optimization).

        Args:
            task: Natural language task description
            dashboard_client: Optional DashboardEventClient for real-time updates
            session_id: Optional session ID for tracking

        Returns:
            Execution result dictionary

        Raises:
            RuntimeError: If SDK client not available
        """
        if not self.sdk_client:
            raise RuntimeError("SDK client not available")

        logger.info(f"Executing task via Shannon Framework task-automation skill: {task}")

        # V3: Check cache first (CORRECT API: cache.analysis.get)
        # Note: For now, skip cache for tasks (different from analysis caching)
        # Tasks are execution-focused, analysis is read-heavy
        # Can add task caching later if needed

        # V3: Cost optimization and model selection
        model = 'sonnet'  # Default
        if self.model_selector and self.budget_enforcer:
            try:
                complexity_estimate = len(task) / 100  # Simple heuristic
                budget_status = self.budget_enforcer.get_status()

                selection = self.model_selector.select_optimal_model(
                    agent_complexity=complexity_estimate,
                    context_size_tokens=0,
                    budget_remaining=budget_status.remaining
                )
                model = selection.model
                logger.info(f"Selected model: {model}")
            except Exception as e:
                logger.warning(f"Cost optimization failed: {e}")

        # Execute via Shannon Framework task-automation skill
        # CORRECT API: invoke_skill() not query()
        logger.info("Invoking Shannon Framework task-automation skill")
        messages = []

        async for msg in self.sdk_client.invoke_skill(
            skill_name='task-automation',
            prompt_content=f"Task: {task}"
        ):
            messages.append(msg)

            # Stream to dashboard if provided
            if dashboard_client:
                await self._stream_message_to_dashboard(msg, dashboard_client)

        # Parse result from messages
        result = self._parse_task_result(messages)

        # V3: Record to analytics (skip cache for now)
        if self.analytics_db and session_id:
            try:
                # Record task execution
                # analytics_db.record_task_execution() may not exist yet
                # Use record_session() with task info
                logger.info("Analytics recording skipped (method TBD)")
            except Exception as e:
                logger.warning(f"Analytics recording failed: {e}")

        logger.info(f"Task execution complete: {result.get('success', False)}")
        return result

    async def _stream_message_to_dashboard(
        self,
        msg: Any,
        dashboard_client: Any
    ) -> None:
        """Stream message to dashboard for real-time updates."""
        from claude_agent_sdk import TextBlock, ToolUseBlock, ThinkingBlock

        try:
            if isinstance(msg, TextBlock):
                await dashboard_client.emit_event('task:progress', {
                    'type': 'text',
                    'content': msg.text[:500]  # Truncate long text
                })
            elif isinstance(msg, ToolUseBlock):
                await dashboard_client.emit_event('tool:use', {
                    'name': msg.name,
                    'input': str(msg.input)[:200]  # Truncate
                })
            elif isinstance(msg, ThinkingBlock):
                await dashboard_client.emit_event('task:thinking', {
                    'content': msg.thinking[:500]  # Truncate
                })
        except Exception as e:
            logger.warning(f"Dashboard streaming failed: {e}")

    def _parse_task_result(self, messages: List) -> Dict[str, Any]:
        """Parse task execution result from Claude messages."""
        from claude_agent_sdk import ResultMessage, ToolUseBlock

        # Extract result message
        result_msgs = [m for m in messages if isinstance(m, ResultMessage)]
        files_created = []

        # Find file operations from messages
        for msg in messages:
            if hasattr(msg, 'content'):
                for block in msg.content:
                    if isinstance(block, ToolUseBlock) and block.name in ['Write', 'Edit']:
                        file_path = block.input.get('file_path')
                        if file_path:
                            files_created.append(file_path)

        return {
            'success': len(result_msgs) > 0 and not result_msgs[-1].is_error if result_msgs else True,
            'files_created': files_created,
            'message_count': len(messages),
            'result_messages': result_msgs
        }

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
