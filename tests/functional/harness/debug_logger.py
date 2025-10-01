"""
Comprehensive debug logging system for Shannon functional testing.

Provides structured logging for command execution, MCP interactions,
artifact creation, and error tracking with session-based organization.
"""

import logging
import json
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum


class LogLevel(Enum):
    """Log severity levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class CommandLogEntry:
    """Structured command log entry"""
    timestamp: str
    command: str
    context: Optional[Dict[str, Any]]
    result: Optional[Any]
    duration: Optional[float]
    status: str  # started, completed, failed

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class MCPLogEntry:
    """Structured MCP interaction log entry"""
    timestamp: str
    server: str
    tool: str
    args: Dict[str, Any]
    result: Optional[Any]
    duration: Optional[float]
    error: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class ArtifactLogEntry:
    """Structured artifact log entry"""
    timestamp: str
    filepath: str
    artifact_type: str
    size_bytes: Optional[int]
    metadata: Optional[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class ErrorLogEntry:
    """Structured error log entry"""
    timestamp: str
    context: str
    error_type: str
    error_message: str
    stacktrace: str
    severity: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class CommandLogger:
    """Logs command execution details"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.commands: List[CommandLogEntry] = []
        self.active_commands: Dict[str, datetime] = {}

    def log_start(self, command: str, context: Optional[Dict] = None) -> None:
        """Log command execution start"""
        timestamp = datetime.now().isoformat()
        self.active_commands[command] = datetime.now()

        entry = CommandLogEntry(
            timestamp=timestamp,
            command=command,
            context=context,
            result=None,
            duration=None,
            status="started"
        )
        self.commands.append(entry)

        self.logger.info(f"COMMAND START: {command}")
        if context:
            self.logger.debug(f"Context: {json.dumps(context, indent=2)}")

    def log_end(
        self,
        command: str,
        result: Any,
        status: str = "completed"
    ) -> None:
        """Log command completion"""
        timestamp = datetime.now().isoformat()

        # Calculate duration
        duration = None
        if command in self.active_commands:
            start_time = self.active_commands.pop(command)
            duration = (datetime.now() - start_time).total_seconds()

        entry = CommandLogEntry(
            timestamp=timestamp,
            command=command,
            context=None,
            result=self._sanitize_result(result),
            duration=duration,
            status=status
        )
        self.commands.append(entry)

        self.logger.info(
            f"COMMAND END: {command} (status: {status}, duration: {duration:.2f}s)"
        )
        self.logger.debug(f"Result: {self._format_result(result)}")

    def log_failure(self, command: str, error: Exception) -> None:
        """Log command failure"""
        self.log_end(command, {"error": str(error)}, status="failed")

    def get_statistics(self) -> Dict[str, Any]:
        """Get command execution statistics"""
        completed = [c for c in self.commands if c.status == "completed"]
        failed = [c for c in self.commands if c.status == "failed"]

        durations = [c.duration for c in completed if c.duration]
        avg_duration = sum(durations) / len(durations) if durations else 0

        return {
            "total_commands": len(self.commands),
            "completed": len(completed),
            "failed": len(failed),
            "success_rate": len(completed) / len(self.commands) if self.commands else 0,
            "average_duration": avg_duration,
            "total_duration": sum(durations)
        }

    def _sanitize_result(self, result: Any) -> Any:
        """Sanitize result for logging"""
        if isinstance(result, (str, int, float, bool, type(None))):
            return result
        elif isinstance(result, dict):
            return {k: self._sanitize_result(v) for k, v in result.items()}
        elif isinstance(result, list):
            return [self._sanitize_result(item) for item in result[:10]]  # Limit size
        else:
            return str(result)[:200]

    def _format_result(self, result: Any) -> str:
        """Format result for logging"""
        result_str = str(result)
        if len(result_str) > 500:
            return result_str[:500] + "... (truncated)"
        return result_str


class MCPLogger:
    """Logs MCP server interactions"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.mcp_calls: List[MCPLogEntry] = []
        self.active_calls: Dict[str, datetime] = {}

    def log_call(
        self,
        server: str,
        tool: str,
        args: Dict[str, Any],
        result: Optional[Any] = None,
        error: Optional[str] = None
    ) -> None:
        """Log MCP server call"""
        timestamp = datetime.now().isoformat()
        call_id = f"{server}.{tool}"

        # Calculate duration if call was tracked
        duration = None
        if call_id in self.active_calls:
            start_time = self.active_calls.pop(call_id)
            duration = (datetime.now() - start_time).total_seconds()

        entry = MCPLogEntry(
            timestamp=timestamp,
            server=server,
            tool=tool,
            args=self._sanitize_args(args),
            result=self._sanitize_result(result) if result else None,
            duration=duration,
            error=error
        )
        self.mcp_calls.append(entry)

        status = "ERROR" if error else "SUCCESS"
        self.logger.info(f"MCP: {server}.{tool} ({status})")
        self.logger.debug(f"Args: {json.dumps(args, indent=2)}")

        if result:
            self.logger.debug(f"Result: {self._format_result(result)}")
        if error:
            self.logger.error(f"Error: {error}")

    def log_call_start(self, server: str, tool: str) -> None:
        """Track MCP call start time"""
        call_id = f"{server}.{tool}"
        self.active_calls[call_id] = datetime.now()

    def get_statistics(self) -> Dict[str, Any]:
        """Get MCP call statistics"""
        by_server = {}
        for call in self.mcp_calls:
            if call.server not in by_server:
                by_server[call.server] = {"total": 0, "errors": 0, "tools": {}}

            by_server[call.server]["total"] += 1
            if call.error:
                by_server[call.server]["errors"] += 1

            tool_count = by_server[call.server]["tools"].get(call.tool, 0)
            by_server[call.server]["tools"][call.tool] = tool_count + 1

        return {
            "total_calls": len(self.mcp_calls),
            "by_server": by_server,
            "error_rate": sum(1 for c in self.mcp_calls if c.error) / len(self.mcp_calls)
                if self.mcp_calls else 0
        }

    def _sanitize_args(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize arguments for logging"""
        sanitized = {}
        for key, value in args.items():
            if isinstance(value, str) and len(value) > 200:
                sanitized[key] = value[:200] + "... (truncated)"
            else:
                sanitized[key] = value
        return sanitized

    def _sanitize_result(self, result: Any) -> Any:
        """Sanitize result for logging"""
        if isinstance(result, str) and len(result) > 500:
            return result[:500] + "... (truncated)"
        return result

    def _format_result(self, result: Any) -> str:
        """Format result for logging"""
        result_str = str(result)
        if len(result_str) > 300:
            return result_str[:300] + "... (truncated)"
        return result_str


class ArtifactLogger:
    """Logs artifact creation and management"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.artifacts: List[ArtifactLogEntry] = []

    def log_created(
        self,
        filepath: Path,
        artifact_type: str = "file",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log artifact creation"""
        timestamp = datetime.now().isoformat()

        # Get file size if exists
        size_bytes = None
        if filepath.exists():
            size_bytes = filepath.stat().st_size

        entry = ArtifactLogEntry(
            timestamp=timestamp,
            filepath=str(filepath),
            artifact_type=artifact_type,
            size_bytes=size_bytes,
            metadata=metadata
        )
        self.artifacts.append(entry)

        self.logger.info(f"ARTIFACT: {filepath} ({artifact_type})")
        if size_bytes:
            self.logger.debug(f"Size: {size_bytes} bytes")
        if metadata:
            self.logger.debug(f"Metadata: {json.dumps(metadata, indent=2)}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get artifact statistics"""
        by_type = {}
        total_size = 0

        for artifact in self.artifacts:
            artifact_type = artifact.artifact_type
            if artifact_type not in by_type:
                by_type[artifact_type] = {"count": 0, "total_size": 0}

            by_type[artifact_type]["count"] += 1
            if artifact.size_bytes:
                by_type[artifact_type]["total_size"] += artifact.size_bytes
                total_size += artifact.size_bytes

        return {
            "total_artifacts": len(self.artifacts),
            "total_size_bytes": total_size,
            "by_type": by_type
        }


class ErrorLogger:
    """Logs errors with detailed context"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.errors: List[ErrorLogEntry] = []

    def log_error(
        self,
        error: Exception,
        context: str,
        severity: str = "ERROR"
    ) -> None:
        """Log error with full context and stacktrace"""
        timestamp = datetime.now().isoformat()

        entry = ErrorLogEntry(
            timestamp=timestamp,
            context=context,
            error_type=type(error).__name__,
            error_message=str(error),
            stacktrace=traceback.format_exc(),
            severity=severity
        )
        self.errors.append(entry)

        self.logger.error(f"ERROR in {context}: {error}")
        self.logger.debug(f"Type: {type(error).__name__}")
        self.logger.debug(f"Stacktrace:\n{traceback.format_exc()}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get error statistics"""
        by_type = {}
        by_context = {}

        for error in self.errors:
            # Count by error type
            error_type = error.error_type
            by_type[error_type] = by_type.get(error_type, 0) + 1

            # Count by context
            context = error.context
            by_context[context] = by_context.get(context, 0) + 1

        return {
            "total_errors": len(self.errors),
            "by_type": by_type,
            "by_context": by_context
        }


class SessionReporter:
    """Generates comprehensive session reports"""

    def __init__(
        self,
        command_logger: CommandLogger,
        mcp_logger: MCPLogger,
        artifact_logger: ArtifactLogger,
        error_logger: ErrorLogger
    ):
        self.command_logger = command_logger
        self.mcp_logger = mcp_logger
        self.artifact_logger = artifact_logger
        self.error_logger = error_logger

    def generate_report(self, session_id: str) -> str:
        """Generate comprehensive markdown report"""
        cmd_stats = self.command_logger.get_statistics()
        mcp_stats = self.mcp_logger.get_statistics()
        artifact_stats = self.artifact_logger.get_statistics()
        error_stats = self.error_logger.get_statistics()

        report = f"""# Shannon Test Session Report

**Session ID**: {session_id}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

### Command Execution
- **Total Commands**: {cmd_stats['total_commands']}
- **Completed**: {cmd_stats['completed']}
- **Failed**: {cmd_stats['failed']}
- **Success Rate**: {cmd_stats['success_rate']:.1%}
- **Average Duration**: {cmd_stats['average_duration']:.2f}s
- **Total Duration**: {cmd_stats['total_duration']:.2f}s

### MCP Interactions
- **Total Calls**: {mcp_stats['total_calls']}
- **Error Rate**: {mcp_stats['error_rate']:.1%}

### Artifacts Created
- **Total Artifacts**: {artifact_stats['total_artifacts']}
- **Total Size**: {artifact_stats['total_size_bytes']} bytes

### Errors
- **Total Errors**: {error_stats['total_errors']}

---

## Detailed Analysis

### Commands
{self._format_command_details(cmd_stats)}

### MCP Server Usage
{self._format_mcp_details(mcp_stats)}

### Artifacts
{self._format_artifact_details(artifact_stats)}

### Errors
{self._format_error_details(error_stats)}

---

## Timeline
{self._format_timeline()}

---

## Recommendations
{self._generate_recommendations(cmd_stats, mcp_stats, error_stats)}
"""

        return report

    def _format_command_details(self, stats: Dict[str, Any]) -> str:
        """Format command execution details"""
        lines = []
        for cmd in self.command_logger.commands[-10:]:  # Last 10 commands
            status_icon = "✅" if cmd.status == "completed" else "❌"
            duration_str = f"{cmd.duration:.2f}s" if cmd.duration else "N/A"
            lines.append(
                f"- {status_icon} `{cmd.command}` - {duration_str}"
            )
        return "\n".join(lines) if lines else "No commands executed"

    def _format_mcp_details(self, stats: Dict[str, Any]) -> str:
        """Format MCP server details"""
        lines = []
        for server, data in stats['by_server'].items():
            lines.append(f"#### {server}")
            lines.append(f"- Total Calls: {data['total']}")
            lines.append(f"- Errors: {data['errors']}")
            lines.append("- Tools Used:")
            for tool, count in data['tools'].items():
                lines.append(f"  - `{tool}`: {count}")
            lines.append("")
        return "\n".join(lines) if lines else "No MCP calls made"

    def _format_artifact_details(self, stats: Dict[str, Any]) -> str:
        """Format artifact details"""
        lines = []
        for artifact_type, data in stats['by_type'].items():
            lines.append(
                f"- **{artifact_type}**: {data['count']} files, "
                f"{data['total_size']} bytes"
            )
        return "\n".join(lines) if lines else "No artifacts created"

    def _format_error_details(self, stats: Dict[str, Any]) -> str:
        """Format error details"""
        lines = []
        for error_type, count in stats['by_type'].items():
            lines.append(f"- `{error_type}`: {count}")
        return "\n".join(lines) if lines else "No errors encountered"

    def _format_timeline(self) -> str:
        """Format execution timeline"""
        events = []

        # Collect all timestamped events
        for cmd in self.command_logger.commands:
            events.append((cmd.timestamp, f"CMD: {cmd.command} ({cmd.status})"))

        for mcp in self.mcp_logger.mcp_calls:
            status = "ERROR" if mcp.error else "OK"
            events.append((mcp.timestamp, f"MCP: {mcp.server}.{mcp.tool} ({status})"))

        for artifact in self.artifact_logger.artifacts:
            events.append((artifact.timestamp, f"ARTIFACT: {Path(artifact.filepath).name}"))

        # Sort by timestamp
        events.sort(key=lambda x: x[0])

        # Format as markdown list
        lines = []
        for timestamp, description in events[-20:]:  # Last 20 events
            time_str = timestamp.split('T')[1].split('.')[0]
            lines.append(f"- **{time_str}**: {description}")

        return "\n".join(lines) if lines else "No events recorded"

    def _generate_recommendations(
        self,
        cmd_stats: Dict[str, Any],
        mcp_stats: Dict[str, Any],
        error_stats: Dict[str, Any]
    ) -> str:
        """Generate recommendations based on session data"""
        recommendations = []

        # Command success rate
        if cmd_stats['success_rate'] < 0.8:
            recommendations.append(
                "⚠️ Command success rate is below 80%. Investigate failures."
            )

        # MCP error rate
        if mcp_stats['error_rate'] > 0.1:
            recommendations.append(
                "⚠️ MCP error rate is above 10%. Check server configurations."
            )

        # Performance
        if cmd_stats['average_duration'] > 5.0:
            recommendations.append(
                "⚠️ Average command duration exceeds 5s. Consider optimization."
            )

        # Errors
        if error_stats['total_errors'] > 0:
            recommendations.append(
                f"⚠️ {error_stats['total_errors']} errors encountered. Review error log."
            )

        if not recommendations:
            recommendations.append("✅ All metrics within acceptable ranges.")

        return "\n".join(recommendations)


class DebugLogger:
    """Main debug logging orchestrator"""

    def __init__(self, log_dir: Path):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Session identification
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.session_log = self.log_dir / f"session_{self.session_id}.log"

        # Set up base logger
        self._setup_base_logger()

        # Initialize specialized loggers
        self.command_logger = CommandLogger(
            self._create_logger('commands')
        )
        self.mcp_logger = MCPLogger(
            self._create_logger('mcp')
        )
        self.artifact_logger = ArtifactLogger(
            self._create_logger('artifacts')
        )
        self.error_logger = ErrorLogger(
            self._create_logger('errors')
        )

        # Session reporter
        self.reporter = SessionReporter(
            self.command_logger,
            self.mcp_logger,
            self.artifact_logger,
            self.error_logger
        )

        self.base_logger.info(f"Debug logging initialized (session: {self.session_id})")

    def _setup_base_logger(self) -> None:
        """Set up base session logger"""
        self.base_logger = logging.getLogger('shannon.debug')
        self.base_logger.setLevel(logging.DEBUG)

        # Session log handler
        session_handler = logging.FileHandler(self.session_log)
        session_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        self.base_logger.addHandler(session_handler)

        # Console handler for critical messages
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(
            logging.Formatter('%(levelname)s: %(message)s')
        )
        self.base_logger.addHandler(console_handler)

    def _create_logger(self, name: str) -> logging.Logger:
        """Create specialized logger"""
        logger = logging.getLogger(f'shannon.{name}')
        logger.setLevel(logging.DEBUG)

        # File handler
        handler = logging.FileHandler(self.log_dir / f"{name}.log")
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        logger.addHandler(handler)

        return logger

    def generate_session_report(self) -> Path:
        """Generate comprehensive session report"""
        report_content = self.reporter.generate_report(self.session_id)
        report_path = self.log_dir / f"report_{self.session_id}.md"
        report_path.write_text(report_content)

        self.base_logger.info(f"Session report generated: {report_path}")
        return report_path

    def get_session_summary(self) -> Dict[str, Any]:
        """Get quick session summary"""
        return {
            "session_id": self.session_id,
            "commands": self.command_logger.get_statistics(),
            "mcp_calls": self.mcp_logger.get_statistics(),
            "artifacts": self.artifact_logger.get_statistics(),
            "errors": self.error_logger.get_statistics()
        }
