"""Shannon core application logic - algorithms and orchestration."""

from shannon.core.session_manager import ISessionStore, SessionManager, get_session

__all__ = ['ISessionStore', 'SessionManager', 'get_session']
