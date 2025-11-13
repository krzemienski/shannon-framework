"""
Shannon Framework v4 - MCP Discovery

Dynamic MCP discovery and progressive recommendation.
"""

from typing import List, Dict, Optional, Any, Set
from datetime import datetime
from .models import (
    MCPServer, MCPRegistry, MCPRecommendation, MCPRequirement,
    MCPStatus, MCPCapability, MCPPattern
)


class MCPDiscovery:
    """
    Discovers and recommends MCP servers based on context.

    Implements 4 integration patterns:
    1. Declarative: Static declarations in skill frontmatter
    2. Progressive: Dynamic recommendations based on complexity/domain
    3. Fallback: Alternative strategies when MCPs unavailable
    4. Orchestration: Coordinate multiple MCPs
    """

    def __init__(self):
        """Initialize MCP discovery."""
        self.registry = MCPRegistry()
        self._initialize_known_mcps()

    def _initialize_known_mcps(self):
        """Initialize registry with known MCP servers."""
        # Serena MCP (Context Preservation)
        serena = MCPServer(
            name="serena",
            version="2.0.0",
            description="Context preservation with zero-context-loss",
            capabilities=[
                MCPCapability(
                    name="context_preservation",
                    description="Save and restore conversation context",
                    tool_names=["store_context", "retrieve_context", "list_contexts"]
                )
            ],
            tools=["store_context", "retrieve_context", "list_contexts", "delete_context"],
            tags=["context", "memory", "preservation", "required"],
            install_command="npm install @shannonai/serena-mcp",
            documentation_url="https://github.com/shannonai/serena-mcp"
        )
        self.registry.add_server(serena)

        # Sequential Thinking MCP
        sequential = MCPServer(
            name="sequential-thinking",
            version="1.0.0",
            description="Extended reasoning for complex analysis (15K+ tokens)",
            capabilities=[
                MCPCapability(
                    name="extended_reasoning",
                    description="Deep analysis with 15K+ token thinking",
                    tool_names=["think", "analyze"]
                )
            ],
            tools=["think", "analyze", "reason"],
            tags=["analysis", "reasoning", "complexity", "recommended"],
            install_command="npm install @shannonai/sequential-thinking-mcp",
            documentation_url="https://github.com/shannonai/sequential-thinking-mcp"
        )
        self.registry.add_server(sequential)

        # Context7 MCP
        context7 = MCPServer(
            name="context7",
            version="1.0.0",
            description="Framework patterns and best practices",
            capabilities=[
                MCPCapability(
                    name="framework_patterns",
                    description="Access to framework patterns and templates",
                    tool_names=["get_pattern", "search_patterns"]
                )
            ],
            tools=["get_pattern", "search_patterns", "list_patterns"],
            tags=["patterns", "frameworks", "best-practices", "recommended"],
            install_command="npm install @shannonai/context7-mcp",
            documentation_url="https://github.com/shannonai/context7-mcp"
        )
        self.registry.add_server(context7)

        # Puppeteer MCP
        puppeteer = MCPServer(
            name="puppeteer",
            version="1.0.0",
            description="Browser automation for testing",
            capabilities=[
                MCPCapability(
                    name="browser_automation",
                    description="Automated browser testing",
                    tool_names=["navigate", "click", "fill", "screenshot"]
                )
            ],
            tools=["navigate", "click", "fill", "screenshot", "evaluate"],
            tags=["testing", "browser", "automation", "recommended"],
            install_command="npm install @shannonai/puppeteer-mcp",
            documentation_url="https://github.com/shannonai/puppeteer-mcp"
        )
        self.registry.add_server(puppeteer)

        # Filesystem MCP
        filesystem = MCPServer(
            name="filesystem",
            version="1.0.0",
            description="File operations and management",
            capabilities=[
                MCPCapability(
                    name="file_operations",
                    description="Read, write, and manage files",
                    tool_names=["read_file", "write_file", "list_directory"]
                )
            ],
            tools=["read_file", "write_file", "list_directory", "create_directory"],
            tags=["filesystem", "files", "optional"],
            install_command="npm install @modelcontextprotocol/server-filesystem",
            documentation_url="https://github.com/modelcontextprotocol/servers"
        )
        self.registry.add_server(filesystem)

    def check_availability(self, mcp_names: List[str] = None) -> Dict[str, MCPStatus]:
        """
        Check availability of MCP servers.

        Args:
            mcp_names: Optional list of MCPs to check (default: all)

        Returns:
            Dictionary mapping MCP name to status
        """
        if mcp_names is None:
            mcp_names = list(self.registry.servers.keys())

        status_map = {}
        for name in mcp_names:
            server = self.registry.get_server(name)
            if server:
                # In real implementation, would check actual availability
                # For now, mark all as UNKNOWN (to be determined at runtime)
                server.status = MCPStatus.UNKNOWN
                server.last_check = datetime.now()
                status_map[name] = server.status
            else:
                status_map[name] = MCPStatus.UNAVAILABLE

        return status_map

    def recommend_for_specification(self, spec: Any) -> List[MCPRecommendation]:
        """
        Recommend MCPs based on specification.

        Args:
            spec: SpecificationObject

        Returns:
            List of MCP recommendations
        """
        recommendations = []

        # Serena is REQUIRED for all specifications
        recommendations.append(MCPRecommendation(
            mcp_name="serena",
            reason="Context preservation is mandatory for Shannon Framework",
            relevance_score=1.0,
            requirement_level=MCPRequirement.REQUIRED,
            estimated_benefit="Zero-context-loss, session persistence, checkpoint/restore",
            triggered_by="framework_requirement"
        ))

        # Check complexity for Sequential Thinking
        if hasattr(spec, 'complexity_scores'):
            overall_complexity = getattr(spec.complexity_scores, 'overall', 0.0)
            if overall_complexity >= 0.60:
                recommendations.append(MCPRecommendation(
                    mcp_name="sequential-thinking",
                    reason=f"High complexity ({overall_complexity:.1%}) benefits from extended reasoning",
                    relevance_score=min(1.0, overall_complexity * 1.2),
                    requirement_level=MCPRequirement.RECOMMENDED,
                    estimated_benefit="15K+ token thinking for complex analysis",
                    triggered_by="complexity_threshold"
                ))

        # Check domain for framework patterns
        if hasattr(spec, 'domain_percentages'):
            backend = getattr(spec.domain_percentages, 'backend', 0.0)
            frontend = getattr(spec.domain_percentages, 'frontend', 0.0)

            if backend > 0.2 or frontend > 0.2:
                recommendations.append(MCPRecommendation(
                    mcp_name="context7",
                    reason="Framework development benefits from pattern library",
                    relevance_score=max(backend, frontend),
                    requirement_level=MCPRequirement.RECOMMENDED,
                    estimated_benefit="Access to proven patterns and best practices",
                    triggered_by="framework_domain"
                ))

        # Check for testing requirements
        if hasattr(spec, 'requirements'):
            testing_keywords = ['test', 'browser', 'ui', 'frontend', 'e2e']
            has_testing = any(
                any(keyword in str(req).lower() for keyword in testing_keywords)
                for req in spec.requirements
            )

            if has_testing:
                recommendations.append(MCPRecommendation(
                    mcp_name="puppeteer",
                    reason="Testing requirements detected",
                    relevance_score=0.80,
                    requirement_level=MCPRequirement.RECOMMENDED,
                    estimated_benefit="Automated browser testing (NO MOCKS philosophy)",
                    triggered_by="testing_requirements"
                ))

        return recommendations

    def recommend_for_skill(self, skill_name: str, context: Dict[str, Any]) -> List[MCPRecommendation]:
        """
        Recommend MCPs for specific skill.

        Args:
            skill_name: Name of skill being activated
            context: Execution context

        Returns:
            List of MCP recommendations
        """
        recommendations = []

        # Skill-specific recommendations
        skill_mcp_map = {
            'spec-analysis': ['sequential-thinking', 'context7'],
            'wave-orchestration': ['serena'],
            'context-preservation': ['serena'],
            'functional-testing': ['puppeteer'],
            'memory-coordination': ['serena'],
        }

        if skill_name in skill_mcp_map:
            for mcp_name in skill_mcp_map[skill_name]:
                server = self.registry.get_server(mcp_name)
                if server:
                    recommendations.append(MCPRecommendation(
                        mcp_name=mcp_name,
                        reason=f"Skill '{skill_name}' benefits from {mcp_name}",
                        relevance_score=0.90,
                        requirement_level=MCPRequirement.RECOMMENDED,
                        estimated_benefit=server.description,
                        triggered_by=f"skill:{skill_name}"
                    ))

        return recommendations

    def recommend_for_complexity(self, complexity: float) -> List[MCPRecommendation]:
        """
        Recommend MCPs based on complexity score.

        Args:
            complexity: Overall complexity (0.0 to 1.0)

        Returns:
            List of MCP recommendations
        """
        recommendations = []

        # Sequential Thinking for high complexity
        if complexity >= 0.60:
            recommendations.append(MCPRecommendation(
                mcp_name="sequential-thinking",
                reason=f"High complexity ({complexity:.1%}) requires extended reasoning",
                relevance_score=min(1.0, complexity * 1.5),
                requirement_level=MCPRequirement.RECOMMENDED,
                estimated_benefit="Deep analysis with 15K+ token thinking",
                triggered_by="complexity_score"
            ))

        # Context7 for moderate complexity
        if complexity >= 0.40:
            recommendations.append(MCPRecommendation(
                mcp_name="context7",
                reason="Framework patterns help manage complexity",
                relevance_score=min(0.90, complexity * 1.2),
                requirement_level=MCPRequirement.OPTIONAL,
                estimated_benefit="Proven patterns reduce implementation risk",
                triggered_by="complexity_score"
            ))

        return recommendations

    def get_fallback_strategy(self, mcp_name: str) -> Dict[str, Any]:
        """
        Get fallback strategy when MCP unavailable.

        Args:
            mcp_name: MCP server name

        Returns:
            Fallback strategy dictionary
        """
        fallback_strategies = {
            'serena': {
                'strategy': 'local_storage',
                'description': 'Use local filesystem for checkpoints',
                'degradation': 'No cross-session persistence',
                'alternative': 'LocalStorage in context-manager'
            },
            'sequential-thinking': {
                'strategy': 'inline_analysis',
                'description': 'Perform analysis inline without extended thinking',
                'degradation': 'Limited to standard context window',
                'alternative': 'Regular Claude analysis'
            },
            'context7': {
                'strategy': 'web_search',
                'description': 'Search for patterns online',
                'degradation': 'Less curated, requires manual verification',
                'alternative': 'WebSearch tool'
            },
            'puppeteer': {
                'strategy': 'manual_testing',
                'description': 'Manual browser testing',
                'degradation': 'No automation, slower feedback',
                'alternative': 'User performs testing'
            },
        }

        return fallback_strategies.get(mcp_name, {
            'strategy': 'skip',
            'description': 'Skip MCP functionality',
            'degradation': 'Feature not available',
            'alternative': None
        })

    def validate_mcp_compatibility(
        self,
        required_mcps: List[str],
        available_mcps: List[str]
    ) -> Dict[str, Any]:
        """
        Validate MCP compatibility.

        Args:
            required_mcps: List of required MCP names
            available_mcps: List of available MCP names

        Returns:
            Compatibility report
        """
        available_set = set(available_mcps)
        missing_required = []
        fallback_available = []

        for mcp_name in required_mcps:
            if mcp_name not in available_set:
                missing_required.append(mcp_name)

                # Check if fallback available
                fallback = self.get_fallback_strategy(mcp_name)
                if fallback['strategy'] != 'skip':
                    fallback_available.append({
                        'mcp': mcp_name,
                        'fallback': fallback
                    })

        # Determine compatibility status
        if not missing_required:
            status = 'compatible'
        elif fallback_available:
            status = 'degraded'
        else:
            status = 'incompatible'

        return {
            'status': status,
            'missing_required': missing_required,
            'fallback_available': fallback_available,
            'can_proceed': status != 'incompatible',
            'warnings': [
                f"MCP '{fb['mcp']}' unavailable, using fallback: {fb['fallback']['strategy']}"
                for fb in fallback_available
            ]
        }

    def get_installation_instructions(self, mcp_name: str) -> Optional[str]:
        """
        Get installation instructions for MCP.

        Args:
            mcp_name: MCP server name

        Returns:
            Installation instructions or None
        """
        server = self.registry.get_server(mcp_name)
        if not server:
            return None

        instructions = f"""
# Installing {server.name}

{server.description}

## Installation
```bash
{server.install_command or 'Installation command not available'}
```

## Documentation
{server.documentation_url or 'Documentation not available'}

## Capabilities
"""
        for capability in server.capabilities:
            instructions += f"- {capability.name}: {capability.description}\n"

        return instructions
