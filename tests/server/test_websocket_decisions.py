"""
Tests for WebSocket decision approval handler

Tests the approve_decision handler functionality.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from server.websocket import sio, decision_engine, approve_decision, get_decision_engine
from orchestration.decision_engine import DecisionOption


@pytest.fixture
async def mock_emit():
    """Mock socketio emit function"""
    original_emit = sio.emit
    sio.emit = AsyncMock()
    yield sio.emit
    sio.emit = original_emit


@pytest.fixture
def clean_decision_engine():
    """Clean decision engine before each test"""
    decision_engine.decisions = {}
    decision_engine.pending_decisions = {}
    yield decision_engine


class TestApproveDecisionHandler:
    """Test approve_decision WebSocket handler"""

    @pytest.mark.asyncio
    async def test_approve_decision_success(self, mock_emit, clean_decision_engine):
        """Test successful decision approval via WebSocket"""
        # Create a pending decision
        decision = await clean_decision_engine.request_decision(
            question="Test decision?",
            options=[
                DecisionOption(
                    id="opt1",
                    label="Option 1",
                    description="First option",
                    confidence=0.7
                ),
                DecisionOption(
                    id="opt2",
                    label="Option 2",
                    description="Second option",
                    confidence=0.8
                )
            ]
        )

        # Simulate WebSocket approval
        await approve_decision('test-sid', {
            'decision_id': decision.id,
            'selected_option_id': 'opt2'
        })

        # Verify emit was called with decision:approved
        assert mock_emit.called
        calls = [call for call in mock_emit.call_args_list if call[0][0] == 'decision:approved']
        assert len(calls) > 0

        # Verify decision was actually approved
        updated = clean_decision_engine.get_decision(decision.id)
        assert updated.status == "approved"
        assert updated.selected_option_id == "opt2"

    @pytest.mark.asyncio
    async def test_approve_decision_missing_id(self, mock_emit, clean_decision_engine):
        """Test approval with missing decision_id returns error"""
        await approve_decision('test-sid', {
            'selected_option_id': 'opt1'
        })

        # Verify error was emitted
        error_calls = [call for call in mock_emit.call_args_list if call[0][0] == 'error']
        assert len(error_calls) > 0

    @pytest.mark.asyncio
    async def test_approve_decision_nonexistent(self, mock_emit, clean_decision_engine):
        """Test approval of nonexistent decision returns error"""
        await approve_decision('test-sid', {
            'decision_id': 'nonexistent-id',
            'selected_option_id': 'opt1'
        })

        # Verify error was emitted
        error_calls = [call for call in mock_emit.call_args_list if call[0][0] == 'error']
        assert len(error_calls) > 0

    @pytest.mark.asyncio
    async def test_approve_decision_emits_resumed(self, mock_emit, clean_decision_engine):
        """Test that approval emits execution:resumed event"""
        # Create pending decision
        decision = await clean_decision_engine.request_decision(
            question="Resume test?",
            options=[
                DecisionOption(id="yes", label="Yes", description="Y", confidence=0.5)
            ]
        )

        # Approve it
        await approve_decision('test-sid', {
            'decision_id': decision.id,
            'selected_option_id': 'yes'
        })

        # Verify execution:resumed was emitted
        resumed_calls = [call for call in mock_emit.call_args_list if call[0][0] == 'execution:resumed']
        assert len(resumed_calls) > 0


class TestDecisionEngineIntegration:
    """Test that WebSocket uses the decision engine correctly"""

    def test_get_decision_engine_returns_instance(self):
        """Test that get_decision_engine returns DecisionEngine instance"""
        engine = get_decision_engine()
        assert engine is not None
        assert hasattr(engine, 'request_decision')
        assert hasattr(engine, 'approve_decision')
