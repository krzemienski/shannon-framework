"""
Command Cache - Stable command result caching.

Caches results for stable commands that don't change frequently:
- shannon prime (initial instructions)
- shannon discover-skills (skill discovery)
- shannon check-mcps (MCP validation)

Uses version-based keys for instant retrieval without re-execution.
"""

import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List


class CommandCache:
    """
    Caches stable command execution results.

    Cache structure:
        ~/.shannon/cache/commands/
        ├── prime_v3.0.0.json
        ├── discover-skills_v3.0.0.json
        ├── check-mcps_v3.0.0.json
        └── stats.json

    Each cached result includes:
        - Command name
        - Framework version
        - Execution result
        - Timestamp
        - TTL
    """

    # Stable commands eligible for caching
    CACHEABLE_COMMANDS = {
        'prime': 30,           # 30-day TTL (instructions rarely change)
        'discover-skills': 7,  # 7-day TTL (skills may be added)
        'check-mcps': 1,       # 1-day TTL (MCPs change more frequently)
    }

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize command cache.

        Args:
            cache_dir: Custom cache directory (default: ~/.shannon/cache/commands)
        """
        self.cache_dir = cache_dir or (Path.home() / ".shannon" / "cache" / "commands")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.stats_file = self.cache_dir / "stats.json"

        # Initialize stats
        self.stats = self._load_stats()

    def _load_stats(self) -> Dict[str, Any]:
        """Load cache statistics from disk."""
        if not self.stats_file.exists():
            return {
                "hits": 0,
                "misses": 0,
                "saves": 0,
                "evictions": 0,
                "total_savings_seconds": 0.0,
                "last_reset": datetime.now().isoformat()
            }

        try:
            return json.loads(self.stats_file.read_text())
        except (json.JSONDecodeError, OSError):
            return self._load_stats.__defaults__[0]

    def _save_stats(self) -> None:
        """Save cache statistics to disk atomically."""
        temp_file = self.stats_file.with_suffix('.tmp')
        temp_file.write_text(json.dumps(self.stats, indent=2))
        temp_file.rename(self.stats_file)

    def _is_cacheable(self, command: str) -> bool:
        """Check if command is eligible for caching."""
        return command in self.CACHEABLE_COMMANDS

    def _get_ttl_days(self, command: str) -> int:
        """Get TTL in days for a command."""
        return self.CACHEABLE_COMMANDS.get(command, 7)

    def compute_key(
        self,
        command: str,
        framework_version: str = "3.0.0",
        args: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Compute cache key for a command.

        Key format: {command}_v{version}_{args_hash}.json

        Args:
            command: Command name (e.g., 'prime', 'discover-skills')
            framework_version: Shannon framework version
            args: Optional command arguments

        Returns:
            Cache key string
        """
        if args:
            # Hash arguments for uniqueness
            args_canonical = json.dumps(args, sort_keys=True)
            args_hash = hashlib.sha256(args_canonical.encode('utf-8')).hexdigest()[:8]
            return f"{command}_v{framework_version}_{args_hash}"
        else:
            return f"{command}_v{framework_version}"

    def get(
        self,
        command: str,
        framework_version: str = "3.0.0",
        args: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get cached command result if available and fresh.

        Returns None if:
        - Command not cacheable
        - Not in cache
        - Older than TTL
        - Cache file corrupted

        Args:
            command: Command name
            framework_version: Shannon framework version
            args: Optional command arguments

        Returns:
            Cached command result, or None if miss
        """
        if not self._is_cacheable(command):
            return None  # Command not eligible for caching

        key = self.compute_key(command, framework_version, args)
        cache_file = self.cache_dir / f"{key}.json"

        if not cache_file.exists():
            self.stats["misses"] += 1
            self._save_stats()
            return None  # Cache miss

        # Check age
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        age = datetime.now() - mtime
        age_days = age.days

        ttl_days = self._get_ttl_days(command)
        if age_days >= ttl_days:
            # Stale - delete and record eviction
            cache_file.unlink()
            self.stats["evictions"] += 1
            self.stats["misses"] += 1
            self._save_stats()
            return None

        # Load and return
        try:
            cached = json.loads(cache_file.read_text())

            # Add cache hit metadata
            result = cached.get('result', {})
            result['_cache_hit'] = True
            result['_cache_age_days'] = age_days
            result['_cache_age_seconds'] = age.total_seconds()
            result['_cached_at'] = mtime.isoformat()

            # Record hit and time savings
            self.stats["hits"] += 1
            # Estimate time saved (typical command: 2-5 seconds)
            estimated_savings = cached.get('_cache_metadata', {}).get('execution_time_seconds', 3.0)
            self.stats["total_savings_seconds"] += estimated_savings
            self._save_stats()

            return result

        except (json.JSONDecodeError, OSError):
            # Corrupted cache file
            cache_file.unlink()
            self.stats["misses"] += 1
            self._save_stats()
            return None

    def save(
        self,
        command: str,
        result: Dict[str, Any],
        framework_version: str = "3.0.0",
        args: Optional[Dict[str, Any]] = None,
        execution_time: float = 0.0
    ) -> None:
        """
        Save command result to cache atomically.

        Args:
            command: Command name
            result: Command execution result
            framework_version: Shannon framework version
            args: Optional command arguments
            execution_time: Execution time in seconds (for savings calculation)
        """
        if not self._is_cacheable(command):
            return  # Don't cache ineligible commands

        key = self.compute_key(command, framework_version, args)
        cache_file = self.cache_dir / f"{key}.json"

        # Build cached entry
        cached_entry = {
            'result': result,
            '_cache_metadata': {
                'command': command,
                'key': key,
                'cached_at': datetime.now().isoformat(),
                'framework_version': framework_version,
                'ttl_days': self._get_ttl_days(command),
                'args': args,
                'execution_time_seconds': execution_time
            }
        }

        # Atomic write: temp file + rename
        temp_file = cache_file.with_suffix('.tmp')
        temp_file.write_text(json.dumps(cached_entry, indent=2))
        temp_file.rename(cache_file)

        # Record save
        self.stats["saves"] += 1
        self._save_stats()

    def clear(self, command: Optional[str] = None) -> int:
        """
        Clear cached command results.

        Args:
            command: Specific command to clear (None = clear all)

        Returns:
            Number of cache files deleted
        """
        count = 0

        if command:
            # Clear specific command
            pattern = f"{command}_*.json"
        else:
            # Clear all commands
            pattern = "*.json"

        for cache_file in self.cache_dir.glob(pattern):
            if cache_file.name != "stats.json":
                cache_file.unlink()
                count += 1

        self.stats["evictions"] += count
        self._save_stats()
        return count

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with hits, misses, hit rate, savings, etc.
        """
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0.0

        return {
            **self.stats,
            "total_requests": total_requests,
            "hit_rate_percent": round(hit_rate, 2),
            "cache_size_files": len(list(self.cache_dir.glob("*.json"))) - 1,  # Exclude stats.json
            "cache_size_mb": self._get_cache_size_mb(),
            "total_savings_minutes": round(self.stats["total_savings_seconds"] / 60, 2)
        }

    def _get_cache_size_mb(self) -> float:
        """Calculate total cache size in MB."""
        total_bytes = sum(
            f.stat().st_size
            for f in self.cache_dir.glob("*.json")
            if f.name != "stats.json"
        )
        return round(total_bytes / (1024 * 1024), 3)

    def evict_old_entries(self) -> int:
        """
        Evict cache entries older than their respective TTLs.

        Returns:
            Number of entries evicted
        """
        count = 0

        for cache_file in self.cache_dir.glob("*.json"):
            if cache_file.name == "stats.json":
                continue

            try:
                # Parse command from filename
                command = cache_file.stem.split('_v')[0]
                if command not in self.CACHEABLE_COMMANDS:
                    continue

                # Check age against TTL
                mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
                ttl_days = self._get_ttl_days(command)
                threshold = datetime.now() - timedelta(days=ttl_days)

                if mtime < threshold:
                    cache_file.unlink()
                    count += 1

            except (ValueError, OSError):
                # Skip malformed files
                continue

        if count > 0:
            self.stats["evictions"] += count
            self._save_stats()

        return count

    def list_cached_commands(self) -> List[Dict[str, Any]]:
        """
        List all cached command entries with metadata.

        Returns:
            List of cached command info dictionaries
        """
        cached = []

        for cache_file in self.cache_dir.glob("*.json"):
            if cache_file.name == "stats.json":
                continue

            try:
                data = json.loads(cache_file.read_text())
                metadata = data.get('_cache_metadata', {})

                mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
                age_days = (datetime.now() - mtime).days

                cached.append({
                    'command': metadata.get('command'),
                    'key': metadata.get('key'),
                    'cached_at': metadata.get('cached_at'),
                    'age_days': age_days,
                    'ttl_days': metadata.get('ttl_days'),
                    'framework_version': metadata.get('framework_version'),
                    'file_size_kb': round(cache_file.stat().st_size / 1024, 2)
                })

            except (json.JSONDecodeError, OSError):
                continue

        return sorted(cached, key=lambda x: x.get('cached_at', ''), reverse=True)
