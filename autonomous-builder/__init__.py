"""
Autonomous Claude Code Builder

An intelligent system that researches capabilities, installs necessary MCPs,
and executes build tasks with full contextual awareness of existing codebases.

Based on:
- Claude Quickstart autonomous-coding patterns
- Anthropic's effective harnesses for long-running agents
- Claude Code Builder multi-agent architecture
- Shannon Framework orchestration
"""

__version__ = "1.0.0"
__author__ = "Shannon Framework Team"

from .builder import AutonomousBuilder
from .config import BuilderConfig
from .scenario_handler import ScenarioHandler, Scenario
from .xml_transformer import XMLPromptTransformer
from .security import SecurityManager
from .mcp_manager import MCPManager
from .serena_context import SerenaContextManager

__all__ = [
    "AutonomousBuilder",
    "BuilderConfig",
    "ScenarioHandler",
    "Scenario",
    "XMLPromptTransformer",
    "SecurityManager",
    "MCPManager",
    "SerenaContextManager",
]
