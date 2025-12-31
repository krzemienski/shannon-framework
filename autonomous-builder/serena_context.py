"""
Serena Context Manager for Autonomous Claude Code Builder.

Manages codebase context via Serena MCP (NOT open memory).
Provides semantic code understanding and cross-session memory.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
from pathlib import Path
import json
import logging
import asyncio

from .xml_transformer import CodebaseContext

logger = logging.getLogger(__name__)


@dataclass
class SymbolLocation:
    """Location of a code symbol."""
    file_path: str
    line_number: int
    column: int
    symbol_type: str  # function, class, variable, etc.
    name: str
    signature: Optional[str] = None


@dataclass
class FileInfo:
    """Information about a source file."""
    path: str
    language: str
    size_bytes: int
    line_count: int
    symbols: List[str] = field(default_factory=list)


@dataclass
class DependencyInfo:
    """Information about a project dependency."""
    name: str
    version: str
    dev: bool = False
    source: str = ""  # package.json, requirements.txt, etc.


class SerenaContextManager:
    """
    Manages codebase context via Serena MCP.

    This is the REQUIRED context system (NOT open memory).
    Provides:
    - Symbol-level code understanding
    - Cross-session memory persistence
    - Semantic code search
    - Project structure awareness
    """

    # File type to language mapping
    LANGUAGE_MAP = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript/React",
        ".jsx": "JavaScript/React",
        ".rs": "Rust",
        ".go": "Go",
        ".java": "Java",
        ".rb": "Ruby",
        ".php": "PHP",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".cs": "C#",
        ".cpp": "C++",
        ".c": "C",
        ".h": "C/C++ Header",
        ".vue": "Vue",
        ".svelte": "Svelte",
    }

    # Framework detection patterns
    FRAMEWORK_PATTERNS = {
        "React": ["react", "react-dom", "next"],
        "Vue": ["vue", "nuxt"],
        "Angular": ["@angular/core"],
        "Express": ["express"],
        "FastAPI": ["fastapi"],
        "Django": ["django"],
        "Flask": ["flask"],
        "Next.js": ["next"],
        "Nest.js": ["@nestjs/core"],
        "Spring": ["spring-boot"],
    }

    def __init__(self, project_dir: Path):
        """
        Initialize Serena context manager.

        Args:
            project_dir: Root directory of the project
        """
        self.project_dir = project_dir
        self.serena_dir = project_dir / ".serena"
        self.memories_dir = self.serena_dir / "memories"
        self._context_cache: Optional[CodebaseContext] = None
        self._symbols_cache: Dict[str, List[SymbolLocation]] = {}

    async def initialize(self) -> bool:
        """
        Initialize Serena context for the project.

        Creates .serena directory if not exists.

        Returns:
            True if initialization successful
        """
        try:
            self.serena_dir.mkdir(parents=True, exist_ok=True)
            self.memories_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Initialized Serena context at {self.serena_dir}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Serena: {e}")
            return False

    async def analyze_existing_directory(self, path: Optional[Path] = None) -> CodebaseContext:
        """
        Build complete understanding of existing codebase.

        Args:
            path: Directory to analyze (defaults to project_dir)

        Returns:
            CodebaseContext with full codebase information
        """
        target = path or self.project_dir

        if not target.exists():
            return CodebaseContext.empty()

        # Check if directory has any source files
        source_files = self._find_source_files(target)
        if not source_files:
            return CodebaseContext.empty()

        # Detect project type and frameworks
        project_type = await self._detect_project_type(target)
        languages = self._detect_languages(source_files)
        frameworks = await self._detect_frameworks(target)
        dependencies = await self._read_dependencies(target)
        structure = self._analyze_structure(target)
        patterns = self._detect_patterns(source_files)
        readme = await self._read_readme(target)

        context = CodebaseContext(
            exists=True,
            project_type=project_type,
            languages=languages,
            frameworks=frameworks,
            dependencies=dependencies,
            structure=structure,
            patterns=patterns,
            readme_summary=readme
        )

        self._context_cache = context
        return context

    def _find_source_files(self, directory: Path) -> List[FileInfo]:
        """Find all source files in directory."""
        files = []
        ignore_dirs = {
            'node_modules', '.git', '__pycache__', '.venv', 'venv',
            'dist', 'build', 'target', '.next', '.nuxt', 'vendor'
        }

        for ext in self.LANGUAGE_MAP.keys():
            for file_path in directory.rglob(f"*{ext}"):
                # Skip ignored directories
                if any(ignored in file_path.parts for ignored in ignore_dirs):
                    continue

                try:
                    stat = file_path.stat()
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    line_count = content.count('\n') + 1

                    files.append(FileInfo(
                        path=str(file_path.relative_to(directory)),
                        language=self.LANGUAGE_MAP[ext],
                        size_bytes=stat.st_size,
                        line_count=line_count
                    ))
                except Exception as e:
                    logger.debug(f"Could not read {file_path}: {e}")

        return files

    async def _detect_project_type(self, directory: Path) -> str:
        """Detect the type of project."""
        # Check for common project markers
        markers = {
            "package.json": "Node.js",
            "requirements.txt": "Python",
            "setup.py": "Python",
            "pyproject.toml": "Python",
            "Cargo.toml": "Rust",
            "go.mod": "Go",
            "pom.xml": "Java/Maven",
            "build.gradle": "Java/Gradle",
            "Gemfile": "Ruby",
            "composer.json": "PHP",
        }

        for marker, proj_type in markers.items():
            if (directory / marker).exists():
                return proj_type

        return "Unknown"

    def _detect_languages(self, files: List[FileInfo]) -> List[str]:
        """Detect languages used in the project."""
        languages = set()
        for f in files:
            languages.add(f.language)
        return sorted(list(languages))

    async def _detect_frameworks(self, directory: Path) -> List[str]:
        """Detect frameworks used in the project."""
        frameworks = []
        deps = await self._read_dependencies(directory)

        for framework, packages in self.FRAMEWORK_PATTERNS.items():
            for pkg in packages:
                if pkg in deps:
                    frameworks.append(framework)
                    break

        return frameworks

    async def _read_dependencies(self, directory: Path) -> Dict[str, str]:
        """Read dependencies from project files."""
        deps = {}

        # package.json
        pkg_json = directory / "package.json"
        if pkg_json.exists():
            try:
                data = json.loads(pkg_json.read_text())
                deps.update(data.get("dependencies", {}))
                deps.update(data.get("devDependencies", {}))
            except Exception as e:
                logger.debug(f"Could not parse package.json: {e}")

        # requirements.txt
        req_txt = directory / "requirements.txt"
        if req_txt.exists():
            try:
                for line in req_txt.read_text().splitlines():
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Parse package==version or package>=version etc.
                        parts = line.split('==')
                        if len(parts) == 2:
                            deps[parts[0].strip()] = parts[1].strip()
                        else:
                            parts = line.split('>=')
                            if len(parts) >= 1:
                                deps[parts[0].strip()] = "*"
            except Exception as e:
                logger.debug(f"Could not parse requirements.txt: {e}")

        # pyproject.toml (simplified)
        pyproject = directory / "pyproject.toml"
        if pyproject.exists():
            try:
                content = pyproject.read_text()
                # Simple extraction - would need toml parser for full support
                if "dependencies" in content:
                    deps["_pyproject"] = "has dependencies"
            except Exception as e:
                logger.debug(f"Could not parse pyproject.toml: {e}")

        return deps

    def _analyze_structure(self, directory: Path) -> Dict[str, Any]:
        """Analyze directory structure."""
        structure = {
            "root_files": [],
            "directories": [],
            "depth": 0
        }

        ignore_dirs = {'node_modules', '.git', '__pycache__', '.venv', 'venv'}

        # Get root level items
        try:
            for item in directory.iterdir():
                if item.name.startswith('.'):
                    continue
                if item.is_file():
                    structure["root_files"].append(item.name)
                elif item.is_dir() and item.name not in ignore_dirs:
                    structure["directories"].append(item.name)
        except Exception as e:
            logger.debug(f"Could not analyze structure: {e}")

        return structure

    def _detect_patterns(self, files: List[FileInfo]) -> List[str]:
        """Detect coding patterns from file structure."""
        patterns = []

        # Check for common patterns
        paths = [f.path for f in files]

        if any('test' in p.lower() for p in paths):
            patterns.append("Has tests")

        if any('component' in p.lower() for p in paths):
            patterns.append("Component-based")

        if any('model' in p.lower() for p in paths):
            patterns.append("Has data models")

        if any('controller' in p.lower() or 'route' in p.lower() for p in paths):
            patterns.append("MVC/Router pattern")

        if any('service' in p.lower() for p in paths):
            patterns.append("Service layer")

        if any('hook' in p.lower() for p in paths):
            patterns.append("Uses hooks")

        return patterns

    async def _read_readme(self, directory: Path) -> Optional[str]:
        """Read and summarize README file."""
        readme_names = ['README.md', 'README.txt', 'README', 'readme.md']

        for name in readme_names:
            readme = directory / name
            if readme.exists():
                try:
                    content = readme.read_text()
                    # Return first 500 chars as summary
                    return content[:500] + "..." if len(content) > 500 else content
                except Exception:
                    pass

        return None

    async def find_symbol(self, symbol_name: str) -> List[SymbolLocation]:
        """
        Locate code symbols semantically.

        This wraps Serena's find_symbol tool for semantic code search.

        Args:
            symbol_name: Name of symbol to find

        Returns:
            List of symbol locations
        """
        if symbol_name in self._symbols_cache:
            return self._symbols_cache[symbol_name]

        # This would call Serena MCP in real implementation
        # For now, use simple file search as fallback
        locations = []
        source_files = self._find_source_files(self.project_dir)

        for file_info in source_files:
            file_path = self.project_dir / file_info.path
            try:
                content = file_path.read_text()
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    if symbol_name in line:
                        locations.append(SymbolLocation(
                            file_path=file_info.path,
                            line_number=i + 1,
                            column=line.index(symbol_name),
                            symbol_type="unknown",
                            name=symbol_name
                        ))
            except Exception as e:
                logger.warning(f"Failed to read file {file_path}: {e}")

        self._symbols_cache[symbol_name] = locations
        return locations

    async def read_memory(self, memory_name: str) -> Optional[str]:
        """
        Read memory from Serena's project-specific store.

        Memories are stored in .serena/memories/

        Args:
            memory_name: Name of the memory to read

        Returns:
            Memory content or None if not found
        """
        # Sanitize memory name
        safe_name = "".join(c for c in memory_name if c.isalnum() or c in '_-')
        memory_file = self.memories_dir / f"{safe_name}.md"

        if memory_file.exists():
            try:
                return memory_file.read_text()
            except Exception as e:
                logger.error(f"Failed to read memory {memory_name}: {e}")

        return None

    async def write_memory(self, memory_name: str, content: str) -> bool:
        """
        Write memory to Serena's project-specific store.

        Args:
            memory_name: Name for the memory
            content: Content to store

        Returns:
            True if successful
        """
        # Ensure directories exist
        await self.initialize()

        # Sanitize memory name
        safe_name = "".join(c for c in memory_name if c.isalnum() or c in '_-')
        memory_file = self.memories_dir / f"{safe_name}.md"

        try:
            memory_file.write_text(content)
            logger.info(f"Wrote memory: {memory_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to write memory {memory_name}: {e}")
            return False

    async def create_execution_summary(
        self,
        session_number: int,
        features_completed: List[str],
        features_remaining: int,
        notes: str
    ) -> str:
        """
        Create summary of current execution state for session continuity.

        Args:
            session_number: Current session number
            features_completed: List of completed feature IDs
            features_remaining: Count of remaining features
            notes: Additional notes

        Returns:
            Formatted summary string
        """
        summary = f"""# Execution Summary - Session {session_number}

## Progress
- Features Completed: {len(features_completed)}
- Features Remaining: {features_remaining}
- Completion: {len(features_completed) / (len(features_completed) + features_remaining) * 100:.1f}%

## Completed This Session
{chr(10).join(f'- {f}' for f in features_completed) if features_completed else '- None'}

## Notes
{notes}

## Next Session
- Continue with highest priority incomplete feature
- Run baseline verification before starting
- Check git history for recent changes
"""
        # Store in memory for next session
        await self.write_memory(f"session_{session_number}_summary", summary)

        return summary

    async def get_continuation_context(self) -> Optional[str]:
        """
        Get context for continuing from previous session.

        Looks for most recent session summary in memories.

        Returns:
            Previous session context or None
        """
        if not self.memories_dir.exists():
            return None

        # Find most recent session summary
        summaries = list(self.memories_dir.glob("session_*_summary.md"))
        if not summaries:
            return None

        # Sort by session number and get latest
        summaries.sort(key=lambda p: int(p.stem.split('_')[1]), reverse=True)
        latest = summaries[0]

        try:
            return latest.read_text()
        except Exception:
            return None

    def get_cached_context(self) -> Optional[CodebaseContext]:
        """Get cached codebase context if available."""
        return self._context_cache
