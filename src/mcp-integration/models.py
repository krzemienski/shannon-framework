"""
Shannon Framework v4 - MCP Integration Models

Data structures for MCP server integration and discovery.
"""

from typing import List, Dict, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class MCPStatus(Enum):
    """MCP server status."""
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    ERROR = "error"
    UNKNOWN = "unknown"


class MCPRequirement(Enum):
    """MCP requirement level."""
    REQUIRED = "required"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"


class MCPPattern(Enum):
    """MCP integration patterns."""
    DECLARATIVE = "declarative"      # Declare in frontmatter
    PROGRESSIVE = "progressive"      # Recommend dynamically
    FALLBACK = "fallback"           # Fallback on unavailability
    ORCHESTRATION = "orchestration"  # Coordinate multiple MCPs


@dataclass
class MCPCapability:
    """MCP server capability."""
    name: str
    description: str
    tool_names: List[str] = field(default_factory=list)
    resource_types: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'description': self.description,
            'tool_names': self.tool_names,
            'resource_types': self.resource_types,
        }


@dataclass
class MCPServer:
    """MCP server definition."""
    name: str
    version: str
    description: str

    # Status
    status: MCPStatus = MCPStatus.UNKNOWN
    last_check: Optional[datetime] = None

    # Capabilities
    capabilities: List[MCPCapability] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)

    # Configuration
    config: Dict[str, Any] = field(default_factory=dict)

    # Metadata
    install_command: Optional[str] = None
    documentation_url: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'status': self.status.value,
            'last_check': self.last_check.isoformat() if self.last_check else None,
            'capabilities': [c.to_dict() for c in self.capabilities],
            'tools': self.tools,
            'resources': self.resources,
            'config': self.config,
            'install_command': self.install_command,
            'documentation_url': self.documentation_url,
            'tags': self.tags,
        }

    def is_available(self) -> bool:
        """Check if MCP is available."""
        return self.status == MCPStatus.AVAILABLE

    def has_capability(self, capability_name: str) -> bool:
        """Check if MCP has specific capability."""
        return any(c.name == capability_name for c in self.capabilities)


@dataclass
class MCPDependency:
    """MCP dependency specification."""
    name: str
    version: str = "*"
    requirement: MCPRequirement = MCPRequirement.REQUIRED
    fallback_strategy: Optional[str] = None  # native, alternative, skip
    alternative_mcp: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'version': self.version,
            'requirement': self.requirement.value,
            'fallback_strategy': self.fallback_strategy,
            'alternative_mcp': self.alternative_mcp,
        }


@dataclass
class MCPRecommendation:
    """MCP recommendation for a specific context."""
    mcp_name: str
    reason: str
    relevance_score: float  # 0.0 to 1.0
    requirement_level: MCPRequirement
    estimated_benefit: str

    # Context
    triggered_by: Optional[str] = None  # Skill, complexity, domain
    alternatives: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'mcp_name': self.mcp_name,
            'reason': self.reason,
            'relevance_score': self.relevance_score,
            'requirement_level': self.requirement_level.value,
            'estimated_benefit': self.estimated_benefit,
            'triggered_by': self.triggered_by,
            'alternatives': self.alternatives,
        }


@dataclass
class MCPRegistry:
    """Registry of known MCP servers."""
    servers: Dict[str, MCPServer] = field(default_factory=dict)
    capability_index: Dict[str, List[str]] = field(default_factory=dict)  # capability -> [mcp_names]
    last_updated: Optional[datetime] = None

    def add_server(self, server: MCPServer):
        """Add MCP server to registry."""
        self.servers[server.name] = server

        # Index capabilities
        for capability in server.capabilities:
            if capability.name not in self.capability_index:
                self.capability_index[capability.name] = []
            self.capability_index[capability.name].append(server.name)

        self.last_updated = datetime.now()

    def get_server(self, name: str) -> Optional[MCPServer]:
        """Get server by name."""
        return self.servers.get(name)

    def find_by_capability(self, capability: str) -> List[MCPServer]:
        """Find servers with specific capability."""
        server_names = self.capability_index.get(capability, [])
        return [self.servers[name] for name in server_names if name in self.servers]

    def get_available_servers(self) -> List[MCPServer]:
        """Get all available servers."""
        return [s for s in self.servers.values() if s.is_available()]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'servers': {name: server.to_dict() for name, server in self.servers.items()},
            'capability_index': self.capability_index,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
        }


@dataclass
class MCPOrchestrationPlan:
    """Plan for coordinating multiple MCPs."""
    name: str
    mcp_servers: List[str] = field(default_factory=list)
    coordination_pattern: MCPPattern = MCPPattern.ORCHESTRATION

    # Execution order
    execution_order: List[str] = field(default_factory=list)

    # Data flow
    data_dependencies: Dict[str, List[str]] = field(default_factory=dict)  # mcp -> [dependencies]

    # Fallbacks
    fallback_chains: Dict[str, List[str]] = field(default_factory=dict)  # mcp -> [fallbacks]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'mcp_servers': self.mcp_servers,
            'coordination_pattern': self.coordination_pattern.value,
            'execution_order': self.execution_order,
            'data_dependencies': self.data_dependencies,
            'fallback_chains': self.fallback_chains,
        }
