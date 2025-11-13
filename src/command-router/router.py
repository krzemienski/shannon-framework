"""
Shannon Framework v4 - Command Router

Thin orchestration layer that coordinates all Shannon components.
"""

from typing import Optional, Dict, Any
from datetime import datetime
from pathlib import Path

from .models import CommandType, CommandContext, CommandResult, ExecutionMode

# Import all Shannon components
from ..specification_engine import SpecificationParser, SpecificationValidator, SpecificationMonitor
from ..skill_registry import SkillManager
from ..sitrep import SITREPGenerator, SITREPTemplate
from ..context_manager import ContextManager, SessionManager, CheckpointType
from ..orchestrator import SubAgentOrchestrator
from ..wave_engine import WaveExecutionEngine
from ..validation_gates import ValidationGateValidator
from ..mcp_integration import MCPDiscovery


class CommandRouter:
    """
    Thin orchestration layer for Shannon Framework.

    Routes commands to appropriate components and coordinates execution.
    """

    def __init__(
        self,
        skills_dir: Path = None,
        storage_backend: str = "local",
        serena_client=None
    ):
        """
        Initialize command router.

        Args:
            skills_dir: Directory containing skill definitions
            storage_backend: Storage backend (local, serena, memory)
            serena_client: Serena MCP client
        """
        # Initialize components
        self.spec_parser = SpecificationParser()
        self.spec_validator = SpecificationValidator()

        self.skill_manager = SkillManager(skills_dir or Path.cwd() / 'skills')

        self.session_manager = SessionManager(
            storage_backend=storage_backend,
            serena_client=serena_client
        )

        self.orchestrator = SubAgentOrchestrator()

        self.wave_engine = WaveExecutionEngine(
            orchestrator=self.orchestrator,
            context_manager=None,  # Set after session creation
            validator=None  # Set after initialization
        )

        self.validation_gate = ValidationGateValidator()

        self.mcp_discovery = MCPDiscovery()

        # State
        self.current_specification = None
        self.current_session = None
        self.current_execution_plan = None

    def execute_command(
        self,
        command_type: CommandType,
        context: CommandContext
    ) -> CommandResult:
        """
        Execute a command.

        Args:
            command_type: Type of command to execute
            context: Command context

        Returns:
            CommandResult
        """
        result = CommandResult(
            command_type=command_type,
            success=False,
            start_time=datetime.now()
        )

        try:
            if command_type == CommandType.ANALYZE_SPEC:
                result = self._analyze_specification(context)
            elif command_type == CommandType.CREATE_PLAN:
                result = self._create_execution_plan(context)
            elif command_type == CommandType.EXECUTE_PHASE:
                result = self._execute_phase(context)
            elif command_type == CommandType.EXECUTE_WAVE:
                result = self._execute_wave(context)
            elif command_type == CommandType.EXECUTE_FULL:
                result = self._execute_full(context)
            elif command_type == CommandType.CHECKPOINT:
                result = self._create_checkpoint(context)
            elif command_type == CommandType.RESTORE:
                result = self._restore_checkpoint(context)
            elif command_type == CommandType.STATUS:
                result = self._get_status(context)
            elif command_type == CommandType.VALIDATE:
                result = self._validate(context)
            else:
                result.errors.append(f"Unknown command type: {command_type}")

        except Exception as e:
            result.errors.append(str(e))

        # Finalize timing
        result.end_time = datetime.now()
        result.duration_seconds = (
            result.end_time - result.start_time
        ).total_seconds()

        return result

    def _analyze_specification(self, context: CommandContext) -> CommandResult:
        """Analyze specification and validate."""
        result = CommandResult(
            command_type=CommandType.ANALYZE_SPEC,
            success=False,
            start_time=datetime.now()
        )

        try:
            # Get specification text
            spec_text = context.specification_text
            if context.specification_file:
                spec_text = Path(context.specification_file).read_text()

            if not spec_text:
                result.errors.append("No specification provided")
                return result

            # Parse specification
            spec = self.spec_parser.parse(spec_text)
            self.current_specification = spec

            # Validate specification
            if not context.skip_validation:
                validation_result = self.validation_gate.validate_specification(spec)
                result.confidence_score = validation_result.confidence_score.overall
                result.validation_passed = validation_result.passed()

                if not validation_result.passed():
                    result.warnings.append(
                        f"Specification validation failed (confidence: {result.confidence_score:.1%})"
                    )
                    for issue in validation_result.get_critical_issues():
                        result.errors.append(issue.description)

            # Get MCP recommendations
            mcp_recommendations = self.mcp_discovery.recommend_for_specification(spec)

            result.success = True
            result.message = f"Specification analyzed: {spec.title}"
            result.output = {
                'specification': spec.to_dict() if hasattr(spec, 'to_dict') else None,
                'validation': {
                    'confidence': result.confidence_score,
                    'passed': result.validation_passed,
                },
                'mcp_recommendations': [r.to_dict() for r in mcp_recommendations]
            }

        except Exception as e:
            result.errors.append(f"Specification analysis failed: {e}")

        return result

    def _create_execution_plan(self, context: CommandContext) -> CommandResult:
        """Create execution plan from specification."""
        result = CommandResult(
            command_type=CommandType.CREATE_PLAN,
            success=False,
            start_time=datetime.now()
        )

        if not self.current_specification:
            result.errors.append("No specification loaded. Run ANALYZE_SPEC first.")
            return result

        try:
            from ..wave_engine import create_execution_plan, create_phase, create_wave, create_task

            # Create execution plan
            plan = create_execution_plan(
                name=f"Execution: {self.current_specification.title}",
                specification_id=getattr(self.current_specification, 'id', None),
                checkpoint_frequency=context.checkpoint_frequency
            )

            # For now, create a simple default plan structure
            # In a full implementation, this would be generated from the specification

            # Phase 1: Setup and Analysis
            phase1 = create_phase(
                name="Setup and Analysis",
                description="Initial project setup and specification analysis",
                phase_number=1
            )

            wave1 = create_wave(
                name="Project Initialization",
                description="Set up project structure and analyze requirements",
                phase_id=phase1.id
            )

            task1 = create_task(
                description="Analyze specification in detail",
                agent_type="research"
            )
            wave1.tasks.append(task1)

            phase1.waves.append(wave1)
            plan.phases.append(phase1)

            self.current_execution_plan = plan

            result.success = True
            result.message = f"Execution plan created with {len(plan.phases)} phases"
            result.output = plan.to_dict()

        except Exception as e:
            result.errors.append(f"Plan creation failed: {e}")

        return result

    def _execute_full(self, context: CommandContext) -> CommandResult:
        """Execute full end-to-end workflow."""
        result = CommandResult(
            command_type=CommandType.EXECUTE_FULL,
            success=False,
            start_time=datetime.now()
        )

        try:
            # Step 1: Analyze specification
            if not self.current_specification:
                analyze_result = self._analyze_specification(context)
                if not analyze_result.success:
                    result.errors.extend(analyze_result.errors)
                    return result

            # Step 2: Create execution plan
            if not self.current_execution_plan:
                plan_result = self._create_execution_plan(context)
                if not plan_result.success:
                    result.errors.extend(plan_result.errors)
                    return result

            # Step 3: Create session
            if not self.current_session:
                self.current_session = self.session_manager.create_session(
                    name=f"Execution: {self.current_specification.title}",
                    specification_title=self.current_specification.title
                )

                # Update wave engine with context manager
                self.wave_engine.context_manager = self.session_manager.context_manager

            # Step 4: Execute plan
            phase_results = self.wave_engine.execute_plan(self.current_execution_plan)

            # Step 5: Validate results
            overall_success = all(
                pr.validation_passed for pr in phase_results.values()
            )

            result.success = overall_success
            result.message = f"Execution completed: {len(phase_results)} phases"
            result.output = {
                'phase_results': {
                    pid: pr.to_dict() for pid, pr in phase_results.items()
                }
            }

        except Exception as e:
            result.errors.append(f"Execution failed: {e}")

        return result

    def _execute_phase(self, context: CommandContext) -> CommandResult:
        """Execute single phase."""
        result = CommandResult(
            command_type=CommandType.EXECUTE_PHASE,
            success=False,
            start_time=datetime.now()
        )

        result.errors.append("Phase execution not yet implemented")
        return result

    def _execute_wave(self, context: CommandContext) -> CommandResult:
        """Execute single wave."""
        result = CommandResult(
            command_type=CommandType.EXECUTE_WAVE,
            success=False,
            start_time=datetime.now()
        )

        result.errors.append("Wave execution not yet implemented")
        return result

    def _create_checkpoint(self, context: CommandContext) -> CommandResult:
        """Create checkpoint."""
        result = CommandResult(
            command_type=CommandType.CHECKPOINT,
            success=False,
            start_time=datetime.now()
        )

        if not self.session_manager.context_manager:
            result.errors.append("No active session")
            return result

        try:
            checkpoint = self.session_manager.checkpoint_session(
                checkpoint_type=CheckpointType.MANUAL,
                description=context.metadata.get('description', 'Manual checkpoint')
            )

            result.success = True
            result.message = f"Checkpoint created: {checkpoint.id}"
            result.output = checkpoint.to_dict()

        except Exception as e:
            result.errors.append(f"Checkpoint creation failed: {e}")

        return result

    def _restore_checkpoint(self, context: CommandContext) -> CommandResult:
        """Restore from checkpoint."""
        result = CommandResult(
            command_type=CommandType.RESTORE,
            success=False,
            start_time=datetime.now()
        )

        if not context.checkpoint_id:
            result.errors.append("No checkpoint ID provided")
            return result

        try:
            restore_result = self.session_manager.restore_session_checkpoint(
                context.checkpoint_id
            )

            result.success = restore_result.success
            result.errors.extend(restore_result.errors)
            result.warnings.extend(restore_result.warnings)
            result.message = "Checkpoint restored" if result.success else "Restore failed"
            result.output = {
                'checkpoint': restore_result.checkpoint.to_dict() if restore_result.checkpoint else None,
                'restored_files': restore_result.restored_files
            }

        except Exception as e:
            result.errors.append(f"Checkpoint restore failed: {e}")

        return result

    def _get_status(self, context: CommandContext) -> CommandResult:
        """Get current execution status."""
        result = CommandResult(
            command_type=CommandType.STATUS,
            success=True,
            start_time=datetime.now()
        )

        status = {
            'specification': self.current_specification.title if self.current_specification else None,
            'session': self.current_session.name if self.current_session else None,
            'execution_plan': self.current_execution_plan.name if self.current_execution_plan else None,
        }

        if self.wave_engine:
            progress = self.wave_engine.get_progress()
            status['progress'] = progress

        result.message = "Status retrieved"
        result.output = status

        return result

    def _validate(self, context: CommandContext) -> CommandResult:
        """Run validation gate."""
        result = CommandResult(
            command_type=CommandType.VALIDATE,
            success=False,
            start_time=datetime.now()
        )

        if not self.current_specification:
            result.errors.append("No specification to validate")
            return result

        try:
            validation_result = self.validation_gate.validate_specification(
                self.current_specification
            )

            result.success = validation_result.passed()
            result.confidence_score = validation_result.confidence_score.overall
            result.validation_passed = validation_result.passed()
            result.message = f"Validation {'passed' if result.success else 'failed'}"
            result.output = validation_result.to_dict()

            if not result.success:
                for issue in validation_result.issues:
                    if issue.severity in ['critical', 'high']:
                        result.errors.append(issue.description)
                    else:
                        result.warnings.append(issue.description)

        except Exception as e:
            result.errors.append(f"Validation failed: {e}")

        return result

    def initialize_skills(self):
        """Initialize skill registry."""
        try:
            self.skill_manager.initialize()
            return True
        except Exception as e:
            print(f"Warning: Failed to initialize skills: {e}")
            return False
