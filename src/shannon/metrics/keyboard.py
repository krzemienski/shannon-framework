"""Non-blocking keyboard input handler for Shannon CLI V3.0

Provides non-blocking keyboard input using termios (macOS/Linux).

Key Features:
- Non-blocking key detection (Enter, Esc, q, p)
- Terminal setup/restoration (no corruption on exit)
- Graceful degradation on Windows (disables keyboard features)
- ESC sequence handling (distinguish ESC key from arrow keys)

Architecture:
    Terminal → termios cbreak mode → select() → Key detection → Dashboard control

Design Decision (from SHANNON_CLI_V3_ARCHITECTURE.md):
    - Use termios for non-blocking input (industry standard)
    - Support macOS/Linux only (Windows fallback: no keyboard)
    - Restore terminal state on exit (no corruption)
"""

import sys
import select
from typing import Optional
from enum import Enum


class Key(Enum):
    """Recognized keyboard keys"""
    ENTER = 'enter'
    ESC = 'esc'
    Q = 'q'
    P = 'p'
    UNKNOWN = 'unknown'


class KeyboardHandler:
    """
    Non-blocking keyboard input handler

    Platform Support:
        - macOS: Full support (termios + select)
        - Linux: Full support (termios + select)
        - Windows: Graceful degradation (no keyboard features)

    Usage:
        handler = KeyboardHandler()

        try:
            handler.setup_nonblocking()

            while running:
                key = handler.read_key(timeout=0.0)  # Non-blocking
                if key == Key.ESC:
                    break

        finally:
            handler.restore_terminal()  # Always restore

    Thread Safety:
        - Not thread-safe (use from main thread only)
        - Terminal state is global (affects all threads)
    """

    def __init__(self):
        """Initialize keyboard handler"""
        self.platform = sys.platform
        self.supported = self.platform in ['darwin', 'linux']
        self.old_settings = None
        self._termios = None
        self._tty = None

        # Import platform-specific modules
        if self.supported:
            try:
                import termios
                import tty
                self._termios = termios
                self._tty = tty
            except ImportError:
                # termios not available (shouldn't happen on macOS/Linux)
                self.supported = False

    def setup_nonblocking(self) -> bool:
        """
        Configure terminal for non-blocking input

        Sets terminal to cbreak mode:
        - Read character-by-character (no line buffering)
        - No echo to screen
        - No special processing (Ctrl+C still works)

        Returns:
            True if setup successful, False if not supported
        """
        if not self.supported or not self._termios or not self._tty:
            return False

        try:
            # Save original terminal settings
            self.old_settings = self._termios.tcgetattr(sys.stdin)

            # Set to cbreak mode (read char-by-char without Enter)
            # This allows non-blocking key detection while preserving Ctrl+C
            self._tty.setcbreak(sys.stdin.fileno())

            return True

        except Exception:
            # Terminal setup failed (not a TTY, redirected, etc.)
            self.supported = False
            return False

    def restore_terminal(self) -> None:
        """
        Restore original terminal settings

        CRITICAL: Always call this before exit to prevent terminal corruption.
        Use in finally block or context manager.
        """
        if self.old_settings and self._termios:
            try:
                self._termios.tcsetattr(
                    sys.stdin,
                    self._termios.TCSADRAIN,  # Drain output before changing
                    self.old_settings
                )
                self.old_settings = None
            except Exception:
                # Best effort - terminal may already be closed
                pass

    def read_key(self, timeout: float = 0.0) -> Optional[Key]:
        """
        Non-blocking key read with timeout

        Uses select() to check for input without blocking.
        Handles ESC sequences (arrow keys, etc.) correctly.

        Args:
            timeout: Max seconds to wait (0 = immediate return)

        Returns:
            Key if pressed, None if no input

        Example:
            # Non-blocking check
            key = handler.read_key(timeout=0.0)
            if key == Key.ENTER:
                expand_view()

            # Wait up to 0.1s for key
            key = handler.read_key(timeout=0.1)
        """
        if not self.supported:
            return None

        try:
            # Use select for non-blocking check
            ready, _, _ = select.select([sys.stdin], [], [], timeout)

            if not ready:
                return None

            # Read single character
            char = sys.stdin.read(1)

            # Map character to Key
            return self._parse_key(char)

        except Exception:
            # Read failed (terminal closed, etc.)
            return None

    def _parse_key(self, char: str) -> Optional[Key]:
        """
        Parse character to Key enum

        Handles:
        - Enter (\r or \n)
        - ESC key (distinguish from ESC sequences)
        - Regular keys (q, p, etc.)

        Args:
            char: Single character read from stdin

        Returns:
            Key enum or None if not recognized
        """
        # Enter key (can be \r or \n depending on platform)
        if char in ['\r', '\n']:
            return Key.ENTER

        # ESC key or start of escape sequence
        if char == '\x1b':
            # Check if more characters follow (escape sequence)
            ready, _, _ = select.select([sys.stdin], [], [], 0.1)

            if ready:
                # Escape sequence (arrow key, etc.) - consume and ignore
                try:
                    # Read rest of sequence (typically 2 more chars)
                    sys.stdin.read(2)
                except Exception:
                    pass
                return None  # Ignore escape sequences
            else:
                # Pure ESC key (no following chars)
                return Key.ESC

        # Regular keys
        if char.lower() == 'q':
            return Key.Q

        if char.lower() == 'p':
            return Key.P

        # Unknown key
        return None

    def __enter__(self):
        """Context manager support"""
        self.setup_nonblocking()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup"""
        self.restore_terminal()
        return False


# Convenience function for simple use cases

def wait_for_key(timeout: Optional[float] = None) -> Optional[Key]:
    """
    Wait for key press with optional timeout

    Simple wrapper for one-off key reads.
    For multiple reads, use KeyboardHandler directly.

    Args:
        timeout: Max seconds to wait (None = wait forever)

    Returns:
        Key pressed or None if timeout

    Example:
        # Wait for Enter or ESC
        key = wait_for_key(timeout=5.0)
        if key == Key.ENTER:
            print("Expanding...")
        elif key == Key.ESC:
            print("Collapsing...")
        else:
            print("Timeout")
    """
    handler = KeyboardHandler()

    if not handler.setup_nonblocking():
        return None

    try:
        # Wait for key with timeout
        key = handler.read_key(timeout=timeout or float('inf'))
        return key

    finally:
        handler.restore_terminal()
