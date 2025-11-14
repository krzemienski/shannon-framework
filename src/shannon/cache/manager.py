"""
Cache Manager - Unified interface for all Shannon cache layers.

Provides centralized cache management with:
- Unified access to all cache types
- LRU eviction when size limit exceeded
- Aggregated statistics
- Cache warming
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

from .analysis_cache import AnalysisCache
from .command_cache import CommandCache
from .mcp_cache import MCPCache


class CacheManager:
    """
    Unified cache manager for Shannon CLI.

    Manages three cache layers:
    1. Analysis cache (7-day TTL, context-aware)
    2. Command cache (30-day TTL, version-based)
    3. MCP cache (indefinite, deterministic)

    Enforces global size limit with LRU eviction.
    """

    # Global cache size limit (500 MB)
    MAX_CACHE_SIZE_MB = 500

    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize cache manager.

        Args:
            base_dir: Base cache directory (default: ~/.shannon/cache)
        """
        self.base_dir = base_dir or (Path.home() / ".shannon" / "cache")
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # Initialize cache layers
        self.analysis = AnalysisCache(self.base_dir / "analyses")
        self.command = CommandCache(self.base_dir / "commands")
        self.mcp = MCPCache(self.base_dir / "mcps")

        # Manager stats
        self.stats_file = self.base_dir / "manager_stats.json"
        self.stats = self._load_stats()

    def _load_stats(self) -> Dict[str, Any]:
        """Load manager statistics from disk."""
        if not self.stats_file.exists():
            return {
                "total_evictions": 0,
                "total_clears": 0,
                "last_eviction": None,
                "last_clear": None,
                "initialized_at": datetime.now().isoformat()
            }

        try:
            return json.loads(self.stats_file.read_text())
        except (json.JSONDecodeError, OSError):
            return self._load_stats.__defaults__[0]

    def _save_stats(self) -> None:
        """Save manager statistics to disk atomically."""
        temp_file = self.stats_file.with_suffix('.tmp')
        temp_file.write_text(json.dumps(self.stats, indent=2))
        temp_file.rename(self.stats_file)

    def get_total_size_mb(self) -> float:
        """
        Get total cache size across all layers.

        Returns:
            Total size in MB
        """
        return (
            self.analysis._get_cache_size_mb() +
            self.command._get_cache_size_mb() +
            self.mcp._get_cache_size_mb()
        )

    def check_size_limit(self) -> bool:
        """
        Check if cache size exceeds limit.

        Returns:
            True if over limit, False otherwise
        """
        return self.get_total_size_mb() > self.MAX_CACHE_SIZE_MB

    def evict_lru(self, target_mb: Optional[float] = None) -> int:
        """
        Evict least-recently-used cache entries until under target size.

        Uses LRU strategy across all cache layers based on file modification times.

        Args:
            target_mb: Target size in MB (default: MAX_CACHE_SIZE_MB * 0.8)

        Returns:
            Number of entries evicted
        """
        target = target_mb if target_mb is not None else (self.MAX_CACHE_SIZE_MB * 0.8)
        current_size = self.get_total_size_mb()

        if current_size <= target:
            return 0  # Already under target

        # Collect all cache files with modification times
        all_files = []

        for cache_dir in [self.analysis.cache_dir, self.command.cache_dir, self.mcp.cache_dir]:
            for cache_file in cache_dir.glob("*.json"):
                if cache_file.name == "stats.json":
                    continue

                all_files.append({
                    'path': cache_file,
                    'mtime': cache_file.stat().st_mtime,
                    'size_mb': cache_file.stat().st_size / (1024 * 1024)
                })

        # Sort by modification time (oldest first)
        all_files.sort(key=lambda x: x['mtime'])

        # Evict oldest until under target
        evicted_count = 0
        freed_mb = 0.0

        for file_info in all_files:
            if current_size - freed_mb <= target:
                break  # Reached target

            file_info['path'].unlink()
            evicted_count += 1
            freed_mb += file_info['size_mb']

        # Record eviction
        if evicted_count > 0:
            self.stats["total_evictions"] += evicted_count
            self.stats["last_eviction"] = datetime.now().isoformat()
            self._save_stats()

        return evicted_count

    def clear_all(self) -> Dict[str, int]:
        """
        Clear all caches.

        Returns:
            Dict with counts per cache type
        """
        counts = {
            'analysis': self.analysis.clear(),
            'command': self.command.clear(),
            'mcp': self.mcp.clear()
        }

        total = sum(counts.values())
        if total > 0:
            self.stats["total_clears"] += 1
            self.stats["last_clear"] = datetime.now().isoformat()
            self._save_stats()

        return counts

    def clear_expired(self) -> Dict[str, int]:
        """
        Clear only expired cache entries from all layers.

        Returns:
            Dict with eviction counts per cache type
        """
        counts = {
            'analysis': self.analysis.evict_old_entries(),
            'command': self.command.evict_old_entries(),
            'mcp': 0  # MCP cache has no TTL
        }

        return counts

    def get_stats(self) -> Dict[str, Any]:
        """
        Get aggregated statistics across all cache layers.

        Returns:
            Comprehensive stats dictionary
        """
        analysis_stats = self.analysis.get_stats()
        command_stats = self.command.get_stats()
        mcp_stats = self.mcp.get_stats()

        # Calculate totals
        total_hits = (
            analysis_stats['hits'] +
            command_stats['hits'] +
            mcp_stats['hits']
        )
        total_misses = (
            analysis_stats['misses'] +
            command_stats['misses'] +
            mcp_stats['misses']
        )
        total_requests = total_hits + total_misses
        overall_hit_rate = (total_hits / total_requests * 100) if total_requests > 0 else 0.0

        # Aggregate savings
        total_savings_usd = analysis_stats.get('total_savings_usd', 0.0)
        total_savings_seconds = command_stats.get('total_savings_seconds', 0.0)

        return {
            'overall': {
                'total_hits': total_hits,
                'total_misses': total_misses,
                'total_requests': total_requests,
                'hit_rate_percent': round(overall_hit_rate, 2),
                'total_size_mb': round(self.get_total_size_mb(), 2),
                'max_size_mb': self.MAX_CACHE_SIZE_MB,
                'utilization_percent': round(
                    (self.get_total_size_mb() / self.MAX_CACHE_SIZE_MB) * 100, 2
                ),
                'total_savings_usd': round(total_savings_usd, 2),
                'total_savings_minutes': round(total_savings_seconds / 60, 2)
            },
            'analysis': analysis_stats,
            'command': command_stats,
            'mcp': mcp_stats,
            'manager': self.stats
        }

    def warm_cache(self, common_operations: List[Dict[str, Any]]) -> int:
        """
        Pre-populate cache with common operations.

        Args:
            common_operations: List of operation specs to pre-cache:
                [
                    {'type': 'command', 'command': 'prime', 'version': '3.0.0'},
                    {'type': 'mcp', 'domains': {...}},
                    ...
                ]

        Returns:
            Number of entries warmed
        """
        warmed = 0

        for op in common_operations:
            try:
                if op['type'] == 'command':
                    # Check if already cached
                    result = self.command.get(
                        op['command'],
                        op.get('version', '3.0.0')
                    )
                    if result:
                        warmed += 1

                elif op['type'] == 'mcp':
                    # Check if already cached
                    result = self.mcp.get(op['domains'])
                    if result:
                        warmed += 1

            except Exception:
                # Skip failed warming attempts
                continue

        return warmed

    def health_check(self) -> Dict[str, Any]:
        """
        Check cache system health.

        Returns:
            Health status with warnings/issues
        """
        issues = []
        warnings = []

        # Check size
        current_size = self.get_total_size_mb()
        if current_size > self.MAX_CACHE_SIZE_MB:
            issues.append(f"Cache size ({current_size:.2f} MB) exceeds limit ({self.MAX_CACHE_SIZE_MB} MB)")
        elif current_size > self.MAX_CACHE_SIZE_MB * 0.9:
            warnings.append(f"Cache size ({current_size:.2f} MB) near limit ({self.MAX_CACHE_SIZE_MB} MB)")

        # Check hit rates
        stats = self.get_stats()
        if stats['analysis']['hit_rate_percent'] < 50:
            warnings.append(f"Analysis cache hit rate low ({stats['analysis']['hit_rate_percent']:.1f}%)")
        if stats['command']['hit_rate_percent'] < 70:
            warnings.append(f"Command cache hit rate low ({stats['command']['hit_rate_percent']:.1f}%)")
        if stats['mcp']['hit_rate_percent'] < 80:
            warnings.append(f"MCP cache hit rate low ({stats['mcp']['hit_rate_percent']:.1f}%)")

        # Check directory permissions
        for cache_dir in [self.analysis.cache_dir, self.command.cache_dir, self.mcp.cache_dir]:
            if not cache_dir.exists():
                issues.append(f"Cache directory missing: {cache_dir}")
            elif not cache_dir.is_dir():
                issues.append(f"Cache path is not a directory: {cache_dir}")

        return {
            'healthy': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        }

    def export_stats(self, output_path: Path) -> None:
        """
        Export cache statistics to JSON file.

        Args:
            output_path: Path to save stats JSON
        """
        stats = self.get_stats()
        output_path.write_text(json.dumps(stats, indent=2))

    def reset_stats(self) -> None:
        """Reset all cache statistics (preserves cached data)."""
        # Reset individual cache stats
        for cache in [self.analysis, self.command, self.mcp]:
            cache.stats = {
                "hits": 0,
                "misses": 0,
                "saves": 0,
                "evictions": 0,
                "last_reset": datetime.now().isoformat()
            }
            if hasattr(cache, 'total_savings_usd'):
                cache.stats['total_savings_usd'] = 0.0
            if hasattr(cache, 'total_savings_seconds'):
                cache.stats['total_savings_seconds'] = 0.0
            if hasattr(cache, 'total_lookups'):
                cache.stats['total_lookups'] = 0
            cache._save_stats()

        # Reset manager stats
        self.stats = {
            "total_evictions": 0,
            "total_clears": 0,
            "last_eviction": None,
            "last_clear": None,
            "initialized_at": datetime.now().isoformat()
        }
        self._save_stats()
