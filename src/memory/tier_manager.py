"""
Memory Tier Management System

Implements 5-tier memory hierarchy with automatic transitions, compression,
and access pattern tracking for Shannon framework.

Tiers:
- Working: Active context (0-1min, no compression)
- Hot: Recent usage (1min-1hr, 5:1 semantic)
- Warm: Occasional access (1hr-24hr, 10:1 AST)
- Cold: Rare access (24hr-7d, 50:1 holographic)
- Archive: Long-term storage (>7d, 100:1 archive)
"""

import asyncio
import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    import lz4.frame
    HAS_LZ4 = True
except ImportError:
    HAS_LZ4 = False

try:
    import zstandard as zstd
    HAS_ZSTD = True
except ImportError:
    HAS_ZSTD = False


class MemoryTier(Enum):
    """Memory tier classification."""
    WORKING = "working"
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"
    ARCHIVE = "archive"


class CompressionType(Enum):
    """Compression algorithm types."""
    NONE = "none"
    SEMANTIC = "semantic"
    AST = "ast"
    HOLOGRAPHIC = "holographic"
    ARCHIVE = "archive"


@dataclass
class MemoryItem:
    """Individual memory item with metadata."""

    key: str
    content: Any
    tier: MemoryTier
    created_at: float
    last_accessed: float
    access_count: int = 0
    compressed: bool = False
    compression_type: CompressionType = CompressionType.NONE
    compressed_size: int = 0
    original_size: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "key": self.key,
            "content": self.content,
            "tier": self.tier.value,
            "created_at": self.created_at,
            "last_accessed": self.last_accessed,
            "access_count": self.access_count,
            "compressed": self.compressed,
            "compression_type": self.compression_type.value,
            "compressed_size": self.compressed_size,
            "original_size": self.original_size,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryItem":
        """Deserialize from dictionary."""
        return cls(
            key=data["key"],
            content=data["content"],
            tier=MemoryTier(data["tier"]),
            created_at=data["created_at"],
            last_accessed=data["last_accessed"],
            access_count=data["access_count"],
            compressed=data["compressed"],
            compression_type=CompressionType(data["compression_type"]),
            compressed_size=data["compressed_size"],
            original_size=data["original_size"],
            metadata=data.get("metadata", {})
        )


class SemanticCompressor:
    """Semantic compression using embeddings and similarity."""

    @staticmethod
    def compress(data: str) -> Tuple[bytes, float]:
        """
        Compress using semantic similarity (target 5:1 ratio).

        In production, this would use embeddings and semantic chunking.
        For now, uses smart text compression with deduplication.
        """
        if not isinstance(data, str):
            data = json.dumps(data)

        # Deduplicate repeated patterns
        lines = data.split('\n')
        seen_patterns = {}
        compressed_lines = []

        for line in lines:
            # Hash line for deduplication
            line_hash = hashlib.md5(line.encode()).hexdigest()[:8]
            if line_hash in seen_patterns:
                compressed_lines.append(f"@REF:{line_hash}")
            else:
                seen_patterns[line_hash] = line
                compressed_lines.append(line)

        compressed = '\n'.join(compressed_lines).encode('utf-8')

        if HAS_LZ4:
            compressed = lz4.frame.compress(compressed)

        ratio = len(data.encode('utf-8')) / len(compressed) if compressed else 1.0
        return compressed, ratio

    @staticmethod
    def decompress(data: bytes) -> str:
        """Decompress semantic data."""
        if HAS_LZ4:
            data = lz4.frame.decompress(data)

        return data.decode('utf-8')


class ASTCompressor:
    """AST-based compression for code structures."""

    @staticmethod
    def compress(data: str) -> Tuple[bytes, float]:
        """
        Compress using AST analysis (target 10:1 ratio).

        In production, this would parse AST and compress structurally.
        For now, uses zstandard with high compression level.
        """
        if not isinstance(data, str):
            data = json.dumps(data)

        encoded = data.encode('utf-8')

        if HAS_ZSTD:
            compressor = zstd.ZstdCompressor(level=15)
            compressed = compressor.compress(encoded)
        else:
            # Fallback to basic compression
            compressed = encoded

        ratio = len(encoded) / len(compressed) if compressed else 1.0
        return compressed, ratio

    @staticmethod
    def decompress(data: bytes) -> str:
        """Decompress AST data."""
        if HAS_ZSTD:
            decompressor = zstd.ZstdDecompressor()
            data = decompressor.decompress(data)

        return data.decode('utf-8')


class HolographicCompressor:
    """Holographic compression using pattern recognition."""

    @staticmethod
    def compress(data: str) -> Tuple[bytes, float]:
        """
        Compress using holographic patterns (target 50:1 ratio).

        In production, this would use holographic reduced representations.
        For now, uses maximum zstandard compression with dictionary.
        """
        if not isinstance(data, str):
            data = json.dumps(data)

        encoded = data.encode('utf-8')

        if HAS_ZSTD:
            # Build compression dictionary from data
            dict_data = zstd.ZstdCompressionDict(encoded[:min(len(encoded), 1024)])
            compressor = zstd.ZstdCompressor(level=22, dict_data=dict_data)
            compressed = compressor.compress(encoded)
        else:
            compressed = encoded

        ratio = len(encoded) / len(compressed) if compressed else 1.0
        return compressed, ratio

    @staticmethod
    def decompress(data: bytes) -> str:
        """Decompress holographic data."""
        if HAS_ZSTD:
            decompressor = zstd.ZstdDecompressor()
            data = decompressor.decompress(data)

        return data.decode('utf-8')


class ArchiveCompressor:
    """Maximum compression for long-term storage."""

    @staticmethod
    def compress(data: str) -> Tuple[bytes, float]:
        """
        Maximum compression for archives (target 100:1 ratio).

        Combines multiple compression techniques for maximum ratio.
        """
        if not isinstance(data, str):
            data = json.dumps(data)

        # First pass: semantic deduplication
        compressed, _ = SemanticCompressor.compress(data)

        # Second pass: maximum zstd compression
        if HAS_ZSTD:
            compressor = zstd.ZstdCompressor(level=22)
            compressed = compressor.compress(compressed)

        ratio = len(data.encode('utf-8')) / len(compressed) if compressed else 1.0
        return compressed, ratio

    @staticmethod
    def decompress(data: bytes) -> str:
        """Decompress archived data."""
        if HAS_ZSTD:
            decompressor = zstd.ZstdDecompressor()
            data = decompressor.decompress(data)

        return SemanticCompressor.decompress(data)


class MemoryTierManager:
    """
    Manages 5-tier memory hierarchy with automatic transitions.

    Tiers and their characteristics:
    - Working: 0-1min, no compression, instant access
    - Hot: 1min-1hr, 5:1 semantic compression
    - Warm: 1hr-24hr, 10:1 AST compression
    - Cold: 24hr-7d, 50:1 holographic compression
    - Archive: >7d, 100:1 archive compression
    """

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize tier manager.

        Args:
            storage_path: Path for persistent storage
        """
        self.storage_path = storage_path or Path.home() / ".shannon" / "memory"
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # Memory storage by tier
        self.tiers: Dict[MemoryTier, Dict[str, MemoryItem]] = {
            tier: {} for tier in MemoryTier
        }

        # Compression engines
        self.compressors = {
            CompressionType.SEMANTIC: SemanticCompressor(),
            CompressionType.AST: ASTCompressor(),
            CompressionType.HOLOGRAPHIC: HolographicCompressor(),
            CompressionType.ARCHIVE: ArchiveCompressor()
        }

        # Tier transition thresholds (in seconds)
        self.transition_thresholds = {
            MemoryTier.WORKING: 60,  # 1 minute
            MemoryTier.HOT: 3600,  # 1 hour
            MemoryTier.WARM: 86400,  # 24 hours
            MemoryTier.COLD: 604800,  # 7 days
        }

        # Tier compression mappings
        self.tier_compression = {
            MemoryTier.WORKING: CompressionType.NONE,
            MemoryTier.HOT: CompressionType.SEMANTIC,
            MemoryTier.WARM: CompressionType.AST,
            MemoryTier.COLD: CompressionType.HOLOGRAPHIC,
            MemoryTier.ARCHIVE: CompressionType.ARCHIVE
        }

        # Statistics
        self.stats = {
            "transitions": 0,
            "compressions": 0,
            "decompressions": 0,
            "access_count": 0,
            "compression_ratios": []
        }

        # Background task for automatic transitions
        self._transition_task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self):
        """Start automatic tier management."""
        if not self._running:
            self._running = True
            self._transition_task = asyncio.create_task(self._background_transition_loop())

    async def stop(self):
        """Stop automatic tier management."""
        self._running = False
        if self._transition_task:
            self._transition_task.cancel()
            try:
                await self._transition_task
            except asyncio.CancelledError:
                pass

    def store(self, key: str, content: Any, metadata: Optional[Dict[str, Any]] = None) -> MemoryItem:
        """
        Store new memory item in Working tier.

        Args:
            key: Unique memory key
            content: Content to store
            metadata: Optional metadata

        Returns:
            Created MemoryItem
        """
        now = time.time()

        # Calculate original size
        content_str = json.dumps(content) if not isinstance(content, str) else content
        original_size = len(content_str.encode('utf-8'))

        item = MemoryItem(
            key=key,
            content=content,
            tier=MemoryTier.WORKING,
            created_at=now,
            last_accessed=now,
            original_size=original_size,
            metadata=metadata or {}
        )

        self.tiers[MemoryTier.WORKING][key] = item
        return item

    def retrieve(self, key: str) -> Optional[Any]:
        """
        Retrieve memory item by key.

        Args:
            key: Memory key

        Returns:
            Content if found, None otherwise
        """
        # Search all tiers
        for tier in MemoryTier:
            if key in self.tiers[tier]:
                item = self.tiers[tier][key]
                item.last_accessed = time.time()
                item.access_count += 1
                self.stats["access_count"] += 1

                # Decompress if needed
                if item.compressed:
                    content = self._decompress_item(item)
                    self.stats["decompressions"] += 1
                    return content

                return item.content

        return None

    def delete(self, key: str) -> bool:
        """
        Delete memory item.

        Args:
            key: Memory key

        Returns:
            True if deleted, False if not found
        """
        for tier in MemoryTier:
            if key in self.tiers[tier]:
                del self.tiers[tier][key]
                return True
        return False

    def get_item(self, key: str) -> Optional[MemoryItem]:
        """
        Get full memory item with metadata.

        Args:
            key: Memory key

        Returns:
            MemoryItem if found, None otherwise
        """
        for tier in MemoryTier:
            if key in self.tiers[tier]:
                return self.tiers[tier][key]
        return None

    async def transition_item(self, key: str, target_tier: MemoryTier) -> bool:
        """
        Manually transition item to specific tier.

        Args:
            key: Memory key
            target_tier: Target tier

        Returns:
            True if transitioned, False if not found
        """
        # Find item
        item = self.get_item(key)
        if not item:
            return False

        # Remove from current tier
        del self.tiers[item.tier][key]

        # Compress/decompress as needed
        if target_tier != item.tier:
            await self._apply_compression(item, target_tier)

        # Move to target tier
        item.tier = target_tier
        self.tiers[target_tier][key] = item
        self.stats["transitions"] += 1

        return True

    async def _background_transition_loop(self):
        """Background task for automatic tier transitions."""
        while self._running:
            try:
                await self._check_and_transition()
                await asyncio.sleep(10)  # Check every 10 seconds
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in transition loop: {e}")

    async def _check_and_transition(self):
        """Check all items and transition based on age and access patterns."""
        now = time.time()
        transitions_needed: List[Tuple[str, MemoryTier, MemoryTier]] = []

        # Check each tier for items that should transition
        for current_tier in [MemoryTier.WORKING, MemoryTier.HOT, MemoryTier.WARM, MemoryTier.COLD]:
            items = list(self.tiers[current_tier].values())

            for item in items:
                age = now - item.last_accessed
                target_tier = self._determine_target_tier(item, age)

                if target_tier != current_tier:
                    transitions_needed.append((item.key, current_tier, target_tier))

        # Execute transitions
        for key, current_tier, target_tier in transitions_needed:
            await self.transition_item(key, target_tier)

    def _determine_target_tier(self, item: MemoryItem, age: float) -> MemoryTier:
        """
        Determine appropriate tier based on age and access patterns.

        Args:
            item: Memory item
            age: Time since last access (seconds)

        Returns:
            Target tier
        """
        # Archive threshold (7 days)
        if age > self.transition_thresholds[MemoryTier.COLD]:
            return MemoryTier.ARCHIVE

        # Cold threshold (24 hours)
        if age > self.transition_thresholds[MemoryTier.WARM]:
            return MemoryTier.COLD

        # Warm threshold (1 hour)
        if age > self.transition_thresholds[MemoryTier.HOT]:
            return MemoryTier.WARM

        # Hot threshold (1 minute)
        if age > self.transition_thresholds[MemoryTier.WORKING]:
            return MemoryTier.HOT

        return MemoryTier.WORKING

    async def _apply_compression(self, item: MemoryItem, target_tier: MemoryTier):
        """
        Apply appropriate compression for target tier.

        Args:
            item: Memory item
            target_tier: Target tier
        """
        compression_type = self.tier_compression[target_tier]

        # Decompress if currently compressed
        if item.compressed:
            content = self._decompress_item(item)
            item.content = content
            item.compressed = False

        # Apply new compression if needed
        if compression_type != CompressionType.NONE:
            content_str = json.dumps(item.content) if not isinstance(item.content, str) else item.content

            compressor = self.compressors[compression_type]
            compressed, ratio = compressor.compress(content_str)

            item.content = compressed
            item.compressed = True
            item.compression_type = compression_type
            item.compressed_size = len(compressed)

            self.stats["compressions"] += 1
            self.stats["compression_ratios"].append(ratio)

    def _decompress_item(self, item: MemoryItem) -> Any:
        """
        Decompress memory item content.

        Args:
            item: Memory item

        Returns:
            Decompressed content
        """
        if not item.compressed:
            return item.content

        compressor = self.compressors[item.compression_type]
        decompressed = compressor.decompress(item.content)

        # Try to parse as JSON
        try:
            return json.loads(decompressed)
        except json.JSONDecodeError:
            return decompressed

    def get_tier_stats(self) -> Dict[str, Any]:
        """
        Get statistics for all tiers.

        Returns:
            Statistics dictionary
        """
        tier_stats = {}

        for tier in MemoryTier:
            items = self.tiers[tier].values()
            total_size = sum(
                item.compressed_size if item.compressed else item.original_size
                for item in items
            )
            original_size = sum(item.original_size for item in items)

            tier_stats[tier.value] = {
                "count": len(items),
                "total_size": total_size,
                "original_size": original_size,
                "compression_ratio": original_size / total_size if total_size > 0 else 1.0,
                "avg_access_count": sum(item.access_count for item in items) / len(items) if items else 0
            }

        return {
            "tiers": tier_stats,
            "global_stats": self.stats,
            "avg_compression_ratio": sum(self.stats["compression_ratios"]) / len(self.stats["compression_ratios"])
                if self.stats["compression_ratios"] else 1.0
        }

    def list_keys(self, tier: Optional[MemoryTier] = None) -> List[str]:
        """
        List all keys, optionally filtered by tier.

        Args:
            tier: Optional tier filter

        Returns:
            List of keys
        """
        if tier:
            return list(self.tiers[tier].keys())

        keys = []
        for tier_dict in self.tiers.values():
            keys.extend(tier_dict.keys())
        return keys

    def save_to_disk(self):
        """Persist memory state to disk."""
        state = {
            "tiers": {
                tier.value: [item.to_dict() for item in items.values()]
                for tier, items in self.tiers.items()
            },
            "stats": self.stats
        }

        state_file = self.storage_path / "memory_state.json"
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def load_from_disk(self):
        """Load memory state from disk."""
        state_file = self.storage_path / "memory_state.json"
        if not state_file.exists():
            return

        with open(state_file, 'r') as f:
            state = json.load(f)

        # Restore tiers
        for tier_name, items_data in state["tiers"].items():
            tier = MemoryTier(tier_name)
            self.tiers[tier] = {
                item_data["key"]: MemoryItem.from_dict(item_data)
                for item_data in items_data
            }

        # Restore stats
        self.stats = state.get("stats", self.stats)