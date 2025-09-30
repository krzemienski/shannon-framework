"""
Shannon Framework v2.1 - Wave Orchestrator

Master coordination of wave execution, complexity analysis, strategy selection,
and agent lifecycle management.
"""

import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import logging

from .agent import BaseAgent, AgentState, AgentResult
from .wave_config import WaveConfig, WavePhase, WaveResult, AgentAllocation

logger = logging.getLogger(__name__)


class WaveStrategy(Enum):
    """Wave execution strategies"""
    PROGRESSIVE = "progressive"
    SYSTEMATIC = "systematic"
    ADAPTIVE = "adaptive"
    ENTERPRISE = "enterprise"
    VALIDATION = "validation"


@dataclass
class ComplexityScore:
    """8-dimensional complexity analysis result"""
    scope: float
    dependencies: float
    operations: float
    domains: float
    concurrency: float
    uncertainty: float
    risk: float
    scale: float
    total: float = 0.0
    threshold_exceeded: bool = False

    def __post_init__(self):
        """Calculate total and check threshold"""
        dimensions = [self.scope, self.dependencies, self.operations, self.domains,
                     self.concurrency, self.uncertainty, self.risk, self.scale]

        for dim in dimensions:
            if not 0.0 <= dim <= 1.0:
                raise ValueError(f"Dimension score must be in [0.0, 1.0], got {dim}")

        self.total = sum(dimensions) / len(dimensions)
        self.threshold_exceeded = self.total >= 0.7

    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            'scope': self.scope,
            'dependencies': self.dependencies,
            'operations': self.operations,
            'domains': self.domains,
            'concurrency': self.concurrency,
            'uncertainty': self.uncertainty,
            'risk': self.risk,
            'scale': self.scale,
            'total': self.total,
            'threshold_exceeded': self.threshold_exceeded
        }


@dataclass
class OrchestrationDecision:
    """Orchestration analysis and decision"""
    should_orchestrate: bool
    complexity: ComplexityScore
    recommended_strategy: WaveStrategy
    recommended_agent_count: int
    reasoning: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            'should_orchestrate': self.should_orchestrate,
            'complexity': self.complexity.to_dict(),
            'recommended_strategy': self.recommended_strategy.value,
            'recommended_agent_count': self.recommended_agent_count,
            'reasoning': self.reasoning,
            'warnings': self.warnings
        }


class ComplexityAnalyzer:
    """
    8-dimensional complexity analysis engine.

    Analyzes task complexity across multiple dimensions to determine
    if automatic wave orchestration should be triggered.
    """

    def __init__(self, threshold: float = 0.7):
        """
        Initialize analyzer with threshold.

        Args:
            threshold: Complexity threshold for orchestration (default 0.7)
        """
        if not 0.0 <= threshold <= 1.0:
            raise ValueError(f"Threshold must be in [0.0, 1.0], got {threshold}")
        self.threshold = threshold

    async def analyze(self, task: Dict[str, Any]) -> ComplexityScore:
        """
        Perform 8-dimensional complexity analysis.

        Args:
            task: Task specification dictionary

        Returns:
            ComplexityScore with all dimensions analyzed
        """
        scope_score = await self._analyze_scope(task)
        deps_score = await self._analyze_dependencies(task)
        ops_score = await self._analyze_operations(task)
        domains_score = await self._analyze_domains(task)
        concurrency_score = await self._analyze_concurrency(task)
        uncertainty_score = await self._analyze_uncertainty(task)
        risk_score = await self._analyze_risk(task)
        scale_score = await self._analyze_scale(task)

        complexity = ComplexityScore(
            scope=scope_score,
            dependencies=deps_score,
            operations=ops_score,
            domains=domains_score,
            concurrency=concurrency_score,
            uncertainty=uncertainty_score,
            risk=risk_score,
            scale=scale_score
        )

        logger.info(f"Complexity analysis: total={complexity.total:.3f}, threshold={self.threshold}")
        return complexity

    async def _analyze_scope(self, task: Dict[str, Any]) -> float:
        """Analyze task scope complexity (0.0-1.0)"""
        scope_indicators = task.get('scope_indicators', {})

        file_count = scope_indicators.get('file_count', 0)
        dir_count = scope_indicators.get('dir_count', 0)
        line_count = scope_indicators.get('line_count', 0)

        score = 0.0
        if file_count > 50:
            score += 0.4
        elif file_count > 20:
            score += 0.25
        elif file_count > 10:
            score += 0.15

        if dir_count > 10:
            score += 0.3
        elif dir_count > 5:
            score += 0.15

        if line_count > 10000:
            score += 0.3
        elif line_count > 5000:
            score += 0.15

        return min(1.0, score)

    async def _analyze_dependencies(self, task: Dict[str, Any]) -> float:
        """Analyze dependency complexity (0.0-1.0)"""
        deps = task.get('dependencies', [])
        external_deps = task.get('external_dependencies', [])

        total_deps = len(deps) + len(external_deps)

        if total_deps > 20:
            return 0.9
        elif total_deps > 10:
            return 0.6
        elif total_deps > 5:
            return 0.3
        elif total_deps > 0:
            return 0.1
        return 0.0

    async def _analyze_operations(self, task: Dict[str, Any]) -> float:
        """Analyze operation type complexity (0.0-1.0)"""
        operations = task.get('operations', [])
        operation_types = set(op.get('type') for op in operations if 'type' in op)

        high_complexity_ops = {'refactor', 'optimize', 'migrate', 'transform'}
        medium_complexity_ops = {'analyze', 'test', 'validate', 'integrate'}

        high_count = len(operation_types & high_complexity_ops)
        medium_count = len(operation_types & medium_complexity_ops)

        score = high_count * 0.3 + medium_count * 0.15
        return min(1.0, score)

    async def _analyze_domains(self, task: Dict[str, Any]) -> float:
        """Analyze domain complexity (0.0-1.0)"""
        domains = task.get('domains', [])
        domain_count = len(set(domains))

        if domain_count >= 5:
            return 1.0
        elif domain_count == 4:
            return 0.75
        elif domain_count == 3:
            return 0.5
        elif domain_count == 2:
            return 0.25
        return 0.0

    async def _analyze_concurrency(self, task: Dict[str, Any]) -> float:
        """Analyze parallelization opportunities (0.0-1.0)"""
        parallel_opportunities = task.get('parallel_opportunities', 0)
        sequential_dependencies = task.get('sequential_dependencies', 0)

        if parallel_opportunities == 0:
            return 0.0

        ratio = parallel_opportunities / max(1, sequential_dependencies + parallel_opportunities)
        return ratio * 0.8

    async def _analyze_uncertainty(self, task: Dict[str, Any]) -> float:
        """Analyze task uncertainty (0.0-1.0)"""
        clarity_score = task.get('clarity_score', 1.0)
        ambiguous_requirements = task.get('ambiguous_requirements', [])

        uncertainty = 1.0 - clarity_score
        uncertainty += len(ambiguous_requirements) * 0.1

        return min(1.0, uncertainty)

    async def _analyze_risk(self, task: Dict[str, Any]) -> float:
        """Analyze risk level (0.0-1.0)"""
        risk_indicators = task.get('risk_indicators', {})

        production_impact = risk_indicators.get('production_impact', False)
        data_loss_risk = risk_indicators.get('data_loss_risk', False)
        security_impact = risk_indicators.get('security_impact', False)
        reversibility = risk_indicators.get('reversibility', True)

        score = 0.0
        if production_impact:
            score += 0.4
        if data_loss_risk:
            score += 0.3
        if security_impact:
            score += 0.2
        if not reversibility:
            score += 0.1

        return min(1.0, score)

    async def _analyze_scale(self, task: Dict[str, Any]) -> float:
        """Analyze task scale (0.0-1.0)"""
        scale_indicators = task.get('scale_indicators', {})

        user_count = scale_indicators.get('user_count', 0)
        data_volume_gb = scale_indicators.get('data_volume_gb', 0)
        request_rate = scale_indicators.get('request_rate', 0)

        score = 0.0
        if user_count > 1000000:
            score += 0.4
        elif user_count > 100000:
            score += 0.25
        elif user_count > 10000:
            score += 0.15

        if data_volume_gb > 1000:
            score += 0.3
        elif data_volume_gb > 100:
            score += 0.15

        if request_rate > 10000:
            score += 0.3
        elif request_rate > 1000:
            score += 0.15

        return min(1.0, score)


class AgentSpawner:
    """
    Agent lifecycle management and spawning.

    Handles agent creation, initialization, and cleanup.
    """

    def __init__(self, max_concurrent_agents: int = 10):
        """
        Initialize spawner with concurrency limit.

        Args:
            max_concurrent_agents: Maximum concurrent agents (default 10)
        """
        self.max_concurrent_agents = max_concurrent_agents
        self._active_agents: Dict[str, BaseAgent] = {}
        self._semaphore = asyncio.Semaphore(max_concurrent_agents)
        self._agent_counter = 0

    async def spawn_agent(self, agent_class: type, capabilities: Set, config: Dict[str, Any]) -> BaseAgent:
        """
        Spawn and initialize a new agent.

        Args:
            agent_class: Agent class to instantiate
            capabilities: Agent capabilities set
            config: Agent configuration

        Returns:
            Initialized agent instance
        """
        self._agent_counter += 1
        agent_id = f"{agent_class.__name__}_{self._agent_counter}_{int(time.time() * 1000)}"

        agent = agent_class(agent_id=agent_id, capabilities=capabilities, config=config)

        success = await agent.initialize()
        if not success:
            raise RuntimeError(f"Failed to initialize agent {agent_id}")

        self._active_agents[agent_id] = agent
        logger.info(f"Spawned agent {agent_id}")

        return agent

    async def execute_agent(self, agent: BaseAgent, task: Dict[str, Any]) -> AgentResult:
        """
        Execute agent with concurrency control.

        Args:
            agent: Agent to execute
            task: Task specification

        Returns:
            Agent execution result
        """
        async with self._semaphore:
            result = await agent.run(task)
        return result

    async def cleanup_agent(self, agent_id: str):
        """Clean up agent resources"""
        if agent_id in self._active_agents:
            agent = self._active_agents[agent_id]
            if agent.state == AgentState.EXECUTING:
                await agent.cancel()
            del self._active_agents[agent_id]
            logger.info(f"Cleaned up agent {agent_id}")

    async def cleanup_all(self):
        """Clean up all active agents"""
        agent_ids = list(self._active_agents.keys())
        for agent_id in agent_ids:
            await self.cleanup_agent(agent_id)

    def get_active_count(self) -> int:
        """Get count of active agents"""
        return len(self._active_agents)


class WaveOrchestrator:
    """
    Master wave orchestrator for automatic multi-agent coordination.

    Analyzes task complexity, selects execution strategy, spawns agents,
    and coordinates wave execution across phases.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize orchestrator with configuration.

        Args:
            config: Orchestrator configuration dictionary
        """
        self.config = config
        self.complexity_threshold = config.get('complexity_threshold', 0.7)
        self.max_concurrent_agents = config.get('max_concurrent_agents', 10)

        self.analyzer = ComplexityAnalyzer(threshold=self.complexity_threshold)
        self.spawner = AgentSpawner(max_concurrent_agents=self.max_concurrent_agents)

        self._active_waves: Dict[str, WaveConfig] = {}
        self._wave_results: Dict[str, WaveResult] = {}

        logger.info(f"WaveOrchestrator initialized with threshold={self.complexity_threshold}")

    async def analyze_and_decide(self, task: Dict[str, Any]) -> OrchestrationDecision:
        """
        Analyze task and decide if orchestration is needed.

        Args:
            task: Task specification dictionary

        Returns:
            OrchestrationDecision with analysis and recommendation
        """
        complexity = await self.analyzer.analyze(task)

        should_orchestrate = complexity.threshold_exceeded
        strategy = self._select_strategy(complexity, task)
        agent_count = self._estimate_agent_count(complexity, task)

        reasoning = []
        warnings = []

        if should_orchestrate:
            reasoning.append(f"Complexity {complexity.total:.3f} exceeds threshold {self.complexity_threshold}")
            reasoning.append(f"Selected strategy: {strategy.value}")
            reasoning.append(f"Recommended agents: {agent_count}")
        else:
            reasoning.append(f"Complexity {complexity.total:.3f} below threshold {self.complexity_threshold}")
            reasoning.append("Single-agent execution recommended")

        if complexity.risk > 0.7:
            warnings.append("High risk detected - validation strategy recommended")

        if complexity.uncertainty > 0.7:
            warnings.append("High uncertainty - adaptive strategy recommended")

        decision = OrchestrationDecision(
            should_orchestrate=should_orchestrate,
            complexity=complexity,
            recommended_strategy=strategy,
            recommended_agent_count=agent_count,
            reasoning=reasoning,
            warnings=warnings
        )

        logger.info(f"Orchestration decision: {should_orchestrate}, strategy={strategy.value}, agents={agent_count}")
        return decision

    async def execute_wave(self, wave_config: WaveConfig, agent_factory: Dict[str, type]) -> WaveResult:
        """
        Execute complete wave with all phases.

        Args:
            wave_config: Wave configuration
            agent_factory: Mapping of agent types to classes

        Returns:
            WaveResult with aggregated outcomes
        """
        wave_id = wave_config.wave_id
        self._active_waves[wave_id] = wave_config

        logger.info(f"Starting wave execution: {wave_id}")
        start_time = time.time()

        phase_results: Dict[WavePhase, List[AgentResult]] = {}
        total_executed = 0
        total_succeeded = 0
        total_failed = 0

        try:
            for allocation in wave_config.phases:
                logger.info(f"Wave {wave_id}: Executing phase {allocation.phase.value}")

                results = await self._execute_phase(allocation, agent_factory, wave_config)
                phase_results[allocation.phase] = results

                total_executed += len(results)
                total_succeeded += sum(1 for r in results if r.success)
                total_failed += sum(1 for r in results if not r.success)

                if total_failed > 0 and wave_config.validation_level.value == 'production':
                    logger.error(f"Wave {wave_id}: Phase {allocation.phase.value} had failures in production mode")
                    break

            duration = time.time() - start_time
            overall_success = total_failed == 0

            result = WaveResult(
                wave_id=wave_id,
                success=overall_success,
                phase_results=phase_results,
                total_duration_seconds=duration,
                agents_executed=total_executed,
                agents_succeeded=total_succeeded,
                agents_failed=total_failed
            )

            self._wave_results[wave_id] = result
            logger.info(f"Wave {wave_id} completed: success={overall_success}, duration={duration:.2f}s")

            return result

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Wave {wave_id} failed: {e}")

            result = WaveResult(
                wave_id=wave_id,
                success=False,
                phase_results=phase_results,
                total_duration_seconds=duration,
                agents_executed=total_executed,
                agents_succeeded=total_succeeded,
                agents_failed=total_failed,
                errors=[str(e)]
            )

            self._wave_results[wave_id] = result
            return result

        finally:
            if wave_id in self._active_waves:
                del self._active_waves[wave_id]

    async def _execute_phase(self, allocation: AgentAllocation, agent_factory: Dict[str, type],
                           wave_config: WaveConfig) -> List[AgentResult]:
        """Execute single wave phase"""
        agents = []
        tasks = []

        for agent_type in allocation.agent_types:
            if agent_type not in agent_factory:
                logger.error(f"Unknown agent type: {agent_type}")
                continue

            agent_class = agent_factory[agent_type]
            config = {'wave_config': wave_config, 'phase': allocation.phase}

            agent = await self.spawner.spawn_agent(agent_class, set(), config)
            agents.append(agent)

            task = {'phase': allocation.phase.value, 'allocation': allocation}
            tasks.append(task)

        if allocation.parallel_execution:
            results = await asyncio.gather(*[
                self.spawner.execute_agent(agent, task)
                for agent, task in zip(agents, tasks)
            ], return_exceptions=True)

            agent_results = []
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Agent execution exception: {result}")
                else:
                    agent_results.append(result)
        else:
            agent_results = []
            for agent, task in zip(agents, tasks):
                result = await self.spawner.execute_agent(agent, task)
                agent_results.append(result)

        for agent in agents:
            await self.spawner.cleanup_agent(agent.agent_id)

        return agent_results

    def _select_strategy(self, complexity: ComplexityScore, task: Dict[str, Any]) -> WaveStrategy:
        """Select optimal wave strategy based on complexity"""
        if complexity.risk > 0.8:
            return WaveStrategy.VALIDATION
        elif complexity.scale > 0.8:
            return WaveStrategy.ENTERPRISE
        elif complexity.uncertainty > 0.7:
            return WaveStrategy.ADAPTIVE
        elif complexity.total > 0.85:
            return WaveStrategy.SYSTEMATIC
        else:
            return WaveStrategy.PROGRESSIVE

    def _estimate_agent_count(self, complexity: ComplexityScore, task: Dict[str, Any]) -> int:
        """Estimate optimal agent count"""
        base_count = 3

        if complexity.total > 0.9:
            return min(10, base_count + 7)
        elif complexity.total > 0.8:
            return min(8, base_count + 5)
        elif complexity.total > 0.7:
            return min(5, base_count + 2)
        else:
            return base_count

    async def cleanup(self):
        """Clean up orchestrator resources"""
        await self.spawner.cleanup_all()
        self._active_waves.clear()
        logger.info("Orchestrator cleanup complete")