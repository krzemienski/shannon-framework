"""
Main Autonomous Builder for Claude Code Builder.

Orchestrates the complete autonomous build process:
1. Scenario detection
2. MCP discovery and installation
3. Context building via Serena
4. Two-agent pattern execution
5. Verification and completion
"""

import asyncio
import json
import re
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
import logging

# Note: These imports would use claude_agent_sdk in production
# For now, we define the interface

from .config import BuilderConfig
from .security import SecurityManager
from .xml_transformer import XMLPromptTransformer, CodebaseContext
from .mcp_manager import MCPManager
from .serena_context import SerenaContextManager
from .scenario_handler import ScenarioHandler, ScenarioType, ExecutionPlan

logger = logging.getLogger(__name__)


@dataclass
class BuildResult:
    """Result of an autonomous build."""
    success: bool
    target_dir: Path
    features_total: int
    features_completed: int
    sessions_executed: int
    total_duration_seconds: float
    total_cost_usd: Optional[float] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class SessionResult:
    """Result of a single session."""
    session_number: int
    session_type: str  # "initializer" or "coding"
    success: bool
    features_completed: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    cost_usd: Optional[float] = None
    error: Optional[str] = None


class AutonomousBuilder:
    """
    Main autonomous builder using two-agent pattern.

    Integrates:
    - Claude Quickstart two-agent pattern
    - Anthropic's long-running agent best practices
    - Shannon Framework orchestration
    - Serena MCP for codebase context
    """

    AUTO_CONTINUE_DELAY_SECONDS = 3.0

    def __init__(self, config: BuilderConfig):
        """
        Initialize autonomous builder.

        Args:
            config: Builder configuration
        """
        self.config = config
        self.serena = SerenaContextManager(config.target_dir)
        self.mcp_manager = MCPManager(config.target_dir)
        self.xml_transformer = XMLPromptTransformer()
        self.security = SecurityManager(config.security, config.target_dir)
        self.scenario_handler = ScenarioHandler(self.serena)

        self.sessions_executed = 0
        self.total_cost = 0.0
        self._halt_requested = False

    async def build(self, user_request: str) -> BuildResult:
        """
        Execute autonomous build.

        Flow:
        1. Detect scenario (existing vs new)
        2. Transform request to XML prompt
        3. Research required capabilities
        4. Install necessary MCPs
        5. Build Serena context
        6. Execute two-agent pattern
        7. Verify completion

        Args:
            user_request: Natural language build request

        Returns:
            BuildResult with completion status
        """
        start_time = time.time()
        errors = []
        warnings = []

        logger.info(f"Starting autonomous build: {user_request[:100]}...")

        try:
            # Phase 1: Initialize Serena
            await self.serena.initialize()

            # Phase 2: Create execution plan
            plan = await self.scenario_handler.create_execution_plan(
                self.config.target_dir,
                user_request
            )
            warnings.extend(plan.warnings)

            logger.info(f"Execution plan: {plan.scenario_type.value}")

            # Phase 3: MCP Discovery & Installation
            mcp_requirements = await self.mcp_manager.analyze_task(user_request)
            mcp_results = await self.mcp_manager.ensure_mcps(mcp_requirements)

            for mcp_name, installed in mcp_results.items():
                if not installed:
                    warnings.append(f"MCP {mcp_name} not available")

            # Phase 4: Build context
            if plan.requires_analysis:
                context = await self.serena.analyze_existing_directory()
            else:
                context = plan.context or CodebaseContext.empty()

            # Phase 5: Execute based on scenario
            if plan.scenario_type == ScenarioType.CONTINUATION:
                # Continue from existing feature list
                result = await self._continue_build(plan)
            else:
                # Fresh build with two-agent pattern
                result = await self._fresh_build(user_request, plan, context)

            duration = time.time() - start_time

            return BuildResult(
                success=result["success"],
                target_dir=self.config.target_dir,
                features_total=result.get("features_total", 0),
                features_completed=result.get("features_completed", 0),
                sessions_executed=self.sessions_executed,
                total_duration_seconds=duration,
                total_cost_usd=self.total_cost if self.total_cost > 0 else None,
                errors=errors + result.get("errors", []),
                warnings=warnings + result.get("warnings", [])
            )

        except Exception as e:
            logger.error(f"Build failed: {e}")
            duration = time.time() - start_time
            return BuildResult(
                success=False,
                target_dir=self.config.target_dir,
                features_total=0,
                features_completed=0,
                sessions_executed=self.sessions_executed,
                total_duration_seconds=duration,
                errors=[str(e)],
                warnings=warnings
            )

    async def _fresh_build(
        self,
        user_request: str,
        plan: ExecutionPlan,
        context: CodebaseContext
    ) -> Dict[str, Any]:
        """
        Execute fresh build with two-agent pattern.

        Args:
            user_request: User's build request
            plan: Execution plan
            context: Codebase context

        Returns:
            Result dictionary
        """
        errors = []

        # Session 1: Initializer Agent
        logger.info("Starting Initializer Agent session...")
        init_result = await self._run_initializer_session(user_request, plan, context)

        if not init_result.success:
            return {
                "success": False,
                "features_total": 0,
                "features_completed": 0,
                "errors": [init_result.error or "Initializer failed"]
            }

        # Read feature list
        feature_list_path = self.config.target_dir / "feature_list.json"
        if not feature_list_path.exists():
            return {
                "success": False,
                "features_total": 0,
                "features_completed": 0,
                "errors": ["Initializer did not create feature_list.json"]
            }

        features = json.loads(feature_list_path.read_text())
        total_features = len(features.get("features", []))

        # Sessions 2+: Coding Agent Loop
        iteration = 0
        max_iterations = self.config.execution.max_iterations

        while not await self._is_complete() and not self._halt_requested:
            iteration += 1

            if max_iterations and iteration > max_iterations:
                logger.info(f"Reached max iterations ({max_iterations})")
                break

            # Delay between sessions
            if iteration > 1:
                logger.info(f"Waiting {self.AUTO_CONTINUE_DELAY_SECONDS}s before next session...")
                await asyncio.sleep(self.AUTO_CONTINUE_DELAY_SECONDS)

            logger.info(f"Starting Coding Agent session {iteration}...")
            coding_result = await self._run_coding_session(iteration + 1)

            if not coding_result.success:
                errors.append(coding_result.error or f"Coding session {iteration} failed")
                # Continue to next session on error (resilience pattern)

        # Count completed features (reuse features from earlier read)
        completed = sum(1 for f in features.get("features", []) if f.get("passes"))

        return {
            "success": len(errors) == 0,
            "features_total": total_features,
            "features_completed": completed,
            "errors": errors
        }

    async def _continue_build(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """
        Continue from existing feature list.

        Args:
            plan: Execution plan with existing feature list

        Returns:
            Result dictionary
        """
        if not plan.existing_feature_list or not plan.existing_feature_list.exists():
            return {
                "success": False,
                "features_total": 0,
                "features_completed": 0,
                "errors": ["No feature list found for continuation"]
            }

        features = json.loads(plan.existing_feature_list.read_text())
        total_features = len(features.get("features", []))
        initial_completed = sum(1 for f in features.get("features", []) if f.get("passes"))

        logger.info(f"Continuing build: {initial_completed}/{total_features} features complete")

        # Determine session number from progress
        session_number = self._get_next_session_number()

        iteration = 0
        max_iterations = self.config.execution.max_iterations
        errors = []

        while not await self._is_complete() and not self._halt_requested:
            iteration += 1
            session_number += 1

            if max_iterations and iteration > max_iterations:
                logger.info(f"Reached max iterations ({max_iterations})")
                break

            if iteration > 1:
                await asyncio.sleep(self.AUTO_CONTINUE_DELAY_SECONDS)

            logger.info(f"Starting Coding Agent session {session_number}...")
            coding_result = await self._run_coding_session(session_number)

            if not coding_result.success:
                errors.append(coding_result.error or f"Session {session_number} failed")

        # Count final completed features
        features = json.loads(plan.existing_feature_list.read_text())
        completed = sum(1 for f in features.get("features", []) if f.get("passes"))

        return {
            "success": len(errors) == 0,
            "features_total": total_features,
            "features_completed": completed,
            "errors": errors
        }

    async def _run_initializer_session(
        self,
        user_request: str,
        plan: ExecutionPlan,
        context: CodebaseContext
    ) -> SessionResult:
        """
        Session 1: Run Initializer Agent.

        Tasks:
        - Read specification
        - Generate feature_list.json (all passes: false)
        - Create init.sh
        - Initialize git
        - Create directory structure
        - Write claude-progress.txt

        Args:
            user_request: User's build request
            plan: Execution plan
            context: Codebase context

        Returns:
            SessionResult
        """
        self.sessions_executed += 1
        start_time = time.time()

        try:
            # Create scenario for XML transformer
            scenario = await self.scenario_handler.detect_scenario(self.config.target_dir)

            # Generate XML prompt
            self.xml_transformer.transform(
                request=user_request,
                context=context,
                scenario=scenario,
                available_mcps=self.mcp_manager.get_available_mcps(),
                template_type="initializer"
            )

            # In production, this would use ClaudeSDKClient
            # For now, we create the required files as templates
            await self._create_initializer_templates(user_request, context)

            duration = time.time() - start_time

            return SessionResult(
                session_number=1,
                session_type="initializer",
                success=True,
                duration_seconds=duration
            )

        except Exception as e:
            logger.error(f"Initializer session failed: {e}")
            duration = time.time() - start_time
            return SessionResult(
                session_number=1,
                session_type="initializer",
                success=False,
                duration_seconds=duration,
                error=str(e)
            )

    async def _run_coding_session(self, session_number: int) -> SessionResult:
        """
        Session 2+: Run Coding Agent.

        Tasks:
        - Read progress files
        - Select next incomplete feature
        - Run init.sh
        - Implement feature
        - Test with Puppeteer
        - Update feature_list.json (passes: true)
        - Git commit
        - Update progress

        Args:
            session_number: Which session this is

        Returns:
            SessionResult
        """
        self.sessions_executed += 1
        start_time = time.time()

        try:
            # Get previous progress
            previous_progress = await self.serena.get_continuation_context()

            # Generate XML prompt
            self.xml_transformer.transform_for_coding(
                target_dir=self.config.target_dir,
                session_number=session_number,
                previous_progress=previous_progress
            )

            # In production, this would use ClaudeSDKClient
            # For demonstration, we simulate progress
            features_completed = await self._simulate_coding_session(session_number)

            duration = time.time() - start_time

            # Create progress summary
            remaining = await self._count_remaining_features()
            await self.serena.create_execution_summary(
                session_number=session_number,
                features_completed=features_completed,
                features_remaining=remaining,
                notes=f"Session {session_number} completed"
            )

            return SessionResult(
                session_number=session_number,
                session_type="coding",
                success=True,
                features_completed=features_completed,
                duration_seconds=duration
            )

        except Exception as e:
            logger.error(f"Coding session {session_number} failed: {e}")
            duration = time.time() - start_time
            return SessionResult(
                session_number=session_number,
                session_type="coding",
                success=False,
                duration_seconds=duration,
                error=str(e)
            )

    async def _is_complete(self) -> bool:
        """Check if all features are complete."""
        feature_list_path = self.config.target_dir / "feature_list.json"
        if not feature_list_path.exists():
            return False

        try:
            features = json.loads(feature_list_path.read_text())
            feature_list = features.get("features", [])
            if not feature_list:
                return True

            return all(f.get("passes", False) for f in feature_list)
        except Exception:
            return False

    async def _count_remaining_features(self) -> int:
        """Count remaining incomplete features."""
        feature_list_path = self.config.target_dir / "feature_list.json"
        if not feature_list_path.exists():
            return 0

        try:
            features = json.loads(feature_list_path.read_text())
            return sum(1 for f in features.get("features", []) if not f.get("passes"))
        except Exception:
            return 0

    def _get_next_session_number(self) -> int:
        """Determine next session number from progress files."""
        progress_file = self.config.target_dir / "claude-progress.txt"
        if not progress_file.exists():
            return 1

        try:
            content = progress_file.read_text()
            # Look for session markers
            matches = re.findall(r'Session (\d+)', content)
            if matches:
                return max(int(m) for m in matches)
        except Exception as e:
            # If reading or parsing the progress file fails, default to session 1.
            logger.warning(f"Failed to read or parse progress file '{progress_file}': {e}")

        return 1

    async def _create_initializer_templates(
        self,
        user_request: str,
        context: CodebaseContext
    ) -> None:
        """
        Create template files for initializer output.

        In production, these would be generated by Claude.
        """
        target = self.config.target_dir

        # Create feature_list.json template
        feature_list = {
            "project_name": "autonomous-build",
            "created_at": datetime.now().isoformat(),
            "specification": user_request[:500],
            "features": [
                {
                    "id": f"feature-{i+1:03d}",
                    "category": "functional",
                    "description": f"Feature {i+1} - to be defined by Claude",
                    "priority": min(i + 1, 10),
                    "steps": [
                        "Implement feature",
                        "Write tests",
                        "Verify functionality"
                    ],
                    "passes": False
                }
                for i in range(50)  # Minimum 50 features
            ]
        }

        (target / "feature_list.json").write_text(
            json.dumps(feature_list, indent=2)
        )

        # Create init.sh template
        init_script = """#!/bin/bash
# Auto-generated initialization script

echo "Initializing development environment..."

# Check for package.json
if [ -f "package.json" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Check for requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

echo "Starting development server..."
# Add server start command based on project type

echo "Development environment ready!"
echo "Access the application at: http://localhost:3000"
"""
        init_path = target / "init.sh"
        init_path.write_text(init_script)
        init_path.chmod(0o755)

        # Create claude-progress.txt
        progress = f"""# Claude Progress Log

## Session 1 - Initialization
Date: {datetime.now().isoformat()}

### Accomplishments
- Created feature_list.json with 50 features
- Created init.sh for environment setup
- Initialized project structure

### Current State
- Ready for feature implementation
- All features marked as passes: false

### Next Steps
- Coding agent should read feature_list.json
- Implement highest priority incomplete feature
- Test with visual verification if applicable
"""
        (target / "claude-progress.txt").write_text(progress)

    async def _simulate_coding_session(self, session_number: int) -> List[str]:
        """
        Simulate a coding session for demonstration.

        In production, this would be replaced by actual Claude execution.
        """
        feature_list_path = self.config.target_dir / "feature_list.json"
        if not feature_list_path.exists():
            return []

        features = json.loads(feature_list_path.read_text())
        feature_list = features.get("features", [])

        # Find first incomplete feature
        completed = []
        for feature in feature_list:
            if not feature.get("passes"):
                feature["passes"] = True
                feature["implemented_at"] = datetime.now().isoformat()
                feature["session_id"] = f"session-{session_number}"
                completed.append(feature["id"])
                break  # One feature per session

        # Save updated feature list
        feature_list_path.write_text(json.dumps(features, indent=2))

        # Update progress file
        progress_file = self.config.target_dir / "claude-progress.txt"
        if progress_file.exists():
            progress = progress_file.read_text()
        else:
            progress = ""

        progress += f"""

## Session {session_number} - Coding
Date: {datetime.now().isoformat()}

### Features Completed
{chr(10).join(f'- {f}' for f in completed) if completed else '- None'}

### Notes
Simulated session for demonstration
"""
        progress_file.write_text(progress)

        return completed

    def halt(self) -> None:
        """Request build halt."""
        logger.info("Halt requested")
        self._halt_requested = True

    def resume(self) -> None:
        """Resume build from halt."""
        logger.info("Resuming build")
        self._halt_requested = False
