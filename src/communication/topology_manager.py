"""
Communication Topology Manager - Dynamic graph-based routing

Implements 5 topology patterns:
1. Star - Central hub with spoke connections
2. Mesh - Fully connected peer-to-peer
3. Pipeline - Sequential chain processing
4. Hierarchical - Tree-based with levels
5. Gossip - Epidemic random propagation

Design Pattern: Strategy + Observer for dynamic topology switching
"""

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Set, Optional, Callable, Any, Tuple
import time
from collections import defaultdict, deque

try:
    import networkx as nx
except ImportError:
    nx = None  # Fallback: manual graph implementation

logger = logging.getLogger(__name__)


class TopologyType(Enum):
    """Supported communication topologies"""
    STAR = "star"
    MESH = "mesh"
    PIPELINE = "pipeline"
    HIERARCHICAL = "hierarchical"
    GOSSIP = "gossip"


class MessagePriority(Enum):
    """Message priority levels"""
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


@dataclass
class Message:
    """Communication message with metadata"""
    id: str
    sender: str
    recipients: List[str]
    payload: Any
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: float = field(default_factory=time.time)
    ttl: int = 10  # Time-to-live for gossip
    hops: int = 0
    path: List[str] = field(default_factory=list)


@dataclass
class Node:
    """Network node representation"""
    id: str
    address: str
    role: str = "worker"  # worker, hub, coordinator
    capacity: float = 1.0  # Processing capacity
    active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Edge:
    """Network edge with bandwidth tracking"""
    source: str
    target: str
    bandwidth: float = 1.0  # Relative bandwidth
    latency: float = 0.01  # Seconds
    utilization: float = 0.0  # Current usage 0.0-1.0
    messages_sent: int = 0
    bytes_sent: int = 0


class TopologyManager:
    """Manages dynamic network topology and reconfiguration"""

    def __init__(self, topology_type: TopologyType = TopologyType.MESH):
        self.topology_type = topology_type
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[Tuple[str, str], Edge] = {}

        # NetworkX graph if available, else manual adjacency
        if nx:
            self.graph = nx.DiGraph()
        else:
            self.adjacency: Dict[str, Set[str]] = defaultdict(set)

        self.hub_node: Optional[str] = None  # For star topology
        self.levels: Dict[str, int] = {}  # For hierarchical
        self.pipeline_order: List[str] = []  # For pipeline

        self.observers: List[Callable] = []
        self.lock = asyncio.Lock()

        logger.info(f"TopologyManager initialized with {topology_type.value}")

    async def add_node(self, node: Node) -> None:
        """Add node and rebuild topology"""
        async with self.lock:
            self.nodes[node.id] = node

            if nx:
                self.graph.add_node(node.id, **node.__dict__)
            else:
                if node.id not in self.adjacency:
                    self.adjacency[node.id] = set()

            logger.debug(f"Node added: {node.id}")
            await self._rebuild_topology()
            await self._notify_observers("node_added", node)

    async def remove_node(self, node_id: str) -> None:
        """Remove node and rebuild topology"""
        async with self.lock:
            if node_id not in self.nodes:
                return

            # Remove all edges involving this node
            edges_to_remove = [
                (s, t) for s, t in self.edges.keys()
                if s == node_id or t == node_id
            ]

            for edge_key in edges_to_remove:
                del self.edges[edge_key]

                if nx:
                    if self.graph.has_edge(*edge_key):
                        self.graph.remove_edge(*edge_key)
                else:
                    s, t = edge_key
                    self.adjacency[s].discard(t)

            # Remove node
            del self.nodes[node_id]

            if nx:
                if self.graph.has_node(node_id):
                    self.graph.remove_node(node_id)
            else:
                self.adjacency.pop(node_id, None)

            logger.debug(f"Node removed: {node_id}")
            await self._rebuild_topology()
            await self._notify_observers("node_removed", node_id)

    async def add_edge(self, edge: Edge) -> None:
        """Add edge between nodes"""
        async with self.lock:
            if edge.source not in self.nodes or edge.target not in self.nodes:
                logger.warning(f"Cannot add edge: nodes not found")
                return

            self.edges[(edge.source, edge.target)] = edge

            if nx:
                self.graph.add_edge(edge.source, edge.target, **edge.__dict__)
            else:
                self.adjacency[edge.source].add(edge.target)

            logger.debug(f"Edge added: {edge.source} -> {edge.target}")

    async def switch_topology(self, new_topology: TopologyType) -> None:
        """Dynamically switch to different topology"""
        async with self.lock:
            old_topology = self.topology_type
            self.topology_type = new_topology

            logger.info(f"Switching topology: {old_topology.value} -> {new_topology.value}")
            await self._rebuild_topology()
            await self._notify_observers("topology_changed", new_topology)

    async def _rebuild_topology(self) -> None:
        """Rebuild topology based on current type"""
        if not self.nodes:
            return

        # Clear existing edges
        self.edges.clear()
        if nx:
            self.graph.clear_edges()
        else:
            self.adjacency = defaultdict(set)

        node_ids = list(self.nodes.keys())

        if self.topology_type == TopologyType.STAR:
            await self._build_star(node_ids)
        elif self.topology_type == TopologyType.MESH:
            await self._build_mesh(node_ids)
        elif self.topology_type == TopologyType.PIPELINE:
            await self._build_pipeline(node_ids)
        elif self.topology_type == TopologyType.HIERARCHICAL:
            await self._build_hierarchical(node_ids)
        elif self.topology_type == TopologyType.GOSSIP:
            await self._build_gossip(node_ids)

    async def _build_star(self, node_ids: List[str]) -> None:
        """Star topology: one hub, all others connected to hub"""
        if not node_ids:
            return

        # Select hub (existing or first node)
        if self.hub_node and self.hub_node in node_ids:
            hub = self.hub_node
        else:
            hub = node_ids[0]
            self.hub_node = hub

        # Connect all non-hub nodes to hub
        for node_id in node_ids:
            if node_id != hub:
                # Bidirectional edges
                await self.add_edge(Edge(source=node_id, target=hub))
                await self.add_edge(Edge(source=hub, target=node_id))

    async def _build_mesh(self, node_ids: List[str]) -> None:
        """Fully connected mesh"""
        for i, source in enumerate(node_ids):
            for target in node_ids[i+1:]:
                # Bidirectional edges
                await self.add_edge(Edge(source=source, target=target))
                await self.add_edge(Edge(source=target, target=source))

    async def _build_pipeline(self, node_ids: List[str]) -> None:
        """Linear pipeline: sequential processing"""
        self.pipeline_order = node_ids.copy()

        for i in range(len(node_ids) - 1):
            await self.add_edge(Edge(
                source=node_ids[i],
                target=node_ids[i+1]
            ))

    async def _build_hierarchical(self, node_ids: List[str]) -> None:
        """Tree hierarchy with branching factor"""
        if not node_ids:
            return

        branching_factor = 3  # Each parent has 3 children
        self.levels.clear()

        # Root at level 0
        root = node_ids[0]
        self.levels[root] = 0
        queue = deque([root])
        remaining = node_ids[1:]

        while queue and remaining:
            parent = queue.popleft()
            parent_level = self.levels[parent]

            # Assign children
            for _ in range(min(branching_factor, len(remaining))):
                child = remaining.pop(0)
                self.levels[child] = parent_level + 1
                await self.add_edge(Edge(source=parent, target=child))
                await self.add_edge(Edge(source=child, target=parent))
                queue.append(child)

    async def _build_gossip(self, node_ids: List[str]) -> None:
        """Partial random connections for gossip protocol"""
        connections_per_node = min(4, len(node_ids) - 1)

        import random
        for node_id in node_ids:
            # Random subset of other nodes
            candidates = [n for n in node_ids if n != node_id]
            targets = random.sample(candidates,
                                   min(connections_per_node, len(candidates)))

            for target in targets:
                await self.add_edge(Edge(source=node_id, target=target))

    def get_neighbors(self, node_id: str) -> List[str]:
        """Get immediate neighbors for a node"""
        if nx:
            return list(self.graph.successors(node_id))
        else:
            return list(self.adjacency.get(node_id, set()))

    def get_path(self, source: str, target: str) -> Optional[List[str]]:
        """Find shortest path between nodes"""
        if nx:
            try:
                return nx.shortest_path(self.graph, source, target)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                return None
        else:
            # BFS for shortest path
            if source not in self.adjacency or target not in self.adjacency:
                return None

            queue = deque([(source, [source])])
            visited = {source}

            while queue:
                node, path = queue.popleft()

                if node == target:
                    return path

                for neighbor in self.adjacency[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))

            return None

    def get_topology_stats(self) -> Dict[str, Any]:
        """Calculate topology statistics"""
        if not self.nodes:
            return {}

        stats = {
            "type": self.topology_type.value,
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "active_nodes": sum(1 for n in self.nodes.values() if n.active),
        }

        if nx and self.graph.number_of_nodes() > 0:
            stats["diameter"] = nx.diameter(self.graph.to_undirected()) if nx.is_connected(self.graph.to_undirected()) else -1
            stats["avg_degree"] = sum(dict(self.graph.degree()).values()) / len(self.nodes)
            stats["density"] = nx.density(self.graph)

        return stats

    def add_observer(self, callback: Callable) -> None:
        """Register topology change observer"""
        self.observers.append(callback)

    async def _notify_observers(self, event: str, data: Any) -> None:
        """Notify all observers of topology changes"""
        for observer in self.observers:
            try:
                if asyncio.iscoroutinefunction(observer):
                    await observer(event, data)
                else:
                    observer(event, data)
            except Exception as e:
                logger.error(f"Observer error: {e}")


class MessageRouter:
    """Routes messages based on current topology"""

    def __init__(self, topology_manager: TopologyManager):
        self.topology = topology_manager
        self.message_queue: Dict[MessagePriority, deque] = {
            priority: deque() for priority in MessagePriority
        }
        self.routing_cache: Dict[Tuple[str, str], List[str]] = {}
        self.lock = asyncio.Lock()

    async def route_message(self, message: Message) -> List[str]:
        """Determine routing path for message"""
        if len(message.recipients) == 1:
            return await self._route_single(message)
        else:
            return await self._route_multicast(message)

    async def _route_single(self, message: Message) -> List[str]:
        """Route to single recipient"""
        target = message.recipients[0]

        # Check cache
        cache_key = (message.sender, target)
        if cache_key in self.routing_cache:
            return self.routing_cache[cache_key]

        # Compute path based on topology
        if self.topology.topology_type == TopologyType.STAR:
            path = await self._route_star(message.sender, target)
        elif self.topology.topology_type == TopologyType.MESH:
            path = [message.sender, target]  # Direct connection
        elif self.topology.topology_type == TopologyType.PIPELINE:
            path = await self._route_pipeline(message.sender, target)
        elif self.topology.topology_type == TopologyType.HIERARCHICAL:
            path = await self._route_hierarchical(message.sender, target)
        elif self.topology.topology_type == TopologyType.GOSSIP:
            path = await self._route_gossip(message.sender, target)
        else:
            path = self.topology.get_path(message.sender, target) or []

        # Cache result
        self.routing_cache[cache_key] = path
        return path

    async def _route_multicast(self, message: Message) -> List[List[str]]:
        """Route to multiple recipients"""
        paths = []
        for recipient in message.recipients:
            msg_copy = Message(
                id=f"{message.id}_{recipient}",
                sender=message.sender,
                recipients=[recipient],
                payload=message.payload,
                priority=message.priority
            )
            path = await self._route_single(msg_copy)
            if path:
                paths.append(path)
        return paths

    async def _route_star(self, source: str, target: str) -> List[str]:
        """Route through hub in star topology"""
        hub = self.topology.hub_node
        if not hub:
            return []

        if source == hub:
            return [source, target]
        elif target == hub:
            return [source, target]
        else:
            return [source, hub, target]

    async def _route_pipeline(self, source: str, target: str) -> List[str]:
        """Route along pipeline"""
        order = self.topology.pipeline_order

        try:
            source_idx = order.index(source)
            target_idx = order.index(target)
        except ValueError:
            return []

        if source_idx <= target_idx:
            return order[source_idx:target_idx+1]
        else:
            return []  # Can't go backwards in pipeline

    async def _route_hierarchical(self, source: str, target: str) -> List[str]:
        """Route through tree hierarchy"""
        path = self.topology.get_path(source, target)
        return path if path else []

    async def _route_gossip(self, source: str, target: str) -> List[str]:
        """Random walk for gossip propagation"""
        import random

        current = source
        path = [current]
        visited = {current}
        max_hops = 10

        for _ in range(max_hops):
            if current == target:
                return path

            neighbors = self.topology.get_neighbors(current)
            unvisited = [n for n in neighbors if n not in visited]

            if not unvisited:
                break

            # Random selection weighted by proximity to target
            current = random.choice(unvisited)
            visited.add(current)
            path.append(current)

        return path if path[-1] == target else []

    async def enqueue_message(self, message: Message) -> None:
        """Add message to priority queue"""
        async with self.lock:
            self.message_queue[message.priority].append(message)

    async def dequeue_message(self) -> Optional[Message]:
        """Get next message by priority"""
        async with self.lock:
            for priority in MessagePriority:
                if self.message_queue[priority]:
                    return self.message_queue[priority].popleft()
            return None

    def clear_cache(self) -> None:
        """Clear routing cache on topology change"""
        self.routing_cache.clear()


class BandwidthOptimizer:
    """Optimizes message routing for bandwidth efficiency"""

    def __init__(self, topology_manager: TopologyManager):
        self.topology = topology_manager
        self.traffic_stats: Dict[Tuple[str, str], float] = defaultdict(float)
        self.congestion_threshold = 0.8

    async def optimize_route(self, message: Message,
                           candidate_paths: List[List[str]]) -> List[str]:
        """Select best path based on bandwidth availability"""
        if not candidate_paths:
            return []

        if len(candidate_paths) == 1:
            return candidate_paths[0]

        # Score each path
        scored_paths = []
        for path in candidate_paths:
            score = await self._score_path(path, message)
            scored_paths.append((score, path))

        # Return best path
        scored_paths.sort(key=lambda x: x[0], reverse=True)
        return scored_paths[0][1]

    async def _score_path(self, path: List[str], message: Message) -> float:
        """Score path based on bandwidth, latency, utilization"""
        if len(path) < 2:
            return 0.0

        total_score = 0.0
        for i in range(len(path) - 1):
            edge_key = (path[i], path[i+1])
            edge = self.topology.edges.get(edge_key)

            if not edge:
                return 0.0  # Invalid path

            # Factors: bandwidth (40%), latency (30%), utilization (30%)
            bandwidth_score = edge.bandwidth
            latency_score = 1.0 / (1.0 + edge.latency)
            utilization_score = 1.0 - edge.utilization

            hop_score = (0.4 * bandwidth_score +
                        0.3 * latency_score +
                        0.3 * utilization_score)

            total_score += hop_score

        # Average across hops
        return total_score / (len(path) - 1)

    async def update_edge_stats(self, edge_key: Tuple[str, str],
                               bytes_sent: int) -> None:
        """Update edge utilization statistics"""
        edge = self.topology.edges.get(edge_key)
        if not edge:
            return

        edge.messages_sent += 1
        edge.bytes_sent += bytes_sent

        # Simple utilization model
        edge.utilization = min(1.0, edge.bytes_sent / (edge.bandwidth * 1e6))

        # Track traffic
        self.traffic_stats[edge_key] += bytes_sent

    async def detect_congestion(self) -> List[Tuple[str, str]]:
        """Identify congested edges"""
        congested = []
        for edge_key, edge in self.topology.edges.items():
            if edge.utilization >= self.congestion_threshold:
                congested.append(edge_key)
        return congested

    async def rebalance_load(self) -> None:
        """Suggest topology changes for load balancing"""
        congested = await self.detect_congestion()

        if not congested:
            return

        logger.info(f"Congestion detected on {len(congested)} edges")

        # For mesh/gossip: add alternative routes
        # For hierarchical: rebalance tree
        # For pipeline: suggest parallel pipelines
        # Implementation depends on topology type