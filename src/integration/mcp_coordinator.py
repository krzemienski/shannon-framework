"""
MCP Coordinator - Multi-server orchestration and intelligent routing

Manages:
1. Connection pooling across MCP servers
2. Intelligent request routing based on capability
3. Response aggregation and synthesis
4. Health checking and automatic fallback
5. Load balancing and parallel execution

Design Pattern: Coordinator + Strategy for multi-server orchestration
"""

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Callable, Set, Tuple
import time
from collections import defaultdict, deque
import json

logger = logging.getLogger(__name__)


class MCPServerType(Enum):
    """MCP server types"""
    CONTEXT7 = "context7"
    SEQUENTIAL = "sequential"
    MAGIC = "magic"
    PLAYWRIGHT = "playwright"
    SERENA = "serena"
    MORPHLLM = "morphllm"
    TAVILY = "tavily"
    PIECES = "pieces"


class ServerStatus(Enum):
    """Server health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


class RoutingStrategy(Enum):
    """Request routing strategies"""
    CAPABILITY_BASED = "capability"  # Route by server expertise
    LOAD_BALANCED = "load_balanced"  # Distribute load evenly
    LATENCY_OPTIMIZED = "latency"  # Route to fastest server
    REDUNDANT = "redundant"  # Send to multiple for reliability
    SEQUENTIAL_CHAIN = "sequential"  # Chain multiple servers


@dataclass
class MCPServer:
    """MCP server representation"""
    type: MCPServerType
    url: str
    capabilities: Set[str] = field(default_factory=set)
    status: ServerStatus = ServerStatus.UNKNOWN
    latency: float = 0.0  # Average response time
    request_count: int = 0
    error_count: int = 0
    last_health_check: float = 0.0
    max_concurrent: int = 10
    current_load: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MCPRequest:
    """MCP request with metadata"""
    id: str
    operation: str
    parameters: Dict[str, Any]
    required_capabilities: Set[str]
    priority: int = 5  # 0-10, higher is more important
    timeout: float = 30.0
    retry_count: int = 0
    max_retries: int = 3
    timestamp: float = field(default_factory=time.time)


@dataclass
class MCPResponse:
    """MCP response with provenance"""
    request_id: str
    server_type: MCPServerType
    success: bool
    data: Any
    latency: float
    error: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


class ServerPool:
    """Manages pool of MCP server connections"""

    def __init__(self):
        self.servers: Dict[MCPServerType, MCPServer] = {}
        self.connections: Dict[MCPServerType, Any] = {}  # Actual connections
        self.health_check_interval = 60.0  # seconds
        self.health_check_task: Optional[asyncio.Task] = None
        self.lock = asyncio.Lock()

    async def register_server(self, server: MCPServer) -> None:
        """Register MCP server with pool"""
        async with self.lock:
            self.servers[server.type] = server
            logger.info(f"Registered MCP server: {server.type.value}")

    async def connect(self, server_type: MCPServerType) -> bool:
        """Establish connection to MCP server"""
        if server_type not in self.servers:
            logger.error(f"Server not registered: {server_type.value}")
            return False

        server = self.servers[server_type]

        try:
            # Actual MCP connection logic would go here
            # For now, simulate connection
            self.connections[server_type] = {"connected": True, "url": server.url}
            server.status = ServerStatus.HEALTHY
            logger.info(f"Connected to {server_type.value}")
            return True
        except Exception as e:
            logger.error(f"Connection failed for {server_type.value}: {e}")
            server.status = ServerStatus.UNAVAILABLE
            return False

    async def disconnect(self, server_type: MCPServerType) -> None:
        """Close connection to MCP server"""
        if server_type in self.connections:
            # Cleanup connection
            del self.connections[server_type]
            logger.info(f"Disconnected from {server_type.value}")

    async def get_healthy_servers(self) -> List[MCPServerType]:
        """Get list of healthy servers"""
        return [
            server_type for server_type, server in self.servers.items()
            if server.status == ServerStatus.HEALTHY
        ]

    async def health_check(self, server_type: MCPServerType) -> ServerStatus:
        """Check health of specific server"""
        server = self.servers.get(server_type)
        if not server:
            return ServerStatus.UNKNOWN

        try:
            # Actual health check logic (ping, status endpoint, etc.)
            # For now, simulate based on error rate
            error_rate = (server.error_count / max(server.request_count, 1))

            if error_rate > 0.5:
                server.status = ServerStatus.UNAVAILABLE
            elif error_rate > 0.2:
                server.status = ServerStatus.DEGRADED
            else:
                server.status = ServerStatus.HEALTHY

            server.last_health_check = time.time()
            return server.status

        except Exception as e:
            logger.error(f"Health check failed for {server_type.value}: {e}")
            server.status = ServerStatus.UNAVAILABLE
            return ServerStatus.UNAVAILABLE

    async def start_health_monitoring(self) -> None:
        """Start periodic health checking"""
        async def monitor():
            while True:
                for server_type in self.servers.keys():
                    await self.health_check(server_type)
                await asyncio.sleep(self.health_check_interval)

        self.health_check_task = asyncio.create_task(monitor())

    async def stop_health_monitoring(self) -> None:
        """Stop health monitoring"""
        if self.health_check_task:
            self.health_check_task.cancel()
            try:
                await self.health_check_task
            except asyncio.CancelledError:
                pass


class RequestRouter:
    """Intelligent routing of requests to MCP servers"""

    def __init__(self, server_pool: ServerPool):
        self.pool = server_pool
        self.routing_strategy = RoutingStrategy.CAPABILITY_BASED
        self.capability_map: Dict[str, Set[MCPServerType]] = defaultdict(set)
        self._build_capability_map()

    def _build_capability_map(self) -> None:
        """Map capabilities to servers"""
        # Context7: documentation, patterns, libraries
        self.capability_map["documentation"].update([MCPServerType.CONTEXT7])
        self.capability_map["library_docs"].update([MCPServerType.CONTEXT7])
        self.capability_map["patterns"].update([MCPServerType.CONTEXT7])

        # Sequential: analysis, reasoning, planning
        self.capability_map["analysis"].update([MCPServerType.SEQUENTIAL])
        self.capability_map["reasoning"].update([MCPServerType.SEQUENTIAL])
        self.capability_map["planning"].update([MCPServerType.SEQUENTIAL])
        self.capability_map["debugging"].update([MCPServerType.SEQUENTIAL])

        # Magic: UI components, design
        self.capability_map["ui_components"].update([MCPServerType.MAGIC])
        self.capability_map["design_systems"].update([MCPServerType.MAGIC])

        # Playwright: browser automation, testing
        self.capability_map["browser_testing"].update([MCPServerType.PLAYWRIGHT])
        self.capability_map["e2e_testing"].update([MCPServerType.PLAYWRIGHT])
        self.capability_map["screenshots"].update([MCPServerType.PLAYWRIGHT])

        # Serena: semantic code, memory, symbols
        self.capability_map["code_symbols"].update([MCPServerType.SERENA])
        self.capability_map["memory"].update([MCPServerType.SERENA])
        self.capability_map["semantic_search"].update([MCPServerType.SERENA])

        # Morphllm: bulk edits, transformations
        self.capability_map["bulk_edit"].update([MCPServerType.MORPHLLM])
        self.capability_map["code_transform"].update([MCPServerType.MORPHLLM])

        # Tavily: web search, research
        self.capability_map["web_search"].update([MCPServerType.TAVILY])
        self.capability_map["research"].update([MCPServerType.TAVILY])

        # Pieces: long-term memory, context
        self.capability_map["ltm"].update([MCPServerType.PIECES])
        self.capability_map["history"].update([MCPServerType.PIECES])

    async def route_request(self, request: MCPRequest) -> List[MCPServerType]:
        """Determine which server(s) should handle request"""
        if self.routing_strategy == RoutingStrategy.CAPABILITY_BASED:
            return await self._route_by_capability(request)
        elif self.routing_strategy == RoutingStrategy.LOAD_BALANCED:
            return await self._route_by_load(request)
        elif self.routing_strategy == RoutingStrategy.LATENCY_OPTIMIZED:
            return await self._route_by_latency(request)
        elif self.routing_strategy == RoutingStrategy.REDUNDANT:
            return await self._route_redundant(request)
        else:
            return []

    async def _route_by_capability(self, request: MCPRequest) -> List[MCPServerType]:
        """Route based on required capabilities"""
        candidates: Set[MCPServerType] = set()

        # Find servers that have ALL required capabilities
        for capability in request.required_capabilities:
            servers = self.capability_map.get(capability, set())
            if not candidates:
                candidates = servers.copy()
            else:
                candidates &= servers

        # Filter by health status
        healthy = await self.pool.get_healthy_servers()
        candidates = [s for s in candidates if s in healthy]

        return candidates

    async def _route_by_load(self, request: MCPRequest) -> List[MCPServerType]:
        """Route to least loaded server with capability"""
        candidates = await self._route_by_capability(request)

        if not candidates:
            return []

        # Sort by current load
        load_sorted = sorted(
            candidates,
            key=lambda s: self.pool.servers[s].current_load
        )

        return [load_sorted[0]]

    async def _route_by_latency(self, request: MCPRequest) -> List[MCPServerType]:
        """Route to fastest server with capability"""
        candidates = await self._route_by_capability(request)

        if not candidates:
            return []

        # Sort by latency
        latency_sorted = sorted(
            candidates,
            key=lambda s: self.pool.servers[s].latency
        )

        return [latency_sorted[0]]

    async def _route_redundant(self, request: MCPRequest) -> List[MCPServerType]:
        """Route to multiple servers for redundancy"""
        candidates = await self._route_by_capability(request)

        # Return top 2-3 servers
        return candidates[:min(3, len(candidates))]

    def set_strategy(self, strategy: RoutingStrategy) -> None:
        """Change routing strategy"""
        self.routing_strategy = strategy
        logger.info(f"Routing strategy changed to {strategy.value}")


class ResponseAggregator:
    """Aggregates responses from multiple MCP servers"""

    def __init__(self):
        self.aggregation_strategies: Dict[str, Callable] = {
            "first": self._first_response,
            "best": self._best_response,
            "consensus": self._consensus_response,
            "merge": self._merge_responses,
        }

    async def aggregate(self, responses: List[MCPResponse],
                       strategy: str = "best") -> Any:
        """Aggregate multiple responses using strategy"""
        if not responses:
            return None

        if len(responses) == 1:
            return responses[0].data

        aggregator = self.aggregation_strategies.get(strategy, self._best_response)
        return await aggregator(responses)

    async def _first_response(self, responses: List[MCPResponse]) -> Any:
        """Return first successful response"""
        for resp in responses:
            if resp.success:
                return resp.data
        return None

    async def _best_response(self, responses: List[MCPResponse]) -> Any:
        """Return response from most reliable server"""
        successful = [r for r in responses if r.success]
        if not successful:
            return None

        # Score by latency and server reliability
        scored = []
        for resp in successful:
            # Lower latency is better
            score = 1.0 / (1.0 + resp.latency)
            scored.append((score, resp))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1].data

    async def _consensus_response(self, responses: List[MCPResponse]) -> Any:
        """Return response with consensus across servers"""
        successful = [r for r in responses if r.success]
        if not successful:
            return None

        # Simple majority voting for boolean/simple responses
        # For complex responses, use first successful
        data_values = [r.data for r in successful]

        # Count occurrences
        from collections import Counter
        counter = Counter(json.dumps(d, sort_keys=True) for d in data_values)
        most_common = counter.most_common(1)[0][0]

        return json.loads(most_common)

    async def _merge_responses(self, responses: List[MCPResponse]) -> Any:
        """Merge data from multiple responses"""
        successful = [r for r in responses if r.success]
        if not successful:
            return None

        # Merge dictionaries
        merged = {}
        for resp in successful:
            if isinstance(resp.data, dict):
                merged.update(resp.data)

        return merged if merged else successful[0].data


class MCPCoordinator:
    """Main coordinator for multi-MCP server orchestration"""

    def __init__(self):
        self.pool = ServerPool()
        self.router = RequestRouter(self.pool)
        self.aggregator = ResponseAggregator()
        self.request_queue: deque[MCPRequest] = deque()
        self.active_requests: Dict[str, MCPRequest] = {}
        self.lock = asyncio.Lock()

    async def initialize(self) -> None:
        """Initialize coordinator and server pool"""
        # Register default servers
        await self._register_default_servers()

        # Connect to servers
        for server_type in self.pool.servers.keys():
            await self.pool.connect(server_type)

        # Start health monitoring
        await self.pool.start_health_monitoring()

        logger.info("MCPCoordinator initialized")

    async def _register_default_servers(self) -> None:
        """Register standard MCP servers"""
        servers = [
            MCPServer(
                type=MCPServerType.CONTEXT7,
                url="context7://localhost",
                capabilities={"documentation", "library_docs", "patterns"}
            ),
            MCPServer(
                type=MCPServerType.SEQUENTIAL,
                url="sequential://localhost",
                capabilities={"analysis", "reasoning", "planning", "debugging"}
            ),
            MCPServer(
                type=MCPServerType.MAGIC,
                url="magic://localhost",
                capabilities={"ui_components", "design_systems"}
            ),
            MCPServer(
                type=MCPServerType.SERENA,
                url="serena://localhost",
                capabilities={"code_symbols", "memory", "semantic_search"}
            ),
        ]

        for server in servers:
            await self.pool.register_server(server)

    async def execute_request(self, request: MCPRequest,
                            aggregation_strategy: str = "best") -> Any:
        """Execute request and return aggregated response"""
        # Route to appropriate servers
        target_servers = await self.router.route_request(request)

        if not target_servers:
            logger.error(f"No servers available for request {request.id}")
            return None

        # Execute in parallel
        tasks = [
            self._execute_on_server(request, server_type)
            for server_type in target_servers
        ]

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions
        valid_responses = [r for r in responses if isinstance(r, MCPResponse)]

        # Aggregate responses
        result = await self.aggregator.aggregate(valid_responses, aggregation_strategy)

        return result

    async def _execute_on_server(self, request: MCPRequest,
                                server_type: MCPServerType) -> MCPResponse:
        """Execute request on specific server"""
        server = self.pool.servers[server_type]
        start_time = time.time()

        try:
            # Check load capacity
            if server.current_load >= server.max_concurrent:
                raise Exception(f"Server {server_type.value} at capacity")

            # Increment load
            server.current_load += 1

            # Actual MCP request execution would go here
            # For now, simulate
            await asyncio.sleep(0.1)  # Simulate network latency

            # Simulate success
            data = {"status": "success", "server": server_type.value}

            latency = time.time() - start_time
            server.latency = (server.latency * server.request_count + latency) / (server.request_count + 1)
            server.request_count += 1

            return MCPResponse(
                request_id=request.id,
                server_type=server_type,
                success=True,
                data=data,
                latency=latency
            )

        except Exception as e:
            logger.error(f"Request failed on {server_type.value}: {e}")
            server.error_count += 1

            return MCPResponse(
                request_id=request.id,
                server_type=server_type,
                success=False,
                data=None,
                latency=time.time() - start_time,
                error=str(e)
            )

        finally:
            # Decrement load
            server.current_load = max(0, server.current_load - 1)

    async def execute_chain(self, requests: List[MCPRequest]) -> List[Any]:
        """Execute chain of requests sequentially"""
        results = []
        for request in requests:
            result = await self.execute_request(request)
            results.append(result)
        return results

    async def execute_parallel(self, requests: List[MCPRequest]) -> List[Any]:
        """Execute multiple requests in parallel"""
        tasks = [self.execute_request(req) for req in requests]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

    async def shutdown(self) -> None:
        """Shutdown coordinator and cleanup"""
        await self.pool.stop_health_monitoring()

        for server_type in self.pool.servers.keys():
            await self.pool.disconnect(server_type)

        logger.info("MCPCoordinator shutdown complete")

    def get_server_stats(self) -> Dict[str, Any]:
        """Get statistics for all servers"""
        stats = {}
        for server_type, server in self.pool.servers.items():
            stats[server_type.value] = {
                "status": server.status.value,
                "requests": server.request_count,
                "errors": server.error_count,
                "latency": server.latency,
                "load": server.current_load,
                "error_rate": server.error_count / max(server.request_count, 1)
            }
        return stats