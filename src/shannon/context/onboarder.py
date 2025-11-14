"""
CodebaseOnboarder - Index existing codebases for Shannon understanding

Implements 3-phase onboarding:
1. Discovery (2 min): Scan directory tree, detect tech stack
2. Analysis (9 min): Extract patterns, identify critical files
3. Storage (1 min): Save to Serena + local index

Total duration: 12-22 minutes for 10K line codebase
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from collections import defaultdict
from dataclasses import dataclass

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.panel import Panel

from .serena_adapter import SerenaAdapter, SerenaNode, SerenaRelation


@dataclass
class DiscoveryResult:
    """Results from Phase 1: Discovery"""
    file_count: int
    total_lines: int
    languages: Dict[str, float]  # Language -> percentage
    tech_stack: List[str]
    architecture: str
    files: List[Dict[str, Any]]


@dataclass
class AnalysisResult:
    """Results from Phase 2: Analysis"""
    entry_points: List[str]
    critical_files: List[str]
    patterns: List[Dict[str, Any]]
    modules: List[Dict[str, Any]]
    tech_debt: Dict[str, Any]
    dependencies: Dict[str, List[str]]


class CodebaseOnboarder:
    """
    Indexes existing codebase for Shannon understanding

    Usage:
        onboarder = CodebaseOnboarder(sdk_client, serena_adapter)
        result = await onboarder.onboard(Path("/path/to/project"))

    Features:
    - Directory tree scanning with language detection
    - Tech stack identification (package.json, requirements.txt, etc.)
    - Pattern extraction (REST API, auth, ORM)
    - Critical file identification
    - Serena knowledge graph creation
    - Local index for fast access
    """

    # Ignore patterns for directory scanning
    IGNORE_PATTERNS = {
        '.git', '.svn', 'node_modules', '__pycache__', '.pytest_cache',
        'venv', 'env', '.env', 'dist', 'build', '.next', '.cache',
        'coverage', '.nyc_output', 'target', 'bin', 'obj'
    }

    # Language detection by file extension
    LANGUAGE_MAP = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'JavaScript',
        '.tsx': 'TypeScript',
        '.java': 'Java',
        '.go': 'Go',
        '.rs': 'Rust',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.c': 'C',
        '.cpp': 'C++',
        '.h': 'C/C++',
        '.cs': 'C#',
        '.sql': 'SQL',
        '.sh': 'Shell',
        '.yml': 'YAML',
        '.yaml': 'YAML',
        '.json': 'JSON',
        '.md': 'Markdown',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS'
    }

    # Tech stack detection files
    TECH_STACK_FILES = {
        'package.json': 'Node.js/NPM',
        'requirements.txt': 'Python/pip',
        'Pipfile': 'Python/pipenv',
        'pyproject.toml': 'Python/Poetry',
        'Cargo.toml': 'Rust/Cargo',
        'go.mod': 'Go modules',
        'pom.xml': 'Java/Maven',
        'build.gradle': 'Java/Gradle',
        'Gemfile': 'Ruby/Bundler',
        'composer.json': 'PHP/Composer',
        'Dockerfile': 'Docker',
        'docker-compose.yml': 'Docker Compose'
    }

    def __init__(
        self,
        sdk_client: Optional[Any] = None,
        serena_adapter: Optional[SerenaAdapter] = None
    ):
        """
        Initialize onboarder

        Args:
            sdk_client: Shannon SDK client for code analysis
            serena_adapter: SerenaAdapter for knowledge graph storage
        """
        self.client = sdk_client
        self.serena = serena_adapter or SerenaAdapter()
        self.console = Console()
        self.logger = logging.getLogger(__name__)

    async def onboard(
        self,
        project_path: Path,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Onboard codebase with 3-phase process

        Args:
            project_path: Path to project root
            project_id: Optional project ID (defaults to directory name)

        Returns:
            Dictionary with project metadata and results

        Raises:
            FileNotFoundError: If project path doesn't exist
            ValueError: If project path is not a directory
        """
        # Validate path
        if not project_path.exists():
            raise FileNotFoundError(f"Project path not found: {project_path}")
        if not project_path.is_dir():
            raise ValueError(f"Project path is not a directory: {project_path}")

        # Generate project ID
        if not project_id:
            project_id = project_path.name.lower().replace(' ', '_').replace('-', '_')

        # Display header
        self.console.print("\n")
        self.console.print(Panel.fit(
            "[bold cyan]Shannon Project Onboarding[/bold cyan]",
            border_style="cyan"
        ))
        self.console.print(f"Project: {project_id}")
        self.console.print(f"Path: {project_path}")
        self.console.print("─" * 60)

        # Phase 1: Discovery
        discovery = await self._phase1_discovery(project_path)

        # Phase 2: Analysis
        analysis = await self._phase2_analysis(project_path, discovery)

        # Phase 3: Storage
        await self._phase3_storage(project_id, project_path, discovery, analysis)

        # Success message
        self.console.print("\n")
        self.console.print("[green]✅ Onboarding complete[/green]")
        self.console.print(f"\nProject: {project_id}")
        self.console.print(f"Serena key: project_{project_id}")
        self.console.print(f"\nNext: shannon prime --project {project_id}")

        return {
            'project_id': project_id,
            'discovery': discovery.__dict__,
            'analysis': analysis.__dict__
        }

    async def _phase1_discovery(self, path: Path) -> DiscoveryResult:
        """
        Phase 1: Discovery (2 minutes)

        Scans:
        - Directory tree
        - File count and sizes
        - Programming languages
        - Tech stack
        - Architecture hints
        """
        self.console.print("\n[bold]Phase 1: Discovery[/bold] (2 min)")

        with self.console.status("[bold green]Scanning directory tree..."):
            files = []
            total_lines = 0
            language_lines = defaultdict(int)

            # Scan all files
            for file_path in path.rglob('*'):
                if file_path.is_file() and not self._should_ignore(file_path, path):
                    try:
                        # Read and count lines
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        lines = len(content.splitlines())
                        total_lines += lines

                        # Detect language
                        lang = self._detect_language(file_path)
                        language_lines[lang] += lines

                        # Store file info
                        files.append({
                            'path': str(file_path.relative_to(path)),
                            'lines': lines,
                            'language': lang
                        })
                    except Exception as e:
                        self.logger.debug(f"Skipping {file_path}: {e}")

            # Calculate language percentages
            language_percentages = {}
            if total_lines > 0:
                language_percentages = {
                    lang: (lines / total_lines * 100)
                    for lang, lines in language_lines.items()
                }

            # Detect tech stack
            tech_stack = self._detect_tech_stack(path)

            # Detect architecture
            architecture = self._detect_architecture(path, files)

        # Display results
        self._show_discovery_results(
            file_count=len(files),
            total_lines=total_lines,
            languages=language_percentages,
            tech_stack=tech_stack,
            architecture=architecture
        )

        return DiscoveryResult(
            file_count=len(files),
            total_lines=total_lines,
            languages=language_percentages,
            tech_stack=tech_stack,
            architecture=architecture,
            files=files
        )

    async def _phase2_analysis(
        self,
        path: Path,
        discovery: DiscoveryResult
    ) -> AnalysisResult:
        """
        Phase 2: Analysis (9 minutes)

        Identifies:
        - Entry points
        - Critical files
        - Patterns (REST API, auth, ORM)
        - Technical debt
        - Dependencies
        """
        self.console.print("\n[bold]Phase 2: Analysis[/bold] (9 min)")

        # Simulate analysis with progress bar
        # In real implementation, would use SDK to analyze codebase
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            task = progress.add_task("[cyan]Analyzing codebase...", total=100)

            # Phase 2a: Identify entry points
            progress.update(task, completed=20)
            entry_points = self._identify_entry_points(discovery.files)

            # Phase 2b: Identify critical files
            progress.update(task, completed=40)
            critical_files = self._identify_critical_files(discovery.files)

            # Phase 2c: Extract patterns
            progress.update(task, completed=60)
            patterns = self._extract_patterns(path, discovery.files)

            # Phase 2d: Detect modules
            progress.update(task, completed=80)
            modules = self._detect_modules(path, discovery.files)

            # Phase 2e: Assess technical debt
            progress.update(task, completed=90)
            tech_debt = self._assess_tech_debt(path, discovery.files)

            progress.update(task, completed=100)

        # Display results
        self._show_analysis_results(
            entry_points=entry_points,
            patterns=patterns,
            tech_debt=tech_debt
        )

        return AnalysisResult(
            entry_points=entry_points,
            critical_files=critical_files,
            patterns=patterns,
            modules=modules,
            tech_debt=tech_debt,
            dependencies={}  # Would be populated by SDK analysis
        )

    async def _phase3_storage(
        self,
        project_id: str,
        path: Path,
        discovery: DiscoveryResult,
        analysis: AnalysisResult
    ):
        """
        Phase 3: Storage (1 minute)

        Stores to:
        - Serena knowledge graph
        - Local index files
        """
        self.console.print("\n[bold]Phase 3: Serena Storage[/bold] (1 min)")

        with self.console.status("[bold green]Creating knowledge graph..."):
            # Create Serena nodes and relations
            await self._store_to_serena(project_id, discovery, analysis)

            # Save local index
            self._save_local_index(project_id, str(path), discovery, analysis)

        # Display storage stats
        stats = self.serena.get_stats()
        self.console.print(f"  ✓ Entities: {stats['entities_created']}")
        self.console.print(f"  ✓ Relations: {stats['relations_created']}")
        self.console.print(f"  ✓ Local index: ~/.shannon/projects/{project_id}/")

    def _should_ignore(self, file_path: Path, base_path: Path) -> bool:
        """Check if file should be ignored during scanning"""
        rel_path = file_path.relative_to(base_path)
        parts = rel_path.parts

        # Check if any part matches ignore patterns
        for part in parts:
            if part in self.IGNORE_PATTERNS:
                return True

        return False

    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        suffix = file_path.suffix.lower()
        return self.LANGUAGE_MAP.get(suffix, 'Other')

    def _detect_tech_stack(self, path: Path) -> List[str]:
        """Detect tech stack from marker files"""
        tech_stack = []

        for filename, tech in self.TECH_STACK_FILES.items():
            if (path / filename).exists():
                tech_stack.append(tech)

        return tech_stack

    def _detect_architecture(self, path: Path, files: List[Dict]) -> str:
        """Detect architecture from directory structure"""
        # Check for common architecture patterns
        dirs = {f['path'].split('/')[0] for f in files if '/' in f['path']}

        if 'frontend' in dirs and 'backend' in dirs:
            return "Microservices (frontend/backend separation)"
        elif 'src' in dirs and 'tests' in dirs:
            return "Standard (src/tests structure)"
        elif 'app' in dirs:
            return "Application-centric"
        else:
            return "Flat/Custom structure"

    def _identify_entry_points(self, files: List[Dict]) -> List[str]:
        """Identify main entry point files"""
        entry_patterns = ['main.', 'index.', 'app.', 'server.', '__main__.']
        entry_points = []

        for file in files:
            filename = Path(file['path']).name.lower()
            if any(pattern in filename for pattern in entry_patterns):
                entry_points.append(file['path'])

        return entry_points[:5]  # Top 5

    def _identify_critical_files(self, files: List[Dict]) -> List[str]:
        """Identify critical files (largest, most important)"""
        # Sort by line count
        sorted_files = sorted(files, key=lambda f: f['lines'], reverse=True)
        return [f['path'] for f in sorted_files[:10]]

    def _extract_patterns(self, path: Path, files: List[Dict]) -> List[Dict[str, Any]]:
        """Extract code patterns (REST API, auth, etc.)"""
        patterns = []

        # Simple pattern detection based on file names and directories
        file_paths = {f['path'].lower() for f in files}

        # REST API pattern
        if any('api' in p or 'route' in p for p in file_paths):
            patterns.append({
                'name': 'REST API',
                'description': 'REST API implementation detected',
                'files': [f['path'] for f in files if 'api' in f['path'].lower()][:3]
            })

        # Authentication pattern
        if any('auth' in p for p in file_paths):
            patterns.append({
                'name': 'Authentication',
                'description': 'Authentication system detected',
                'files': [f['path'] for f in files if 'auth' in f['path'].lower()][:3]
            })

        # Database pattern
        if any('model' in p or 'schema' in p or 'db' in p for p in file_paths):
            patterns.append({
                'name': 'Database/ORM',
                'description': 'Database layer detected',
                'files': [f['path'] for f in files if any(x in f['path'].lower() for x in ['model', 'schema', 'db'])][:3]
            })

        return patterns

    def _detect_modules(self, path: Path, files: List[Dict]) -> List[Dict[str, Any]]:
        """Detect logical modules from directory structure"""
        # Group files by top-level directory
        modules = defaultdict(list)

        for file in files:
            parts = file['path'].split('/')
            if len(parts) > 1:
                module_name = parts[0]
                modules[module_name].append(file['path'])

        # Create module objects
        return [
            {
                'name': name,
                'files': file_list,
                'purpose': f"Module containing {len(file_list)} files"
            }
            for name, file_list in modules.items()
            if len(file_list) >= 3  # Only modules with 3+ files
        ]

    def _assess_tech_debt(self, path: Path, files: List[Dict]) -> Dict[str, Any]:
        """Assess technical debt indicators"""
        return {
            'test_coverage': 'Unknown',  # Would require running coverage tool
            'todo_count': 0,  # Would require scanning file contents
            'outdated_deps': 0  # Would require dependency analysis
        }

    async def _store_to_serena(
        self,
        project_id: str,
        discovery: DiscoveryResult,
        analysis: AnalysisResult
    ):
        """Store project to Serena knowledge graph"""
        # Create project node
        project_node = SerenaNode(
            entity_id=f"project_{project_id}",
            entity_type="Project",
            observations=[
                f"Files: {discovery.file_count}",
                f"Lines: {discovery.total_lines}",
                f"Languages: {', '.join(f'{l} {p:.0f}%' for l, p in discovery.languages.items())}",
                f"Tech: {', '.join(discovery.tech_stack)}",
                f"Architecture: {discovery.architecture}",
                f"Onboarded: {datetime.now().isoformat()}"
            ]
        )

        await self.serena.create_node(
            entity_id=project_node.entity_id,
            entity_type=project_node.entity_type,
            observations=project_node.observations
        )

        # Create module nodes in batch
        module_nodes = [
            SerenaNode(
                entity_id=f"project_{project_id}_module_{module['name']}",
                entity_type="Module",
                observations=[
                    f"Name: {module['name']}",
                    f"Files: {len(module['files'])}",
                    f"Purpose: {module.get('purpose', 'N/A')}"
                ]
            )
            for module in analysis.modules
        ]

        if module_nodes:
            await self.serena.create_nodes_batch(module_nodes)

        # Create pattern nodes in batch
        pattern_nodes = [
            SerenaNode(
                entity_id=f"project_{project_id}_pattern_{pattern['name'].replace(' ', '_')}",
                entity_type="Pattern",
                observations=[
                    f"Pattern: {pattern['name']}",
                    f"Description: {pattern['description']}",
                    f"Files: {', '.join(pattern.get('files', []))}"
                ]
            )
            for pattern in analysis.patterns
        ]

        if pattern_nodes:
            await self.serena.create_nodes_batch(pattern_nodes)

        # Create relations
        relations = []

        # Project -> Module relations
        for module in analysis.modules:
            relations.append(SerenaRelation(
                from_id=f"project_{project_id}",
                to_id=f"project_{project_id}_module_{module['name']}",
                relation_type="hasModule"
            ))

        # Project -> Pattern relations
        for pattern in analysis.patterns:
            relations.append(SerenaRelation(
                from_id=f"project_{project_id}",
                to_id=f"project_{project_id}_pattern_{pattern['name'].replace(' ', '_')}",
                relation_type="hasPattern"
            ))

        if relations:
            await self.serena.create_relations_batch(relations)

    def _save_local_index(
        self,
        project_id: str,
        project_path: str,
        discovery: DiscoveryResult,
        analysis: AnalysisResult
    ):
        """Save local index files"""
        project_dir = Path.home() / ".shannon" / "projects" / project_id
        project_dir.mkdir(parents=True, exist_ok=True)

        # Save project metadata
        (project_dir / "project.json").write_text(json.dumps({
            'project_id': project_id,
            'project_path': project_path,
            'created_at': datetime.now().isoformat(),
            'file_count': discovery.file_count,
            'total_lines': discovery.total_lines,
            'languages': discovery.languages,
            'tech_stack': discovery.tech_stack,
            'architecture': discovery.architecture
        }, indent=2))

        # Save file structure
        (project_dir / "structure.json").write_text(json.dumps(
            discovery.files, indent=2
        ))

        # Save patterns
        (project_dir / "patterns.json").write_text(json.dumps(
            analysis.patterns, indent=2
        ))

        # Save critical files
        (project_dir / "critical_files.json").write_text(json.dumps(
            analysis.critical_files, indent=2
        ))

        # Save modules
        (project_dir / "modules.json").write_text(json.dumps(
            analysis.modules, indent=2
        ))

    def _show_discovery_results(
        self,
        file_count: int,
        total_lines: int,
        languages: Dict[str, float],
        tech_stack: List[str],
        architecture: str
    ):
        """Display discovery results"""
        lang_str = ", ".join(f"{l} {p:.0f}%" for l, p in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3])
        self.console.print(f"  ✓ Files: {file_count} | Lines: {total_lines:,} | Languages: {lang_str}")
        self.console.print(f"  ✓ Tech stack: {', '.join(tech_stack) if tech_stack else 'Not detected'}")
        self.console.print(f"  ✓ Architecture: {architecture}")

    def _show_analysis_results(
        self,
        entry_points: List[str],
        patterns: List[Dict],
        tech_debt: Dict
    ):
        """Display analysis results"""
        self.console.print(f"  ✓ Entry points: {', '.join(entry_points[:3]) if entry_points else 'None detected'}")
        self.console.print(f"  ✓ Patterns: {', '.join(p['name'] for p in patterns) if patterns else 'None detected'}")
        self.console.print(f"  ✓ Technical debt: Test coverage {tech_debt.get('test_coverage', 'Unknown')}")
