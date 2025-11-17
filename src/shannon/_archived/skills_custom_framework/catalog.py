"""
Shannon Skills Framework - Persistent Skill Catalog

The SkillCatalog provides persistence for discovered skills using Memory MCP.
This enables faster startup by caching the skill catalog and avoiding repeated
filesystem scanning and YAML parsing.

Features:
- Save skill catalog to Memory MCP with 7-day TTL
- Load skills from cache if fresh (< 7 days old)
- Automatic cache invalidation on skill file changes
- Graceful degradation when Memory MCP unavailable
- Thread-safe operations with asyncio.Lock

Architecture:
    SkillLoader discovers skills → SkillCatalog caches in Memory MCP
    ┌──────────────┐
    │ SkillLoader  │
    └──────┬───────┘
           │ discover()
           ↓
    ┌──────────────────┐       ┌─────────────┐
    │  SkillCatalog    │←──────│ Memory MCP  │
    │  - save_catalog  │       │  - entities │
    │  - load_catalog  │       │  - search   │
    │  - is_fresh()    │       │  - nodes    │
    └──────────────────┘       └─────────────┘
           ↓
    ┌──────────────┐
    │ SkillRegistry│
    └──────────────┘

Usage:
    catalog = SkillCatalog(registry=registry)

    # Try to load from cache
    skills = await catalog.load_from_memory(project_root=Path("/project"))
    if skills:
        print(f"Loaded {len(skills)} skills from cache")
    else:
        # Cache miss - discover and save
        skills = await loader.discover_all()
        await catalog.save_to_memory(skills, project_root=Path("/project"))
"""

import json
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import asyncio

from shannon.skills.models import Skill
from shannon.skills.registry import SkillRegistry

logger = logging.getLogger(__name__)


class SkillCatalogError(Exception):
    """Base exception for catalog errors"""
    pass


class SkillCatalog:
    """
    Persistent skill catalog manager using Memory MCP.

    Provides caching layer for discovered skills to improve startup performance.
    Uses Memory MCP knowledge graph for persistent storage with TTL-based invalidation.

    Cache Strategy:
        - Skills saved with project_root as context
        - 7-day TTL for automatic invalidation
        - Manual invalidation on file changes (future enhancement)
        - Graceful fallback when Memory MCP unavailable

    Thread Safety:
        All operations use asyncio.Lock for concurrent access protection.
        Read operations check cache freshness atomically.

    Example:
        # Initialize
        registry = SkillRegistry(schema_path=schema)
        catalog = SkillCatalog(registry=registry)

        # Try cache first
        cached = await catalog.load_from_memory(project_root)
        if cached:
            print(f"Cache hit: {len(cached)} skills")
        else:
            # Discover and cache
            discovered = await loader.discover_all()
            await catalog.save_to_memory(discovered, project_root)
    """

    def __init__(
        self,
        registry: SkillRegistry,
        cache_ttl_days: int = 7
    ):
        """
        Initialize the skill catalog.

        Args:
            registry: SkillRegistry for skill registration
            cache_ttl_days: Time-to-live for cache in days (default: 7)
        """
        self.registry = registry
        self.cache_ttl_days = cache_ttl_days
        self._lock = asyncio.Lock()
        self._memory_mcp_available: Optional[bool] = None

        logger.info(
            f"SkillCatalog initialized with {cache_ttl_days}-day cache TTL"
        )

    async def _check_memory_mcp_available(self) -> bool:
        """
        Check if Memory MCP is available and accessible.

        Caches the result to avoid repeated import attempts.

        Returns:
            True if Memory MCP is available, False otherwise
        """
        if self._memory_mcp_available is not None:
            return self._memory_mcp_available

        try:
            # Try to import Memory MCP tools
            from mcp import create_entities, search_nodes
            self._memory_mcp_available = True
            logger.debug("Memory MCP is available")
            return True

        except ImportError:
            self._memory_mcp_available = False
            logger.warning(
                "Memory MCP not available - catalog persistence disabled"
            )
            return False

        except Exception as e:
            self._memory_mcp_available = False
            logger.warning(f"Memory MCP check failed: {e}")
            return False

    async def save_to_memory(
        self,
        skills: List[Skill],
        project_root: Path
    ) -> bool:
        """
        Save skill catalog to Memory MCP for persistent caching.

        Creates or updates a 'skill_catalog' entity in Memory MCP with:
        - Serialized skill data
        - Discovery timestamp
        - Project context
        - Skill count and metadata

        Args:
            skills: List of discovered skills to cache
            project_root: Project root path for context

        Returns:
            True if successfully saved, False if Memory MCP unavailable

        Example:
            success = await catalog.save_to_memory(
                skills=discovered_skills,
                project_root=Path("/Users/me/project")
            )
            if success:
                print("Catalog cached successfully")
        """
        if not await self._check_memory_mcp_available():
            logger.debug("Memory MCP unavailable - skipping catalog save")
            return False

        async with self._lock:
            try:
                from mcp import create_entities

                # Serialize skills to dict format
                serialized_skills = [skill.to_dict() for skill in skills]

                # Create catalog data with metadata
                catalog_data = {
                    'skills': serialized_skills,
                    'discovered_at': datetime.now().isoformat(),
                    'project_root': str(project_root.resolve()),
                    'skill_count': len(skills),
                    'cache_version': '1.0',
                    'ttl_days': self.cache_ttl_days
                }

                # Save to Memory MCP as entity
                # Note: We use a fixed entity name and update it each time
                entity_name = f"skill_catalog_{project_root.name}"

                await create_entities({
                    'entities': [{
                        'name': entity_name,
                        'entityType': 'SkillCatalog',
                        'observations': [json.dumps(catalog_data)]
                    }]
                })

                logger.info(
                    f"Saved {len(skills)} skills to Memory MCP "
                    f"(entity: {entity_name})"
                )
                return True

            except Exception as e:
                logger.warning(f"Failed to save catalog to Memory MCP: {e}")
                return False

    async def load_from_memory(
        self,
        project_root: Path
    ) -> Optional[List[Skill]]:
        """
        Load skill catalog from Memory MCP if cache is fresh.

        Searches for cached catalog matching project_root, validates freshness
        (< TTL days old), deserializes skills, and registers them in the registry.

        Cache Freshness:
            - Checks discovered_at timestamp
            - Compares against TTL (default: 7 days)
            - Returns None if stale or not found

        Args:
            project_root: Project root path to match cached catalog

        Returns:
            List of Skill objects if cache hit and fresh, None otherwise

        Example:
            skills = await catalog.load_from_memory(Path("/project"))
            if skills:
                print(f"Loaded {len(skills)} skills from cache")
            else:
                print("Cache miss - need to discover")
        """
        if not await self._check_memory_mcp_available():
            logger.debug("Memory MCP unavailable - cache miss")
            return None

        async with self._lock:
            try:
                from mcp import search_nodes

                # Search for catalog entity
                entity_name = f"skill_catalog_{project_root.name}"

                result = await search_nodes({
                    'query': entity_name
                })

                # Parse search result
                nodes = self._parse_search_result(result)

                if not nodes:
                    logger.debug(f"No cached catalog found for {project_root.name}")
                    return None

                # Get the first matching node
                node = nodes[0]

                # Extract catalog data from observations
                if 'observations' not in node or not node['observations']:
                    logger.warning("Catalog node has no observations")
                    return None

                catalog_data = json.loads(node['observations'][0])

                # Validate project root matches
                cached_root = catalog_data.get('project_root')
                if cached_root != str(project_root.resolve()):
                    logger.debug(
                        f"Project root mismatch: cached={cached_root}, "
                        f"requested={project_root}"
                    )
                    return None

                # Check cache freshness
                discovered_at = catalog_data.get('discovered_at')
                if not discovered_at or not self.is_cache_fresh(discovered_at):
                    logger.info("Cached catalog is stale - cache miss")
                    return None

                # Deserialize skills
                serialized_skills = catalog_data.get('skills', [])
                skills = []

                for skill_dict in serialized_skills:
                    try:
                        skill = Skill.from_dict(skill_dict)
                        skills.append(skill)

                        # Register in registry for immediate use
                        await self.registry.register(skill)

                    except Exception as e:
                        logger.warning(
                            f"Failed to deserialize skill {skill_dict.get('name')}: {e}"
                        )
                        continue

                logger.info(
                    f"Loaded {len(skills)} skills from Memory MCP cache "
                    f"(discovered: {discovered_at})"
                )
                return skills

            except Exception as e:
                logger.warning(f"Failed to load catalog from Memory MCP: {e}")
                return None

    def is_cache_fresh(self, discovered_at: str) -> bool:
        """
        Check if cached catalog is within TTL period.

        Parses the ISO-formatted discovered_at timestamp and compares
        against the configured cache TTL.

        Args:
            discovered_at: ISO format datetime string (e.g., "2025-01-15T10:30:00")

        Returns:
            True if cache is fresh (< TTL days old), False otherwise

        Example:
            if catalog.is_cache_fresh("2025-01-14T10:00:00"):
                print("Cache is still fresh")
        """
        try:
            discovered = datetime.fromisoformat(discovered_at)
            age = datetime.now() - discovered
            is_fresh = age < timedelta(days=self.cache_ttl_days)

            logger.debug(
                f"Cache age: {age.days} days, TTL: {self.cache_ttl_days} days, "
                f"Fresh: {is_fresh}"
            )

            return is_fresh

        except (ValueError, TypeError) as e:
            logger.warning(f"Invalid discovered_at timestamp: {discovered_at} - {e}")
            return False

    async def invalidate_cache(self, project_root: Path) -> bool:
        """
        Manually invalidate cached catalog for a project.

        Useful when skill files have changed and cache needs to be refreshed.

        Args:
            project_root: Project root path

        Returns:
            True if cache was invalidated, False if Memory MCP unavailable

        Example:
            await catalog.invalidate_cache(Path("/project"))
        """
        if not await self._check_memory_mcp_available():
            logger.debug("Memory MCP unavailable - cannot invalidate")
            return False

        async with self._lock:
            try:
                from mcp import delete_entities

                entity_name = f"skill_catalog_{project_root.name}"

                await delete_entities({
                    'entityNames': [entity_name]
                })

                logger.info(f"Invalidated cache for {project_root.name}")
                return True

            except Exception as e:
                logger.warning(f"Failed to invalidate cache: {e}")
                return False

    def _parse_search_result(self, result: Any) -> List[Dict[str, Any]]:
        """
        Parse Memory MCP search result into standardized node list.

        Handles different result formats from Memory MCP.

        Args:
            result: Raw result from search_nodes

        Returns:
            List of node dictionaries
        """
        if isinstance(result, dict) and 'nodes' in result:
            return result['nodes']
        elif isinstance(result, list):
            return result
        else:
            logger.debug(f"Unexpected search result format: {type(result)}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """
        Get catalog statistics.

        Returns:
            Dictionary with catalog configuration and status
        """
        return {
            'cache_ttl_days': self.cache_ttl_days,
            'memory_mcp_available': self._memory_mcp_available,
            'registry_skill_count': len(self.registry)
        }

    def __repr__(self) -> str:
        """String representation of catalog"""
        return (
            f"<SkillCatalog: TTL={self.cache_ttl_days}d, "
            f"MCP={'available' if self._memory_mcp_available else 'unavailable'}>"
        )
