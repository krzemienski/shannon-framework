"""
Enhanced Keyboard Handler for V3.1 Interactive Dashboard

Supports full keyboard input: Enter, Esc, 1-9, Arrows, Page Up/Down, Home/End, Space, etc.
Unix-only (uses termios for raw keyboard input).

Created: 2025-11-14
Part of: V3.1 Wave 1 (Navigation & State)
"""

import sys
import tty
import termios
import select
from typing import Optional
from .models import KeyEvent


class EnhancedKeyboardHandler:
    """
    Capture keyboard input in raw mode (non-blocking)

    Supports:
    - Enter, Esc, Space
    - Numbers 1-9
    - Arrow keys (↑↓←→)
    - Page Up/Down
    - Home/End
    - Letters (h, q, t, c, etc.)
    - Vim-style (j/k for down/up, g/G for home/end)

    Unix-only (requires termios).

    Usage:
        handler = EnhancedKeyboardHandler()
        handler.setup_nonblocking()

        try:
            while running:
                key = handler.poll_key()
                if key:
                    print(f"Key pressed: {key.key}")
        finally:
            handler.restore_terminal()
    """

    def __init__(self):
        if sys.platform == 'win32':
            raise RuntimeError("EnhancedKeyboardHandler requires Unix (termios not available on Windows)")

        self.fd = sys.stdin.fileno()
        self.old_settings = None
        self._setup_complete = False

    def setup_nonblocking(self):
        """
        Setup terminal for raw, non-blocking input

        Saves current terminal settings for restoration.
        """
        # Save original terminal settings
        self.old_settings = termios.tcgetattr(self.fd)

        # Set to raw mode (no echo, no line buffering)
        tty.setraw(self.fd)

        self._setup_complete = True

    def restore_terminal(self):
        """Restore terminal to original settings"""
        if self.old_settings:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            self._setup_complete = False

    def poll_key(self, timeout: float = 0.0) -> Optional[KeyEvent]:
        """
        Poll for keyboard input (non-blocking)

        Args:
            timeout: Max time to wait for input (default 0 = instant poll)

        Returns:
            KeyEvent if key pressed, None if no input
        """
        if not self._setup_complete:
            return None

        # Check if input available (non-blocking select)
        ready, _, _ = select.select([sys.stdin], [], [], timeout)

        if not ready:
            return None

        # Read one character
        ch = sys.stdin.read(1)

        # Parse character into KeyEvent
        return self._parse_key(ch)

    def _parse_key(self, ch: str) -> KeyEvent:
        """
        Parse raw character into KeyEvent

        Handles:
        - Single chars: 'a', '1', 'q'
        - Control chars: '\r' (Enter), '\x1b' (Esc)
        - Escape sequences: '\x1b[A' (Arrow Up), etc.
        """
        # Enter
        if ch == '\r' or ch == '\n':
            return KeyEvent('enter')

        # Escape or escape sequence
        if ch == '\x1b':
            # Check if there's more input (escape sequence vs just Esc key)
            ready, _, _ = select.select([sys.stdin], [], [], 0.05)

            if ready:
                # Read next char
                ch2 = sys.stdin.read(1)

                if ch2 == '[':
                    # ANSI escape sequence
                    ch3 = sys.stdin.read(1)

                    # Arrow keys
                    if ch3 == 'A':
                        return KeyEvent('up')
                    elif ch3 == 'B':
                        return KeyEvent('down')
                    elif ch3 == 'C':
                        return KeyEvent('right')
                    elif ch3 == 'D':
                        return KeyEvent('left')

                    # Check for extended sequences (Page Up/Down, Home/End)
                    elif ch3.isdigit():
                        # Read until ~
                        seq = ch3
                        while True:
                            ready, _, _ = select.select([sys.stdin], [], [], 0.01)
                            if not ready:
                                break
                            next_ch = sys.stdin.read(1)
                            seq += next_ch
                            if next_ch == '~':
                                break

                        # Parse sequences
                        if seq == '5~':
                            return KeyEvent('page_up')
                        elif seq == '6~':
                            return KeyEvent('page_down')
                        elif seq == '1~' or seq == 'H':
                            return KeyEvent('home')
                        elif seq == '4~' or seq == 'F':
                            return KeyEvent('end')

                # Alt+key combinations (not used currently)
                return KeyEvent('escape')  # Treat as Esc if unrecognized

            else:
                # Just Esc key (no sequence)
                return KeyEvent('escape')

        # Space
        if ch == ' ':
            return KeyEvent('space')

        # Tab
        if ch == '\t':
            return KeyEvent('tab')

        # Backspace
        if ch == '\x7f':
            return KeyEvent('backspace')

        # Ctrl+C (interrupt)
        if ch == '\x03':
            raise KeyboardInterrupt()

        # Regular characters (letters, numbers, symbols)
        return KeyEvent(ch.lower())  # Normalize to lowercase
