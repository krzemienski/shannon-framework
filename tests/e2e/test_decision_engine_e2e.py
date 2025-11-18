"""
End-to-End Test for Decision Engine

Tests the complete decision flow:
1. Orchestrator creates decision
2. Decision appears in pending (if not auto-approved)
3. Human approves via WebSocket
4. Execution resumes
"""
import pytest
import asyncio
from orchestration.orchestrator import Orchestrator
from orchestration.decision_engine import DecisionOption
from server.websocket import get_decision_engine


class TestDecisionEngineE2E:
    """End-to-end decision engine tests"""

    @pytest.mark.asyncio
    async def test_auto_approve_high_confidence(self):
        """Test that high confidence decisions auto-approve"""
        orchestrator = Orchestrator()

        decision = await orchestrator._request_decision(
            question="Use standard HTTP library?",
            options=[
                DecisionOption(
                    id="requests",
                    label="Requests library",
                    description="Industry standard, well-tested",
                    confidence=0.98,  # Above 0.95 threshold
                    pros=["Widely used", "Well documented"],
                    cons=[]
                ),
                DecisionOption(
                    id="urllib",
                    label="urllib",
                    description="Built-in, but lower-level",
                    confidence=0.3,
                    pros=["Built-in"],
                    cons=["More complex API"]
                )
            ],
            context={"task": "API client implementation"}
        )

        # Verify auto-approved
        assert decision.auto_approved is True
        assert decision.status == "approved"
        assert decision.selected_option_id == "requests"

    @pytest.mark.asyncio
    async def test_pending_decision_requires_approval(self):
        """Test that low confidence decisions remain pending"""
        orchestrator = Orchestrator()

        decision = await orchestrator._request_decision(
            question="Which frontend framework?",
            options=[
                DecisionOption(
                    id="react",
                    label="React",
                    description="Popular but complex",
                    confidence=0.75,
                    pros=["Large ecosystem", "Component reuse"],
                    cons=["Steep learning curve"]
                ),
                DecisionOption(
                    id="vue",
                    label="Vue",
                    description="Simpler alternative",
                    confidence=0.70,
                    pros=["Easier to learn"],
                    cons=["Smaller ecosystem"]
                )
            ]
        )

        # Should be pending
        assert decision.auto_approved is False
        assert decision.status == "pending"
        assert decision.id in orchestrator.decision_engine.pending_decisions

    @pytest.mark.asyncio
    async def test_decision_approval_flow(self):
        """Test complete approval flow"""
        orchestrator = Orchestrator()

        # Create pending decision
        decision = await orchestrator._request_decision(
            question="Database choice?",
            options=[
                DecisionOption(
                    id="postgres",
                    label="PostgreSQL",
                    description="Relational database",
                    confidence=0.6,
                    pros=["ACID compliance", "Mature"],
                    cons=["More setup"]
                ),
                DecisionOption(
                    id="mongodb",
                    label="MongoDB",
                    description="Document database",
                    confidence=0.5,
                    pros=["Flexible schema"],
                    cons=["Less strict"]
                )
            ]
        )

        # Verify pending
        assert decision.status == "pending"

        # Simulate human approval
        await orchestrator.decision_engine.approve_decision(
            decision.id,
            selected_option_id="postgres",
            approved_by="human-test"
        )

        # Verify approved
        updated = orchestrator.decision_engine.get_decision(decision.id)
        assert updated.status == "approved"
        assert updated.selected_option_id == "postgres"
        assert updated.approved_by == "human-test"
        assert decision.id not in orchestrator.decision_engine.pending_decisions

    @pytest.mark.asyncio
    async def test_multiple_pending_decisions(self):
        """Test managing multiple pending decisions"""
        orchestrator = Orchestrator()

        # Create 3 pending decisions
        d1 = await orchestrator._request_decision(
            "Choice 1?",
            [DecisionOption(id="a", label="A", description="A", confidence=0.5)]
        )
        d2 = await orchestrator._request_decision(
            "Choice 2?",
            [DecisionOption(id="b", label="B", description="B", confidence=0.6)]
        )
        d3 = await orchestrator._request_decision(
            "Choice 3?",
            [DecisionOption(id="c", label="C", description="C", confidence=0.7)]
        )

        # Verify all pending
        pending = orchestrator.decision_engine.get_pending_decisions()
        assert len(pending) == 3
        assert d1.id in [d.id for d in pending]
        assert d2.id in [d.id for d in pending]
        assert d3.id in [d.id for d in pending]

        # Approve middle one
        await orchestrator.decision_engine.approve_decision(d2.id, "b")

        # Verify only 2 remain pending
        pending = orchestrator.decision_engine.get_pending_decisions()
        assert len(pending) == 2
        assert d2.id not in [d.id for d in pending]


class TestDecisionEngineMetrics:
    """Test decision engine metrics and reporting"""

    @pytest.mark.asyncio
    async def test_decision_history_tracking(self):
        """Test that all decisions are tracked in history"""
        orchestrator = Orchestrator()

        # Create mix of auto-approved and pending
        await orchestrator._request_decision(
            "Q1?",
            [DecisionOption(id="a", label="A", description="A", confidence=0.99)]
        )
        await orchestrator._request_decision(
            "Q2?",
            [DecisionOption(id="b", label="B", description="B", confidence=0.5)]
        )

        history = orchestrator.decision_engine.get_decision_history()
        assert len(history) == 2
        assert history[0].auto_approved is True
        assert history[1].auto_approved is False

    @pytest.mark.asyncio
    async def test_decision_context_preservation(self):
        """Test that decision context is preserved"""
        orchestrator = Orchestrator()

        decision = await orchestrator._request_decision(
            "Test?",
            [DecisionOption(id="x", label="X", description="X", confidence=0.5)],
            context={
                "task": "implement feature X",
                "complexity": 8.5,
                "dependencies": ["lib1", "lib2"]
            }
        )

        assert decision.context is not None
        assert decision.context["task"] == "implement feature X"
        assert decision.context["complexity"] == 8.5
        assert len(decision.context["dependencies"]) == 2


@pytest.mark.asyncio
async def test_full_orchestrator_decision_integration():
    """
    Complete integration test: Orchestrator uses decisions during execution
    """
    orchestrator = Orchestrator()

    # Test that orchestrator has decision engine
    assert orchestrator.decision_engine is not None

    # Test decision creation
    decision = await orchestrator._request_decision(
        "Proceed with implementation?",
        options=[
            DecisionOption(
                id="yes",
                label="Yes, proceed",
                description="Continue with current approach",
                confidence=0.85,
                pros=["Fast to implement"],
                cons=["May need refactoring later"]
            ),
            DecisionOption(
                id="no",
                label="No, reconsider",
                description="Take time to redesign",
                confidence=0.40,
                pros=["Better architecture"],
                cons=["Slower delivery"]
            )
        ]
    )

    # Should be pending (0.85 < 0.95)
    assert decision.status == "pending"

    # Get all pending decisions
    pending = orchestrator.decision_engine.get_pending_decisions()
    assert len(pending) == 1
    assert pending[0].question == "Proceed with implementation?"

    # Approve it
    await orchestrator.decision_engine.approve_decision(decision.id, "yes")

    # Verify no longer pending
    pending = orchestrator.decision_engine.get_pending_decisions()
    assert len(pending) == 0

    # Verify in history
    history = orchestrator.decision_engine.get_decision_history()
    assert len(history) == 1
    assert history[0].status == "approved"
    assert history[0].selected_option_id == "yes"
