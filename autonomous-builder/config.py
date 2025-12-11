"""
Configuration for Autonomous Claude Code Builder.

Provides configuration management for the builder system including
MCP settings, security rules, and execution parameters.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
import yaml


@dataclass
class MCPConfig:
    """Configuration for an MCP server."""
    name: str
    command: str
    args: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    required: bool = False
    description: str = ""


@dataclass
class SecurityConfig:
    """Security configuration for command execution."""
    allowed_commands: List[str] = field(default_factory=list)
    commands_needing_validation: List[str] = field(default_factory=list)
    sandbox_enabled: bool = True
    allow_network: bool = True
    restricted_paths: List[str] = field(default_factory=list)


@dataclass
class ExecutionConfig:
    """Execution parameters for the builder."""
    max_iterations: Optional[int] = None
    auto_continue_delay_seconds: float = 3.0
    max_cost_usd: Optional[float] = None
    max_tokens: Optional[int] = None
    model: str = "claude-sonnet-4-5-20250929"
    halt_on_error: bool = False
    checkpoint_frequency: int = 1  # Create checkpoint every N waves


@dataclass
class BuilderConfig:
    """
    Main configuration for the Autonomous Builder.

    Attributes:
        target_dir: Directory to build in
        mcps: MCP server configurations
        security: Security settings
        execution: Execution parameters
        serena_enabled: Use Serena MCP for codebase context
        puppeteer_enabled: Use Puppeteer for visual verification
        verbose: Enable verbose logging
    """

    target_dir: Path
    mcps: Dict[str, MCPConfig] = field(default_factory=dict)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    execution: ExecutionConfig = field(default_factory=ExecutionConfig)
    serena_enabled: bool = True
    puppeteer_enabled: bool = True
    verbose: bool = False

    def __post_init__(self):
        """Initialize default configurations."""
        if isinstance(self.target_dir, str):
            self.target_dir = Path(self.target_dir)

        # Set default allowed commands if not provided
        if not self.security.allowed_commands:
            self.security.allowed_commands = DEFAULT_ALLOWED_COMMANDS.copy()

        if not self.security.commands_needing_validation:
            self.security.commands_needing_validation = DEFAULT_VALIDATION_COMMANDS.copy()

        # Set default MCPs if not provided
        if not self.mcps:
            self.mcps = self._get_default_mcps()

    def _get_default_mcps(self) -> Dict[str, MCPConfig]:
        """Get default MCP configurations."""
        mcps = {}

        # Serena MCP (required for codebase context)
        if self.serena_enabled:
            mcps["serena"] = MCPConfig(
                name="serena",
                command="uvx",
                args=[
                    "--from", "git+https://github.com/oraios/serena",
                    "serena", "start-mcp-server"
                ],
                env={"SERENA_PROJECT_ROOT": str(self.target_dir)},
                required=True,
                description="Semantic code analysis and codebase memory"
            )

        # Puppeteer MCP (for visual verification)
        if self.puppeteer_enabled:
            mcps["puppeteer"] = MCPConfig(
                name="puppeteer",
                command="npx",
                args=["-y", "@anthropic-ai/puppeteer-mcp-server"],
                env={"PUPPETEER_HEADLESS": "true"},
                required=False,
                description="Browser automation for visual testing"
            )

        # Filesystem MCP
        mcps["filesystem"] = MCPConfig(
            name="filesystem",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", str(self.target_dir)],
            required=False,
            description="File system operations"
        )

        return mcps

    def to_mcp_servers_config(self) -> Dict[str, Any]:
        """Convert to MCP servers configuration format for SDK."""
        config = {}
        for name, mcp in self.mcps.items():
            config[name] = {
                "command": mcp.command,
                "args": mcp.args,
            }
            if mcp.env:
                config[name]["env"] = mcp.env
        return config

    @classmethod
    def from_yaml(cls, path: Path) -> "BuilderConfig":
        """Load configuration from YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls._from_dict(data)

    @classmethod
    def from_json(cls, path: Path) -> "BuilderConfig":
        """Load configuration from JSON file."""
        with open(path) as f:
            data = json.load(f)
        return cls._from_dict(data)

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> "BuilderConfig":
        """Create config from dictionary."""
        # Parse MCPs
        mcps = {}
        for name, mcp_data in data.get("mcps", {}).items():
            mcps[name] = MCPConfig(
                name=name,
                command=mcp_data.get("command", ""),
                args=mcp_data.get("args", []),
                env=mcp_data.get("env", {}),
                required=mcp_data.get("required", False),
                description=mcp_data.get("description", "")
            )

        # Parse security config
        security_data = data.get("security", {})
        security = SecurityConfig(
            allowed_commands=security_data.get("allowed_commands", []),
            commands_needing_validation=security_data.get("commands_needing_validation", []),
            sandbox_enabled=security_data.get("sandbox_enabled", True),
            allow_network=security_data.get("allow_network", True),
            restricted_paths=security_data.get("restricted_paths", [])
        )

        # Parse execution config
        exec_data = data.get("execution", {})
        execution = ExecutionConfig(
            max_iterations=exec_data.get("max_iterations"),
            auto_continue_delay_seconds=exec_data.get("auto_continue_delay_seconds", 3.0),
            max_cost_usd=exec_data.get("max_cost_usd"),
            max_tokens=exec_data.get("max_tokens"),
            model=exec_data.get("model", "claude-sonnet-4-5-20250929"),
            halt_on_error=exec_data.get("halt_on_error", False),
            checkpoint_frequency=exec_data.get("checkpoint_frequency", 1)
        )

        return cls(
            target_dir=Path(data.get("target_dir", ".")),
            mcps=mcps,
            security=security,
            execution=execution,
            serena_enabled=data.get("serena_enabled", True),
            puppeteer_enabled=data.get("puppeteer_enabled", True),
            verbose=data.get("verbose", False)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "target_dir": str(self.target_dir),
            "mcps": {
                name: {
                    "command": mcp.command,
                    "args": mcp.args,
                    "env": mcp.env,
                    "required": mcp.required,
                    "description": mcp.description
                }
                for name, mcp in self.mcps.items()
            },
            "security": {
                "allowed_commands": self.security.allowed_commands,
                "commands_needing_validation": self.security.commands_needing_validation,
                "sandbox_enabled": self.security.sandbox_enabled,
                "allow_network": self.security.allow_network,
                "restricted_paths": self.security.restricted_paths
            },
            "execution": {
                "max_iterations": self.execution.max_iterations,
                "auto_continue_delay_seconds": self.execution.auto_continue_delay_seconds,
                "max_cost_usd": self.execution.max_cost_usd,
                "max_tokens": self.execution.max_tokens,
                "model": self.execution.model,
                "halt_on_error": self.execution.halt_on_error,
                "checkpoint_frequency": self.execution.checkpoint_frequency
            },
            "serena_enabled": self.serena_enabled,
            "puppeteer_enabled": self.puppeteer_enabled,
            "verbose": self.verbose
        }


# Default allowed commands (from Claude Quickstart security model)
DEFAULT_ALLOWED_COMMANDS = [
    # File inspection
    "ls", "cat", "head", "tail", "wc", "grep", "find", "file",
    # File operations
    "cp", "mkdir", "chmod", "rm", "mv", "touch",
    # Directory
    "pwd", "cd",
    # Development - Node/JS
    "npm", "node", "npx", "yarn", "pnpm", "bun",
    # Development - Python
    "python", "python3", "pip", "pip3", "uv", "poetry", "pipenv",
    # Development - Rust
    "cargo", "rustc", "rustup",
    # Development - Go
    "go",
    # Development - Java
    "java", "javac", "gradle", "mvn", "maven",
    # Development - Ruby
    "ruby", "gem", "bundle", "bundler",
    # Development - Other
    "make", "cmake",
    # Version control
    "git",
    # Process management
    "ps", "lsof", "sleep", "pkill", "kill",
    # Network (limited)
    "curl", "wget",
    # Scripts
    "init.sh", "setup.sh", "build.sh", "test.sh",
    # Utilities
    "echo", "printf", "date", "env", "which", "type",
]

# Commands requiring extra validation
DEFAULT_VALIDATION_COMMANDS = [
    "pkill",  # Must target dev processes only
    "kill",   # Must target dev processes only
    "chmod",  # Only specific modes allowed
    "rm",     # Validate paths
    "curl",   # Validate URLs
    "wget",   # Validate URLs
]
