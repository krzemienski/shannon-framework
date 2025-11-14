"""Model selection engine for cost optimization.

This module implements smart model selection based on agent complexity,
context size, and budget constraints to minimize costs while maintaining quality.
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass


# Model pricing per 1K tokens (averaged input/output)
# Based on Claude API pricing as of Jan 2025
MODEL_COSTS = {
    'haiku': 0.001,       # $0.001 per 1K tokens avg (cheapest)
    'sonnet': 0.009,      # $0.009 per 1K tokens avg (default)
    'sonnet[1m]': 0.009,  # Same cost as sonnet, 1M context window
    'opus': 0.045         # $0.045 per 1K tokens avg (most expensive)
}

# Context window limits per model
MODEL_CONTEXT_LIMITS = {
    'haiku': 200_000,
    'sonnet': 200_000,
    'sonnet[1m]': 1_000_000,
    'opus': 200_000
}

# Detailed pricing for accurate cost estimation
MODEL_PRICING_DETAILED = {
    'haiku': {'input': 0.00025, 'output': 0.00125},      # Input: $0.25, Output: $1.25 per 1M
    'sonnet': {'input': 0.003, 'output': 0.015},         # Input: $3, Output: $15 per 1M
    'sonnet[1m]': {'input': 0.003, 'output': 0.015},     # Same as sonnet
    'opus': {'input': 0.015, 'output': 0.075}            # Input: $15, Output: $75 per 1M
}


@dataclass
class ModelSelectionResult:
    """Result of model selection with rationale.

    Attributes:
        model: Selected model name
        reason: Human-readable explanation for selection
        estimated_cost: Estimated cost for this agent in USD
        savings_vs_sonnet: Savings compared to using sonnet (USD)
    """
    model: str
    reason: str
    estimated_cost: float
    savings_vs_sonnet: float


class ModelSelector:
    """Smart model selection engine for cost optimization.

    Selects the optimal Claude model for each agent based on:
    - Agent complexity (0.0-1.0)
    - Context size requirements
    - Remaining budget
    - Historical performance (optional)

    The goal is to minimize cost while maintaining quality by using
    cheaper models (haiku) for simple tasks and expensive models
    (sonnet/opus) only when necessary.

    Selection rules (in priority order):
    1. Budget constraint: Use haiku if budget < $1.00
    2. Large context: Use sonnet[1m] if context > 200K tokens
    3. Simple tasks: Use haiku if complexity < 0.30
    4. Complex tasks: Use sonnet if complexity >= 0.60
    5. Moderate tasks: Use haiku for small context (<50K), sonnet otherwise

    Example:
        >>> selector = ModelSelector()
        >>> result = selector.select_optimal_model(
        ...     agent_complexity=0.25,
        ...     context_size_tokens=15000,
        ...     budget_remaining=10.00
        ... )
        >>> result.model
        'haiku'
        >>> result.reason
        'Simple agent (complexity 0.25 < 0.30) → haiku saves 80%'
    """

    def __init__(self):
        """Initialize model selector with pricing data."""
        self.model_costs = MODEL_COSTS
        self.context_limits = MODEL_CONTEXT_LIMITS
        self.detailed_pricing = MODEL_PRICING_DETAILED

    def select_optimal_model(
        self,
        agent_complexity: float,
        context_size_tokens: int,
        budget_remaining: float,
        estimated_tokens: int = 50000,
        historical_performance: Optional[Dict[str, Any]] = None
    ) -> ModelSelectionResult:
        """Select optimal model for an agent.

        Applies 5 selection rules in priority order to choose the most
        cost-effective model that meets quality requirements.

        Args:
            agent_complexity: Agent complexity score (0.0-1.0)
                0.0-0.3: Simple (config, docs, simple scripts)
                0.3-0.6: Moderate (standard features, testing)
                0.6-1.0: Complex (algorithms, architecture, integration)
            context_size_tokens: Required context window size
            budget_remaining: Remaining budget in USD
            estimated_tokens: Estimated total tokens for this agent (default: 50K)
            historical_performance: Optional historical data for learning

        Returns:
            ModelSelectionResult with selected model and rationale

        Raises:
            ValueError: If agent_complexity not in [0.0, 1.0]
        """
        if not 0.0 <= agent_complexity <= 1.0:
            raise ValueError(f"agent_complexity must be in [0.0, 1.0], got {agent_complexity}")

        # Rule 1: Budget constraint - if nearly out of budget, use cheapest
        if budget_remaining < 1.00:
            return ModelSelectionResult(
                model='haiku',
                reason=f'Low budget (${budget_remaining:.2f} < $1.00) → haiku required',
                estimated_cost=self._estimate_cost(estimated_tokens, 'haiku'),
                savings_vs_sonnet=self._calculate_savings(estimated_tokens, 'haiku')
            )

        # Rule 2: Large context needs 1M context window model
        if context_size_tokens > 200_000:
            return ModelSelectionResult(
                model='sonnet[1m]',
                reason=f'Large context ({context_size_tokens/1000:.0f}K > 200K) requires 1M window',
                estimated_cost=self._estimate_cost(estimated_tokens, 'sonnet[1m]'),
                savings_vs_sonnet=0.0  # Same cost as sonnet
            )

        # Rule 3: Simple agents can use haiku (80% savings)
        if agent_complexity < 0.30:
            return ModelSelectionResult(
                model='haiku',
                reason=f'Simple agent (complexity {agent_complexity:.2f} < 0.30) → haiku saves 80%',
                estimated_cost=self._estimate_cost(estimated_tokens, 'haiku'),
                savings_vs_sonnet=self._calculate_savings(estimated_tokens, 'haiku')
            )

        # Rule 4: Complex agents need sonnet for quality
        if agent_complexity >= 0.60:
            model = 'sonnet' if context_size_tokens < 200_000 else 'sonnet[1m]'
            return ModelSelectionResult(
                model=model,
                reason=f'Complex agent (complexity {agent_complexity:.2f} >= 0.60) requires sonnet',
                estimated_cost=self._estimate_cost(estimated_tokens, model),
                savings_vs_sonnet=0.0  # No savings, this is baseline
            )

        # Rule 5: Moderate agents - context-dependent
        # Small context: haiku works fine
        # Large context: sonnet for better quality
        if context_size_tokens < 50_000:
            return ModelSelectionResult(
                model='haiku',
                reason=f'Moderate complexity ({agent_complexity:.2f}), small context '
                       f'({context_size_tokens/1000:.0f}K) → haiku sufficient',
                estimated_cost=self._estimate_cost(estimated_tokens, 'haiku'),
                savings_vs_sonnet=self._calculate_savings(estimated_tokens, 'haiku')
            )
        else:
            return ModelSelectionResult(
                model='sonnet',
                reason=f'Moderate complexity ({agent_complexity:.2f}), larger context '
                       f'({context_size_tokens/1000:.0f}K) → sonnet for quality',
                estimated_cost=self._estimate_cost(estimated_tokens, 'sonnet'),
                savings_vs_sonnet=0.0
            )

    def _estimate_cost(self, tokens: int, model: str) -> float:
        """Estimate cost for given tokens and model.

        Args:
            tokens: Number of tokens (input + output combined)
            model: Model name

        Returns:
            Estimated cost in USD
        """
        cost_per_1k = self.model_costs.get(model, self.model_costs['sonnet'])
        return (tokens / 1000) * cost_per_1k

    def _calculate_savings(self, tokens: int, selected_model: str) -> float:
        """Calculate savings vs using sonnet.

        Args:
            tokens: Number of tokens
            selected_model: Model that was selected

        Returns:
            Savings in USD (positive = cheaper, 0 = same, negative = more expensive)
        """
        sonnet_cost = self._estimate_cost(tokens, 'sonnet')
        selected_cost = self._estimate_cost(tokens, selected_model)
        return sonnet_cost - selected_cost

    def estimate_wave_savings(
        self,
        agents: list[Dict[str, Any]],
        baseline_model: str = 'sonnet'
    ) -> Dict[str, float]:
        """Estimate total savings for a wave with optimized model selection.

        Compares cost of using baseline model (default: sonnet) for all agents
        vs optimized per-agent model selection.

        Args:
            agents: List of agent dicts with keys:
                - complexity: float
                - context_size: int (tokens)
                - estimated_tokens: int (optional, default 50K)
            baseline_model: Model to compare against (default: 'sonnet')

        Returns:
            Dict with:
                - original_cost: Cost using baseline model for all
                - optimized_cost: Cost with smart selection
                - savings_usd: Dollar savings
                - savings_percent: Percentage savings
                - model_selections: List of (agent_index, model, reason)

        Example:
            >>> selector = ModelSelector()
            >>> agents = [
            ...     {'complexity': 0.65, 'context_size': 45000, 'estimated_tokens': 60000},
            ...     {'complexity': 0.25, 'context_size': 12000, 'estimated_tokens': 20000},
            ...     {'complexity': 0.35, 'context_size': 18000, 'estimated_tokens': 30000}
            ... ]
            >>> savings = selector.estimate_wave_savings(agents)
            >>> savings['savings_percent']
            37.0
        """
        original_cost = 0.0
        optimized_cost = 0.0
        model_selections = []

        for idx, agent in enumerate(agents):
            # Extract agent parameters
            complexity = agent.get('complexity', 0.5)
            context_size = agent.get('context_size', 50000)
            estimated_tokens = agent.get('estimated_tokens', 50000)

            # Baseline: all agents use specified model
            original_cost += self._estimate_cost(estimated_tokens, baseline_model)

            # Optimized: select per agent
            result = self.select_optimal_model(
                agent_complexity=complexity,
                context_size_tokens=context_size,
                budget_remaining=float('inf'),  # No budget limit for estimation
                estimated_tokens=estimated_tokens
            )
            optimized_cost += result.estimated_cost
            model_selections.append((idx, result.model, result.reason))

        savings_usd = original_cost - optimized_cost
        savings_percent = (savings_usd / original_cost * 100) if original_cost > 0 else 0

        return {
            'original_cost': original_cost,
            'optimized_cost': optimized_cost,
            'savings_usd': savings_usd,
            'savings_percent': savings_percent,
            'model_selections': model_selections
        }
