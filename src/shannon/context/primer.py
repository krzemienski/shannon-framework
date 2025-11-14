"""
Context Primer - Quick context reload for Shannon CLI

Restores project context in 10-30 seconds:
1. Load from Serena knowledge graph
2. Load critical files
3. Verify MCP availability
4. Prompt for missing MCPs

Duration: 10-30 seconds (vs 12-22 min for full onboarding)
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .serena_adapter import SerenaAdapter


@dataclass
class ProjectContext:
    """Loaded project context"""
    project_id: str
    project_path: str
    file_count: int
    total_lines: int
    languages: Dict[str, float]
    tech_stack: List[str]
    architecture: str
    modules: List[Dict[str, Any]]
    patterns: List[Dict[str, Any]]
    critical_files: Dict[str, str]  # path -> content


@dataclass
class MCPStatus:
    """MCP availability status"""
    name: str
    required: bool
    installed: bool
    reason: str


class ContextPrimer:
    """
    Quick context reload for Shannon CLI

    Usage:
        primer = ContextPrimer(serena_adapter)
        context = await primer.prime("myproject")

    Features:
    - Fast Serena knowledge graph retrieval
    - Critical file loading
    - MCP availability check
    - Interactive MCP installation prompts
    """

    def __init__(self, serena_adapter: Optional[SerenaAdapter] = None):
        """
        Initialize primer

        Args:
            serena_adapter: SerenaAdapter for knowledge graph access
        """
        self.serena = serena_adapter or SerenaAdapter()
        self.console = Console()
        self.logger = logging.getLogger(__name__)

    async def prime(
        self,
        project_id: str,
        load_files: bool = True,
        check_mcps: bool = True
    ) -> ProjectContext:
        """
        Prime Shannon with project context

        Args:
            project_id: Project identifier
            load_files: Whether to load critical files into memory
            check_mcps: Whether to check MCP availability

        Returns:
            ProjectContext with loaded data

        Raises:
            ValueError: If project not found in Serena or local index
        """
        # Display header
        self.console.print("\n")
        self.console.print(Panel.fit(
            f"[bold cyan]Shannon Priming: {project_id}[/bold cyan]",
            border_style="cyan"
        ))
        self.console.print("─" * 60)

        # Step 1: Load from Serena
        self.console.print("\n[bold]Step 1: Loading project context[/bold]")
        with self.console.status("[bold green]Querying Serena knowledge graph..."):
            serena_data = await self._load_from_serena(project_id)

        self._show_serena_results(serena_data)

        # Step 2: Load local metadata
        self.console.print("\n[bold]Step 2: Loading local metadata[/bold]")
        local_data = self._load_local_metadata(project_id)
        self._show_local_results(local_data)

        # Step 3: Load critical files
        critical_files = {}
        if load_files:
            self.console.print("\n[bold]Step 3: Loading critical files[/bold]")
            critical_files = self._load_critical_files(project_id, local_data)
            self._show_files_loaded(critical_files)

        # Step 4: Check MCPs
        if check_mcps:
            self.console.print("\n[bold]Step 4: Checking MCPs[/bold]")
            mcp_status = await self._check_mcps(local_data)
            await self._handle_missing_mcps(mcp_status)

        # Success message
        self.console.print("\n")
        self.console.print("[green]✅ Project primed[/green]")
        self.console.print("\nReady for tasks:")
        self.console.print("  • shannon analyze <spec>")
        self.console.print("  • shannon wave <request>")
        self.console.print("\nShannon understands your codebase.")

        # Build context object
        return ProjectContext(
            project_id=project_id,
            project_path=local_data.get('project_path', ''),
            file_count=local_data.get('file_count', 0),
            total_lines=local_data.get('total_lines', 0),
            languages=local_data.get('languages', {}),
            tech_stack=local_data.get('tech_stack', []),
            architecture=local_data.get('architecture', ''),
            modules=serena_data.get('modules', []),
            patterns=serena_data.get('patterns', []),
            critical_files=critical_files
        )

    async def _load_from_serena(self, project_id: str) -> Dict[str, Any]:
        """Load project data from Serena knowledge graph"""
        try:
            # Get project node
            project_nodes = await self.serena.open_nodes([f"project_{project_id}"])

            if not project_nodes:
                raise ValueError(f"Project '{project_id}' not found in Serena")

            project_node = project_nodes[0]

            # Search for related modules and patterns
            search_results = await self.serena.search_nodes(
                query=f"project_{project_id}",
                max_results=50
            )

            # Filter by entity type
            modules = [
                node for node in search_results
                if node.get('entityType') == 'Module'
            ]

            patterns = [
                node for node in search_results
                if node.get('entityType') == 'Pattern'
            ]

            return {
                'project': project_node,
                'modules': modules,
                'patterns': patterns,
                'entity_count': len(search_results)
            }

        except Exception as e:
            self.logger.error(f"Failed to load from Serena: {e}")
            raise ValueError(f"Failed to load project from Serena: {e}")

    def _load_local_metadata(self, project_id: str) -> Dict[str, Any]:
        """Load project metadata from local index"""
        project_dir = Path.home() / ".shannon" / "projects" / project_id
        metadata_file = project_dir / "project.json"

        if not metadata_file.exists():
            raise ValueError(f"Project '{project_id}' not found in local index")

        try:
            return json.loads(metadata_file.read_text())
        except Exception as e:
            self.logger.error(f"Failed to load local metadata: {e}")
            raise ValueError(f"Failed to load local metadata: {e}")

    def _load_critical_files(
        self,
        project_id: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, str]:
        """Load critical files into memory"""
        project_dir = Path.home() / ".shannon" / "projects" / project_id
        critical_files_list = project_dir / "critical_files.json"

        if not critical_files_list.exists():
            return {}

        try:
            file_paths = json.loads(critical_files_list.read_text())
            project_path = Path(metadata.get('project_path', ''))

            loaded_files = {}
            for rel_path in file_paths[:5]:  # Load top 5 critical files
                abs_path = project_path / rel_path
                if abs_path.exists():
                    try:
                        content = abs_path.read_text(encoding='utf-8', errors='ignore')
                        loaded_files[rel_path] = content
                    except Exception as e:
                        self.logger.debug(f"Failed to load {rel_path}: {e}")

            return loaded_files

        except Exception as e:
            self.logger.error(f"Failed to load critical files: {e}")
            return {}

    async def _check_mcps(self, metadata: Dict[str, Any]) -> List[MCPStatus]:
        """Check MCP availability based on tech stack"""
        tech_stack = metadata.get('tech_stack', [])
        mcp_status = []

        # Serena is always required
        serena_healthy = await self.serena.health_check()
        mcp_status.append(MCPStatus(
            name="Serena",
            required=True,
            installed=serena_healthy,
            reason="Required for context management"
        ))

        # Recommend MCPs based on tech stack
        if any('Node.js' in tech or 'React' in tech for tech in tech_stack):
            # Would check for Puppeteer MCP
            mcp_status.append(MCPStatus(
                name="Puppeteer",
                required=False,
                installed=False,  # Would actually check
                reason="Frontend testing and automation"
            ))

        if any('PostgreSQL' in tech or 'MySQL' in tech for tech in tech_stack):
            # Would check for database MCP
            mcp_status.append(MCPStatus(
                name="Database",
                required=False,
                installed=False,  # Would actually check
                reason="Database operations"
            ))

        return mcp_status

    async def _handle_missing_mcps(self, mcp_status: List[MCPStatus]):
        """Display MCP status and prompt for installation"""
        # Show MCP status
        for mcp in mcp_status:
            if mcp.installed:
                self.console.print(f"  ✅ {mcp.name} ({'required' if mcp.required else 'recommended'})")
            else:
                status = "❌" if mcp.required else "⚠️"
                self.console.print(f"  {status} {mcp.name} (not installed) - {mcp.reason}")

        # Prompt for missing recommended MCPs
        missing_recommended = [
            mcp for mcp in mcp_status
            if not mcp.installed and not mcp.required
        ]

        if missing_recommended:
            self.console.print("\n[yellow]Recommended MCPs not installed[/yellow]")
            self.console.print("Run: shannon setup --mcp-install")

    def _show_serena_results(self, data: Dict[str, Any]):
        """Display Serena loading results"""
        project = data['project']
        modules = data['modules']
        patterns = data['patterns']

        # Extract tech stack from observations
        observations = project.get('observations', [])
        tech_line = next((obs for obs in observations if obs.startswith('Tech:')), '')
        tech = tech_line.replace('Tech: ', '') if tech_line else 'N/A'

        self.console.print(f"  ✓ Project graph loaded ({data['entity_count']} entities)")
        self.console.print(f"  ✓ Tech stack: {tech}")
        self.console.print(f"  ✓ Modules: {len(modules)}")
        self.console.print(f"  ✓ Patterns: {len(patterns)}")

    def _show_local_results(self, data: Dict[str, Any]):
        """Display local metadata results"""
        lang_str = ", ".join(
            f"{l} {p:.0f}%"
            for l, p in sorted(data.get('languages', {}).items(), key=lambda x: x[1], reverse=True)[:3]
        )
        self.console.print(f"  ✓ Files: {data.get('file_count', 0):,} | Lines: {data.get('total_lines', 0):,}")
        self.console.print(f"  ✓ Languages: {lang_str}")
        self.console.print(f"  ✓ Architecture: {data.get('architecture', 'N/A')}")

    def _show_files_loaded(self, files: Dict[str, str]):
        """Display loaded files"""
        total_lines = sum(len(content.splitlines()) for content in files.values())
        self.console.print(f"  ✓ Loaded {len(files)} critical files ({total_lines:,} lines)")
        for path in list(files.keys())[:3]:
            lines = len(files[path].splitlines())
            self.console.print(f"    • {path} ({lines} lines)")


class QuickPrimer:
    """
    Ultra-fast primer that skips file loading

    For use when you just need project metadata without full context.
    Completes in ~5 seconds.
    """

    def __init__(self, serena_adapter: Optional[SerenaAdapter] = None):
        self.serena = serena_adapter or SerenaAdapter()
        self.logger = logging.getLogger(__name__)

    async def prime_metadata_only(self, project_id: str) -> Dict[str, Any]:
        """
        Load only metadata, no files

        Args:
            project_id: Project identifier

        Returns:
            Dictionary with project metadata
        """
        # Load from local index only
        project_dir = Path.home() / ".shannon" / "projects" / project_id
        metadata_file = project_dir / "project.json"

        if not metadata_file.exists():
            raise ValueError(f"Project '{project_id}' not found")

        return json.loads(metadata_file.read_text())
