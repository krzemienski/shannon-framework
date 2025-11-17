"""Shannon Dashboard Server - FastAPI Application.

This module provides the FastAPI application with RESTful endpoints
and Socket.IO integration for the Shannon v4.0 dashboard.

Endpoints:
- GET /health: Server health check
- GET /api/skills: List all registered skills
- GET /api/skills/{name}: Get skill details
- GET /api/sessions: List active execution sessions
- GET /api/sessions/{session_id}: Get session details
- POST /api/sessions: Create new execution session

Socket.IO:
- Mounted at /socket.io for WebSocket communication
- See websocket.py for event handlers
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import socketio

from shannon.skills.registry import SkillRegistry, SkillNotFoundError
from shannon.skills.models import Skill

logger = logging.getLogger(__name__)

# FastAPI application
app = FastAPI(
    title="Shannon Dashboard Server",
    version="4.0.0",
    description="WebSocket communication layer for Shannon Framework dashboard",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for development (React on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.IO server instance
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=False,
    engineio_logger=False,
    ping_timeout=60,
    ping_interval=25
)

# ASGI application combining FastAPI and Socket.IO
socket_app = socketio.ASGIApp(sio, app)

# Global state for active sessions
active_sessions: Dict[str, Dict[str, Any]] = {}
session_lock = asyncio.Lock()


@app.on_event("startup")
async def startup_event():
    """Initialize server on startup."""
    logger.info("Shannon Dashboard Server v4.0.0 starting...")

    # Import websocket handlers to register them
    try:
        from shannon.server import websocket
        logger.info("Socket.IO handlers registered")
    except ImportError as e:
        logger.warning(f"Failed to import websocket handlers: {e}")

    logger.info("Server startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on server shutdown."""
    logger.info("Shannon Dashboard Server shutting down...")

    # Notify all connected clients
    try:
        await sio.emit('server:shutdown', {'message': 'Server is shutting down'})
        # Note: Connections close automatically on server shutdown
        # sio.disconnect() requires sid parameter - not needed here
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

    logger.info("Server shutdown complete")


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.

    Returns:
        Server health status, version, and uptime
    """
    return {
        "status": "healthy",
        "version": "4.0.0",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(active_sessions),
        "connected_clients": len(sio.manager.rooms.get('/', {}).get('', set()))
    }


@app.get("/api/skills")
async def list_skills(
    category: Optional[str] = Query(None, description="Filter by category"),
    domain: Optional[str] = Query(None, description="Filter by domain"),
    tag: Optional[str] = Query(None, description="Filter by tag")
) -> Dict[str, Any]:
    """
    List all registered skills with optional filtering.

    Args:
        category: Filter by skill category
        domain: Filter by domain (e.g., "iOS", "Testing")
        tag: Filter by tag

    Returns:
        List of skills with metadata
    """
    try:
        # Get registry instance
        schema_path = Path(__file__).parent.parent / "skills" / "schemas" / "skill.schema.json"

        # Try to get existing instance or create new one
        try:
            registry = await SkillRegistry.get_instance()
        except ValueError:
            # First initialization
            if not schema_path.exists():
                return {
                    "skills": [],
                    "total": 0,
                    "message": "Skills registry not initialized (schema not found)"
                }
            registry = await SkillRegistry.get_instance(schema_path)

        # Apply filters
        if category:
            skills = registry.find_by_category(category)
        elif domain:
            skills = registry.find_for_domain(domain)
        elif tag:
            skills = registry.find_by_tag(tag)
        else:
            skills = registry.list_all()

        # Serialize skills
        skills_data = [
            {
                "name": skill.name,
                "version": skill.version,
                "description": skill.description,
                "category": skill.category,
                "domains": skill.domains,
                "tags": skill.tags,
                "execution_type": skill.execution_type.value,
                "parameters": [p.to_dict() for p in skill.parameters],
                "dependencies": skill.dependencies,
                "metadata": skill.metadata
            }
            for skill in skills
        ]

        return {
            "skills": skills_data,
            "total": len(skills_data),
            "filters": {
                "category": category,
                "domain": domain,
                "tag": tag
            }
        }

    except Exception as e:
        logger.error(f"Error listing skills: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list skills: {str(e)}")


@app.get("/api/skills/{skill_name}")
async def get_skill_details(skill_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific skill.

    Args:
        skill_name: Name of the skill

    Returns:
        Detailed skill information
    """
    try:
        # Get registry instance
        try:
            registry = await SkillRegistry.get_instance()
        except ValueError:
            raise HTTPException(
                status_code=503,
                detail="Skills registry not initialized"
            )

        # Get skill
        skill = registry.get(skill_name)
        if not skill:
            raise HTTPException(
                status_code=404,
                detail=f"Skill not found: {skill_name}"
            )

        # Serialize with full details
        return {
            "name": skill.name,
            "version": skill.version,
            "description": skill.description,
            "category": skill.category,
            "domains": skill.domains,
            "tags": skill.tags,
            "execution_type": skill.execution_type.value,
            "execution_config": skill.execution_config,
            "parameters": [p.to_dict() for p in skill.parameters],
            "dependencies": skill.dependencies,
            "hooks": skill.hooks.to_dict() if skill.hooks else None,
            "timeout": skill.timeout,
            "retry": skill.retry,
            "metadata": skill.metadata
        }

    except SkillNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Skill not found: {skill_name}"
        )
    except Exception as e:
        logger.error(f"Error getting skill details: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get skill details: {str(e)}"
        )


@app.get("/api/sessions")
async def list_sessions() -> Dict[str, Any]:
    """
    List all active execution sessions.

    Returns:
        List of active sessions with basic info
    """
    async with session_lock:
        sessions_data = [
            {
                "session_id": session_id,
                "created_at": data.get("created_at"),
                "status": data.get("status"),
                "current_skill": data.get("current_skill"),
                "progress": data.get("progress", 0)
            }
            for session_id, data in active_sessions.items()
        ]

        return {
            "sessions": sessions_data,
            "total": len(sessions_data)
        }


@app.get("/api/sessions/{session_id}")
async def get_session_details(session_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific session.

    Args:
        session_id: Unique session identifier

    Returns:
        Detailed session information
    """
    async with session_lock:
        if session_id not in active_sessions:
            raise HTTPException(
                status_code=404,
                detail=f"Session not found: {session_id}"
            )

        return active_sessions[session_id]


@app.post("/api/sessions")
async def create_session(session_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new execution session.

    Args:
        session_data: Session configuration

    Returns:
        Created session information
    """
    session_id = session_data.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=400,
            detail="session_id is required"
        )

    async with session_lock:
        if session_id in active_sessions:
            raise HTTPException(
                status_code=409,
                detail=f"Session already exists: {session_id}"
            )

        # Create session entry
        active_sessions[session_id] = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "status": "created",
            "skills": session_data.get("skills", []),
            "metadata": session_data.get("metadata", {}),
            "progress": 0,
            "current_skill": None
        }

        # Emit session created event
        await sio.emit('session:created', {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        })

        return active_sessions[session_id]


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str) -> Dict[str, str]:
    """
    Delete an execution session.

    Args:
        session_id: Session to delete

    Returns:
        Confirmation message
    """
    async with session_lock:
        if session_id not in active_sessions:
            raise HTTPException(
                status_code=404,
                detail=f"Session not found: {session_id}"
            )

        del active_sessions[session_id]

        # Emit session deleted event
        await sio.emit('session:deleted', {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        })

        return {"message": f"Session {session_id} deleted"}


# Helper function for session management
async def update_session(session_id: str, updates: Dict[str, Any]) -> None:
    """
    Update session state.

    Args:
        session_id: Session to update
        updates: Fields to update
    """
    async with session_lock:
        if session_id in active_sessions:
            active_sessions[session_id].update(updates)
            active_sessions[session_id]["updated_at"] = datetime.now().isoformat()


# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


# Import websocket handlers to register Socket.IO events
# Must be done AFTER all app.py definitions are complete (circular dependency resolution)
from shannon.server import websocket
logger.info("Socket.IO handlers registered")


# Server entry point
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "shannon.server.app:socket_app",  # ASGI app with FastAPI + Socket.IO
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False  # Critical: Disable reload for stability
    )
