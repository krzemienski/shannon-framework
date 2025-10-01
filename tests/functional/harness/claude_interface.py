"""
Test Harness for Claude Code Command Execution

Provides programmatic interface for executing Shannon commands in Claude Code
and capturing outputs for validation.

Classes:
    CommandResult: Data class for command outputs
    OutputCapture: Captures and parses command outputs
    SessionManager: Manages Claude Code session lifecycle
    ClaudeCodeInterface: Main interface for command execution
"""

import subprocess
import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from datetime import datetime
import tempfile
import shutil


@dataclass
class CommandResult:
    """
    Captures the result of a Claude Code command execution.

    Attributes:
        command: Original command string executed
        output: Captured stdout from command
        artifacts: List of files created by command
        success: Whether command completed successfully
        duration: Execution time in seconds
        timestamp: ISO format timestamp of execution
        errors: Captured stderr if any
        exit_code: Process exit code
        metadata: Additional command-specific metadata
    """
    command: str
    output: str
    artifacts: List[Path]
    success: bool
    duration: float
    timestamp: str
    errors: Optional[str] = None
    exit_code: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'command': self.command,
            'output': self.output,
            'artifacts': [str(a) for a in self.artifacts],
            'success': self.success,
            'duration': self.duration,
            'timestamp': self.timestamp,
            'errors': self.errors,
            'exit_code': self.exit_code,
            'metadata': self.metadata
        }

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class OutputCapture:
    """
    Captures and parses Claude Code command outputs.

    Provides utilities for extracting structured information from
    command outputs including artifacts, metrics, and status.
    """

    @staticmethod
    def parse_spec_output(output: str) -> Dict[str, Any]:
        """
        Parse /sh:spec command output.

        Extracts:
            - Complexity scores
            - Pattern detections
            - Recommendation counts
            - File paths
        """
        metadata = {
            'complexity_score': None,
            'patterns_detected': [],
            'recommendations': [],
            'spec_file': None
        }

        # Extract complexity score
        complexity_match = re.search(r'Complexity:\s*([\d.]+)', output)
        if complexity_match:
            metadata['complexity_score'] = float(complexity_match.group(1))

        # Extract patterns
        pattern_matches = re.findall(r'Pattern:\s*(\w+)', output)
        metadata['patterns_detected'] = pattern_matches

        # Extract recommendations
        rec_matches = re.findall(r'Recommendation:\s*(.+?)(?=\n|$)', output)
        metadata['recommendations'] = rec_matches

        # Extract spec file path
        spec_match = re.search(r'Spec file:\s*(.+\.md)', output)
        if spec_match:
            metadata['spec_file'] = spec_match.group(1)

        return metadata

    @staticmethod
    def parse_wave_output(output: str) -> Dict[str, Any]:
        """
        Parse wave orchestration command output.

        Extracts:
            - Wave count
            - Completion status
            - Wave summaries
        """
        metadata = {
            'wave_count': 0,
            'completed_waves': [],
            'pending_waves': [],
            'wave_summaries': []
        }

        # Extract wave count
        wave_count_match = re.search(r'Total waves:\s*(\d+)', output)
        if wave_count_match:
            metadata['wave_count'] = int(wave_count_match.group(1))

        # Extract completed waves
        completed_matches = re.findall(r'Wave (\d+):\s*✅', output)
        metadata['completed_waves'] = [int(w) for w in completed_matches]

        # Extract pending waves
        pending_matches = re.findall(r'Wave (\d+):\s*⏳', output)
        metadata['pending_waves'] = [int(w) for w in pending_matches]

        # Extract wave summaries
        summary_matches = re.findall(r'Wave (\d+) Summary:\s*(.+?)(?=Wave \d+|$)', output, re.DOTALL)
        metadata['wave_summaries'] = [
            {'wave': int(w), 'summary': s.strip()}
            for w, s in summary_matches
        ]

        return metadata

    @staticmethod
    def parse_checkpoint_output(output: str) -> Dict[str, Any]:
        """
        Parse /sh:checkpoint command output.

        Extracts:
            - Memory keys created
            - State snapshot info
            - Storage location
        """
        metadata = {
            'memory_keys': [],
            'snapshot_id': None,
            'storage_path': None
        }

        # Extract memory keys
        key_matches = re.findall(r'Memory:\s*(\w+)', output)
        metadata['memory_keys'] = key_matches

        # Extract snapshot ID
        snapshot_match = re.search(r'Snapshot:\s*(\w+)', output)
        if snapshot_match:
            metadata['snapshot_id'] = snapshot_match.group(1)

        # Extract storage path
        path_match = re.search(r'Stored:\s*(.+)', output)
        if path_match:
            metadata['storage_path'] = path_match.group(1)

        return metadata

    @staticmethod
    def extract_artifacts(output: str, project_dir: Path) -> List[Path]:
        """
        Extract artifact file paths from command output.

        Searches for common artifact patterns:
            - "Created: <path>"
            - "Generated: <path>"
            - "Saved to: <path>"
        """
        artifacts = []

        # Common artifact patterns
        patterns = [
            r'Created:\s*(.+\.(?:md|json|py|txt))',
            r'Generated:\s*(.+\.(?:md|json|py|txt))',
            r'Saved to:\s*(.+\.(?:md|json|py|txt))',
            r'Output:\s*(.+\.(?:md|json|py|txt))',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, output)
            for match in matches:
                artifact_path = project_dir / match.strip()
                if artifact_path.exists():
                    artifacts.append(artifact_path)

        return artifacts


class SessionManager:
    """
    Manages Claude Code session lifecycle.

    Handles:
        - Session initialization
        - Environment setup
        - Cleanup and teardown
        - State persistence
    """

    def __init__(self, project_dir: Path, session_id: Optional[str] = None):
        """
        Initialize session manager.

        Args:
            project_dir: Root directory for Shannon project
            session_id: Optional session identifier (auto-generated if None)
        """
        self.project_dir = project_dir
        self.session_id = session_id or self._generate_session_id()
        self.session_dir = project_dir / ".shannon" / "sessions" / self.session_id
        self.session_log: List[Dict[str, Any]] = []
        self.active = False

    def _generate_session_id(self) -> str:
        """Generate unique session identifier."""
        return f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def start(self) -> bool:
        """
        Start new session.

        Creates session directory and initializes state.

        Returns:
            True if session started successfully
        """
        try:
            self.session_dir.mkdir(parents=True, exist_ok=True)

            # Create session metadata
            metadata = {
                'session_id': self.session_id,
                'start_time': datetime.now().isoformat(),
                'project_dir': str(self.project_dir),
                'status': 'active'
            }

            metadata_file = self.session_dir / "metadata.json"
            metadata_file.write_text(json.dumps(metadata, indent=2))

            self.active = True
            return True

        except Exception as e:
            print(f"Failed to start session: {e}")
            return False

    def log_command(self, result: CommandResult) -> None:
        """
        Log command execution to session history.

        Args:
            result: CommandResult to log
        """
        log_entry = {
            'timestamp': result.timestamp,
            'command': result.command,
            'success': result.success,
            'duration': result.duration,
            'artifacts': [str(a) for a in result.artifacts],
            'metadata': result.metadata
        }

        self.session_log.append(log_entry)

        # Persist to disk
        log_file = self.session_dir / "command_log.json"
        log_file.write_text(json.dumps(self.session_log, indent=2))

    def end(self) -> Dict[str, Any]:
        """
        End session and generate summary.

        Returns:
            Session summary dictionary
        """
        if not self.active:
            return {}

        summary = {
            'session_id': self.session_id,
            'command_count': len(self.session_log),
            'successful_commands': sum(1 for log in self.session_log if log['success']),
            'total_duration': sum(log['duration'] for log in self.session_log),
            'artifacts_created': sum(len(log['artifacts']) for log in self.session_log),
            'end_time': datetime.now().isoformat()
        }

        # Update metadata
        metadata_file = self.session_dir / "metadata.json"
        if metadata_file.exists():
            metadata = json.loads(metadata_file.read_text())
            metadata.update({
                'status': 'completed',
                'summary': summary
            })
            metadata_file.write_text(json.dumps(metadata, indent=2))

        self.active = False
        return summary

    def cleanup(self, keep_artifacts: bool = True) -> None:
        """
        Clean up session resources.

        Args:
            keep_artifacts: If False, delete all session artifacts
        """
        if not keep_artifacts and self.session_dir.exists():
            shutil.rmtree(self.session_dir)


class ClaudeCodeInterface:
    """
    Main interface for Claude Code command execution.

    Provides methods for:
        - Executing Shannon commands
        - Capturing results
        - Managing sessions
        - Simulating command behavior
    """

    def __init__(
        self,
        project_dir: Path,
        debug: bool = True,
        simulation_mode: bool = True
    ):
        """
        Initialize Claude Code interface.

        Args:
            project_dir: Root directory for Shannon project
            debug: Enable debug logging
            simulation_mode: Use simulation instead of real Claude Code
        """
        self.project_dir = Path(project_dir).resolve()
        self.debug = debug
        self.simulation_mode = simulation_mode
        self.session: Optional[SessionManager] = None
        self.output_capture = OutputCapture()

        # Ensure Shannon directory exists
        self.shannon_dir = self.project_dir / ".shannon"
        self.shannon_dir.mkdir(exist_ok=True)

    def start_session(self, session_id: Optional[str] = None) -> bool:
        """
        Start new test session.

        Args:
            session_id: Optional session identifier

        Returns:
            True if session started successfully
        """
        self.session = SessionManager(self.project_dir, session_id)
        return self.session.start()

    def execute_command(
        self,
        command: str,
        timeout: int = 60,
        capture_artifacts: bool = True
    ) -> CommandResult:
        """
        Execute Shannon command and capture result.

        Args:
            command: Shannon command to execute (e.g., "/sh:spec @file.py")
            timeout: Maximum execution time in seconds
            capture_artifacts: Whether to discover created artifacts

        Returns:
            CommandResult with execution details
        """
        start_time = time.time()

        if self.debug:
            print(f"Executing: {command}")

        if self.simulation_mode:
            result = self._simulate_command(command, timeout)
        else:
            result = self._execute_real_command(command, timeout)

        result.duration = time.time() - start_time
        result.timestamp = datetime.now().isoformat()

        # Capture artifacts if requested
        if capture_artifacts:
            result.artifacts.extend(
                self.output_capture.extract_artifacts(result.output, self.project_dir)
            )

        # Log to session if active
        if self.session and self.session.active:
            self.session.log_command(result)

        return result

    def _simulate_command(self, command: str, timeout: int) -> CommandResult:
        """
        Simulate command execution for testing.

        Creates realistic output and artifacts without actual Claude Code.
        """
        # Parse command type
        cmd_type = self._parse_command_type(command)

        # Generate simulated output
        if cmd_type == 'spec':
            output = self._simulate_spec_command(command)
            metadata = self.output_capture.parse_spec_output(output)
        elif cmd_type == 'wave':
            output = self._simulate_wave_command(command)
            metadata = self.output_capture.parse_wave_output(output)
        elif cmd_type == 'checkpoint':
            output = self._simulate_checkpoint_command(command)
            metadata = self.output_capture.parse_checkpoint_output(output)
        else:
            output = f"Simulated output for: {command}"
            metadata = {}

        return CommandResult(
            command=command,
            output=output,
            artifacts=[],
            success=True,
            duration=0.0,
            timestamp="",
            metadata=metadata
        )

    def _simulate_spec_command(self, command: str) -> str:
        """Generate simulated /sh:spec output."""
        return """
Shannon Specification Analysis

Complexity: 0.75
Pattern: complex_logic
Pattern: multi_component
Recommendation: Break into smaller functions
Recommendation: Add unit tests

Spec file: .shannon/analysis/spec_20240930_120000.md
"""

    def _simulate_wave_command(self, command: str) -> str:
        """Generate simulated wave orchestration output."""
        return """
Wave Orchestration Started

Total waves: 3

Wave 1: ✅
Wave 1 Summary: Analysis completed successfully

Wave 2: ✅
Wave 2 Summary: Implementation phase complete

Wave 3: ⏳
Wave 3 Summary: Validation pending
"""

    def _simulate_checkpoint_command(self, command: str) -> str:
        """Generate simulated /sh:checkpoint output."""
        return """
Checkpoint Created

Memory: current_state
Memory: command_history
Snapshot: checkpoint_20240930_120000
Stored: .shannon/checkpoints/checkpoint_20240930_120000.json
"""

    def _execute_real_command(self, command: str, timeout: int) -> CommandResult:
        """
        Execute real Claude Code command via subprocess.

        Note: This requires actual Claude Code installation and configuration.
        """
        # Prepare command script
        script = self._prepare_command_script(command)

        try:
            result = subprocess.run(
                ['bash', '-c', script],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            return CommandResult(
                command=command,
                output=result.stdout,
                artifacts=[],
                success=result.returncode == 0,
                duration=0.0,
                timestamp="",
                errors=result.stderr if result.stderr else None,
                exit_code=result.returncode
            )

        except subprocess.TimeoutExpired:
            return CommandResult(
                command=command,
                output="",
                artifacts=[],
                success=False,
                duration=timeout,
                timestamp="",
                errors=f"Command timed out after {timeout} seconds",
                exit_code=-1
            )
        except Exception as e:
            return CommandResult(
                command=command,
                output="",
                artifacts=[],
                success=False,
                duration=0.0,
                timestamp="",
                errors=str(e),
                exit_code=-1
            )

    def _prepare_command_script(self, command: str) -> str:
        """
        Prepare bash script for command execution.

        In production, this would interact with actual Claude Code CLI.
        """
        return f'''
        cd {self.project_dir}
        # TODO: Actual Claude Code CLI integration
        # For now, return simulated output
        echo "Command: {command}"
        echo "Implementation pending: Requires Claude Code CLI interface"
        '''

    def _parse_command_type(self, command: str) -> str:
        """Parse command type from command string."""
        if command.startswith('/sh:spec'):
            return 'spec'
        elif command.startswith('/sh:wave'):
            return 'wave'
        elif command.startswith('/sh:checkpoint'):
            return 'checkpoint'
        else:
            return 'unknown'

    def end_session(self) -> Optional[Dict[str, Any]]:
        """
        End current session and return summary.

        Returns:
            Session summary if session was active
        """
        if self.session:
            return self.session.end()
        return None

    def cleanup_session(self, keep_artifacts: bool = True) -> None:
        """
        Clean up session resources.

        Args:
            keep_artifacts: If False, delete all session artifacts
        """
        if self.session:
            self.session.cleanup(keep_artifacts)
