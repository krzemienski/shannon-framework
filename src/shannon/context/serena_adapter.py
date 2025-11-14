"""
Serena MCP Adapter for Shannon Context Management

Provides integration with Serena MCP for persistent knowledge graph storage.
Handles entity and relation creation for projects, modules, files, and patterns.

Architecture:
    Project → hasModule → Module
           → hasPattern → Pattern
           → hasFile → File
           → hasTechDebt → TechnicalDebt
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SerenaNode:
    """Represents a node in Serena knowledge graph"""
    entity_id: str
    entity_type: str
    observations: List[str]

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'entityId': self.entity_id,
            'entityType': self.entity_type,
            'observations': self.observations
        }


@dataclass
class SerenaRelation:
    """Represents a relation between nodes"""
    from_id: str
    to_id: str
    relation_type: str

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'from': self.from_id,
            'to': self.to_id,
            'relationType': self.relation_type
        }


class SerenaAdapter:
    """
    Adapter for Serena MCP knowledge graph operations

    Provides high-level API for Shannon context management:
    - Create/update/delete entities (projects, modules, files, patterns)
    - Create/delete relations
    - Search and retrieve nodes
    - Batch operations for efficiency

    Uses Serena MCP tools directly without abstraction layer.
    """

    def __init__(self):
        """Initialize Serena adapter"""
        self.logger = logging.getLogger(__name__)
        self._created_entities: set = set()  # Track created entities
        self._created_relations: set = set()  # Track created relations

    async def create_node(
        self,
        entity_id: str,
        entity_type: str,
        observations: List[str]
    ) -> bool:
        """
        Create a single node in Serena knowledge graph

        Args:
            entity_id: Unique identifier (e.g., "project_myapp")
            entity_type: Type of entity (Project, Module, File, Pattern)
            observations: List of observation strings about this entity

        Returns:
            True if successful, False otherwise

        Example:
            await adapter.create_node(
                entity_id="project_myapp",
                entity_type="Project",
                observations=[
                    "Files: 150",
                    "Lines: 10234",
                    "Languages: Python 65%, TypeScript 35%"
                ]
            )
        """
        try:
            # Import Serena MCP tools dynamically
            from mcp import create_entities

            # Create entity using Serena MCP
            await create_entities({
                'entities': [{
                    'name': entity_id,
                    'entityType': entity_type,
                    'observations': observations
                }]
            })

            self._created_entities.add(entity_id)
            self.logger.debug(f"Created node: {entity_id} ({entity_type})")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create node {entity_id}: {e}")
            return False

    async def create_nodes_batch(
        self,
        nodes: List[SerenaNode]
    ) -> Dict[str, bool]:
        """
        Create multiple nodes in a single batch operation

        More efficient than individual create_node calls.

        Args:
            nodes: List of SerenaNode objects to create

        Returns:
            Dictionary mapping entity_id to success status

        Example:
            results = await adapter.create_nodes_batch([
                SerenaNode(
                    entity_id="module_frontend",
                    entity_type="Module",
                    observations=["React 18", "50 components"]
                ),
                SerenaNode(
                    entity_id="module_backend",
                    entity_type="Module",
                    observations=["Express 4", "REST API"]
                )
            ])
        """
        try:
            from mcp import create_entities

            # Prepare batch request
            entities = [
                {
                    'name': node.entity_id,
                    'entityType': node.entity_type,
                    'observations': node.observations
                }
                for node in nodes
            ]

            # Execute batch creation
            await create_entities({'entities': entities})

            # Track all as created
            results = {}
            for node in nodes:
                self._created_entities.add(node.entity_id)
                results[node.entity_id] = True

            self.logger.info(f"Created {len(nodes)} nodes in batch")
            return results

        except Exception as e:
            self.logger.error(f"Batch node creation failed: {e}")
            # Return all False on batch failure
            return {node.entity_id: False for node in nodes}

    async def create_relation(
        self,
        from_id: str,
        to_id: str,
        relation_type: str
    ) -> bool:
        """
        Create a relation between two entities

        Args:
            from_id: Source entity ID
            to_id: Target entity ID
            relation_type: Type of relation (hasModule, hasPattern, dependsOn, etc.)

        Returns:
            True if successful, False otherwise

        Example:
            await adapter.create_relation(
                from_id="project_myapp",
                to_id="module_frontend",
                relation_type="hasModule"
            )
        """
        try:
            from mcp import create_relations

            # Create relation using Serena MCP
            await create_relations({
                'relations': [{
                    'from': from_id,
                    'to': to_id,
                    'relationType': relation_type
                }]
            })

            relation_key = f"{from_id}:{relation_type}:{to_id}"
            self._created_relations.add(relation_key)
            self.logger.debug(f"Created relation: {from_id} --{relation_type}--> {to_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create relation: {e}")
            return False

    async def create_relations_batch(
        self,
        relations: List[SerenaRelation]
    ) -> Dict[str, bool]:
        """
        Create multiple relations in a single batch operation

        Args:
            relations: List of SerenaRelation objects to create

        Returns:
            Dictionary mapping relation key to success status
        """
        try:
            from mcp import create_relations

            # Prepare batch request
            relation_data = [
                {
                    'from': rel.from_id,
                    'to': rel.to_id,
                    'relationType': rel.relation_type
                }
                for rel in relations
            ]

            # Execute batch creation
            await create_relations({'relations': relation_data})

            # Track all as created
            results = {}
            for rel in relations:
                relation_key = f"{rel.from_id}:{rel.relation_type}:{rel.to_id}"
                self._created_relations.add(relation_key)
                results[relation_key] = True

            self.logger.info(f"Created {len(relations)} relations in batch")
            return results

        except Exception as e:
            self.logger.error(f"Batch relation creation failed: {e}")
            return {
                f"{rel.from_id}:{rel.relation_type}:{rel.to_id}": False
                for rel in relations
            }

    async def add_observations(
        self,
        entity_id: str,
        observations: List[str]
    ) -> bool:
        """
        Add new observations to an existing entity

        Args:
            entity_id: Entity to update
            observations: New observations to append

        Returns:
            True if successful, False otherwise
        """
        try:
            from mcp import add_observations

            await add_observations({
                'observations': [{
                    'entityName': entity_id,
                    'contents': observations
                }]
            })

            self.logger.debug(f"Added {len(observations)} observations to {entity_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add observations: {e}")
            return False

    async def search_nodes(
        self,
        query: str,
        max_results: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search for nodes matching a query

        Uses Serena's semantic search capabilities.

        Args:
            query: Search query (can be keywords or natural language)
            max_results: Maximum number of results to return

        Returns:
            List of matching nodes with their data

        Example:
            nodes = await adapter.search_nodes(
                query="authentication REST API",
                max_results=10
            )
        """
        try:
            from mcp import search_nodes

            result = await search_nodes({
                'query': query
            })

            # Parse result and return top matches
            nodes = self._parse_search_result(result)
            return nodes[:max_results]

        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            return []

    async def open_nodes(
        self,
        entity_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Retrieve specific nodes by their IDs

        Args:
            entity_ids: List of entity IDs to retrieve

        Returns:
            List of node data dictionaries

        Example:
            nodes = await adapter.open_nodes([
                "project_myapp",
                "module_frontend"
            ])
        """
        try:
            from mcp import open_nodes

            result = await open_nodes({
                'names': entity_ids
            })

            return self._parse_nodes_result(result)

        except Exception as e:
            self.logger.error(f"Failed to open nodes: {e}")
            return []

    async def delete_entity(
        self,
        entity_id: str
    ) -> bool:
        """
        Delete an entity and all its relations

        Args:
            entity_id: Entity to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            from mcp import delete_entities

            await delete_entities({
                'entityNames': [entity_id]
            })

            self._created_entities.discard(entity_id)
            self.logger.debug(f"Deleted entity: {entity_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to delete entity: {e}")
            return False

    def _parse_search_result(self, result: Any) -> List[Dict[str, Any]]:
        """Parse Serena search result into standardized format"""
        # Serena returns nodes in result format
        # Extract relevant fields
        if isinstance(result, dict) and 'nodes' in result:
            return result['nodes']
        elif isinstance(result, list):
            return result
        else:
            return []

    def _parse_nodes_result(self, result: Any) -> List[Dict[str, Any]]:
        """Parse Serena open_nodes result into standardized format"""
        if isinstance(result, dict) and 'nodes' in result:
            return result['nodes']
        elif isinstance(result, list):
            return result
        else:
            return []

    def get_stats(self) -> Dict[str, int]:
        """
        Get adapter statistics

        Returns:
            Dictionary with entity and relation counts
        """
        return {
            'entities_created': len(self._created_entities),
            'relations_created': len(self._created_relations)
        }

    async def health_check(self) -> bool:
        """
        Verify Serena MCP is accessible and working

        Returns:
            True if Serena is healthy, False otherwise
        """
        try:
            # Try to read the knowledge graph
            from mcp import read_graph

            await read_graph({})
            return True

        except Exception as e:
            self.logger.error(f"Serena health check failed: {e}")
            return False
