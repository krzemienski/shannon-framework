"""
Communication Module - Dynamic topology management and message routing

Exports:
- TopologyManager: Dynamic graph reconfiguration
- MessageRouter: Topology-aware routing
- BandwidthOptimizer: Efficiency optimization
- TopologyType, MessagePriority: Enums
- Message, Node, Edge: Data classes
"""

from .topology_manager import (
    TopologyManager,
    MessageRouter,
    BandwidthOptimizer,
    TopologyType,
    MessagePriority,
    Message,
    Node,
    Edge,
)

__all__ = [
    "TopologyManager",
    "MessageRouter",
    "BandwidthOptimizer",
    "TopologyType",
    "MessagePriority",
    "Message",
    "Node",
    "Edge",
]