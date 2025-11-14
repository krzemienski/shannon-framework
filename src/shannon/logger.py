"""Shannon CLI logging infrastructure with extreme logging support.

This module implements Shannon's extreme logging philosophy where EVERY function,
calculation, decision, and operation is logged with complete detail. This enables
functional testing via shell scripts that grep log output.

Logging Principles (from TECHNICAL_SPEC.md Section 15):
- P1: EVERY function logs entry and exit
- P2: EVERY calculation logs formula, inputs, result
- P3: EVERY decision logs condition and branch taken
- P4: EVERY loop logs iteration count and current item
- P5: EVERY exception logs full context before raising
- P6: EVERY file operation logs path, operation, success/failure
- P7: EVERY SDK call logs prompt preview, options, response
"""

from pathlib import Path
from typing import Any, Optional, Dict
from datetime import datetime
import sys
import os


class ShannonLogger:
    """Shannon CLI extreme logging implementation.

    Provides structured logging with both file and console output,
    designed to support functional testing via shell script validation.

    Log Format:
        TIMESTAMP | MODULE | LEVEL | MESSAGE

    Example:
        2025-11-09 14:30:15.123 | shannon.core.spec_analyzer | DEBUG | ENTER: analyze

    Attributes:
        session_id: Unique session identifier for log file naming
        module_name: Python module name for log prefixing
        log_file: Path to session log file
        log_level: Minimum log level to output (DEBUG, INFO, WARNING, ERROR)
        file_handle: Open file handle for log file
        _indent_level: Current indentation level for nested calls

    Usage:
        >>> logger = ShannonLogger('session_123', 'shannon.core')
        >>> logger.log_function_entry('analyze', spec_file='spec.md')
        >>> logger.debug("Processing specification")
        >>> logger.log_calculation('complexity', 'sum(dims)/8', {'dims': [0.5, 0.6]}, 0.55)
        >>> logger.log_function_exit('analyze', return_value={'complexity': 0.55})
    """

    # ANSI color codes for console output
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'RESET': '\033[0m'      # Reset
    }

    def __init__(
        self,
        session_id: str,
        module_name: str = 'shannon',
        log_level: str = 'DEBUG'
    ) -> None:
        """Initialize Shannon logger for a specific session.

        Args:
            session_id: Unique identifier for the session
            module_name: Python module name (e.g., 'shannon.core.spec_analyzer')
            log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR)

        Raises:
            OSError: If log directory cannot be created or file cannot be opened
        """
        self.session_id = session_id
        self.module_name = module_name
        self.log_level = log_level
        self._indent_level = 0

        # Determine log directory
        config_dir = Path.home() / '.shannon'
        log_dir = config_dir / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create log file path
        self.log_file = log_dir / f"{session_id}.log"

        # Open log file for appending
        self.file_handle = open(self.log_file, 'a', encoding='utf-8')

        # Log logger initialization
        self._write_log('INFO', f"Logger initialized for session {session_id}")

    def _get_timestamp(self) -> str:
        """Get formatted timestamp with millisecond precision.

        Returns:
            Timestamp string in format: YYYY-MM-DD HH:MM:SS.mmm

        Example:
            2025-11-09 14:30:15.123
        """
        now = datetime.now()
        return now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    def _should_log(self, level: str) -> bool:
        """Check if message should be logged based on log level.

        Args:
            level: Log level of message (DEBUG, INFO, WARNING, ERROR)

        Returns:
            True if message should be logged, False otherwise
        """
        level_priority = {
            'DEBUG': 0,
            'INFO': 1,
            'WARNING': 2,
            'ERROR': 3
        }

        message_priority = level_priority.get(level, 0)
        current_priority = level_priority.get(self.log_level, 0)

        return message_priority >= current_priority

    def _format_value(self, value: Any, max_length: int = 100) -> str:
        """Format value for logging with length limit.

        Args:
            value: Value to format
            max_length: Maximum length of formatted string

        Returns:
            Formatted string representation of value
        """
        if value is None:
            return 'None'

        if isinstance(value, str):
            if len(value) > max_length:
                return f"{value[:max_length]}... ({len(value)} chars)"
            return f"'{value}'"

        if isinstance(value, (list, tuple)):
            if len(value) > 5:
                items = ', '.join(str(v) for v in value[:5])
                return f"[{items}, ... ({len(value)} items)]"
            return str(value)

        if isinstance(value, dict):
            if len(value) > 5:
                items = list(value.items())[:5]
                formatted = ', '.join(f"{k}: {v}" for k, v in items)
                return f"{{{formatted}, ... ({len(value)} keys)}}"
            return str(value)

        return str(value)

    def _write_log(
        self,
        level: str,
        message: str,
        indent: bool = True
    ) -> None:
        """Write log message to both file and console.

        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR)
            message: Log message
            indent: Whether to apply current indentation level
        """
        if not self._should_log(level):
            return

        timestamp = self._get_timestamp()

        # Apply indentation if requested
        indent_str = '  ' * self._indent_level if indent else ''

        # Format log line
        log_line = f"{timestamp} | {self.module_name} | {level:7} | {indent_str}{message}"

        # Write to file (no color)
        self.file_handle.write(log_line + '\n')
        self.file_handle.flush()

        # Write to console (with color)
        color = self.COLORS.get(level, self.COLORS['RESET'])
        console_line = f"{color}{log_line}{self.COLORS['RESET']}"
        print(console_line)

    def debug(self, message: str) -> None:
        """Log debug message.

        Args:
            message: Debug message to log
        """
        self._write_log('DEBUG', message)

    def info(self, message: str) -> None:
        """Log info message.

        Args:
            message: Info message to log
        """
        self._write_log('INFO', message)

    def warning(self, message: str) -> None:
        """Log warning message.

        Args:
            message: Warning message to log
        """
        self._write_log('WARNING', message)

    def error(self, message: str) -> None:
        """Log error message.

        Args:
            message: Error message to log
        """
        self._write_log('ERROR', message)

    def log_function_entry(
        self,
        func_name: str,
        **params: Any
    ) -> None:
        """Log function entry with parameters (P1: EVERY function logs entry).

        This should be called at the start of EVERY function in Shannon CLI.

        Args:
            func_name: Name of the function being entered
            **params: Function parameters as keyword arguments

        Example:
            >>> logger.log_function_entry('analyze', spec_file='spec.md', depth=3)

            Output:
                DEBUG | ========================================
                DEBUG | ENTER: analyze
                DEBUG |   Parameters:
                DEBUG |     spec_file: 'spec.md'
                DEBUG |     depth: 3
                DEBUG | ========================================
        """
        self._write_log('DEBUG', '========================================', indent=False)
        self._write_log('DEBUG', f'ENTER: {func_name}', indent=False)

        if params:
            self._write_log('DEBUG', '  Parameters:', indent=False)
            for key, value in params.items():
                formatted_value = self._format_value(value)
                self._write_log('DEBUG', f'    {key}: {formatted_value}', indent=False)

        self._write_log('DEBUG', '========================================', indent=False)

        # Increase indentation for nested calls
        self._indent_level += 1

    def log_function_exit(
        self,
        func_name: str,
        return_value: Any = None,
        duration_ms: Optional[float] = None
    ) -> None:
        """Log function exit with return value (P1: EVERY function logs exit).

        This should be called at the end of EVERY function in Shannon CLI.

        Args:
            func_name: Name of the function being exited
            return_value: Value being returned by function
            duration_ms: Optional execution duration in milliseconds

        Example:
            >>> logger.log_function_exit('analyze', return_value={'complexity': 0.55}, duration_ms=123.5)

            Output:
                DEBUG | EXIT: analyze
                DEBUG |   Return value: {'complexity': 0.55}
                DEBUG |   Duration: 123.5ms
        """
        # Decrease indentation
        self._indent_level = max(0, self._indent_level - 1)

        self._write_log('DEBUG', f'EXIT: {func_name}', indent=False)

        if return_value is not None:
            formatted_value = self._format_value(return_value)
            self._write_log('DEBUG', f'  Return value: {formatted_value}', indent=False)

        if duration_ms is not None:
            self._write_log('DEBUG', f'  Duration: {duration_ms:.1f}ms', indent=False)

    def log_calculation(
        self,
        name: str,
        formula: str,
        inputs: Dict[str, Any],
        result: Any,
        intermediate_steps: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log calculation with formula, inputs, and result (P2: EVERY calculation logs).

        This should be called for EVERY calculation in Shannon CLI.

        Args:
            name: Name of the calculation
            formula: Mathematical formula or algorithm description
            inputs: Input values used in calculation
            result: Calculated result
            intermediate_steps: Optional intermediate calculation steps

        Example:
            >>> logger.log_calculation(
            ...     'structural_score',
            ...     'file_count * 0.02',
            ...     {'file_count': 50},
            ...     1.0,
            ...     {'file_factor': 0.567, 'weighted': 0.113}
            ... )

            Output:
                DEBUG | CALCULATION: structural_score
                DEBUG |   Formula: file_count * 0.02
                DEBUG |   Inputs:
                DEBUG |     file_count: 50
                DEBUG |   Intermediate:
                DEBUG |     file_factor: 0.567
                DEBUG |     weighted: 0.113
                DEBUG |   Result: 1.0
        """
        self._write_log('DEBUG', f'CALCULATION: {name}')
        self._write_log('DEBUG', f'  Formula: {formula}')

        if inputs:
            self._write_log('DEBUG', '  Inputs:')
            for key, value in inputs.items():
                self._write_log('DEBUG', f'    {key}: {value}')

        if intermediate_steps:
            self._write_log('DEBUG', '  Intermediate:')
            for key, value in intermediate_steps.items():
                self._write_log('DEBUG', f'    {key}: {value}')

        formatted_result = self._format_value(result)
        self._write_log('DEBUG', f'  Result: {formatted_result}')

    def log_decision(
        self,
        name: str,
        condition: str,
        result: bool,
        branch_taken: str
    ) -> None:
        """Log decision with condition and branch taken (P3: EVERY decision logs).

        Args:
            name: Name of the decision point
            condition: Condition being evaluated
            result: Boolean result of condition
            branch_taken: Which branch was taken

        Example:
            >>> logger.log_decision(
            ...     'complexity_threshold',
            ...     'complexity > 0.6',
            ...     True,
            ...     'WAVE-BASED execution'
            ... )

            Output:
                DEBUG | DECISION: complexity_threshold
                DEBUG |   Condition: complexity > 0.6
                DEBUG |   Result: True
                DEBUG |   Branch: WAVE-BASED execution
        """
        self._write_log('DEBUG', f'DECISION: {name}')
        self._write_log('DEBUG', f'  Condition: {condition}')
        self._write_log('DEBUG', f'  Result: {result}')
        self._write_log('DEBUG', f'  Branch: {branch_taken}')

    def log_loop_iteration(
        self,
        loop_name: str,
        iteration: int,
        total: Optional[int] = None,
        current_item: Any = None
    ) -> None:
        """Log loop iteration (P4: EVERY loop logs iteration count).

        Args:
            loop_name: Name of the loop
            iteration: Current iteration number (0-based)
            total: Total number of iterations (if known)
            current_item: Current item being processed

        Example:
            >>> logger.log_loop_iteration('process_files', 3, 10, 'spec.md')

            Output:
                DEBUG | LOOP: process_files
                DEBUG |   Iteration: 3/10
                DEBUG |   Current: 'spec.md'
        """
        if total is not None:
            iteration_str = f'{iteration}/{total}'
        else:
            iteration_str = str(iteration)

        self._write_log('DEBUG', f'LOOP: {loop_name}')
        self._write_log('DEBUG', f'  Iteration: {iteration_str}')

        if current_item is not None:
            formatted_item = self._format_value(current_item)
            self._write_log('DEBUG', f'  Current: {formatted_item}')

    def log_exception(
        self,
        exception: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log exception with full context (P5: EVERY exception logs full context).

        Args:
            exception: Exception object
            context: Additional context information

        Example:
            >>> logger.log_exception(
            ...     ValueError("Invalid complexity"),
            ...     {'input': -0.5, 'expected': '0.0-1.0'}
            ... )

            Output:
                ERROR | EXCEPTION: ValueError
                ERROR |   Message: Invalid complexity
                ERROR |   Context:
                ERROR |     input: -0.5
                ERROR |     expected: '0.0-1.0'
        """
        self._write_log('ERROR', f'EXCEPTION: {type(exception).__name__}')
        self._write_log('ERROR', f'  Message: {str(exception)}')

        if context:
            self._write_log('ERROR', '  Context:')
            for key, value in context.items():
                formatted_value = self._format_value(value)
                self._write_log('ERROR', f'    {key}: {formatted_value}')

    def log_file_operation(
        self,
        operation: str,
        path: str | Path,
        success: bool,
        details: Optional[str] = None
    ) -> None:
        """Log file operation (P6: EVERY file operation logs).

        Args:
            operation: Type of operation (read, write, delete, etc.)
            path: File or directory path
            success: Whether operation succeeded
            details: Optional additional details

        Example:
            >>> logger.log_file_operation('write', '/path/to/file.json', True, '1234 bytes')

            Output:
                DEBUG | FILE: write
                DEBUG |   Path: /path/to/file.json
                DEBUG |   Success: True
                DEBUG |   Details: 1234 bytes
        """
        self._write_log('DEBUG', f'FILE: {operation}')
        self._write_log('DEBUG', f'  Path: {path}')
        self._write_log('DEBUG', f'  Success: {success}')

        if details:
            self._write_log('DEBUG', f'  Details: {details}')

    def log_sdk_call(
        self,
        operation: str,
        prompt_preview: str,
        options: Dict[str, Any],
        response_preview: Optional[str] = None
    ) -> None:
        """Log Claude SDK call (P7: EVERY SDK call logs).

        Args:
            operation: SDK operation name
            prompt_preview: Preview of prompt (first 200 chars)
            options: SDK call options
            response_preview: Preview of response (if available)

        Example:
            >>> logger.log_sdk_call(
            ...     'create_agent',
            ...     'Analyze specification...',
            ...     {'max_tokens': 150000, 'temperature': 0.0},
            ...     'Analysis complete: 0.68'
            ... )

            Output:
                DEBUG | SDK: create_agent
                DEBUG |   Prompt: Analyze specification... (1234 chars)
                DEBUG |   Options:
                DEBUG |     max_tokens: 150000
                DEBUG |     temperature: 0.0
                DEBUG |   Response: Analysis complete: 0.68
        """
        self._write_log('DEBUG', f'SDK: {operation}')
        self._write_log('DEBUG', f'  Prompt: {prompt_preview[:200]}...')

        if options:
            self._write_log('DEBUG', '  Options:')
            for key, value in options.items():
                self._write_log('DEBUG', f'    {key}: {value}')

        if response_preview:
            self._write_log('DEBUG', f'  Response: {response_preview[:200]}...')

    def close(self) -> None:
        """Close logger and flush file handle.

        Should be called when logging session is complete.
        """
        self._write_log('INFO', f'Logger closed for session {self.session_id}')
        self.file_handle.close()

    def __enter__(self) -> 'ShannonLogger':
        """Context manager entry.

        Returns:
            Self for context manager usage
        """
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        if exc_type is not None:
            self.log_exception(exc_val)

        self.close()

    def __repr__(self) -> str:
        """String representation of logger.

        Returns:
            String representation showing session ID and module name
        """
        return f"ShannonLogger(session={self.session_id!r}, module={self.module_name!r})"
