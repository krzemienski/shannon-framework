"""
Tests for DecisionEngine - Human-in-the-Loop Decision Making

These tests define the behavior BEFORE implementation (TDD).
Run them and watch them FAIL, then implement until PASS.
"""
import pytest
from orchestration.decision_engine import DecisionEngine, Decision, DecisionOption


class TestDecisionEngineCore:
    """Test core decision request functionality"""

    @pytest.fixture
    def engine(self):
        """Create DecisionEngine instance"""
        return DecisionEngine()

    def test_engine_initialization(self, engine):
        """Verify DecisionEngine initializes correctly"""
        assert engine is not None
        assert hasattr(engine, 'request_decision')
        assert len(engine.pending_decisions) == 0

    @pytest.mark.asyncio
    async def test_request_decision_creates_decision_object(self, engine):
        """Test that request_decision creates a Decision with options"""
        decision = await engine.request_decision(
            question="Which implementation approach?",
            options=[
                DecisionOption(
                    id="opt1",
                    label="Approach A: Simple",
                    description="Quick implementation, less flexible",
                    confidence=0.7
                ),
                DecisionOption(
                    id="opt2",
                    label="Approach B: Complex",
                    description="More implementation work, very flexible",
                    confidence=0.6
                )
            ],
            context={"task": "implement auth"}
        )

        assert decision is not None
        assert decision.question == "Which implementation approach?"
        assert len(decision.options) == 2
        assert decision.status in ["pending", "approved"]

    @pytest.mark.asyncio
    async def test_auto_approve_high_confidence(self, engine):
        """Test auto-approval when confidence >= 0.95"""
        decision = await engine.request_decision(
            question="Use standard approach?",
            options=[
                DecisionOption(
                    id="standard",
                    label="Standard Pattern",
                    description="Well-tested approach",
                    confidence=0.96  # Above 0.95 threshold
                ),
                DecisionOption(
                    id="alternative",
                    label="Alternative",
                    description="Untested approach",
                    confidence=0.3
                )
            ]
        )

        # Should be auto-approved
        assert decision.status == "approved"
        assert decision.selected_option_id == "standard"
        assert decision.auto_approved is True

    @pytest.mark.asyncio
    async def test_no_auto_approve_low_confidence(self, engine):
        """Test that low confidence decisions require human approval"""
        decision = await engine.request_decision(
            question="Choose framework?",
            options=[
                DecisionOption(
                    id="react",
                    label="React",
                    description="Popular but complex",
                    confidence=0.7  # Below 0.95
                ),
                DecisionOption(
                    id="vue",
                    label="Vue",
                    description="Simpler learning curve",
                    confidence=0.8  # Below 0.95
                )
            ]
        )

        # Should remain pending
        assert decision.status == "pending"
        assert decision.auto_approved is False
        assert decision.id in engine.pending_decisions


class TestDecisionApproval:
    """Test human approval workflow"""

    @pytest.fixture
    def engine(self):
        return DecisionEngine()

    @pytest.mark.asyncio
    async def test_approve_decision_updates_status(self, engine):
        """Test that approving a decision updates its status"""
        # Create pending decision
        decision = await engine.request_decision(
            question="Which option?",
            options=[
                DecisionOption(id="a", label="A", description="Option A", confidence=0.5),
                DecisionOption(id="b", label="B", description="Option B", confidence=0.6)
            ]
        )

        # Approve it
        await engine.approve_decision(decision.id, selected_option_id="b")

        # Check status updated
        updated = engine.get_decision(decision.id)
        assert updated.status == "approved"
        assert updated.selected_option_id == "b"
        assert decision.id not in engine.pending_decisions

    @pytest.mark.asyncio
    async def test_approve_nonexistent_decision_raises_error(self, engine):
        """Test that approving non-existent decision raises error"""
        with pytest.raises(ValueError, match="Decision .* not found"):
            await engine.approve_decision("nonexistent-id", selected_option_id="opt1")


class TestDecisionRetrieval:
    """Test decision retrieval methods"""

    @pytest.fixture
    def engine(self):
        return DecisionEngine()

    @pytest.mark.asyncio
    async def test_get_pending_decisions(self, engine):
        """Test retrieving all pending decisions"""
        # Create 2 pending decisions
        d1 = await engine.request_decision(
            question="Q1?",
            options=[
                DecisionOption(id="a", label="A", description="A", confidence=0.5)
            ]
        )
        d2 = await engine.request_decision(
            question="Q2?",
            options=[
                DecisionOption(id="b", label="B", description="B", confidence=0.6)
            ]
        )

        pending = engine.get_pending_decisions()
        assert len(pending) == 2
        assert d1.id in [d.id for d in pending]
        assert d2.id in [d.id for d in pending]

    @pytest.mark.asyncio
    async def test_get_decision_history(self, engine):
        """Test retrieving decision history"""
        # Create and approve a decision
        decision = await engine.request_decision(
            question="Test?",
            options=[
                DecisionOption(id="yes", label="Yes", description="Y", confidence=0.5)
            ]
        )
        await engine.approve_decision(decision.id, selected_option_id="yes")

        history = engine.get_decision_history()
        assert len(history) == 1
        assert history[0].status == "approved"
