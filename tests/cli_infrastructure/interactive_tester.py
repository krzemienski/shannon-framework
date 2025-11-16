"""
InteractiveCLITester - Test interactive CLI behavior with keyboard input

Uses pseudo-terminal (pty) to simulate real terminal interaction.
Unix-only (requires pty module).

Part of Wave 0: Testing Infrastructure
"""

import subprocess
import time
import os
import sys
import re
import select
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class InteractionEvent:
    """One keyboard interaction event"""
    time: float                    # Time since start
    key: str                       # Key pressed
    output_before: str            # Output before key press
    output_after: str             # Output after key press
    response_detected: bool       # Whether output changed


@dataclass
class InteractiveResult:
    """
    Result of interactive CLI test

    Contains complete output history and all interaction events.
    """

    command: str                              # Command executed
    exit_code: int                            # Exit code
    output_history: List[Tuple[float, str]]  # [(time, output)]
    interactions: List[InteractionEvent]     # All interactions
    duration_seconds: float                  # Total duration

    def validate_key_response(self, key: str, expected_pattern: str) -> bool:
        """
        Validate output changed after key press

        Args:
            key: Key that was pressed
            expected_pattern: Regex pattern expected in output after keypress

        Returns:
            True if pattern found in output after keypress
        """

        # Find interaction with this key
        interaction = next(
            (i for i in self.interactions if i.key == key),
            None
        )

        if not interaction:
            return False

        # Check if output after matches expected pattern
        output_after = interaction.output_after
        return re.search(expected_pattern, output_after) is not None

    def get_expansion_ratio(self, key: str = '\r') -> Optional[float]:
        """
        Calculate expansion ratio after key press

        Args:
            key: Key to check (default Enter)

        Returns:
            Ratio of lines after / lines before, or None
        """

        interaction = next(
            (i for i in self.interactions if i.key == key),
            None
        )

        if not interaction:
            return None

        lines_before = len(interaction.output_before.splitlines())
        lines_after = len(interaction.output_after.splitlines())

        if lines_before == 0:
            return None

        return lines_after / lines_before


class InteractiveCLITester:
    """
    Test interactive CLI behavior with keyboard input

    Uses pseudo-terminal (pty) to simulate real terminal interaction.
    Unix-only (requires pty module).

    Usage:
        tester = InteractiveCLITester()
        result = tester.run_interactive(
            command=['shannon', 'analyze', 'spec.md'],
            interactions=[
                (2.0, '\r'),  # Wait 2s, press Enter
                (1.0, 'p'),   # Wait 1s, press p
                (3.0, 'q')    # Wait 3s, press q
            ]
        )

        assert result.validate_key_response('\r', 'Expanded')
    """

    def __init__(self):
        if sys.platform == 'win32':
            raise RuntimeError("InteractiveCLITester requires Unix (pty not available on Windows)")

        self.master_fd: Optional[int] = None
        self.slave_fd: Optional[int] = None

    def run_interactive(
        self,
        command: List[str],
        interactions: List[Tuple[float, str]],
        timeout_seconds: int = 120,
        cwd: Optional[str] = None
    ) -> InteractiveResult:
        """
        Run command with interactive keyboard input

        Args:
            command: CLI command to execute
            interactions: List of (delay_seconds, key) tuples
                Example: [(2.0, '\r'), (1.0, 'esc'), (3.0, 'q')]
                Means: Wait 2s then press Enter, wait 1s then press Esc, wait 3s then press q
            timeout_seconds: Maximum execution time
            cwd: Working directory for command execution

        Returns:
            InteractiveResult with output history and interaction events
        """

        import pty

        # Create pseudo-terminal
        self.master_fd, self.slave_fd = pty.openpty()

        # Start process with pty
        process = subprocess.Popen(
            command,
            stdin=self.slave_fd,
            stdout=self.slave_fd,
            stderr=self.slave_fd,
            close_fds=False,
            cwd=cwd
        )

        start_time = time.time()
        output_history = []
        interaction_results = []

        interaction_idx = 0
        next_interaction_time = start_time + interactions[0][0] if interactions else None

        try:
            while process.poll() is None:
                now = time.time()

                # Check for interaction
                if (next_interaction_time and
                    now >= next_interaction_time and
                    interaction_idx < len(interactions)):

                    delay, key = interactions[interaction_idx]

                    # Capture output before interaction
                    output_before = self._read_available(self.master_fd, timeout=0.1)

                    # Send key
                    self._send_key(key)

                    # Wait for response
                    time.sleep(0.5)

                    # Capture output after interaction
                    output_after = self._read_available(self.master_fd, timeout=0.1)

                    interaction_results.append(InteractionEvent(
                        time=now - start_time,
                        key=key,
                        output_before=output_before,
                        output_after=output_after,
                        response_detected=output_after != output_before
                    ))

                    # Schedule next interaction
                    interaction_idx += 1
                    if interaction_idx < len(interactions):
                        next_interaction_time = now + interactions[interaction_idx][0]

                # Read available output
                output = self._read_available(self.master_fd, timeout=0.1)
                if output:
                    output_history.append((now - start_time, output))

                # Timeout check
                if (now - start_time) > timeout_seconds:
                    process.kill()
                    raise TimeoutError(f"Command timeout: {timeout_seconds}s")

                # Small sleep to prevent busy loop
                time.sleep(0.05)

            # Final output
            final_output = self._read_available(self.master_fd, timeout=0.5)
            if final_output:
                output_history.append((time.time() - start_time, final_output))

            returncode = process.returncode

        finally:
            os.close(self.master_fd)
            os.close(self.slave_fd)

        return InteractiveResult(
            command=' '.join(command),
            exit_code=returncode,
            output_history=output_history,
            interactions=interaction_results,
            duration_seconds=time.time() - start_time
        )

    def _read_available(self, fd: int, timeout: float = 0.0) -> str:
        """
        Read all available data from file descriptor

        Args:
            fd: File descriptor to read from
            timeout: Timeout in seconds

        Returns:
            Data as string (decoded UTF-8)
        """

        ready, _, _ = select.select([fd], [], [], timeout)

        if ready:
            try:
                data = os.read(fd, 4096)
                return data.decode('utf-8', errors='replace')
            except OSError:
                return ''

        return ''

    def _send_key(self, key: str):
        """
        Send key to process

        Args:
            key: Key to send (e.g., 'enter', '\r', 'esc', 'q', 'p')
        """

        # Map special keys to byte sequences
        key_bytes_map = {
            'enter': b'\r',
            '\r': b'\r',
            'esc': b'\x1b',
            '\x1b': b'\x1b',
            'q': b'q',
            'p': b'p',
            'up': b'\x1b[A',
            'down': b'\x1b[B',
            'left': b'\x1b[D',
            'right': b'\x1b[C',
            'space': b' ',
            'tab': b'\t',
            'backspace': b'\x7f'
        }

        key_bytes = key_bytes_map.get(key, key.encode('utf-8'))

        os.write(self.master_fd, key_bytes)
