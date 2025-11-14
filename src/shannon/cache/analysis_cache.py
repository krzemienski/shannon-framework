"""
Analysis Cache - Context-aware caching for specification analysis results.

Caches complete analysis results with SHA-256 key computation and 7-day TTL.
Includes context hashing to ensure cached results match current project state.
"""

import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, Tuple


class AnalysisCache:
    """
    Caches specification analysis results with context awareness.

    Cache structure:
        ~/.shannon/cache/analyses/
        ├── {hash1}.json
        ├── {hash2}.json
        └── stats.json

    Each cached result includes:
        - Original spec hash
        - Analysis result
        - Framework version
        - Model used
        - Context hash (if applicable)
        - Timestamp
    """

    def __init__(self, cache_dir: Optional[Path] = None, ttl_days: int = 7):
        """
        Initialize analysis cache.

        Args:
            cache_dir: Custom cache directory (default: ~/.shannon/cache/analyses)
            ttl_days: Time-to-live in days (default: 7)
        """
        self.cache_dir = cache_dir or (Path.home() / ".shannon" / "cache" / "analyses")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl_days = ttl_days
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
                "total_savings_usd": 0.0,
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

    def compute_key(
        self,
        spec_text: str,
        context: Optional[Dict[str, Any]] = None,
        model: str = "sonnet[1m]",
        framework_version: str = "3.0.0"
    ) -> str:
        """
        Compute SHA-256 cache key from inputs.

        Critical: Context must be included in hash to avoid returning
        cached results that didn't consider current project context.

        Args:
            spec_text: Specification content
            context: Optional project context (files, tech stack, etc.)
            model: Model identifier
            framework_version: Shannon framework version

        Returns:
            64-character hex SHA-256 hash
        """
        # Build composite key parts
        key_parts = [
            spec_text,
            framework_version,
            model
        ]

        # Include context hash if present
        if context:
            context_hash = self._hash_context(context)
            key_parts.append(context_hash)

        # Compute SHA-256 hash of all parts
        composite = "|".join(key_parts)
        return hashlib.sha256(composite.encode('utf-8')).hexdigest()

    def _hash_context(self, context: Dict[str, Any]) -> str:
        """
        Hash project context for cache key.

        Only includes relevant deterministic parts:
        - Project ID
        - Technology stack
        - Loaded file paths

        Ignores timestamps, execution state, etc.

        Args:
            context: Project context dictionary

        Returns:
            16-character hex hash of canonical context
        """
        relevant = {
            'project_id': context.get('project_id'),
            'tech_stack': sorted(context.get('tech_stack', [])),
            'file_paths': sorted(context.get('loaded_files', {}).keys())
        }

        # Canonical JSON representation
        canonical = json.dumps(relevant, sort_keys=True)
        full_hash = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
        return full_hash[:16]  # First 16 chars for brevity

    def get(
        self,
        spec_text: str,
        context: Optional[Dict[str, Any]] = None,
        model: str = "sonnet[1m]",
        framework_version: str = "3.0.0"
    ) -> Optional[Dict[str, Any]]:
        """
        Get cached analysis if available and fresh.

        Returns None if:
        - Not in cache
        - Older than TTL
        - Cache file corrupted

        Args:
            spec_text: Specification content
            context: Optional project context
            model: Model identifier
            framework_version: Shannon framework version

        Returns:
            Cached analysis result with metadata, or None if miss
        """
        key = self.compute_key(spec_text, context, model, framework_version)
        cache_file = self.cache_dir / f"{key}.json"

        if not cache_file.exists():
            self.stats["misses"] += 1
            self._save_stats()
            return None  # Cache miss

        # Check age
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        age = datetime.now() - mtime
        age_days = age.days

        if age_days >= self.ttl_days:
            # Stale - delete and record eviction
            cache_file.unlink()
            self.stats["evictions"] += 1
            self.stats["misses"] += 1
            self._save_stats()
            return None

        # Load and return
        try:
            result = json.loads(cache_file.read_text())

            # Add cache hit metadata
            result['_cache_hit'] = True
            result['_cache_age_days'] = age_days
            result['_cache_age_hours'] = age.total_seconds() / 3600
            result['_cached_at'] = mtime.isoformat()

            # Record hit and savings
            self.stats["hits"] += 1
            # Estimate cost saved (typical analysis: $0.15)
            estimated_savings = 0.15
            self.stats["total_savings_usd"] += estimated_savings
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
        spec_text: str,
        result: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        model: str = "sonnet[1m]",
        framework_version: str = "3.0.0"
    ) -> None:
        """
        Save analysis result to cache atomically.

        Uses temp file + rename for atomic write (no corruption on crash).

        Args:
            spec_text: Specification content
            result: Analysis result to cache
            context: Optional project context
            model: Model identifier
            framework_version: Shannon framework version
        """
        key = self.compute_key(spec_text, context, model, framework_version)
        cache_file = self.cache_dir / f"{key}.json"

        # Add metadata
        cached_result = {
            **result,
            '_cache_metadata': {
                'key': key,
                'cached_at': datetime.now().isoformat(),
                'framework_version': framework_version,
                'model': model,
                'has_context': context is not None,
                'spec_hash': hashlib.sha256(spec_text.encode('utf-8')).hexdigest()[:16],
                'ttl_days': self.ttl_days
            }
        }

        # Atomic write: temp file + rename
        temp_file = cache_file.with_suffix('.tmp')
        temp_file.write_text(json.dumps(cached_result, indent=2))
        temp_file.rename(cache_file)

        # Record save
        self.stats["saves"] += 1
        self._save_stats()

    def clear(self) -> int:
        """
        Clear all cached analyses.

        Returns:
            Number of cache files deleted
        """
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
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
            "cache_size_mb": self._get_cache_size_mb()
        }

    def _get_cache_size_mb(self) -> float:
        """Calculate total cache size in MB."""
        total_bytes = sum(
            f.stat().st_size
            for f in self.cache_dir.glob("*.json")
            if f.name != "stats.json"
        )
        return round(total_bytes / (1024 * 1024), 2)

    def evict_old_entries(self, days: Optional[int] = None) -> int:
        """
        Evict cache entries older than specified days.

        Args:
            days: Age threshold in days (default: use TTL)

        Returns:
            Number of entries evicted
        """
        threshold_days = days if days is not None else self.ttl_days
        threshold = datetime.now() - timedelta(days=threshold_days)
        count = 0

        for cache_file in self.cache_dir.glob("*.json"):
            if cache_file.name == "stats.json":
                continue

            mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if mtime < threshold:
                cache_file.unlink()
                count += 1

        if count > 0:
            self.stats["evictions"] += count
            self._save_stats()

        return count
