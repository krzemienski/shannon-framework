"""Shannon Framework SDK Client

Thin wrapper over Claude Agent SDK for invoking Shannon Framework skills.
All algorithm logic (8D analysis, wave orchestration) lives in Shannon Framework.
"""

from pathlib import Path
from typing import AsyncIterator, Optional, Callable, Any
import os
import logging

try:
    from claude_agent_sdk import (
        query,
        ClaudeAgentOptions,
        AssistantMessage,
        TextBlock,
        ToolUseBlock,
        SystemMessage,
        ResultMessage
    )
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False


class ShannonSDKClient:
    """
    Client for invoking Shannon Framework via Claude Agent SDK

    Loads Shannon Framework as plugin and delegates all algorithm logic
    to framework's 18 skills via @skill commands.

    Architecture:
        Shannon CLI → ShannonSDKClient → Claude Agent SDK → Shannon Framework Plugin → Skills
    """

    def __init__(
        self,
        framework_path: Optional[Path] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize SDK client with Shannon Framework plugin

        Args:
            framework_path: Path to shannon-framework directory
                          (default: auto-detect from environment or standard locations)
            logger: Optional logger instance

        Raises:
            ImportError: If claude_agent_sdk not installed
            FileNotFoundError: If Shannon Framework not found
        """
        if not SDK_AVAILABLE:
            raise ImportError(
                "claude_agent_sdk not installed. Install with: pip install claude-agent-sdk"
            )

        self.logger = logger or self._default_logger()

        # Locate Shannon Framework
        self.framework_path = framework_path or self._find_shannon_framework()

        self.logger.debug(f"Shannon Framework path: {self.framework_path}")

        # Verify framework exists
        if not self.framework_path.exists():
            raise FileNotFoundError(
                f"Shannon Framework not found at: {self.framework_path}"
            )

        # Verify plugin structure
        plugin_json = self.framework_path / ".claude-plugin" / "plugin.json"
        if not plugin_json.exists():
            raise FileNotFoundError(
                f"Invalid Shannon Framework: missing {plugin_json}"
            )

        # Base options for all SDK calls
        # Note: plugins parameter expects list of dicts with "type" and "path"
        self.base_options = ClaudeAgentOptions(
            plugins=[{
                "type": "local",
                "path": str(self.framework_path)
            }],
            setting_sources=["user", "project"],  # CRITICAL: Load skills from filesystem
            allowed_tools=["Skill", "Read", "Write", "Bash", "SlashCommand"],
            model="sonnet[1m]"  # 1M context model for Shannon Framework
        )

        self.logger.info("ShannonSDKClient initialized")
        self.logger.debug(f"  Plugin: {self.framework_path}")
        self.logger.debug(f"  Setting sources: user, project")
        self.logger.debug(f"  Model: sonnet[1m]")

    async def invoke_skill(
        self,
        skill_name: str,
        prompt_content: str,
        progress_callback: Optional[Callable[[Any], None]] = None
    ) -> AsyncIterator[Any]:
        """
        Invoke a Shannon Framework skill

        Args:
            skill_name: Skill name (e.g., 'spec-analysis', 'wave-orchestration')
            prompt_content: Content to pass to skill
            progress_callback: Optional callback(message) for progress updates

        Yields:
            SDK messages (AssistantMessage, ToolUseBlock, SystemMessage, etc.)

        Example:
            async for msg in client.invoke_skill('spec-analysis', spec_text):
                if isinstance(msg, AssistantMessage):
                    print(f"Response: {msg.content}")
        """
        self.logger.info(f"Invoking skill: {skill_name}")
        self.logger.debug(f"  Content length: {len(prompt_content)} chars")

        # Format prompt for skill invocation
        # Skills are invoked with @skill command syntax
        prompt = f"@skill {skill_name}\n\n{prompt_content}"

        self.logger.debug(f"  Prompt preview: {prompt[:200]}...")

        # Query SDK with Shannon Framework plugin loaded
        message_count = 0
        try:
            async for msg in query(prompt=prompt, options=self.base_options):
                message_count += 1
                msg_type = type(msg).__name__
                self.logger.debug(f"  Message {message_count}: {msg_type}")

                # Call progress callback if provided
                if progress_callback:
                    try:
                        progress_callback(msg)
                    except Exception as e:
                        self.logger.warning(f"Progress callback error: {e}")

                yield msg

            self.logger.info(f"Skill {skill_name} complete ({message_count} messages)")

        except Exception as e:
            self.logger.error(f"Skill invocation failed: {e}")
            raise

    async def invoke_command(
        self,
        command: str,
        args: str = "",
        progress_callback: Optional[Callable[[Any], None]] = None
    ) -> AsyncIterator[Any]:
        """
        Invoke a Shannon Framework slash command

        Args:
            command: Command name (e.g., '/shannon:spec', '/shannon:wave')
            args: Command arguments
            progress_callback: Optional callback for progress

        Yields:
            SDK messages

        Example:
            async for msg in client.invoke_command('/shannon:spec', 'analyze todo.md'):
                print(msg)
        """
        self.logger.info(f"Invoking command: {command} {args}")

        # Format command with args
        prompt = f"{command} {args}".strip()

        self.logger.debug(f"  Command: {prompt}")

        try:
            async for msg in query(prompt=prompt, options=self.base_options):
                if progress_callback:
                    try:
                        progress_callback(msg)
                    except Exception as e:
                        self.logger.warning(f"Progress callback error: {e}")

                yield msg

        except Exception as e:
            self.logger.error(f"Command invocation failed: {e}")
            raise

    def _find_shannon_framework(self) -> Path:
        """
        Locate Shannon Framework directory

        Checks (in order):
        1. SHANNON_FRAMEWORK_PATH environment variable
        2. /Users/nick/Desktop/shannon-framework (development)
        3. ~/.shannon/shannon-framework (user install)
        4. /usr/local/shannon/shannon-framework (system install)

        Returns:
            Path to shannon-framework directory

        Raises:
            FileNotFoundError: If framework not found
        """
        # Check env var
        env_path = os.getenv('SHANNON_FRAMEWORK_PATH')
        if env_path:
            path = Path(env_path)
            if path.exists():
                self.logger.debug(f"Found via SHANNON_FRAMEWORK_PATH: {path}")
                return path

        # Check common locations
        candidates = [
            Path("/Users/nick/Desktop/shannon-framework"),
            Path.home() / ".shannon" / "shannon-framework",
            Path("/usr/local/shannon/shannon-framework")
        ]

        for candidate in candidates:
            plugin_json = candidate / ".claude-plugin" / "plugin.json"
            if candidate.exists() and plugin_json.exists():
                self.logger.debug(f"Found Shannon Framework at: {candidate}")
                return candidate

        # Framework not found
        raise FileNotFoundError(
            "Shannon Framework not found. Tried:\n"
            f"  - SHANNON_FRAMEWORK_PATH env var\n"
            f"  - {candidates[0]}\n"
            f"  - {candidates[1]}\n"
            f"  - {candidates[2]}\n"
            "\n"
            "Set SHANNON_FRAMEWORK_PATH or install Shannon Framework to one of the above locations."
        )

    def _default_logger(self) -> logging.Logger:
        """Create default logger if none provided"""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
