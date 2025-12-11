"""
Scenario Handler for Autonomous Claude Code Builder.

Handles both existing directory and new project scenarios,
determining the appropriate approach for each.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path
from enum import Enum
import logging

from .serena_context import SerenaContextManager
from .xml_transformer import CodebaseContext, Scenario

logger = logging.getLogger(__name__)


class ScenarioType(Enum):
    """Types of build scenarios."""
    NEW_PROJECT = "new_project"
    EXISTING_EMPTY = "existing_empty"
    EXISTING_WITH_CODE = "existing_with_code"
    CONTINUATION = "continuation"  # Resuming previous autonomous build


@dataclass
class ExecutionPlan:
    """Plan for executing the build."""
    scenario_type: ScenarioType
    target_dir: Path
    requires_initialization: bool
    requires_analysis: bool
    existing_feature_list: Optional[Path] = None
    context: Optional[CodebaseContext] = None
    recommended_mcps: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    notes: str = ""


class ScenarioHandler:
    """
    Handles detection and planning for different build scenarios.

    Scenarios:
    A. New Project - Empty or non-existent directory
    B. Existing Directory - Has files, requires analysis before modification
    C. Continuation - Previous autonomous build, has feature_list.json
    """

    # Files that indicate a project exists
    PROJECT_MARKERS = [
        "package.json",
        "requirements.txt",
        "setup.py",
        "pyproject.toml",
        "Cargo.toml",
        "go.mod",
        "pom.xml",
        "build.gradle",
        "Gemfile",
        "composer.json",
        "Makefile",
        "CMakeLists.txt",
    ]

    # Files that indicate an autonomous build in progress
    AUTONOMOUS_MARKERS = [
        "feature_list.json",
        "claude-progress.txt",
    ]

    def __init__(self, serena: SerenaContextManager):
        """
        Initialize scenario handler.

        Args:
            serena: Serena context manager for codebase analysis
        """
        self.serena = serena

    async def detect_scenario(self, target_dir: Path) -> Scenario:
        """
        Detect the build scenario for a target directory.

        Args:
            target_dir: Directory to analyze

        Returns:
            Scenario object describing the situation
        """
        # Create directory if it doesn't exist
        target_dir.mkdir(parents=True, exist_ok=True)

        # Check what exists
        is_empty = self._is_empty_directory(target_dir)
        has_project = self._has_project_markers(target_dir)
        has_autonomous = self._has_autonomous_markers(target_dir)
        has_git = (target_dir / ".git").exists()

        # Check for specific config files
        has_package_json = (target_dir / "package.json").exists()
        has_requirements_txt = (target_dir / "requirements.txt").exists()
        has_cargo_toml = (target_dir / "Cargo.toml").exists()
        has_go_mod = (target_dir / "go.mod").exists()

        scenario = Scenario(
            is_existing=not is_empty or has_project,
            target_dir=target_dir,
            has_package_json=has_package_json,
            has_requirements_txt=has_requirements_txt,
            has_cargo_toml=has_cargo_toml,
            has_go_mod=has_go_mod,
            git_initialized=has_git
        )

        logger.info(f"Detected scenario: existing={scenario.is_existing}, git={has_git}")
        return scenario

    async def create_execution_plan(
        self,
        target_dir: Path,
        task: str
    ) -> ExecutionPlan:
        """
        Create an execution plan based on detected scenario.

        Args:
            target_dir: Target directory
            task: Task description

        Returns:
            ExecutionPlan with recommended approach
        """
        scenario = await self.detect_scenario(target_dir)

        # Determine scenario type
        if self._has_autonomous_markers(target_dir):
            scenario_type = ScenarioType.CONTINUATION
            requires_init = False
            requires_analysis = False
            feature_list = target_dir / "feature_list.json"
        elif self._is_empty_directory(target_dir):
            scenario_type = ScenarioType.NEW_PROJECT
            requires_init = True
            requires_analysis = False
            feature_list = None
        elif self._has_project_markers(target_dir):
            scenario_type = ScenarioType.EXISTING_WITH_CODE
            requires_init = True
            requires_analysis = True
            feature_list = None
        else:
            scenario_type = ScenarioType.EXISTING_EMPTY
            requires_init = True
            requires_analysis = False
            feature_list = None

        # Get codebase context if needed
        context = None
        if requires_analysis:
            context = await self.serena.analyze_existing_directory(target_dir)

        # Determine recommended MCPs based on scenario and task
        recommended_mcps = self._recommend_mcps(scenario_type, task, context)

        # Generate warnings
        warnings = self._generate_warnings(scenario_type, target_dir, context)

        # Generate notes
        notes = self._generate_notes(scenario_type, context)

        plan = ExecutionPlan(
            scenario_type=scenario_type,
            target_dir=target_dir,
            requires_initialization=requires_init,
            requires_analysis=requires_analysis,
            existing_feature_list=feature_list if feature_list and feature_list.exists() else None,
            context=context,
            recommended_mcps=recommended_mcps,
            warnings=warnings,
            notes=notes
        )

        logger.info(f"Created execution plan: {scenario_type.value}")
        return plan

    async def handle_existing_directory(
        self,
        target_dir: Path,
        task: str
    ) -> ExecutionPlan:
        """
        Scenario A: Implementation in existing directory.

        Steps:
        1. Query Serena for complete codebase context
        2. Identify existing patterns and conventions
        3. Build dependency map
        4. Plan changes that respect existing architecture
        5. Generate feature list considering existing code

        Args:
            target_dir: Existing directory
            task: Task description

        Returns:
            ExecutionPlan for existing directory
        """
        logger.info(f"Handling existing directory: {target_dir}")

        # Get full context from Serena
        context = await self.serena.analyze_existing_directory(target_dir)

        warnings = []
        notes_parts = []

        # Check for potential conflicts
        if context.exists:
            notes_parts.append(f"Project Type: {context.project_type}")
            notes_parts.append(f"Languages: {', '.join(context.languages)}")

            if context.frameworks:
                notes_parts.append(f"Frameworks: {', '.join(context.frameworks)}")

            if context.patterns:
                notes_parts.append(f"Patterns: {', '.join(context.patterns)}")

            # Warn about potential conflicts
            if len(context.languages) > 3:
                warnings.append("Multiple languages detected - ensure consistency")

            if context.dependencies:
                dep_count = len(context.dependencies)
                if dep_count > 50:
                    warnings.append(f"Large dependency tree ({dep_count} deps) - check for conflicts")

        # Recommend MCPs
        recommended = ["serena"]  # Always required
        if context.project_type in ["Node.js", "JavaScript", "TypeScript"]:
            recommended.append("puppeteer")
        if any(fw in ["React", "Vue", "Angular"] for fw in context.frameworks):
            recommended.append("puppeteer")

        return ExecutionPlan(
            scenario_type=ScenarioType.EXISTING_WITH_CODE,
            target_dir=target_dir,
            requires_initialization=True,
            requires_analysis=True,
            context=context,
            recommended_mcps=recommended,
            warnings=warnings,
            notes="\n".join(notes_parts)
        )

    async def handle_new_project(
        self,
        target_dir: Path,
        task: str
    ) -> ExecutionPlan:
        """
        Scenario B: New project initialization.

        Steps:
        1. Analyze requirements for tooling
        2. Determine project type and stack
        3. Install required MCPs
        4. Scaffold project structure
        5. Generate comprehensive feature list

        Args:
            target_dir: Target directory for new project
            task: Task description

        Returns:
            ExecutionPlan for new project
        """
        logger.info(f"Handling new project: {target_dir}")

        # Ensure directory exists
        target_dir.mkdir(parents=True, exist_ok=True)

        # Analyze task to determine project type
        task_lower = task.lower()
        recommended_mcps = ["serena"]  # Always required

        notes_parts = []

        # Detect project type from task
        if any(kw in task_lower for kw in ["web app", "website", "frontend", "react", "vue", "angular"]):
            notes_parts.append("Detected: Web Application")
            recommended_mcps.append("puppeteer")

        if any(kw in task_lower for kw in ["api", "backend", "server", "rest"]):
            notes_parts.append("Detected: Backend/API")
            recommended_mcps.append("fetch")

        if any(kw in task_lower for kw in ["mobile", "ios", "android", "react native", "flutter"]):
            notes_parts.append("Detected: Mobile Application")

        if any(kw in task_lower for kw in ["cli", "command line", "terminal"]):
            notes_parts.append("Detected: CLI Application")

        if any(kw in task_lower for kw in ["github", "repository", "git"]):
            recommended_mcps.append("github")

        if not notes_parts:
            notes_parts.append("Project type: General")

        return ExecutionPlan(
            scenario_type=ScenarioType.NEW_PROJECT,
            target_dir=target_dir,
            requires_initialization=True,
            requires_analysis=False,
            context=CodebaseContext.empty(),
            recommended_mcps=recommended_mcps,
            warnings=[],
            notes="\n".join(notes_parts)
        )

    async def handle_continuation(
        self,
        target_dir: Path
    ) -> ExecutionPlan:
        """
        Scenario C: Continue previous autonomous build.

        Args:
            target_dir: Directory with existing feature_list.json

        Returns:
            ExecutionPlan for continuation
        """
        logger.info(f"Handling continuation: {target_dir}")

        feature_list = target_dir / "feature_list.json"
        progress_file = target_dir / "claude-progress.txt"

        notes_parts = ["Resuming autonomous build"]

        # Get progress context
        previous_context = await self.serena.get_continuation_context()
        if previous_context:
            notes_parts.append("Found previous session context")

        if progress_file.exists():
            try:
                progress = progress_file.read_text()
                # Extract last few lines
                lines = progress.strip().split('\n')[-10:]
                notes_parts.append("Recent progress:")
                notes_parts.extend(f"  {line}" for line in lines)
            except Exception:
                pass

        return ExecutionPlan(
            scenario_type=ScenarioType.CONTINUATION,
            target_dir=target_dir,
            requires_initialization=False,
            requires_analysis=False,
            existing_feature_list=feature_list,
            recommended_mcps=["serena", "puppeteer"],
            warnings=[],
            notes="\n".join(notes_parts)
        )

    def _is_empty_directory(self, directory: Path) -> bool:
        """Check if directory is empty (ignoring hidden files)."""
        if not directory.exists():
            return True

        for item in directory.iterdir():
            if not item.name.startswith('.'):
                return False

        return True

    def _has_project_markers(self, directory: Path) -> bool:
        """Check if directory has project marker files."""
        for marker in self.PROJECT_MARKERS:
            if (directory / marker).exists():
                return True
        return False

    def _has_autonomous_markers(self, directory: Path) -> bool:
        """Check if directory has autonomous build markers."""
        for marker in self.AUTONOMOUS_MARKERS:
            if (directory / marker).exists():
                return True
        return False

    def _recommend_mcps(
        self,
        scenario_type: ScenarioType,
        task: str,
        context: Optional[CodebaseContext]
    ) -> List[str]:
        """Recommend MCPs based on scenario and task."""
        mcps = ["serena"]  # Always required

        task_lower = task.lower()

        # Web-related
        if any(kw in task_lower for kw in ["web", "browser", "ui", "frontend"]):
            mcps.append("puppeteer")

        # Context-based recommendations
        if context and context.exists:
            if context.project_type in ["Node.js"]:
                mcps.append("puppeteer")
            if any(fw in context.frameworks for fw in ["React", "Vue", "Angular", "Next.js"]):
                mcps.append("puppeteer")

        return list(set(mcps))

    def _generate_warnings(
        self,
        scenario_type: ScenarioType,
        target_dir: Path,
        context: Optional[CodebaseContext]
    ) -> List[str]:
        """Generate warnings based on scenario."""
        warnings = []

        if scenario_type == ScenarioType.EXISTING_WITH_CODE:
            warnings.append("Existing code detected - changes will be integrated")

            if context and context.exists:
                # Check for potential issues
                if len(context.languages) > 4:
                    warnings.append("Many languages detected - ensure task is compatible")

                if ".env" in str(context.structure.get("root_files", [])):
                    warnings.append("Environment file detected - handle secrets carefully")

        return warnings

    def _generate_notes(
        self,
        scenario_type: ScenarioType,
        context: Optional[CodebaseContext]
    ) -> str:
        """Generate notes for the execution plan."""
        if scenario_type == ScenarioType.NEW_PROJECT:
            return "Fresh project - full initialization required"
        elif scenario_type == ScenarioType.CONTINUATION:
            return "Continuing previous build - check feature_list.json for progress"
        elif scenario_type == ScenarioType.EXISTING_WITH_CODE:
            if context and context.exists:
                return f"Existing {context.project_type} project with {', '.join(context.languages)}"
            return "Existing project - analysis recommended"
        else:
            return "Empty directory - can initialize new project"
