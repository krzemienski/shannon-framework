"""Cost optimization module for Shannon CLI.

This module provides smart model selection, cost estimation, and budget
enforcement to minimize Claude API costs while maintaining quality.

Key components:
- ModelSelector: Selects optimal model based on complexity and context
- CostEstimator: Provides pre-execution cost estimates
- BudgetEnforcer: Tracks spending and enforces budget limits

Example:
    >>> from shannon.optimization import ModelSelector, CostEstimator, BudgetEnforcer
    >>>
    >>> # Set up cost optimization
    >>> selector = ModelSelector()
    >>> estimator = CostEstimator(selector)
    >>> enforcer = BudgetEnforcer(budget_limit=15.00)
    >>>
    >>> # Estimate wave cost
    >>> agents = [
    ...     {'complexity': 0.65, 'context_size': 45000, 'estimated_tokens': 60000},
    ...     {'complexity': 0.25, 'context_size': 12000, 'estimated_tokens': 20000}
    ... ]
    >>> estimate = estimator.estimate_wave_cost(agents)
    >>>
    >>> # Check budget
    >>> check = enforcer.pre_execution_check('wave-1', estimate.estimated_cost_usd)
    >>> if check['allowed']:
    ...     print(f"Proceeding with wave (${estimate.estimated_cost_usd:.2f})")
"""

from .model_selector import (
    ModelSelector,
    ModelSelectionResult,
    MODEL_COSTS,
    MODEL_CONTEXT_LIMITS,
    MODEL_PRICING_DETAILED
)
from .cost_estimator import CostEstimator, CostEstimate
from .budget_enforcer import BudgetEnforcer, BudgetStatus

__all__ = [
    'ModelSelector',
    'ModelSelectionResult',
    'MODEL_COSTS',
    'MODEL_CONTEXT_LIMITS',
    'MODEL_PRICING_DETAILED',
    'CostEstimator',
    'CostEstimate',
    'BudgetEnforcer',
    'BudgetStatus'
]
