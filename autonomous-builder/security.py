"""
Security Manager for Autonomous Claude Code Builder.

Implements defense-in-depth security based on Claude Quickstart patterns:
- Command allowlist validation
- Extra validation for sensitive commands
- Path restriction enforcement
- Sandbox integration
"""

import shlex
import re
import ipaddress
from dataclasses import dataclass
from typing import List, Set, Optional, Dict, Any
from pathlib import Path
import logging

from .config import SecurityConfig

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of command validation."""
    allowed: bool
    reason: str
    command: str
    blocked_commands: List[str] = None

    def __post_init__(self):
        if self.blocked_commands is None:
            self.blocked_commands = []


class SecurityManager:
    """
    Manages security for command execution.

    Implements multiple layers of validation:
    1. Command allowlist - only permitted commands can execute
    2. Extra validation - sensitive commands get additional checks
    3. Path restriction - operations limited to allowed directories
    4. Sandbox integration - OS-level containment
    """

    # Process names that can be targeted by pkill/kill
    ALLOWED_PROCESS_TARGETS = {
        "node", "npm", "npx", "yarn", "pnpm", "bun",
        "python", "python3", "pip",
        "vite", "next", "webpack", "esbuild",
        "cargo", "rustc",
        "go",
        "java", "gradle", "mvn",
        "ruby", "bundle"
    }

    # Allowed chmod modes
    ALLOWED_CHMOD_MODES = {"+x", "u+x", "a+x", "755", "700"}

    def __init__(
        self,
        config: SecurityConfig,
        project_dir: Optional[Path] = None
    ):
        """
        Initialize security manager.

        Args:
            config: Security configuration
            project_dir: Project directory for path restrictions
        """
        self.config = config
        self.project_dir = project_dir
        self.allowed_commands: Set[str] = set(config.allowed_commands)
        self.validation_commands: Set[str] = set(config.commands_needing_validation)
        self.blocked_count = 0
        self.validated_count = 0

    def validate_command(self, command: str) -> ValidationResult:
        """
        Validate a bash command against security rules.

        Args:
            command: Full bash command string

        Returns:
            ValidationResult with allowed status and reason
        """
        self.validated_count += 1

        # Extract base commands from the full command
        try:
            base_commands = self._extract_commands(command)
        except ValueError as e:
            self.blocked_count += 1
            return ValidationResult(
                allowed=False,
                reason=f"Failed to parse command: {e}",
                command=command
            )

        # Check each command against allowlist
        blocked = []
        for cmd in base_commands:
            if cmd not in self.allowed_commands:
                blocked.append(cmd)

        if blocked:
            self.blocked_count += 1
            return ValidationResult(
                allowed=False,
                reason=f"Command(s) not in allowlist: {', '.join(blocked)}",
                command=command,
                blocked_commands=blocked
            )

        # Extra validation for sensitive commands
        for cmd in base_commands:
            if cmd in self.validation_commands:
                extra_result = self._validate_sensitive_command(cmd, command)
                if not extra_result.allowed:
                    self.blocked_count += 1
                    return extra_result

        # Path validation
        if self.project_dir:
            path_result = self._validate_paths(command)
            if not path_result.allowed:
                self.blocked_count += 1
                return path_result

        return ValidationResult(
            allowed=True,
            reason="Command passed all security checks",
            command=command
        )

    def _extract_commands(self, command: str) -> List[str]:
        """
        Extract base command names from a shell command string.

        Handles:
        - Simple commands
        - Pipes (|)
        - Command chaining (&&, ||, ;)
        - Subshells ($())

        Args:
            command: Full shell command

        Returns:
            List of base command names
        """
        commands = []

        # Split on pipes and command separators
        parts = re.split(r'\s*(?:\||&&|\|\||;)\s*', command)

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # Handle subshell commands
            # Note: This only matches simple $() subshells and does not handle:
            # - Nested subshells like $(echo $(date))
            # - Backtick syntax like `command`
            # - Complex command substitution patterns
            # For comprehensive handling, consider using a full shell parser.
            subshell_match = re.search(r'\$\((.+?)\)', part)
            if subshell_match:
                sub_commands = self._extract_commands(subshell_match.group(1))
                commands.extend(sub_commands)

            # Extract base command
            try:
                tokens = shlex.split(part)
                if tokens:
                    base_cmd = tokens[0]
                    # Handle path-based commands (e.g., ./init.sh)
                    if '/' in base_cmd:
                        base_cmd = Path(base_cmd).name
                    commands.append(base_cmd)
            except ValueError:
                # If shlex fails, try simple split
                simple_tokens = part.split()
                if simple_tokens:
                    base_cmd = simple_tokens[0]
                    if '/' in base_cmd:
                        base_cmd = Path(base_cmd).name
                    commands.append(base_cmd)

        return commands

    def _validate_sensitive_command(
        self,
        cmd: str,
        full_command: str
    ) -> ValidationResult:
        """
        Extra validation for sensitive commands.

        Args:
            cmd: Base command name
            full_command: Full command string

        Returns:
            ValidationResult
        """
        if cmd in ("pkill", "kill"):
            return self._validate_process_kill(full_command)
        elif cmd == "chmod":
            return self._validate_chmod(full_command)
        elif cmd == "rm":
            return self._validate_rm(full_command)
        elif cmd in ("curl", "wget"):
            return self._validate_network(full_command)
        else:
            # Unknown sensitive command - default allow with warning
            logger.warning(f"Unknown sensitive command: {cmd}")
            return ValidationResult(
                allowed=True,
                reason="Unknown sensitive command - allowed with warning",
                command=full_command
            )

    def _validate_process_kill(self, command: str) -> ValidationResult:
        """Validate pkill/kill commands target only dev processes."""
        tokens = shlex.split(command)

        # Find the process target (last non-flag argument)
        target = None
        for token in reversed(tokens):
            if not token.startswith('-'):
                target = token
                break

        if target is None:
            return ValidationResult(
                allowed=False,
                reason="pkill/kill command has no target",
                command=command
            )

        if target not in self.ALLOWED_PROCESS_TARGETS:
            return ValidationResult(
                allowed=False,
                reason=f"Cannot kill process '{target}' - only dev processes allowed",
                command=command
            )

        return ValidationResult(
            allowed=True,
            reason=f"Process target '{target}' is allowed",
            command=command
        )

    def _validate_chmod(self, command: str) -> ValidationResult:
        """Validate chmod commands use only allowed modes."""
        tokens = shlex.split(command)

        # Find mode argument
        mode = None
        for i, token in enumerate(tokens):
            if i == 0:  # Skip 'chmod'
                continue
            if not token.startswith('-'):
                mode = token
                break

        if mode is None:
            return ValidationResult(
                allowed=False,
                reason="chmod command has no mode specified",
                command=command
            )

        if mode not in self.ALLOWED_CHMOD_MODES:
            return ValidationResult(
                allowed=False,
                reason=f"chmod mode '{mode}' not allowed - only {self.ALLOWED_CHMOD_MODES}",
                command=command
            )

        # Check for recursive flag
        if '-R' in tokens or '--recursive' in tokens:
            return ValidationResult(
                allowed=False,
                reason="Recursive chmod not allowed",
                command=command
            )

        return ValidationResult(
            allowed=True,
            reason=f"chmod mode '{mode}' is allowed",
            command=command
        )

    def _validate_rm(self, command: str) -> ValidationResult:
        """Validate rm commands don't delete critical paths."""
        tokens = shlex.split(command)

        # Dangerous flags
        recursive_flags = {'-rf', '-fr', '--recursive', '-r'}
        force_flags = {'-f', '--force', '-rf', '-fr'}
        has_recursive = any(flag in tokens for flag in recursive_flags)
        has_force = any(flag in tokens for flag in force_flags)

        # Block if both recursive and force flags are present (in any form)
        if has_recursive and has_force:
            return ValidationResult(
                allowed=False,
                reason="Use of rm with both recursive and force flags is not allowed",
                command=command
            )
        # Get target paths
        targets = [t for t in tokens[1:] if not t.startswith('-')]

        for target in targets:
            target_path = Path(target)

            # Block absolute paths outside project
            if target_path.is_absolute():
                if self.project_dir and not str(target_path).startswith(str(self.project_dir)):
                    return ValidationResult(
                        allowed=False,
                        reason=f"Cannot delete outside project directory: {target}",
                        command=command
                    )

            # Block dangerous patterns
            dangerous_patterns = [
                '/', '/home', '/etc', '/var', '/usr', '/bin', '/sbin',
                '~', '.git', 'node_modules', '.env'
            ]
            if target in dangerous_patterns:
                return ValidationResult(
                    allowed=False,
                    reason=f"Cannot delete critical path: {target}",
                    command=command
                )

            # Block .. traversal with force/recursive
            if '..' in target and (has_force or has_recursive):
                return ValidationResult(
                    allowed=False,
                    reason="Cannot use rm -rf with path traversal",
                    command=command
                )

        return ValidationResult(
            allowed=True,
            reason="rm command paths validated",
            command=command
        )

    def _validate_network(self, command: str) -> ValidationResult:
        """Validate curl/wget commands don't access dangerous URLs."""
        # Extract URLs from command
        # Pattern captures hostname (with optional port) from URLs
        # Handles domains, IPv4, and IPv6 (in brackets) with optional ports
        url_pattern = r'https?://([^\s/]+)'
        urls = re.findall(url_pattern, command)

        for host_with_port in urls:
            # Handle different URL formats:
            # - IPv6 with port: [2001:db8::1]:8080 -> extract 2001:db8::1
            # - IPv6 without port: [2001:db8::1] -> extract 2001:db8::1
            # - IPv4/domain with port: example.com:8080 -> extract example.com
            # - IPv4/domain without port: example.com -> keep as is
            if host_with_port.startswith('['):
                # IPv6 address in brackets
                if ']:' in host_with_port:
                    # IPv6 with port: [addr]:port -> extract just the addr part
                    # Split on ']:' gives ['[addr', 'port'], take first element and remove leading '['
                    bracketed_addr = host_with_port.split(']:')[0]
                    host = bracketed_addr[1:]  # Remove the leading '['
                else:
                    # IPv6 without port: [addr] -> just strip the brackets
                    host = host_with_port.strip('[]')
            elif ':' in host_with_port:
                # IPv4 or domain with port
                host = host_with_port.split(':')[0]
            else:
                # No port specified
                host = host_with_port
            
            # Check for localhost variants
            if host.lower() in ['localhost', '127.0.0.1', '0.0.0.0', '::1']:
                return ValidationResult(
                    allowed=False,
                    reason=f"Cannot access localhost URL: {host}",
                    command=command
                )
            
            # Try to parse as IP address and check if it's private
            try:
                ip = ipaddress.ip_address(host)
                if ip.is_private or ip.is_link_local or ip.is_loopback:
                    return ValidationResult(
                        allowed=False,
                        reason=f"Cannot access private/internal IP: {host}",
                        command=command
                    )
            except ValueError:
                # Not an IP address, continue (domain names are ok)
                pass

        return ValidationResult(
            allowed=True,
            reason="Network URLs validated",
            command=command
        )

    def _validate_paths(self, command: str) -> ValidationResult:
        """Validate file paths are within allowed directories."""
        if not self.project_dir:
            return ValidationResult(
                allowed=True,
                reason="No project directory restriction",
                command=command
            )

        # Tokenize the command to extract possible file paths
        tokens = shlex.split(command)
        project_dir = Path(self.project_dir).resolve()
        blocked_paths = []

        for token in tokens:
            # Skip flags and options (start with - or --)
            if token.startswith('-'):
                continue
            # Skip URLs
            if re.match(r'^[a-zA-Z]+://', token):
                continue
            # Try to resolve as a path
            try:
                path = Path(token)
                # Only check if it's a relative or absolute path (not just a word/command)
                if path.is_absolute() or any(sep in token for sep in ('/', '\\')):
                    resolved_path = path.resolve()
                    try:
                        resolved_path.relative_to(project_dir)
                    except ValueError:
                        blocked_paths.append(str(resolved_path))
            except Exception:
                continue

        if blocked_paths:
            return ValidationResult(
                allowed=False,
                reason=f"Path traversal detected: {blocked_paths}",
                command=command,
                blocked_commands=blocked_paths
            )

        return ValidationResult(
            allowed=True,
            reason="Paths validated",
            command=command
        )

    async def bash_security_hook(
        self,
        input_data: Dict[str, Any],
        tool_use_id: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Pre-tool-use hook for bash command validation.

        This hook is called by the Claude Agent SDK before executing
        bash commands, allowing us to block unauthorized commands.

        Args:
            input_data: Tool input containing 'command' field
            tool_use_id: Unique identifier for this tool use
            context: Additional context

        Returns:
            Hook result with 'block' or continue status
        """
        command = input_data.get("command", "")

        logger.debug(f"Security hook validating: {command}")

        result = self.validate_command(command)

        if not result.allowed:
            logger.warning(f"Blocked command: {command} - {result.reason}")
            return {
                "block": True,
                "systemMessage": f"Command blocked by security policy: {result.reason}"
            }

        logger.debug(f"Command allowed: {command}")
        return {}

    def get_stats(self) -> Dict[str, Any]:
        """Get security validation statistics."""
        return {
            "total_validated": self.validated_count,
            "total_blocked": self.blocked_count,
            "block_rate": self.blocked_count / max(1, self.validated_count),
            "allowed_commands_count": len(self.allowed_commands),
            "validation_commands_count": len(self.validation_commands)
        }
