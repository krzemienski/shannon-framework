"""
Shannon WebSocket Server

Handles real-time communication between Shannon backend and dashboard.
Includes HALT/RESUME/ROLLBACK control handlers.
"""
import socketio
import asyncio
from typing import Dict, Any, Optional, Callable
from orchestration.decision_engine import DecisionEngine

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=False,
    engineio_logger=False
)

# Global decision engine instance (shared across connections)
decision_engine = DecisionEngine()

# Global orchestrator instance (set by server initialization)
orchestrator = None

# Event handlers registry
event_handlers: Dict[str, Callable] = {}


def set_orchestrator(orch):
    """Set the global orchestrator instance"""
    global orchestrator
    orchestrator = orch


@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    print(f"[WebSocket] Client connected: {sid}")
    await sio.emit('connection_status', {'status': 'connected', 'sid': sid}, room=sid)


@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    print(f"[WebSocket] Client disconnected: {sid}")


@sio.event
async def approve_decision(sid, data: Dict[str, Any]):
    """
    Handle decision approval from dashboard.

    Expected data:
    {
        "decision_id": "uuid-here",
        "selected_option_id": "option-id"
    }

    Emits:
    - decision:approved - Confirmation to dashboard
    - execution:resumed - Execution continues
    """
    try:
        decision_id = data.get('decision_id')
        selected_option_id = data.get('selected_option_id')

        if not decision_id or not selected_option_id:
            await sio.emit('error', {
                'message': 'Missing decision_id or selected_option_id',
                'code': 'INVALID_REQUEST'
            }, room=sid)
            return

        # Approve the decision
        decision = await decision_engine.approve_decision(
            decision_id=decision_id,
            selected_option_id=selected_option_id,
            approved_by=f"dashboard-{sid}"
        )

        # Emit confirmation to dashboard
        await sio.emit('decision:approved', {
            'decision_id': decision.id,
            'selected_option': selected_option_id,
            'question': decision.question,
            'status': decision.status,
            'timestamp': decision.approved_at.isoformat() if decision.approved_at else None
        }, room=sid)

        # Notify execution can resume
        await sio.emit('execution:resumed', {
            'reason': 'decision_approved',
            'decision_id': decision_id
        })

        print(f"[WebSocket] Decision approved: {decision_id} -> {selected_option_id}")

    except ValueError as e:
        await sio.emit('error', {
            'message': str(e),
            'code': 'DECISION_ERROR'
        }, room=sid)
    except Exception as e:
        await sio.emit('error', {
            'message': f"Failed to approve decision: {str(e)}",
            'code': 'INTERNAL_ERROR'
        }, room=sid)


@sio.event
async def request_pending_decisions(sid, data: Dict[str, Any] = None):
    """
    Handle request for pending decisions list.

    Emits:
    - decisions:pending - List of all pending decisions
    """
    try:
        pending = decision_engine.get_pending_decisions()

        await sio.emit('decisions:pending', {
            'decisions': [
                {
                    'id': d.id,
                    'question': d.question,
                    'options': [
                        {
                            'id': opt.id,
                            'label': opt.label,
                            'description': opt.description,
                            'confidence': opt.confidence,
                            'pros': opt.pros,
                            'cons': opt.cons
                        }
                        for opt in d.options
                    ],
                    'status': d.status,
                    'context': d.context,
                    'created_at': d.created_at.isoformat()
                }
                for d in pending
            ],
            'count': len(pending)
        }, room=sid)

    except Exception as e:
        await sio.emit('error', {
            'message': f"Failed to get pending decisions: {str(e)}",
            'code': 'INTERNAL_ERROR'
        }, room=sid)


async def emit_decision_request(decision_id: str):
    """
    Emit a decision request to all connected clients.

    Called by orchestrator when a decision is needed.
    """
    decision = decision_engine.get_decision(decision_id)
    if not decision:
        return

    await sio.emit('decision:requested', {
        'id': decision.id,
        'question': decision.question,
        'options': [
            {
                'id': opt.id,
                'label': opt.label,
                'description': opt.description,
                'confidence': opt.confidence,
                'pros': opt.pros,
                'cons': opt.cons
            }
            for opt in decision.options
        ],
        'status': decision.status,
        'context': decision.context,
        'created_at': decision.created_at.isoformat()
    })


# ============================================================================
# CONTROL HANDLERS - HALT/RESUME/ROLLBACK
# ============================================================================

@sio.event
async def halt_execution(sid, data: Dict[str, Any] = None):
    """
    Handle HALT command - pause execution.

    Emits:
    - execution:halted - Confirmation of halt
    """
    try:
        if not orchestrator:
            await sio.emit('error', {
                'message': 'Orchestrator not initialized',
                'code': 'NO_ORCHESTRATOR'
            }, room=sid)
            return

        result = orchestrator.halt()

        await sio.emit('execution:halted', {
            'success': True,
            'result': result,
            'halt_response_time_ms': result.get('halt_response_time_ms')
        }, room=sid)

        # Broadcast status update
        await broadcast_status()

        print(f"[WebSocket] Execution halted by {sid}")

    except Exception as e:
        await sio.emit('error', {
            'message': f"Failed to halt execution: {str(e)}",
            'code': 'HALT_ERROR'
        }, room=sid)


@sio.event
async def resume_execution(sid, data: Dict[str, Any] = None):
    """
    Handle RESUME command - continue execution.

    Emits:
    - execution:resumed - Confirmation of resume
    """
    try:
        if not orchestrator:
            await sio.emit('error', {
                'message': 'Orchestrator not initialized',
                'code': 'NO_ORCHESTRATOR'
            }, room=sid)
            return

        result = await orchestrator.resume()

        await sio.emit('execution:resumed', {
            'success': True,
            'result': result,
            'reason': 'manual_resume'
        }, room=sid)

        # Broadcast status update
        await broadcast_status()

        print(f"[WebSocket] Execution resumed by {sid}")

    except ValueError as e:
        await sio.emit('error', {
            'message': str(e),
            'code': 'RESUME_ERROR'
        }, room=sid)
    except Exception as e:
        await sio.emit('error', {
            'message': f"Failed to resume execution: {str(e)}",
            'code': 'RESUME_ERROR'
        }, room=sid)


@sio.event
async def rollback_execution(sid, data: Dict[str, Any]):
    """
    Handle ROLLBACK command - revert N steps.

    Expected data:
    {
        "steps": 1  // Number of steps to rollback
    }

    Emits:
    - execution:rolled_back - Confirmation of rollback
    """
    try:
        if not orchestrator:
            await sio.emit('error', {
                'message': 'Orchestrator not initialized',
                'code': 'NO_ORCHESTRATOR'
            }, room=sid)
            return

        steps = data.get('steps', 1)

        result = orchestrator.rollback(steps)

        await sio.emit('execution:rolled_back', {
            'success': True,
            'result': result,
            'steps': steps
        }, room=sid)

        # Broadcast status update
        await broadcast_status()

        print(f"[WebSocket] Execution rolled back {steps} steps by {sid}")

    except ValueError as e:
        await sio.emit('error', {
            'message': str(e),
            'code': 'ROLLBACK_ERROR'
        }, room=sid)
    except Exception as e:
        await sio.emit('error', {
            'message': f"Failed to rollback execution: {str(e)}",
            'code': 'ROLLBACK_ERROR'
        }, room=sid)


@sio.event
async def get_execution_status(sid, data: Dict[str, Any] = None):
    """
    Handle GET_STATUS command - get current orchestrator status.

    Emits:
    - execution:status - Current status
    """
    try:
        if not orchestrator:
            await sio.emit('error', {
                'message': 'Orchestrator not initialized',
                'code': 'NO_ORCHESTRATOR'
            }, room=sid)
            return

        status = orchestrator.get_status()

        await sio.emit('execution:status', {
            'success': True,
            'status': status
        }, room=sid)

    except Exception as e:
        await sio.emit('error', {
            'message': f"Failed to get status: {str(e)}",
            'code': 'STATUS_ERROR'
        }, room=sid)


async def broadcast_status():
    """Broadcast status update to all connected clients"""
    if not orchestrator:
        return

    try:
        status = orchestrator.get_status()
        await sio.emit('execution:status_update', {
            'status': status
        })
    except Exception as e:
        print(f"[WebSocket] Error broadcasting status: {e}")


# ASGI application
app = socketio.ASGIApp(sio)


# Utility function for testing
def get_decision_engine() -> DecisionEngine:
    """Get the global decision engine instance"""
    return decision_engine
