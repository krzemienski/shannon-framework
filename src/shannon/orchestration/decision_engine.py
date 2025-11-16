"""Decision Engine for Shannon Framework.

Manages decision points during execution with options for:
- REDIRECT: Change execution path
- INJECT: Add tasks or context
- APPROVE: Continue as planned
- OVERRIDE: Manual intervention

Part of: Wave 8 - Full Dashboard
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio


class DecisionType(Enum):
    """Types of decisions."""
    REDIRECT = "redirect"
    INJECT = "inject"
    APPROVE = "approve"
    OVERRIDE = "override"
    SKIP = "skip"


class DecisionPriority(Enum):
    """Decision priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class DecisionOption:
    """An option for a decision."""
    option_id: str
    label: str
    description: str
    action: DecisionType
    consequences: List[str] = field(default_factory=list)
    recommended: bool = False


@dataclass
class DecisionPoint:
    """A point in execution requiring a decision."""
    decision_id: str
    title: str
    description: str
    context: Dict[str, Any]
    options: List[DecisionOption]
    priority: DecisionPriority = DecisionPriority.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    selected_option: Optional[str] = None
    auto_resolve_seconds: Optional[int] = None


@dataclass
class DecisionResponse:
    """Response to a decision."""
    decision_id: str
    selected_option_id: str
    reason: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


class DecisionEngine:
    """Engine for managing decision points.

    Features:
    - Present decisions with multiple options
    - Auto-resolution with timeout
    - Decision history tracking
    - Dashboard integration
    """

    def __init__(self):
        """Initialize decision engine."""
        self.pending_decisions: Dict[str, DecisionPoint] = {}
        self.resolved_decisions: Dict[str, DecisionPoint] = {}
        self.decision_history: List[DecisionPoint] = []

        # Decision callbacks
        self.decision_callbacks: Dict[str, asyncio.Future] = {}

    async def present_decision(
        self,
        title: str,
        description: str,
        options: List[DecisionOption],
        context: Optional[Dict[str, Any]] = None,
        priority: DecisionPriority = DecisionPriority.MEDIUM,
        auto_resolve_seconds: Optional[int] = None
    ) -> str:
        """Present a decision point.

        Args:
            title: Decision title
            description: Decision description
            options: Available options
            context: Additional context
            priority: Decision priority
            auto_resolve_seconds: Auto-resolve timeout

        Returns:
            Decision ID
        """
        decision_id = f"decision_{len(self.decision_history) + 1}"

        decision = DecisionPoint(
            decision_id=decision_id,
            title=title,
            description=description,
            context=context or {},
            options=options,
            priority=priority,
            auto_resolve_seconds=auto_resolve_seconds
        )

        self.pending_decisions[decision_id] = decision
        self.decision_history.append(decision)

        # Create future for response
        future = asyncio.Future()
        self.decision_callbacks[decision_id] = future

        # Set up auto-resolution if specified
        if auto_resolve_seconds:
            asyncio.create_task(
                self._auto_resolve_after_timeout(decision_id, auto_resolve_seconds)
            )

        return decision_id

    async def wait_for_decision(self, decision_id: str) -> DecisionResponse:
        """Wait for a decision to be resolved.

        Args:
            decision_id: Decision identifier

        Returns:
            Decision response
        """
        if decision_id not in self.decision_callbacks:
            raise ValueError(f"No decision found: {decision_id}")

        future = self.decision_callbacks[decision_id]
        response = await future

        return response

    async def resolve_decision(
        self,
        decision_id: str,
        selected_option_id: str,
        reason: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None
    ):
        """Resolve a decision.

        Args:
            decision_id: Decision identifier
            selected_option_id: Selected option
            reason: Optional reason for selection
            additional_data: Additional data
        """
        if decision_id not in self.pending_decisions:
            raise ValueError(f"No pending decision: {decision_id}")

        decision = self.pending_decisions[decision_id]

        # Validate option exists
        valid_options = {opt.option_id for opt in decision.options}
        if selected_option_id not in valid_options:
            raise ValueError(f"Invalid option: {selected_option_id}")

        # Mark as resolved
        decision.resolved_at = datetime.now()
        decision.selected_option = selected_option_id

        # Move to resolved
        del self.pending_decisions[decision_id]
        self.resolved_decisions[decision_id] = decision

        # Create response
        response = DecisionResponse(
            decision_id=decision_id,
            selected_option_id=selected_option_id,
            reason=reason,
            additional_data=additional_data or {}
        )

        # Resolve future
        if decision_id in self.decision_callbacks:
            future = self.decision_callbacks[decision_id]
            if not future.done():
                future.set_result(response)
            del self.decision_callbacks[decision_id]

    async def _auto_resolve_after_timeout(
        self,
        decision_id: str,
        timeout_seconds: int
    ):
        """Auto-resolve decision after timeout.

        Args:
            decision_id: Decision identifier
            timeout_seconds: Timeout in seconds
        """
        await asyncio.sleep(timeout_seconds)

        # Check if still pending
        if decision_id in self.pending_decisions:
            decision = self.pending_decisions[decision_id]

            # Find recommended option or first option
            recommended = next(
                (opt for opt in decision.options if opt.recommended),
                decision.options[0] if decision.options else None
            )

            if recommended:
                await self.resolve_decision(
                    decision_id,
                    recommended.option_id,
                    reason="Auto-resolved after timeout"
                )

    def get_pending_decisions(self) -> List[DecisionPoint]:
        """Get all pending decisions.

        Returns:
            List of pending decisions
        """
        return list(self.pending_decisions.values())

    def get_resolved_decisions(self) -> List[DecisionPoint]:
        """Get all resolved decisions.

        Returns:
            List of resolved decisions
        """
        return list(self.resolved_decisions.values())

    def get_decision(self, decision_id: str) -> Optional[DecisionPoint]:
        """Get decision by ID.

        Args:
            decision_id: Decision identifier

        Returns:
            Decision or None
        """
        return (
            self.pending_decisions.get(decision_id) or
            self.resolved_decisions.get(decision_id)
        )

    def get_statistics(self) -> Dict[str, Any]:
        """Get decision statistics.

        Returns:
            Statistics dictionary
        """
        total_decisions = len(self.decision_history)
        pending_count = len(self.pending_decisions)
        resolved_count = len(self.resolved_decisions)

        # Count by type
        decision_types = {}
        for decision in self.decision_history:
            if decision.selected_option:
                selected = next(
                    (opt for opt in decision.options if opt.option_id == decision.selected_option),
                    None
                )
                if selected:
                    action_type = selected.action.value
                    decision_types[action_type] = decision_types.get(action_type, 0) + 1

        return {
            'total_decisions': total_decisions,
            'pending': pending_count,
            'resolved': resolved_count,
            'by_type': decision_types
        }


# Convenience functions for common decision types
async def create_redirect_decision(
    engine: DecisionEngine,
    current_path: str,
    alternative_paths: List[str],
    reason: str
) -> str:
    """Create a REDIRECT decision.

    Args:
        engine: Decision engine
        current_path: Current execution path
        alternative_paths: Alternative paths
        reason: Reason for redirect

    Returns:
        Decision ID
    """
    options = [
        DecisionOption(
            option_id="continue",
            label="Continue Current Path",
            description=f"Continue with: {current_path}",
            action=DecisionType.APPROVE,
            recommended=True
        )
    ]

    for i, path in enumerate(alternative_paths):
        options.append(
            DecisionOption(
                option_id=f"redirect_{i}",
                label=f"Redirect to {path}",
                description=f"Switch to: {path}",
                action=DecisionType.REDIRECT
            )
        )

    return await engine.present_decision(
        title="Execution Path Decision",
        description=reason,
        options=options,
        context={'current_path': current_path, 'alternatives': alternative_paths}
    )


async def create_inject_decision(
    engine: DecisionEngine,
    injection_point: str,
    suggested_content: str
) -> str:
    """Create an INJECT decision.

    Args:
        engine: Decision engine
        injection_point: Where to inject
        suggested_content: Content to inject

    Returns:
        Decision ID
    """
    options = [
        DecisionOption(
            option_id="approve",
            label="Approve Injection",
            description=f"Inject: {suggested_content}",
            action=DecisionType.INJECT,
            recommended=True
        ),
        DecisionOption(
            option_id="skip",
            label="Skip Injection",
            description="Continue without injection",
            action=DecisionType.SKIP
        )
    ]

    return await engine.present_decision(
        title="Content Injection Decision",
        description=f"Inject content at {injection_point}?",
        options=options,
        context={'injection_point': injection_point, 'content': suggested_content}
    )
