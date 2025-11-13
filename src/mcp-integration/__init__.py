"""
Shannon Framework v4 - MCP Integration Layer

Purpose: Dynamic MCP discovery, progressive recommendation, and orchestration.

Components:
  - MCPDiscovery: MCP detection and recommendation
  - MCPRegistry: Catalog of known MCPs
  - MCPServer: MCP server definition
  - MCPRecommendation: Context-based recommendation

Integration Patterns:
  1. Declarative: Static frontmatter declarations
  2. Progressive: Dynamic recommendations by context
  3. Fallback: Graceful degradation when unavailable
  4. Orchestration: Multi-MCP coordination

Known MCPs:
  - serena (REQUIRED): Context preservation
  - sequential-thinking (RECOMMENDED): Extended reasoning
  - context7 (RECOMMENDED): Framework patterns
  - puppeteer (RECOMMENDED): Browser automation
  - filesystem (OPTIONAL): File operations

Recommendation Triggers:
  - Complexity ≥ 60%: sequential-thinking
  - Framework domain: context7
  - Testing requirements: puppeteer
  - Always: serena (mandatory)

Fallback Strategies:
  - serena → local storage (degraded)
  - sequential-thinking → inline analysis
  - context7 → web search
  - puppeteer → manual testing

Author: Shannon Framework Team
Version: 1.0.0
License: MIT
"""

from .models import (
    MCPServer,
    MCPRegistry,
    MCPRecommendation,
    MCPDependency,
    MCPOrchestrationPlan,
    MCPCapability,
    MCPStatus,
    MCPRequirement,
    MCPPattern,
)
from .discovery import MCPDiscovery

__all__ = [
    # Discovery
    'MCPDiscovery',

    # Models
    'MCPServer',
    'MCPRegistry',
    'MCPRecommendation',
    'MCPDependency',
    'MCPOrchestrationPlan',
    'MCPCapability',

    # Enums
    'MCPStatus',
    'MCPRequirement',
    'MCPPattern',
]

__version__ = '1.0.0'


# Convenience functions

def discover_mcps() -> MCPDiscovery:
    """
    Create MCP discovery instance with known MCPs.

    Returns:
        MCPDiscovery instance
    """
    return MCPDiscovery()


def check_mcp_requirements(
    required_mcps: list,
    available_mcps: list
) -> dict:
    """
    Check MCP requirements.

    Args:
        required_mcps: List of required MCP names
        available_mcps: List of available MCP names

    Returns:
        Compatibility report
    """
    discovery = MCPDiscovery()
    return discovery.validate_mcp_compatibility(required_mcps, available_mcps)


def get_recommended_mcps(specification: object) -> list:
    """
    Get recommended MCPs for specification.

    Args:
        specification: SpecificationObject

    Returns:
        List of MCPRecommendation objects
    """
    discovery = MCPDiscovery()
    return discovery.recommend_for_specification(specification)
