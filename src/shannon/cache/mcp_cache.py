"""
MCP Cache - Domain-based MCP recommendation caching.

Caches MCP recommendations based on canonical domain signatures.
Uses deterministic lookups for instant retrieval without re-analysis.
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Set


class MCPCache:
    """
    Caches MCP recommendations based on domain patterns.

    Cache structure:
        ~/.shannon/cache/mcps/
        ├── F40B35D25.json  (Backend domain signature)
        ├── A89C12F46.json  (Analytics domain signature)
        └── stats.json

    Each cached entry includes:
        - Domain signature
        - Domain breakdown
        - Recommended MCPs (prioritized list)
        - Timestamp
        - No TTL (deterministic mapping)
    """

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize MCP cache.

        Args:
            cache_dir: Custom cache directory (default: ~/.shannon/cache/mcps)
        """
        self.cache_dir = cache_dir or (Path.home() / ".shannon" / "cache" / "mcps")
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
                "total_lookups": 0,
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

    def compute_domain_signature(self, domain_breakdown: Dict[str, float]) -> str:
        """
        Compute canonical domain signature from breakdown.

        The signature is deterministic - same domain percentages always
        produce the same signature, enabling instant MCP lookups.

        Args:
            domain_breakdown: Dict mapping domain names to percentages
                             e.g., {'Backend': 30.0, 'Analytics': 20.0, ...}

        Returns:
            9-character hex signature (first 9 chars of SHA-256)
        """
        # Canonical representation: sorted domains with rounded percentages
        canonical_items = []
        for domain in sorted(domain_breakdown.keys()):
            percentage = round(domain_breakdown[domain], 1)  # Round to 1 decimal
            canonical_items.append(f"{domain}:{percentage}")

        canonical = "|".join(canonical_items)
        full_hash = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
        return full_hash[:9].upper()  # First 9 chars, uppercase

    def get(
        self,
        domain_breakdown: Dict[str, float]
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get cached MCP recommendations for domain breakdown.

        Returns None if not in cache (no TTL - deterministic mapping).

        Args:
            domain_breakdown: Dict mapping domain names to percentages

        Returns:
            List of recommended MCPs with metadata, or None if miss
        """
        signature = self.compute_domain_signature(domain_breakdown)
        cache_file = self.cache_dir / f"{signature}.json"

        self.stats["total_lookups"] += 1

        if not cache_file.exists():
            self.stats["misses"] += 1
            self._save_stats()
            return None  # Cache miss

        # Load and return
        try:
            cached = json.loads(cache_file.read_text())

            # Add cache hit metadata
            mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
            recommendations = cached.get('recommendations', [])

            # Annotate with cache info
            for mcp in recommendations:
                mcp['_cache_hit'] = True
                mcp['_cached_at'] = mtime.isoformat()

            # Record hit
            self.stats["hits"] += 1
            self._save_stats()

            return recommendations

        except (json.JSONDecodeError, OSError):
            # Corrupted cache file
            cache_file.unlink()
            self.stats["misses"] += 1
            self._save_stats()
            return None

    def save(
        self,
        domain_breakdown: Dict[str, float],
        recommendations: List[Dict[str, Any]]
    ) -> None:
        """
        Save MCP recommendations to cache atomically.

        Args:
            domain_breakdown: Dict mapping domain names to percentages
            recommendations: List of MCP recommendation dicts with:
                - mcp_name: str
                - tier: int (1-4)
                - justification: str
                - priority_score: float
        """
        signature = self.compute_domain_signature(domain_breakdown)
        cache_file = self.cache_dir / f"{signature}.json"

        # Build cached entry
        cached_entry = {
            'signature': signature,
            'domain_breakdown': domain_breakdown,
            'recommendations': recommendations,
            '_cache_metadata': {
                'signature': signature,
                'cached_at': datetime.now().isoformat(),
                'num_mcps': len(recommendations),
                'primary_domains': [
                    domain for domain, pct in domain_breakdown.items()
                    if pct >= 15.0
                ]
            }
        }

        # Atomic write: temp file + rename
        temp_file = cache_file.with_suffix('.tmp')
        temp_file.write_text(json.dumps(cached_entry, indent=2))
        temp_file.rename(cache_file)

        # Record save
        self.stats["saves"] += 1
        self._save_stats()

    def clear(self) -> int:
        """
        Clear all cached MCP recommendations.

        Returns:
            Number of cache files deleted
        """
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            if cache_file.name != "stats.json":
                cache_file.unlink()
                count += 1

        return count

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with hits, misses, hit rate, etc.
        """
        hit_rate = (
            (self.stats["hits"] / self.stats["total_lookups"] * 100)
            if self.stats["total_lookups"] > 0
            else 0.0
        )

        return {
            **self.stats,
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
        return round(total_bytes / (1024 * 1024), 3)

    def list_cached_signatures(self) -> List[Dict[str, Any]]:
        """
        List all cached domain signatures with metadata.

        Returns:
            List of cached signature info dictionaries
        """
        cached = []

        for cache_file in self.cache_dir.glob("*.json"):
            if cache_file.name == "stats.json":
                continue

            try:
                data = json.loads(cache_file.read_text())
                metadata = data.get('_cache_metadata', {})

                cached.append({
                    'signature': metadata.get('signature'),
                    'cached_at': metadata.get('cached_at'),
                    'num_mcps': metadata.get('num_mcps'),
                    'primary_domains': metadata.get('primary_domains', []),
                    'domain_breakdown': data.get('domain_breakdown', {}),
                    'file_size_kb': round(cache_file.stat().st_size / 1024, 2)
                })

            except (json.JSONDecodeError, OSError):
                continue

        return sorted(cached, key=lambda x: x.get('cached_at', ''), reverse=True)

    def find_similar_domains(
        self,
        domain_breakdown: Dict[str, float],
        threshold: float = 0.8
    ) -> List[Dict[str, Any]]:
        """
        Find cached signatures with similar domain breakdowns.

        Uses cosine similarity to find close matches even if
        exact signature doesn't match.

        Args:
            domain_breakdown: Target domain breakdown
            threshold: Similarity threshold (0.0-1.0)

        Returns:
            List of similar cached entries with similarity scores
        """
        similar = []

        # Get all cached entries
        cached_entries = self.list_cached_signatures()

        # Compute similarity for each
        for entry in cached_entries:
            similarity = self._compute_similarity(
                domain_breakdown,
                entry['domain_breakdown']
            )

            if similarity >= threshold:
                similar.append({
                    **entry,
                    'similarity': round(similarity, 3)
                })

        # Sort by similarity (highest first)
        return sorted(similar, key=lambda x: x['similarity'], reverse=True)

    def _compute_similarity(
        self,
        breakdown1: Dict[str, float],
        breakdown2: Dict[str, float]
    ) -> float:
        """
        Compute cosine similarity between two domain breakdowns.

        Args:
            breakdown1: First domain breakdown
            breakdown2: Second domain breakdown

        Returns:
            Similarity score (0.0-1.0)
        """
        # Get all unique domains
        all_domains = set(breakdown1.keys()) | set(breakdown2.keys())

        # Build vectors
        vec1 = [breakdown1.get(d, 0.0) for d in all_domains]
        vec2 = [breakdown2.get(d, 0.0) for d in all_domains]

        # Compute cosine similarity
        dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
        magnitude1 = sum(v ** 2 for v in vec1) ** 0.5
        magnitude2 = sum(v ** 2 for v in vec2) ** 0.5

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)
