"""Cost estimation for Shannon operations.

This module provides pre-execution cost estimates for spec analysis,
wave execution, and individual agents to help users make informed decisions.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from .model_selector import ModelSelector, MODEL_COSTS


@dataclass
class CostEstimate:
    """Cost estimate for an operation.

    Attributes:
        operation: Name of operation (e.g., 'spec-analysis', 'wave-1')
        estimated_cost_usd: Estimated cost in USD
        estimated_tokens: Estimated total tokens
        model: Model that will be used
        breakdown: Optional detailed breakdown
        confidence: Confidence level ('low', 'medium', 'high')
    """
    operation: str
    estimated_cost_usd: float
    estimated_tokens: int
    model: str
    breakdown: Optional[Dict[str, float]] = None
    confidence: str = 'medium'


class CostEstimator:
    """Pre-execution cost estimator for Shannon operations.

    Provides accurate cost estimates before running operations to help
    users make informed decisions and stay within budget.

    Estimation is based on:
    - Operation type (analysis, wave, agent)
    - Spec size (for analysis)
    - Agent count and complexity (for waves)
    - Context reuse factor (reduces costs for repeated operations)
    - Selected model (from ModelSelector)

    Example:
        >>> estimator = CostEstimator()
        >>> estimate = estimator.estimate_spec_analysis(spec_size_lines=1500)
        >>> estimate.estimated_cost_usd
        0.5
        >>> estimate.confidence
        'high'
    """

    def __init__(self, model_selector: Optional[ModelSelector] = None):
        """Initialize cost estimator.

        Args:
            model_selector: Optional ModelSelector instance (creates one if not provided)
        """
        self.model_selector = model_selector or ModelSelector()

        # Base token estimates for different operations
        # These are calibrated from actual Shannon usage data
        self.BASE_ESTIMATES = {
            'spec_analysis': {
                'tokens_per_line': 30,  # Average tokens per line of spec
                'base_tokens': 5000,    # Base overhead (instructions, analysis framework)
                'model': 'sonnet'       # Analysis always uses sonnet for quality
            },
            'wave_execution': {
                'tokens_per_agent': 50000,  # Average per agent
                'coordination_overhead': 10000,  # Wave coordination overhead
            }
        }

        # Context reuse factor: how much context can be reused across agents
        # Higher reuse = lower costs (agents share context, don't reload everything)
        self.CONTEXT_REUSE_FACTORS = {
            'same_wave': 0.7,      # Agents in same wave share 70% context
            'sequential_waves': 0.5,  # Sequential waves share 50%
            'different_project': 0.0  # Different projects share 0%
        }

    def estimate_spec_analysis(
        self,
        spec_size_lines: int,
        spec_complexity: Optional[float] = None
    ) -> CostEstimate:
        """Estimate cost for spec analysis.

        Spec analysis cost depends on:
        - Spec size (more lines = more tokens to analyze)
        - Spec complexity (complex specs may need multiple passes)
        - Model used (always sonnet for quality)

        Args:
            spec_size_lines: Number of lines in specification
            spec_complexity: Optional complexity score (0.0-1.0)
                If provided, adjusts estimate for complex specs

        Returns:
            CostEstimate for spec analysis

        Example:
            >>> estimator = CostEstimator()
            >>> estimate = estimator.estimate_spec_analysis(1500, complexity=0.65)
            >>> estimate.estimated_cost_usd
            0.52  # Approximate
        """
        base = self.BASE_ESTIMATES['spec_analysis']

        # Calculate token estimate
        spec_tokens = spec_size_lines * base['tokens_per_line']
        total_tokens = base['base_tokens'] + spec_tokens

        # Complexity adjustment (complex specs may need deeper analysis)
        if spec_complexity is not None:
            # Complex specs (>0.6) may use up to 20% more tokens
            complexity_factor = 1.0 + (spec_complexity - 0.5) * 0.4
            complexity_factor = max(0.8, min(1.2, complexity_factor))
            total_tokens = int(total_tokens * complexity_factor)

        # Calculate cost (spec analysis always uses sonnet)
        model = base['model']
        cost = (total_tokens / 1000) * MODEL_COSTS[model]

        # High confidence for spec analysis (well-calibrated estimates)
        confidence = 'high'

        breakdown = {
            'base_overhead': base['base_tokens'],
            'spec_content': spec_tokens,
            'complexity_adjustment': total_tokens - (base['base_tokens'] + spec_tokens)
        }

        return CostEstimate(
            operation='spec-analysis',
            estimated_cost_usd=cost,
            estimated_tokens=total_tokens,
            model=model,
            breakdown=breakdown,
            confidence=confidence
        )

    def estimate_wave_cost(
        self,
        agents: list[Dict[str, Any]],
        context_reuse: str = 'same_wave',
        budget_remaining: float = float('inf')
    ) -> CostEstimate:
        """Estimate cost for wave execution with multiple agents.

        Wave cost depends on:
        - Number of agents
        - Agent complexity (determines model selection)
        - Context size and reuse (shared context reduces cost)
        - Budget constraints (may force cheaper models)

        Args:
            agents: List of agent dicts with keys:
                - complexity: float (0.0-1.0)
                - context_size: int (tokens)
                - estimated_tokens: int (optional)
            context_reuse: Context reuse scenario ('same_wave', 'sequential_waves', 'different_project')
            budget_remaining: Remaining budget (affects model selection)

        Returns:
            CostEstimate for wave execution

        Example:
            >>> estimator = CostEstimator()
            >>> agents = [
            ...     {'complexity': 0.65, 'context_size': 45000},
            ...     {'complexity': 0.25, 'context_size': 12000},
            ...     {'complexity': 0.35, 'context_size': 18000}
            ... ]
            >>> estimate = estimator.estimate_wave_cost(agents)
            >>> estimate.estimated_cost_usd
            2.4  # Approximate with optimization
        """
        total_cost = 0.0
        total_tokens = 0
        reuse_factor = self.CONTEXT_REUSE_FACTORS.get(context_reuse, 0.0)

        # Coordination overhead (one-time cost for wave setup)
        wave_overhead = self.BASE_ESTIMATES['wave_execution']['coordination_overhead']
        total_tokens += wave_overhead

        agent_costs = []
        models_used = []

        for agent in agents:
            # Extract agent parameters
            complexity = agent.get('complexity', 0.5)
            context_size = agent.get('context_size', 50000)
            estimated_tokens = agent.get('estimated_tokens', 50000)

            # Apply context reuse (agents share context, reducing total tokens)
            effective_tokens = estimated_tokens
            if reuse_factor > 0:
                # First agent loads full context, subsequent reuse
                is_first = len(agent_costs) == 0
                if not is_first:
                    effective_tokens = int(estimated_tokens * (1 - reuse_factor))

            total_tokens += effective_tokens

            # Select optimal model for this agent
            result = self.model_selector.select_optimal_model(
                agent_complexity=complexity,
                context_size_tokens=context_size,
                budget_remaining=budget_remaining,
                estimated_tokens=effective_tokens
            )

            agent_costs.append(result.estimated_cost)
            models_used.append(result.model)
            total_cost += result.estimated_cost

        # Add coordination overhead cost (uses sonnet)
        overhead_cost = (wave_overhead / 1000) * MODEL_COSTS['sonnet']
        total_cost += overhead_cost

        # Determine primary model (most common in wave)
        primary_model = max(set(models_used), key=models_used.count) if models_used else 'sonnet'

        # Confidence: medium for waves (depends on agent complexity estimates)
        confidence = 'medium'

        breakdown = {
            'wave_overhead': overhead_cost,
            'agent_costs': sum(agent_costs),
            'context_reuse_savings': (
                sum(a.get('estimated_tokens', 50000) for a in agents) - total_tokens
            ) / 1000 * MODEL_COSTS['sonnet']
        }

        return CostEstimate(
            operation=f'wave-{len(agents)}-agents',
            estimated_cost_usd=total_cost,
            estimated_tokens=total_tokens,
            model=primary_model,
            breakdown=breakdown,
            confidence=confidence
        )

    def estimate_agent_cost(
        self,
        agent_complexity: float,
        context_size_tokens: int,
        estimated_tokens: int = 50000,
        budget_remaining: float = float('inf')
    ) -> CostEstimate:
        """Estimate cost for a single agent.

        Args:
            agent_complexity: Agent complexity score (0.0-1.0)
            context_size_tokens: Required context size
            estimated_tokens: Estimated total tokens
            budget_remaining: Remaining budget

        Returns:
            CostEstimate for single agent

        Example:
            >>> estimator = CostEstimator()
            >>> estimate = estimator.estimate_agent_cost(0.25, 15000, 25000)
            >>> estimate.model
            'haiku'
            >>> estimate.estimated_cost_usd
            0.025
        """
        # Use model selector to pick optimal model
        result = self.model_selector.select_optimal_model(
            agent_complexity=agent_complexity,
            context_size_tokens=context_size_tokens,
            budget_remaining=budget_remaining,
            estimated_tokens=estimated_tokens
        )

        return CostEstimate(
            operation='single-agent',
            estimated_cost_usd=result.estimated_cost,
            estimated_tokens=estimated_tokens,
            model=result.model,
            breakdown={'base_cost': result.estimated_cost},
            confidence='medium'
        )

    def validate_against_budget(
        self,
        estimate: CostEstimate,
        budget_remaining: float
    ) -> Dict[str, Any]:
        """Validate estimate against remaining budget.

        Args:
            estimate: Cost estimate to validate
            budget_remaining: Remaining budget in USD

        Returns:
            Dict with:
                - within_budget: bool
                - remaining_after: float (remaining budget after operation)
                - buffer: float (buffer remaining, negative if over)
                - recommendation: str (proceed/warn/abort)

        Example:
            >>> estimator = CostEstimator()
            >>> estimate = estimator.estimate_spec_analysis(1500)
            >>> result = estimator.validate_against_budget(estimate, 10.00)
            >>> result['within_budget']
            True
            >>> result['recommendation']
            'proceed'
        """
        within_budget = estimate.estimated_cost_usd <= budget_remaining
        remaining_after = budget_remaining - estimate.estimated_cost_usd
        buffer = remaining_after

        # Recommendation logic
        if not within_budget:
            recommendation = 'abort'
        elif remaining_after < 1.00:
            recommendation = 'warn'  # Low buffer, proceed with caution
        else:
            recommendation = 'proceed'

        return {
            'within_budget': within_budget,
            'remaining_after': remaining_after,
            'buffer': buffer,
            'recommendation': recommendation
        }
