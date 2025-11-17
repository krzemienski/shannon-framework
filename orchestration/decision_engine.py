"""
Decision Engine - Human-in-the-Loop Decision Making

Enables Shannon to request decisions from humans during execution.
Auto-approves high-confidence decisions (>= 0.95) to maintain flow.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid


@dataclass
class DecisionOption:
    """A single option in a decision"""
    id: str
    label: str
    description: str
    confidence: float  # 0.0 to 1.0
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Decision:
    """A decision point requiring human input (or auto-approved)"""
    id: str
    question: str
    options: List[DecisionOption]
    status: str  # "pending", "approved", "rejected"
    selected_option_id: Optional[str] = None
    auto_approved: bool = False
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    approved_at: Optional[datetime] = None
    approved_by: Optional[str] = None  # "auto" or user identifier


class DecisionEngine:
    """
    Manages decision points in Shannon execution.

    Features:
    - Request decisions with multiple options
    - Auto-approve high confidence decisions (>= 0.95)
    - Track pending decisions
    - Maintain decision history
    """

    AUTO_APPROVE_THRESHOLD = 0.95

    def __init__(self):
        self.decisions: Dict[str, Decision] = {}
        self.pending_decisions: Dict[str, Decision] = {}

    async def request_decision(
        self,
        question: str,
        options: List[DecisionOption],
        context: Optional[Dict[str, Any]] = None
    ) -> Decision:
        """
        Request a decision from the human operator.

        Auto-approves if any option has confidence >= 0.95.
        Otherwise, creates pending decision for human approval.

        Args:
            question: The decision question
            options: List of possible options
            context: Additional context for the decision

        Returns:
            Decision object (may be auto-approved or pending)
        """
        decision_id = str(uuid.uuid4())

        # Check for high-confidence option (auto-approve)
        highest_confidence_option = max(options, key=lambda opt: opt.confidence)

        if highest_confidence_option.confidence >= self.AUTO_APPROVE_THRESHOLD:
            # Auto-approve
            decision = Decision(
                id=decision_id,
                question=question,
                options=options,
                status="approved",
                selected_option_id=highest_confidence_option.id,
                auto_approved=True,
                context=context or {},
                approved_at=datetime.now(),
                approved_by="auto"
            )
        else:
            # Requires human approval
            decision = Decision(
                id=decision_id,
                question=question,
                options=options,
                status="pending",
                auto_approved=False,
                context=context or {}
            )
            self.pending_decisions[decision_id] = decision

        # Store in history
        self.decisions[decision_id] = decision

        return decision

    async def approve_decision(
        self,
        decision_id: str,
        selected_option_id: str,
        approved_by: str = "human"
    ) -> Decision:
        """
        Approve a pending decision by selecting an option.

        Args:
            decision_id: ID of the decision to approve
            selected_option_id: ID of the selected option
            approved_by: Identifier of who approved

        Returns:
            Updated Decision object

        Raises:
            ValueError: If decision not found or invalid option
        """
        if decision_id not in self.decisions:
            raise ValueError(f"Decision {decision_id} not found")

        decision = self.decisions[decision_id]

        # Validate option exists
        if not any(opt.id == selected_option_id for opt in decision.options):
            raise ValueError(f"Option {selected_option_id} not found in decision")

        # Update decision
        decision.status = "approved"
        decision.selected_option_id = selected_option_id
        decision.approved_at = datetime.now()
        decision.approved_by = approved_by

        # Remove from pending
        if decision_id in self.pending_decisions:
            del self.pending_decisions[decision_id]

        return decision

    def get_decision(self, decision_id: str) -> Optional[Decision]:
        """Get a decision by ID"""
        return self.decisions.get(decision_id)

    def get_pending_decisions(self) -> List[Decision]:
        """Get all pending decisions"""
        return list(self.pending_decisions.values())

    def get_decision_history(self) -> List[Decision]:
        """Get all decisions (pending and resolved)"""
        return list(self.decisions.values())

    def reject_decision(self, decision_id: str, reason: str = "") -> Decision:
        """
        Reject a decision (execution should halt or retry)

        Args:
            decision_id: ID of the decision to reject
            reason: Optional reason for rejection

        Returns:
            Updated Decision object
        """
        if decision_id not in self.decisions:
            raise ValueError(f"Decision {decision_id} not found")

        decision = self.decisions[decision_id]
        decision.status = "rejected"
        decision.context["rejection_reason"] = reason

        # Remove from pending
        if decision_id in self.pending_decisions:
            del self.pending_decisions[decision_id]

        return decision
