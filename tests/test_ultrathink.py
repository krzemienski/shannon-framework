"""Tests for Ultrathink mode - 500+ step reasoning.

GATE 5.1 Tests:
- Test 1: UltrathinkEngine generates 500+ thoughts
- Test 2: Thought count validation
"""

import pytest
import anyio
from shannon.modes.ultrathink import UltrathinkEngine, UltrathinkSession


class TestUltrathinkEngine:
    """Test UltrathinkEngine functionality."""

    @pytest.mark.asyncio
    async def test_engine_generates_500_plus_thoughts(self):
        """Test that UltrathinkEngine generates at least 500 thoughts.

        GATE 5.1 - Test 1/2
        """
        engine = UltrathinkEngine(min_thoughts=500)
        result = await engine.analyze("complex task requiring deep analysis")

        # Verify 500+ thoughts generated
        assert result['total_thoughts'] >= 500, (
            f"Expected at least 500 thoughts, got {result['total_thoughts']}"
        )

        # Verify result structure
        assert 'task' in result
        assert 'reasoning_chain' in result
        assert 'hypotheses' in result
        assert 'conclusion' in result
        assert 'duration_seconds' in result

        # Verify reasoning chain matches thought count
        assert len(result['reasoning_chain']) == result['total_thoughts']

    @pytest.mark.asyncio
    async def test_thought_count_accuracy(self):
        """Test that thought count is accurate and traceable.

        GATE 5.1 - Test 2/2
        """
        engine = UltrathinkEngine(min_thoughts=500)
        result = await engine.analyze("test task")

        # Verify thought count matches internal state
        assert len(engine.thoughts) == result['total_thoughts']
        assert len(engine.reasoning_steps) == result['total_thoughts']

        # Verify each thought has a corresponding reasoning step
        for i, step in enumerate(result['reasoning_chain']):
            assert step['step'] == i
            assert 'thought' in step
            assert 'type' in step
            assert 'confidence' in step

        # Verify minimum threshold met
        assert result['total_thoughts'] >= 500


class TestHypothesisEngine:
    """Test hypothesis generation and comparison.

    GATE 5.2 Tests
    """

    @pytest.mark.asyncio
    async def test_generate_hypotheses(self):
        """Test hypothesis generation from thoughts.

        GATE 5.2 - Test 1/3
        """
        engine = UltrathinkEngine(min_thoughts=500)
        result = await engine.analyze("generate hypotheses test")

        # Verify hypotheses were generated
        assert len(result['hypotheses']) > 0
        assert len(result['hypotheses']) <= 10  # Max 10 hypotheses

        # Verify hypothesis structure
        for hypothesis in result['hypotheses']:
            assert 'id' in hypothesis
            assert 'statement' in hypothesis
            assert 'confidence' in hypothesis
            assert 'status' in hypothesis

    @pytest.mark.asyncio
    async def test_compare_hypotheses(self):
        """Test hypothesis comparison logic.

        GATE 5.2 - Test 2/3
        """
        engine = UltrathinkEngine(min_thoughts=500)
        result = await engine.analyze("compare hypotheses test")

        hypotheses = result['hypotheses']

        if len(hypotheses) >= 2:
            # Verify different hypotheses have different confidence levels
            confidences = [h['confidence'] for h in hypotheses]
            # Should have some variation in confidence
            assert len(set(confidences)) > 1

    @pytest.mark.asyncio
    async def test_hypothesis_coherence(self):
        """Test that hypotheses are coherent and derived from thoughts.

        GATE 5.2 - Test 3/3
        """
        engine = UltrathinkEngine(min_thoughts=500)
        result = await engine.analyze("coherence test")

        # All hypotheses should contain the keyword "hypothesis"
        for hypothesis in result['hypotheses']:
            statement = hypothesis['statement'].lower()
            assert 'hypothesis' in statement or 'formulating' in statement


class TestUltrathinkSession:
    """Test UltrathinkSession wrapper."""

    @pytest.mark.asyncio
    async def test_session_reason(self):
        """Test session-based reasoning."""
        session = UltrathinkSession(session_id="test_session", max_steps=500)
        result = await session.reason("test query")

        assert result['total_steps'] >= 500
        assert result['hypotheses_generated'] > 0
        assert 'final_conclusion' in result
        assert 'duration_seconds' in result

        # Verify session state updated
        assert session.current_step == result['total_steps']
        assert len(session.reasoning_chain) == result['total_steps']
        assert len(session.hypotheses) == result['hypotheses_generated']

    @pytest.mark.asyncio
    async def test_session_info(self):
        """Test session info retrieval."""
        session = UltrathinkSession(
            session_id="info_test",
            max_steps=500,
            depth="ultra"
        )

        info = session.get_session_info()

        assert info['session_id'] == "info_test"
        assert info['max_steps'] == 500
        assert info['depth'] == "ultra"
        assert info['current_step'] == 0
        assert info['hypotheses'] == 0


# Run tests with: pytest tests/test_ultrathink.py -v
