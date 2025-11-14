"""
Shannon Cache System - 3-tier caching for optimal performance.

Provides:
1. Analysis Cache - Context-aware spec analysis caching (7-day TTL)
2. Command Cache - Stable command result caching (30-day TTL)
3. MCP Cache - Domain-based MCP recommendation caching (indefinite)

All caches use SHA-256 hashing and atomic writes for safety.
"""

from .analysis_cache import AnalysisCache
from .command_cache import CommandCache
from .mcp_cache import MCPCache
from .manager import CacheManager

__all__ = [
    'AnalysisCache',
    'CommandCache',
    'MCPCache',
    'CacheManager',
]
