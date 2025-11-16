"""Tests for Shannon Dashboard Server WebSocket Integration.

This test suite validates:
- Connection/disconnection handling
- Event emission to clients
- Command processing (HALT, RESUME, ROLLBACK, etc.)
- Room-based session management
- Latency requirements (<50ms target)
- Error handling and edge cases

Run with: pytest tests/server/test_websocket.py -v
"""

import asyncio
import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
import time

# Mock socketio before import
import sys
from unittest.mock import MagicMock
sys.modules['socketio'] = MagicMock()

from shannon.server.websocket import (
    ConnectionManager,
    CommandType,
    ExecutionState,
    handle_halt_command,
    handle_resume_command,
    handle_rollback_command,
    handle_redirect_command,
    handle_decision_command,
    handle_inject_command,
    emit_skill_event,
    emit_file_event,
    emit_decision_event,
    conn_manager
)


@pytest.fixture
def reset_conn_manager():
    """Reset connection manager state before each test."""
    conn_manager.connections.clear()
    conn_manager.session_rooms.clear()
    conn_manager.execution_state = ExecutionState.RUNNING
    yield conn_manager


@pytest.fixture
def mock_sio():
    """Mock Socket.IO server."""
    mock = AsyncMock()
    mock.emit = AsyncMock()
    mock.enter_room = AsyncMock()
    mock.leave_room = AsyncMock()
    return mock


# ============================================================================
# Connection Management Tests
# ============================================================================

class TestConnectionManager:
    """Test ConnectionManager functionality."""

    @pytest.mark.asyncio
    async def test_add_connection_without_session(self, reset_conn_manager):
        """Test adding connection without session."""
        manager = reset_conn_manager

        await manager.add_connection("sid_123")

        assert "sid_123" in manager.connections
        assert manager.connections["sid_123"]["sid"] == "sid_123"
        assert manager.connections["sid_123"]["session_id"] is None

    @pytest.mark.asyncio
    async def test_add_connection_with_session(self, reset_conn_manager):
        """Test adding connection with session."""
        manager = reset_conn_manager

        # Mock sio.enter_room
        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.enter_room = AsyncMock()

            await manager.add_connection("sid_123", "session_abc")

            assert "sid_123" in manager.connections
            assert manager.connections["sid_123"]["session_id"] == "session_abc"
            assert "session_abc" in manager.session_rooms
            assert "sid_123" in manager.session_rooms["session_abc"]

            # Verify room join
            mock_sio.enter_room.assert_called_once_with("sid_123", "session_abc")

    @pytest.mark.asyncio
    async def test_remove_connection(self, reset_conn_manager):
        """Test removing connection."""
        manager = reset_conn_manager

        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.enter_room = AsyncMock()
            mock_sio.leave_room = AsyncMock()

            # Add connection
            await manager.add_connection("sid_123", "session_abc")
            assert "sid_123" in manager.connections

            # Remove connection
            await manager.remove_connection("sid_123")

            assert "sid_123" not in manager.connections
            assert "session_abc" not in manager.session_rooms

            # Verify room leave
            mock_sio.leave_room.assert_called_once_with("sid_123", "session_abc")

    @pytest.mark.asyncio
    async def test_multiple_connections_same_session(self, reset_conn_manager):
        """Test multiple connections to same session."""
        manager = reset_conn_manager

        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.enter_room = AsyncMock()

            await manager.add_connection("sid_1", "session_abc")
            await manager.add_connection("sid_2", "session_abc")
            await manager.add_connection("sid_3", "session_abc")

            assert len(manager.session_rooms["session_abc"]) == 3
            assert "sid_1" in manager.session_rooms["session_abc"]
            assert "sid_2" in manager.session_rooms["session_abc"]
            assert "sid_3" in manager.session_rooms["session_abc"]

    @pytest.mark.asyncio
    async def test_get_connection_count(self, reset_conn_manager):
        """Test connection count tracking."""
        manager = reset_conn_manager

        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.enter_room = AsyncMock()

            # Add connections
            await manager.add_connection("sid_1", "session_1")
            await manager.add_connection("sid_2", "session_1")
            await manager.add_connection("sid_3", "session_2")

            # Total count
            total = await manager.get_connection_count()
            assert total == 3

            # Session-specific counts
            session1_count = await manager.get_connection_count("session_1")
            assert session1_count == 2

            session2_count = await manager.get_connection_count("session_2")
            assert session2_count == 1

    @pytest.mark.asyncio
    async def test_track_metrics(self, reset_conn_manager):
        """Test event and command tracking."""
        manager = reset_conn_manager

        await manager.add_connection("sid_123")

        # Track events
        await manager.track_event("sid_123")
        await manager.track_event("sid_123")
        assert manager.connections["sid_123"]["events_sent"] == 2

        # Track commands
        await manager.track_command("sid_123")
        assert manager.connections["sid_123"]["commands_received"] == 1

    @pytest.mark.asyncio
    async def test_execution_state_management(self, reset_conn_manager):
        """Test execution state tracking."""
        manager = reset_conn_manager

        # Initial state
        state = await manager.get_execution_state()
        assert state == ExecutionState.RUNNING

        # Change state
        await manager.set_execution_state(ExecutionState.HALTED)
        state = await manager.get_execution_state()
        assert state == ExecutionState.HALTED


# ============================================================================
# Command Handler Tests
# ============================================================================

class TestCommandHandlers:
    """Test command processing functions."""

    @pytest.mark.asyncio
    async def test_halt_command(self, reset_conn_manager):
        """Test HALT command handling."""
        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.emit = AsyncMock()

            result = await handle_halt_command("sid_123", {
                'reason': 'Test halt'
            })

            assert result['success'] is True
            assert 'halted successfully' in result['message']

            # Verify execution state changed
            state = await conn_manager.get_execution_state()
            assert state == ExecutionState.HALTED

            # Verify event emitted
            mock_sio.emit.assert_called_once()
            call_args = mock_sio.emit.call_args
            assert call_args[0][0] == 'execution:halted'

    @pytest.mark.asyncio
    async def test_resume_command(self, reset_conn_manager):
        """Test RESUME command handling."""
        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.emit = AsyncMock()

            # First halt
            await conn_manager.set_execution_state(ExecutionState.HALTED)

            # Then resume
            result = await handle_resume_command("sid_123", {})

            assert result['success'] is True
            assert 'resumed successfully' in result['message']

            # Verify execution state changed
            state = await conn_manager.get_execution_state()
            assert state == ExecutionState.RUNNING

    @pytest.mark.asyncio
    async def test_resume_when_not_halted(self, reset_conn_manager):
        """Test RESUME fails when not halted."""
        result = await handle_resume_command("sid_123", {})

        assert result['success'] is False
        assert 'Cannot resume' in result['error']

    @pytest.mark.asyncio
    async def test_rollback_command(self, reset_conn_manager):
        """Test ROLLBACK command handling."""
        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.emit = AsyncMock()

            result = await handle_rollback_command("sid_123", {
                'steps': 3,
                'session_id': 'session_abc'
            })

            assert result['success'] is True
            assert result['steps'] == 3

            # Verify event emitted to correct room
            call_args = mock_sio.emit.call_args
            assert call_args[0][0] == 'execution:rollback'
            assert call_args[1]['room'] == 'session_abc'

    @pytest.mark.asyncio
    async def test_rollback_without_session_id(self, reset_conn_manager):
        """Test ROLLBACK fails without session_id."""
        result = await handle_rollback_command("sid_123", {'steps': 2})

        assert result['success'] is False
        assert 'session_id is required' in result['error']

    @pytest.mark.asyncio
    async def test_redirect_command(self, reset_conn_manager):
        """Test REDIRECT command handling."""
        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.emit = AsyncMock()

            result = await handle_redirect_command("sid_123", {
                'target_skill': 'validation_skill',
                'session_id': 'session_abc'
            })

            assert result['success'] is True
            assert result['target'] == 'validation_skill'

    @pytest.mark.asyncio
    async def test_redirect_without_target(self, reset_conn_manager):
        """Test REDIRECT fails without target."""
        result = await handle_redirect_command("sid_123", {})

        assert result['success'] is False
        assert 'target_skill or target_path is required' in result['error']

    @pytest.mark.asyncio
    async def test_decision_command(self, reset_conn_manager):
        """Test DECISION command handling."""
        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.emit = AsyncMock()

            result = await handle_decision_command("sid_123", {
                'decision_id': 'decision_001',
                'choice': 'option_A',
                'session_id': 'session_abc'
            })

            assert result['success'] is True
            assert result['decision_id'] == 'decision_001'
            assert result['choice'] == 'option_A'

    @pytest.mark.asyncio
    async def test_decision_missing_params(self, reset_conn_manager):
        """Test DECISION fails with missing params."""
        result = await handle_decision_command("sid_123", {
            'decision_id': 'decision_001'
            # Missing 'choice'
        })

        assert result['success'] is False
        assert 'choice are required' in result['error']

    @pytest.mark.asyncio
    async def test_inject_command(self, reset_conn_manager):
        """Test INJECT command handling."""
        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.emit = AsyncMock()

            result = await handle_inject_command("sid_123", {
                'skill_name': 'test_skill',
                'parameters': {'param1': 'value1'},
                'position': 'next',
                'session_id': 'session_abc'
            })

            assert result['success'] is True
            assert result['skill_name'] == 'test_skill'
            assert result['position'] == 'next'

    @pytest.mark.asyncio
    async def test_inject_without_skill_name(self, reset_conn_manager):
        """Test INJECT fails without skill_name."""
        result = await handle_inject_command("sid_123", {
            'parameters': {}
        })

        assert result['success'] is False
        assert 'skill_name is required' in result['error']


# ============================================================================
# Event Emission Tests
# ============================================================================

class TestEventEmission:
    """Test event emission helpers."""

    @pytest.mark.asyncio
    async def test_emit_skill_event(self, mock_sio):
        """Test skill event emission."""
        with patch('shannon.server.websocket.sio', mock_sio):
            await emit_skill_event('skill:started', {
                'skill_name': 'test_skill',
                'parameters': {}
            })

            mock_sio.emit.assert_called_once()
            call_args = mock_sio.emit.call_args
            assert call_args[0][0] == 'skill:started'
            assert 'timestamp' in call_args[0][1]
            assert 'data' in call_args[0][1]

    @pytest.mark.asyncio
    async def test_emit_skill_event_with_session(self, mock_sio):
        """Test skill event emission to specific session."""
        with patch('shannon.server.websocket.sio', mock_sio):
            await emit_skill_event(
                'skill:completed',
                {'skill_name': 'test_skill'},
                session_id='session_abc'
            )

            call_args = mock_sio.emit.call_args
            assert call_args[1]['room'] == 'session_abc'

    @pytest.mark.asyncio
    async def test_emit_file_event(self, mock_sio):
        """Test file event emission."""
        with patch('shannon.server.websocket.sio', mock_sio):
            await emit_file_event('file:modified', {
                'path': '/path/to/file.py',
                'changes': 'Added function'
            })

            mock_sio.emit.assert_called_once()
            call_args = mock_sio.emit.call_args
            assert call_args[0][0] == 'file:modified'

    @pytest.mark.asyncio
    async def test_emit_decision_event(self, mock_sio):
        """Test decision event emission."""
        with patch('shannon.server.websocket.sio', mock_sio):
            await emit_decision_event('decision:point', {
                'decision_id': 'decision_001',
                'options': ['A', 'B', 'C']
            })

            mock_sio.emit.assert_called_once()
            call_args = mock_sio.emit.call_args
            assert call_args[0][0] == 'decision:point'


# ============================================================================
# Performance Tests
# ============================================================================

class TestPerformance:
    """Test performance and latency requirements."""

    @pytest.mark.asyncio
    async def test_event_emission_latency(self, mock_sio):
        """Test event emission latency (<50ms target)."""
        with patch('shannon.server.websocket.sio', mock_sio):
            start = time.perf_counter()

            await emit_skill_event('skill:started', {
                'skill_name': 'test_skill'
            })

            end = time.perf_counter()
            latency_ms = (end - start) * 1000

            # Target: <50ms
            assert latency_ms < 50, f"Latency {latency_ms:.2f}ms exceeds 50ms target"

    @pytest.mark.asyncio
    async def test_command_processing_latency(self, reset_conn_manager):
        """Test command processing latency (<50ms target)."""
        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.emit = AsyncMock()

            start = time.perf_counter()

            await handle_halt_command("sid_123", {
                'reason': 'Test'
            })

            end = time.perf_counter()
            latency_ms = (end - start) * 1000

            # Target: <50ms
            assert latency_ms < 50, f"Latency {latency_ms:.2f}ms exceeds 50ms target"

    @pytest.mark.asyncio
    async def test_connection_manager_performance(self, reset_conn_manager):
        """Test connection manager operations latency."""
        manager = reset_conn_manager

        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.enter_room = AsyncMock()

            start = time.perf_counter()

            # Add 100 connections
            for i in range(100):
                await manager.add_connection(f"sid_{i}", f"session_{i % 10}")

            end = time.perf_counter()
            latency_ms = (end - start) * 1000

            # Should handle 100 connections quickly
            assert latency_ms < 500, f"Adding 100 connections took {latency_ms:.2f}ms"

            # Verify all added
            total = await manager.get_connection_count()
            assert total == 100


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Test integrated workflows."""

    @pytest.mark.asyncio
    async def test_full_execution_cycle(self, reset_conn_manager):
        """Test complete execution cycle: start → halt → resume."""
        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.emit = AsyncMock()

            # 1. Start execution (default state)
            state = await conn_manager.get_execution_state()
            assert state == ExecutionState.RUNNING

            # 2. Halt execution
            result = await handle_halt_command("sid_123", {
                'reason': 'Test halt'
            })
            assert result['success'] is True

            state = await conn_manager.get_execution_state()
            assert state == ExecutionState.HALTED

            # 3. Resume execution
            result = await handle_resume_command("sid_123", {})
            assert result['success'] is True

            state = await conn_manager.get_execution_state()
            assert state == ExecutionState.RUNNING

    @pytest.mark.asyncio
    async def test_multi_client_session(self, reset_conn_manager):
        """Test multiple clients connecting to same session."""
        manager = reset_conn_manager

        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.enter_room = AsyncMock()
            mock_sio.emit = AsyncMock()

            # Add multiple connections to same session
            await manager.add_connection("sid_1", "session_abc")
            await manager.add_connection("sid_2", "session_abc")
            await manager.add_connection("sid_3", "session_abc")

            # Emit event to session
            await emit_skill_event(
                'skill:started',
                {'skill_name': 'test'},
                session_id='session_abc'
            )

            # Verify event sent to room (all clients will receive)
            call_args = mock_sio.emit.call_args
            assert call_args[1]['room'] == 'session_abc'


# ============================================================================
# Error Handling Tests
# ============================================================================

class TestErrorHandling:
    """Test error handling and edge cases."""

    @pytest.mark.asyncio
    async def test_remove_nonexistent_connection(self, reset_conn_manager):
        """Test removing connection that doesn't exist."""
        manager = reset_conn_manager

        # Should not raise error
        await manager.remove_connection("nonexistent_sid")

    @pytest.mark.asyncio
    async def test_command_with_exception(self, reset_conn_manager):
        """Test command handler with internal exception."""
        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.emit = AsyncMock(side_effect=Exception("Test error"))

            result = await handle_halt_command("sid_123", {})

            assert result['success'] is False
            assert 'error' in result

    @pytest.mark.asyncio
    async def test_concurrent_connections(self, reset_conn_manager):
        """Test concurrent connection management."""
        manager = reset_conn_manager

        with patch('shannon.server.websocket.sio') as mock_sio:
            mock_sio.enter_room = AsyncMock()

            # Add connections concurrently
            tasks = [
                manager.add_connection(f"sid_{i}", "session_abc")
                for i in range(20)
            ]
            await asyncio.gather(*tasks)

            # Verify all added without race conditions
            count = await manager.get_connection_count("session_abc")
            assert count == 20


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
