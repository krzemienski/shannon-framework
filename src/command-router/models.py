"""
Shannon Framework v4 - Command Router Models

Data structures for command routing and execution.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CommandType(Enum):
    """Command types."""
    ANALYZE_SPEC = "analyze_spec"         # Parse and analyze specification
    CREATE_PLAN = "create_plan"           # Create execution plan
    EXECUTE_PHASE = "execute_phase"       # Execute single phase
    EXECUTE_WAVE = "execute_wave"         # Execute single wave
    EXECUTE_FULL = "execute_full"         # Full end-to-end execution
    CHECKPOINT = "checkpoint"             # Create checkpoint
    RESTORE = "restore"                   # Restore from checkpoint
    STATUS = "status"                     # Get current status
    VALIDATE = "validate"                 # Run validation gate


class ExecutionMode(Enum):
    """Execution modes."""
    INTERACTIVE = "interactive"  # User confirms each step
    AUTO = "auto"               # Automatic execution
    DRY_RUN = "dry_run"        # Plan only, don't execute


@dataclass
class CommandContext:
    """Context for command execution."""
    # User input
    specification_text: Optional[str] = None
    specification_file: Optional[str] = None

    # Execution control
    mode: ExecutionMode = ExecutionMode.AUTO
    checkpoint_frequency: str = "per_wave"  # per_wave, per_phase, manual

    # Validation
    confidence_threshold: float = 0.90
    skip_validation: bool = False

    # Session
    session_id: Optional[str] = None
    checkpoint_id: Optional[str] = None

    # MCP
    available_mcps: List[str] = field(default_factory=list)

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CommandResult:
    """Result of command execution."""
    command_type: CommandType
    success: bool

    # Timing
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0

    # Output
    output: Optional[Any] = None
    message: str = ""

    # Validation
    confidence_score: Optional[float] = None
    validation_passed: bool = False

    # Errors and warnings
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # Artifacts
    artifacts: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'command_type': self.command_type.value,
            'success': self.success,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds,
            'output': self.output,
            'message': self.message,
            'confidence_score': self.confidence_score,
            'validation_passed': self.validation_passed,
            'errors': self.errors,
            'warnings': self.warnings,
            'artifacts': self.artifacts,
        }
