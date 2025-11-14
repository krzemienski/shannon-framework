"""
Shannon V3.1 - Complete Interactive Dashboard

True 4-layer interactive TUI with:
- Layer 1: Session overview (goals, waves, progress)
- Layer 2: Agent list with selection (multi-agent waves)
- Layer 3: Agent detail (context, tools, operation)
- Layer 4: Message stream (USER/ASSISTANT/TOOL with scrolling)

Full keyboard navigation with htop/k9s-level interactivity.

Created: 2025-11-14
Version: 3.1.0
"""

from .models import (
    DashboardSnapshot,
    SessionSnapshot,
    AgentSnapshot,
    ContextSnapshot,
    MessageHistory,
    MessageEntry,
    MCPServerInfo,
    KeyEvent,
    DashboardUIState
)

from .data_provider import DashboardDataProvider
from .dashboard import InteractiveDashboard

__all__ = [
    # Data models
    'DashboardSnapshot',
    'SessionSnapshot',
    'AgentSnapshot',
    'ContextSnapshot',
    'MessageHistory',
    'MessageEntry',
    'MCPServerInfo',
    'KeyEvent',
    'DashboardUIState',

    # Components
    'DashboardDataProvider',
    'InteractiveDashboard'
]

__version__ = '3.1.0'
