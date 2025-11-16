"""Shannon Dashboard Server - WebSocket Communication Layer for v4.0.

This module provides the FastAPI-based server with Socket.IO integration
for real-time communication between Shannon orchestrator and the dashboard.

Key Features:
- Real-time event streaming (skill execution, file changes, decisions)
- Command reception from dashboard (HALT, RESUME, ROLLBACK, etc.)
- Room-based namespacing per execution session
- Low-latency communication (<50ms target)
- Connection management and authentication

Components:
- app.py: FastAPI application with CORS and health endpoints
- websocket.py: Socket.IO integration with event handlers
- events.py: Event emission helpers for orchestrator
- commands.py: Command processing logic
"""

from shannon.server.app import app, sio, socket_app
from shannon.server.websocket import (
    emit_skill_event,
    emit_file_event,
    emit_decision_event,
    emit_validation_event,
    emit_agent_event,
    emit_checkpoint_event,
    emit_execution_event,
    ConnectionManager
)

__all__ = [
    "app",
    "sio",
    "socket_app",
    "emit_skill_event",
    "emit_file_event",
    "emit_decision_event",
    "emit_validation_event",
    "emit_agent_event",
    "emit_checkpoint_event",
    "emit_execution_event",
    "ConnectionManager"
]
