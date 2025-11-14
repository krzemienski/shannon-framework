"""Budget enforcement and tracking for Shannon operations.

This module provides budget management, tracking spending against limits,
and preventing operations that would exceed budget.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json


@dataclass
class BudgetStatus:
    """Current budget status.

    Attributes:
        budget_limit: Total budget limit in USD
        total_spent: Total amount spent so far
        remaining: Remaining budget
        operations: List of operations with costs
        within_budget: Whether currently within budget
        warnings: List of budget warnings
    """
    budget_limit: float
    total_spent: float
    remaining: float
    operations: List[Dict[str, Any]] = field(default_factory=list)
    within_budget: bool = True
    warnings: List[str] = field(default_factory=list)


class BudgetEnforcer:
    """Budget enforcement and cost tracking for Shannon operations.

    Tracks spending against a budget limit, prevents operations that
    would exceed budget, and provides optimization suggestions when
    approaching limits.

    Budget data is persisted to ~/.shannon/budget.json for tracking
    across sessions.

    Example:
        >>> enforcer = BudgetEnforcer(budget_limit=15.00)
        >>> enforcer.can_proceed(estimated_cost=0.50)
        True
        >>> enforcer.record_operation('spec-analysis', actual_cost=0.52)
        >>> enforcer.remaining()
        14.48
    """

    def __init__(self, budget_limit: float = 100.00, data_dir: Optional[Path] = None):
        """Initialize budget enforcer.

        Args:
            budget_limit: Budget limit in USD (default: $100)
            data_dir: Directory for budget data (default: ~/.shannon)
        """
        self.budget_limit = budget_limit
        self.data_dir = data_dir or Path.home() / '.shannon'
        self.budget_file = self.data_dir / 'budget.json'

        # In-memory tracking
        self.total_spent = 0.0
        self.operations: List[Dict[str, Any]] = []

        # Load existing budget data
        self._load_budget()

    def _load_budget(self) -> None:
        """Load budget data from file if exists."""
        if not self.budget_file.exists():
            return

        try:
            with open(self.budget_file, 'r') as f:
                data = json.load(f)

                self.budget_limit = data.get('budget_limit', self.budget_limit)
                self.total_spent = data.get('total_spent', 0.0)
                self.operations = data.get('operations', [])
        except (json.JSONDecodeError, OSError):
            # If file is corrupted, start fresh
            pass

    def _save_budget(self) -> None:
        """Save budget data to file."""
        self.data_dir.mkdir(parents=True, exist_ok=True)

        data = {
            'budget_limit': self.budget_limit,
            'total_spent': self.total_spent,
            'operations': self.operations,
            'last_updated': datetime.now().isoformat()
        }

        with open(self.budget_file, 'w') as f:
            json.dump(data, f, indent=2)

    def set_budget(self, budget_limit: float) -> None:
        """Set new budget limit.

        Args:
            budget_limit: New budget limit in USD

        Raises:
            ValueError: If budget_limit is negative
        """
        if budget_limit < 0:
            raise ValueError(f"Budget limit must be non-negative, got {budget_limit}")

        self.budget_limit = budget_limit
        self._save_budget()

    def reset_budget(self) -> None:
        """Reset spending to zero, keeping budget limit."""
        self.total_spent = 0.0
        self.operations = []
        self._save_budget()

    def remaining(self) -> float:
        """Get remaining budget.

        Returns:
            Remaining budget in USD (can be negative if overspent)
        """
        return self.budget_limit - self.total_spent

    def can_proceed(
        self,
        estimated_cost: float,
        require_buffer: float = 0.0
    ) -> bool:
        """Check if operation can proceed within budget.

        Args:
            estimated_cost: Estimated cost of operation in USD
            require_buffer: Minimum buffer to maintain after operation (default: 0)

        Returns:
            True if operation would stay within budget with required buffer

        Example:
            >>> enforcer = BudgetEnforcer(budget_limit=10.00)
            >>> enforcer.total_spent = 8.00
            >>> enforcer.can_proceed(1.50)  # $9.50 total, OK
            True
            >>> enforcer.can_proceed(2.50)  # $10.50 total, exceeds
            False
            >>> enforcer.can_proceed(1.50, require_buffer=1.00)  # $9.50 + $1 buffer = $10.50
            False
        """
        remaining_after = self.remaining() - estimated_cost
        return remaining_after >= require_buffer

    def pre_execution_check(
        self,
        operation_name: str,
        estimated_cost: float,
        require_buffer: float = 1.00
    ) -> Dict[str, Any]:
        """Perform pre-execution budget check with detailed result.

        Args:
            operation_name: Name of operation
            estimated_cost: Estimated cost in USD
            require_buffer: Minimum buffer to maintain (default: $1.00)

        Returns:
            Dict with:
                - allowed: bool (whether operation can proceed)
                - current_spent: float
                - budget_limit: float
                - remaining_before: float
                - remaining_after: float
                - buffer_after: float
                - recommendation: str
                - warnings: list of warning messages

        Example:
            >>> enforcer = BudgetEnforcer(budget_limit=15.00)
            >>> enforcer.total_spent = 5.80
            >>> result = enforcer.pre_execution_check('wave-2', 8.20)
            >>> result['allowed']
            True
            >>> result['buffer_after']
            1.0
        """
        remaining_before = self.remaining()
        remaining_after = remaining_before - estimated_cost
        buffer_after = remaining_after
        allowed = remaining_after >= require_buffer

        warnings = []
        if not allowed:
            warnings.append(
                f"Operation '{operation_name}' estimated ${estimated_cost:.2f} "
                f"would exceed budget by ${abs(remaining_after):.2f}"
            )
        elif buffer_after < require_buffer:
            warnings.append(
                f"Low buffer: ${buffer_after:.2f} remaining (< ${require_buffer:.2f} recommended)"
            )
        elif remaining_after < self.budget_limit * 0.2:
            warnings.append(
                f"Approaching budget limit: ${remaining_after:.2f} / ${self.budget_limit:.2f} remaining"
            )

        # Recommendation
        if not allowed:
            recommendation = 'abort'
        elif buffer_after < require_buffer:
            recommendation = 'warn'
        else:
            recommendation = 'proceed'

        return {
            'allowed': allowed,
            'current_spent': self.total_spent,
            'budget_limit': self.budget_limit,
            'remaining_before': remaining_before,
            'remaining_after': remaining_after,
            'buffer_after': buffer_after,
            'recommendation': recommendation,
            'warnings': warnings
        }

    def record_operation(
        self,
        operation_name: str,
        actual_cost: float,
        model: str = 'sonnet',
        tokens: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Record actual operation cost.

        Args:
            operation_name: Name of operation
            actual_cost: Actual cost in USD
            model: Model used
            tokens: Tokens consumed
            metadata: Optional additional metadata

        Example:
            >>> enforcer = BudgetEnforcer(budget_limit=10.00)
            >>> enforcer.record_operation(
            ...     'spec-analysis',
            ...     actual_cost=0.52,
            ...     model='sonnet',
            ...     tokens=5800
            ... )
            >>> enforcer.total_spent
            0.52
        """
        operation = {
            'name': operation_name,
            'cost': actual_cost,
            'model': model,
            'tokens': tokens,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }

        self.operations.append(operation)
        self.total_spent += actual_cost
        self._save_budget()

    def get_status(self) -> BudgetStatus:
        """Get current budget status with all details.

        Returns:
            BudgetStatus object with complete budget information

        Example:
            >>> enforcer = BudgetEnforcer(budget_limit=15.00)
            >>> enforcer.total_spent = 8.50
            >>> status = enforcer.get_status()
            >>> status.remaining
            6.5
            >>> status.within_budget
            True
        """
        remaining = self.remaining()
        within_budget = remaining >= 0

        warnings = []
        if not within_budget:
            warnings.append(f"Budget exceeded by ${abs(remaining):.2f}")
        elif remaining < self.budget_limit * 0.2:
            warnings.append(f"Approaching budget limit ({remaining/self.budget_limit*100:.0f}% remaining)")

        return BudgetStatus(
            budget_limit=self.budget_limit,
            total_spent=self.total_spent,
            remaining=remaining,
            operations=self.operations.copy(),
            within_budget=within_budget,
            warnings=warnings
        )

    def suggest_optimizations(
        self,
        estimated_cost: float,
        current_model: str = 'sonnet'
    ) -> List[str]:
        """Suggest cost optimizations if budget is tight.

        Args:
            estimated_cost: Estimated cost of pending operation
            current_model: Current model being used

        Returns:
            List of optimization suggestions

        Example:
            >>> enforcer = BudgetEnforcer(budget_limit=10.00)
            >>> enforcer.total_spent = 9.00
            >>> suggestions = enforcer.suggest_optimizations(2.00, 'sonnet')
            >>> suggestions
            ['Operation would exceed budget by $1.00',
             'Consider using haiku model (saves ~80%)',
             'Increase budget limit to $12.00']
        """
        suggestions = []
        remaining = self.remaining()

        # Check if operation would exceed budget
        if estimated_cost > remaining:
            exceed_by = estimated_cost - remaining
            suggestions.append(f"Operation would exceed budget by ${exceed_by:.2f}")

            # Suggest cheaper model
            if current_model == 'sonnet':
                haiku_cost = estimated_cost * (0.001 / 0.009)  # haiku is ~11% of sonnet cost
                if haiku_cost <= remaining:
                    suggestions.append(
                        f"Consider using haiku model (saves ~80%, estimated ${haiku_cost:.2f})"
                    )

            # Suggest budget increase
            min_budget = self.total_spent + estimated_cost
            suggestions.append(f"Increase budget limit to ${min_budget:.2f}")

        # Warn about low remaining budget
        elif remaining < estimated_cost * 1.5:
            suggestions.append(
                f"Low budget buffer: ${remaining:.2f} remaining, operation costs ${estimated_cost:.2f}"
            )
            suggestions.append("Consider increasing budget for future operations")

        return suggestions

    def get_spending_summary(self) -> Dict[str, Any]:
        """Get summary of spending by operation type and model.

        Returns:
            Dict with spending breakdown by operation and model

        Example:
            >>> enforcer = BudgetEnforcer()
            >>> summary = enforcer.get_spending_summary()
            >>> summary['by_operation']['spec-analysis']
            1.52
            >>> summary['by_model']['haiku']
            0.35
        """
        by_operation = {}
        by_model = {}
        total_tokens = 0

        for op in self.operations:
            name = op['name']
            cost = op['cost']
            model = op.get('model', 'unknown')
            tokens = op.get('tokens', 0)

            by_operation[name] = by_operation.get(name, 0.0) + cost
            by_model[model] = by_model.get(model, 0.0) + cost
            total_tokens += tokens

        return {
            'total_spent': self.total_spent,
            'budget_limit': self.budget_limit,
            'remaining': self.remaining(),
            'operation_count': len(self.operations),
            'by_operation': by_operation,
            'by_model': by_model,
            'total_tokens': total_tokens
        }
