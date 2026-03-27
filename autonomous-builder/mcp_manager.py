"""
MCP Manager for Autonomous Claude Code Builder.

Handles dynamic MCP discovery, installation, and skill generation.
Maps task types to required MCPs and manages their lifecycle.
"""

import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any
from pathlib import Path
import logging

from .config import MCPConfig

logger = logging.getLogger(__name__)


@dataclass
class MCPStatus:
    """Status of an MCP server."""
    name: str
    installed: bool
    available: bool
    version: Optional[str] = None
    error: Optional[str] = None


@dataclass
class MCPRequirement:
    """Requirement analysis result."""
    mcp_name: str
    reason: str
    priority: int  # 1=required, 2=recommended, 3=optional
    task_types: List[str] = field(default_factory=list)


class MCPManager:
    """
    Manages MCP discovery, installation, and skill generation.

    Responsibilities:
    - Analyze tasks to determine required MCPs
    - Check MCP availability
    - Install MCPs dynamically
    - Generate usage skills for installed MCPs
    """

    # Task type to MCP mapping
    MCP_MAPPING: Dict[str, List[str]] = {
        # Web & Browser
        "web_scraping": ["puppeteer"],
        "web_automation": ["puppeteer"],
        "browser_testing": ["puppeteer"],
        "ui_testing": ["puppeteer"],
        "screenshot": ["puppeteer"],

        # Code & Development
        "code_analysis": ["serena"],
        "codebase_context": ["serena"],
        "symbol_search": ["serena"],
        "semantic_code": ["serena"],

        # File Operations
        "file_operations": ["filesystem"],
        "file_management": ["filesystem"],

        # Version Control
        "github": ["github"],
        "git_operations": ["github"],
        "pull_request": ["github"],
        "issue_management": ["github"],

        # Research & Search
        "web_search": ["tavily", "perplexity"],
        "research": ["tavily", "perplexity"],
        "documentation_lookup": ["context7"],

        # Data & APIs
        "api_testing": ["fetch"],
        "http_requests": ["fetch"],
        "rest_api": ["fetch"],

        # Database
        "sqlite": ["sqlite"],
        "postgres": ["postgres"],
        "database": ["sqlite"],  # Default

        # Memory
        "memory": ["serena"],  # Use Serena, NOT open memory
        "context_persistence": ["serena"],
    }

    # MCP installation commands
    MCP_INSTALL_COMMANDS: Dict[str, Dict[str, Any]] = {
        "serena": {
            "command": "uvx",
            "args": ["--from", "git+https://github.com/oraios/serena", "serena", "--version"],
            "install": ["uv", "tool", "install", "git+https://github.com/oraios/serena"],
            "check": ["uvx", "--from", "git+https://github.com/oraios/serena", "serena", "--help"]
        },
        "puppeteer": {
            "command": "npx",
            "args": ["-y", "@anthropic-ai/puppeteer-mcp-server", "--version"],
            "install": ["npm", "install", "-g", "@anthropic-ai/puppeteer-mcp-server"],
            "check": ["npx", "-y", "@anthropic-ai/puppeteer-mcp-server", "--help"]
        },
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "--help"],
            "install": ["npm", "install", "-g", "@modelcontextprotocol/server-filesystem"],
            "check": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "--help"]
        },
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github", "--help"],
            "install": ["npm", "install", "-g", "@modelcontextprotocol/server-github"],
            "check": ["npx", "-y", "@modelcontextprotocol/server-github", "--help"]
        },
        "fetch": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-fetch", "--help"],
            "install": ["npm", "install", "-g", "@modelcontextprotocol/server-fetch"],
            "check": ["npx", "-y", "@modelcontextprotocol/server-fetch", "--help"]
        },
        "tavily": {
            "command": "npx",
            "args": ["-y", "tavily-mcp-server", "--help"],
            "install": ["npm", "install", "-g", "tavily-mcp-server"],
            "check": ["npx", "-y", "tavily-mcp-server", "--help"]
        },
        "sqlite": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-sqlite", "--help"],
            "install": ["npm", "install", "-g", "@modelcontextprotocol/server-sqlite"],
            "check": ["npx", "-y", "@modelcontextprotocol/server-sqlite", "--help"]
        }
    }

    # Keywords for task detection
    TASK_KEYWORDS: Dict[str, List[str]] = {
        "web_scraping": ["scrape", "crawl", "extract from web", "web data"],
        "web_automation": ["automate browser", "click", "form", "navigate"],
        "browser_testing": ["browser test", "e2e test", "end-to-end", "ui test"],
        "ui_testing": ["visual test", "screenshot", "ui verification"],
        "code_analysis": ["analyze code", "understand codebase", "code structure"],
        "github": ["github", "pull request", "pr", "issue", "repository"],
        "web_search": ["search web", "look up", "find information", "research"],
        "api_testing": ["api", "endpoint", "rest", "http request"],
        "database": ["database", "sql", "query", "store data"],
        "file_operations": ["read file", "write file", "create file", "file system"],
    }

    def __init__(self, project_dir: Optional[Path] = None):
        """
        Initialize MCP Manager.

        Args:
            project_dir: Project directory for context
        """
        self.project_dir = project_dir
        self.installed_mcps: Set[str] = set()
        self.available_mcps: Set[str] = set()
        self.skill_cache: Dict[str, str] = {}

    async def analyze_task(self, task: str) -> List[MCPRequirement]:
        """
        Analyze a task to determine required MCPs.

        Args:
            task: Task description in natural language

        Returns:
            List of MCPRequirement objects sorted by priority
        """
        task_lower = task.lower()
        requirements: Dict[str, MCPRequirement] = {}

        # Detect task types from keywords
        detected_types: Set[str] = set()
        for task_type, keywords in self.TASK_KEYWORDS.items():
            for keyword in keywords:
                if keyword in task_lower:
                    detected_types.add(task_type)
                    break

        # Always require serena for codebase context
        requirements["serena"] = MCPRequirement(
            mcp_name="serena",
            reason="Required for codebase context and memory (NOT open memory)",
            priority=1,
            task_types=["codebase_context", "memory"]
        )

        # Map detected types to MCPs
        for task_type in detected_types:
            mcps = self.MCP_MAPPING.get(task_type, [])
            for mcp in mcps:
                if mcp not in requirements:
                    requirements[mcp] = MCPRequirement(
                        mcp_name=mcp,
                        reason=f"Recommended for {task_type}",
                        priority=2,
                        task_types=[task_type]
                    )
                else:
                    requirements[mcp].task_types.append(task_type)

        # Check for web UI tasks - require puppeteer
        web_ui_keywords = ["web app", "website", "frontend", "react", "vue", "angular", "ui"]
        if any(kw in task_lower for kw in web_ui_keywords):
            if "puppeteer" not in requirements:
                requirements["puppeteer"] = MCPRequirement(
                    mcp_name="puppeteer",
                    reason="Required for web UI visual verification",
                    priority=1,
                    task_types=["ui_testing", "browser_testing"]
                )
            else:
                requirements["puppeteer"].priority = 1

        # Sort by priority
        return sorted(requirements.values(), key=lambda r: r.priority)

    async def check_mcp_available(self, mcp_name: str) -> MCPStatus:
        """
        Check if an MCP is available/installed.

        Args:
            mcp_name: Name of the MCP

        Returns:
            MCPStatus with availability info
        """
        if mcp_name not in self.MCP_INSTALL_COMMANDS:
            return MCPStatus(
                name=mcp_name,
                installed=False,
                available=False,
                error=f"Unknown MCP: {mcp_name}"
            )

        config = self.MCP_INSTALL_COMMANDS[mcp_name]
        check_cmd = config.get("check", [config["command"]] + config["args"])

        try:
            process = await asyncio.create_subprocess_exec(
                *check_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=30.0
            )

            if process.returncode == 0:
                self.available_mcps.add(mcp_name)
                return MCPStatus(
                    name=mcp_name,
                    installed=True,
                    available=True
                )
            else:
                return MCPStatus(
                    name=mcp_name,
                    installed=False,
                    available=False,
                    error=stderr.decode() if stderr else "Check failed"
                )

        except asyncio.TimeoutError:
            return MCPStatus(
                name=mcp_name,
                installed=False,
                available=False,
                error="Check timed out"
            )
        except FileNotFoundError:
            return MCPStatus(
                name=mcp_name,
                installed=False,
                available=False,
                error="Command not found"
            )
        except Exception as e:
            return MCPStatus(
                name=mcp_name,
                installed=False,
                available=False,
                error=str(e)
            )

    async def install_mcp(self, mcp_name: str) -> bool:
        """
        Install an MCP if not already installed.

        Args:
            mcp_name: Name of the MCP to install

        Returns:
            True if installed successfully or already installed
        """
        # Check if already available
        status = await self.check_mcp_available(mcp_name)
        if status.available:
            logger.info(f"MCP {mcp_name} already available")
            return True

        if mcp_name not in self.MCP_INSTALL_COMMANDS:
            logger.error(f"Unknown MCP: {mcp_name}")
            return False

        config = self.MCP_INSTALL_COMMANDS[mcp_name]
        install_cmd = config.get("install")

        if not install_cmd:
            logger.error(f"No install command for MCP: {mcp_name}")
            return False

        logger.info(f"Installing MCP: {mcp_name}")

        try:
            process = await asyncio.create_subprocess_exec(
                *install_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=300.0  # 5 minute timeout for installation
            )

            if process.returncode == 0:
                self.installed_mcps.add(mcp_name)
                self.available_mcps.add(mcp_name)
                logger.info(f"Successfully installed MCP: {mcp_name}")
                return True
            else:
                logger.error(f"Failed to install MCP {mcp_name}: {stderr.decode()}")
                return False

        except asyncio.TimeoutError:
            logger.error(f"Installation timed out for MCP: {mcp_name}")
            return False
        except Exception as e:
            logger.error(f"Failed to install MCP {mcp_name}: {e}")
            return False

    async def ensure_mcps(self, requirements: List[MCPRequirement]) -> Dict[str, bool]:
        """
        Ensure all required MCPs are installed.

        Args:
            requirements: List of MCP requirements

        Returns:
            Dictionary mapping MCP names to installation success
        """
        results = {}

        # Process in priority order
        for req in requirements:
            if req.priority == 1:  # Required
                success = await self.install_mcp(req.mcp_name)
                results[req.mcp_name] = success
                if not success:
                    logger.warning(f"Failed to install required MCP: {req.mcp_name}")
            else:  # Recommended/Optional
                status = await self.check_mcp_available(req.mcp_name)
                results[req.mcp_name] = status.available
                if not status.available:
                    logger.info(f"Optional MCP not available: {req.mcp_name}")

        return results

    def generate_usage_skill(self, mcp_name: str) -> str:
        """
        Generate a usage skill document for an MCP.

        Args:
            mcp_name: Name of the MCP

        Returns:
            Skill document in markdown format
        """
        if mcp_name in self.skill_cache:
            return self.skill_cache[mcp_name]

        # Generate skill based on MCP type
        skill = self._generate_skill_template(mcp_name)
        self.skill_cache[mcp_name] = skill
        return skill

    def _generate_skill_template(self, mcp_name: str) -> str:
        """Generate skill template for MCP."""
        templates = {
            "serena": SERENA_SKILL,
            "puppeteer": PUPPETEER_SKILL,
            "filesystem": FILESYSTEM_SKILL,
            "github": GITHUB_SKILL,
            "fetch": FETCH_SKILL,
        }

        return templates.get(mcp_name, self._generate_generic_skill(mcp_name))

    def _generate_generic_skill(self, mcp_name: str) -> str:
        """Generate generic skill for unknown MCP."""
        return f"""# {mcp_name.title()} MCP Usage Skill

## Overview
This skill documents the usage of the {mcp_name} MCP server.

## Available Tools
Tools are accessed via `mcp__{mcp_name}__<tool_name>`.

## Usage Pattern
1. Check MCP is available
2. Use appropriate tools for your task
3. Handle errors gracefully

## Notes
- Refer to official MCP documentation for complete tool list
- Test tool availability before relying on specific features
"""

    def get_mcp_config(self, mcp_name: str) -> Optional[MCPConfig]:
        """
        Get MCPConfig for a specific MCP.

        Args:
            mcp_name: Name of the MCP

        Returns:
            MCPConfig or None if not found
        """
        if mcp_name not in self.MCP_INSTALL_COMMANDS:
            return None

        install_info = self.MCP_INSTALL_COMMANDS[mcp_name]
        return MCPConfig(
            name=mcp_name,
            command=install_info["command"],
            # Only the first two arguments are used here because MCPConfig expects at most two arguments
            # for MCP startup based on the current design of MCP_INSTALL_COMMANDS. The first two args
            # typically represent the main execution command and its primary argument (e.g., ["uvx", "serena"]).
            # If future MCPs require more arguments, this logic should be revisited.
            args=install_info["args"][:2] if install_info["args"] else [],
            required=mcp_name == "serena"
        )

    def get_available_mcps(self) -> List[str]:
        """Get list of available MCPs."""
        return list(self.available_mcps)


# Skill Templates

SERENA_SKILL = """# Serena MCP Usage Skill

## Overview
Serena provides semantic code analysis and codebase memory.
Use Serena for ALL codebase context - NOT open memory.

## Key Tools
- `mcp__serena__find_symbol` - Locate code symbols semantically
- `mcp__serena__find_referencing_symbols` - Find code dependencies
- `mcp__serena__insert_after_symbol` - Precise code insertion
- `mcp__serena__read_memory` - Retrieve persistent memory
- `mcp__serena__write_memory` - Store memory for future sessions

## Memory System
Memories stored in `.serena/memories/` directory.
Use for cross-session state persistence.

## Usage Pattern
1. Query codebase structure before modifications
2. Find symbols rather than text search when possible
3. Store important context in memory for future sessions
4. Create execution summaries before session end

## Best Practices
- Always use Serena for codebase context, not grep/find
- Store session progress in memory
- Use symbol-level operations for precision
"""

PUPPETEER_SKILL = """# Puppeteer MCP Usage Skill

## Overview
Browser automation for visual testing and verification.

## Key Tools
- `mcp__puppeteer__puppeteer_navigate` - Navigate to URL
- `mcp__puppeteer__puppeteer_screenshot` - Capture screenshot
- `mcp__puppeteer__puppeteer_click` - Click element
- `mcp__puppeteer__puppeteer_fill` - Fill form field
- `mcp__puppeteer__puppeteer_select` - Select dropdown
- `mcp__puppeteer__puppeteer_hover` - Hover element
- `mcp__puppeteer__puppeteer_evaluate` - Run JavaScript

## Usage Pattern
1. Navigate to target page
2. Wait for elements to load
3. Interact like a human user
4. Take screenshots for verification

## Best Practices
- Test like a human with mouse and keyboard
- Don't take shortcuts with JavaScript evaluation
- Use screenshots to verify visual changes
- Handle dynamic content with appropriate waits
"""

FILESYSTEM_SKILL = """# Filesystem MCP Usage Skill

## Overview
Secure file system operations within project boundaries.

## Key Tools
- `mcp__filesystem__read_file` - Read file contents
- `mcp__filesystem__write_file` - Write file contents
- `mcp__filesystem__list_directory` - List directory contents
- `mcp__filesystem__create_directory` - Create directory
- `mcp__filesystem__move_file` - Move/rename file
- `mcp__filesystem__search_files` - Search for files

## Security
Operations restricted to project directory.
Cannot access files outside allowed paths.

## Best Practices
- Use relative paths within project
- Check file existence before operations
- Handle errors for missing files
"""

GITHUB_SKILL = """# GitHub MCP Usage Skill

## Overview
GitHub operations including repos, PRs, and issues.

## Key Tools
- `mcp__github__create_repository` - Create new repo
- `mcp__github__create_pull_request` - Create PR
- `mcp__github__create_issue` - Create issue
- `mcp__github__search_repositories` - Search repos
- `mcp__github__get_file_contents` - Get file from repo
- `mcp__github__push_files` - Push files to repo

## Authentication
Requires GITHUB_TOKEN environment variable.

## Best Practices
- Use meaningful PR/issue titles
- Include detailed descriptions
- Link related issues/PRs
"""

FETCH_SKILL = """# Fetch MCP Usage Skill

## Overview
HTTP requests for API testing and web content retrieval.

## Key Tools
- `mcp__fetch__fetch` - Make HTTP request

## Usage Pattern
1. Specify URL and method
2. Include headers if needed
3. Handle response appropriately

## Best Practices
- Use appropriate HTTP methods
- Handle errors and timeouts
- Respect rate limits
"""
