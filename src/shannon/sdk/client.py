"""Shannon Framework SDK Client

Thin wrapper over Claude Agent SDK for invoking Shannon Framework skills.
All algorithm logic (8D analysis, wave orchestration) lives in Shannon Framework.
"""

from pathlib import Path
from typing import AsyncIterator, Optional, Callable, Any, List
import os
import logging

try:
    from claude_agent_sdk import (
        query,
        ClaudeSDKClient,
        ClaudeAgentOptions,
        AssistantMessage,
        TextBlock,
        ThinkingBlock,
        ToolUseBlock,
        SystemMessage,
        ResultMessage,
        HookMatcher,
        HookContext,
        CLINotFoundError,
        ProcessError,
        CLIConnectionError,
        CLIJSONDecodeError
    )
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    # Define stub classes if SDK not available
    ClaudeSDKClient = None
    ThinkingBlock = None
    HookMatcher = None
    HookContext = None
    CLINotFoundError = Exception
    ProcessError = Exception
    CLIConnectionError = Exception
    CLIJSONDecodeError = Exception

# V3 Imports
from .interceptor import MessageInterceptor, MessageCollector
from .stream_handler import StreamHandler


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
        logger: Optional[logging.Logger] = None,
        enable_v3_features: bool = False,
        message_collectors: Optional[List[MessageCollector]] = None
    ):
        """
        Initialize SDK client with Shannon Framework plugin

        Args:
            framework_path: Path to shannon-framework directory
                          (default: auto-detect from environment or standard locations)
            logger: Optional logger instance
            enable_v3_features: Enable V3 message interception and streaming (default: False)
            message_collectors: Optional collectors for V3 message interception

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

        # SDK Hooks for tool-level monitoring
        async def pre_tool_hook(input_data: dict, tool_use_id: Optional[str], context: HookContext) -> dict:
            """Log tool usage before execution"""
            tool_name = input_data.get('tool_name', 'unknown')
            self.logger.debug(f"[PRE-TOOL] {tool_name}")
            return {}
        
        async def post_tool_hook(input_data: dict, tool_use_id: Optional[str], context: HookContext) -> dict:
            """Log tool completion after execution"""
            tool_name = input_data.get('tool_name', 'unknown')
            self.logger.debug(f"[POST-TOOL] {tool_name} completed")
            return {}
        
        # stderr callback for integrated logging
        def stderr_handler(stderr_line: str) -> None:
            """Integrate SDK stderr into shannon logging"""
            self.logger.debug(f"[SDK stderr] {stderr_line.strip()}")
        
        # Base options for all SDK calls
        # Note: plugins parameter expects list of dicts with "type" and "path"
        self.base_options = ClaudeAgentOptions(
            plugins=[{
                "type": "local",
                "path": str(self.framework_path)
            }],
            setting_sources=["user", "project"],  # CRITICAL: Load skills from filesystem
            permission_mode="bypassPermissions",  # Auto-approve for CLI usage
            allowed_tools=[
                "Skill", "Read", "Write", "Edit",  # Added Edit for precise code modifications
                "Bash", "SlashCommand", "Grep", "Glob", "TodoWrite",
                # Serena MCP tools (required by spec-analysis skill)
                "mcp__serena__write_memory",
                "mcp__serena__read_memory",
                "mcp__serena__list_memories",
                "mcp__serena__get_current_config",
                # Sequential thinking (optional but recommended)
                "mcp__sequential-thinking__sequentialthinking"
            ],
            max_turns=50,  # Prevent runaway costs and infinite loops
            hooks={
                'PreToolUse': [HookMatcher(hooks=[pre_tool_hook])],
                'PostToolUse': [HookMatcher(hooks=[post_tool_hook])]
            },
            stderr=stderr_handler  # Integrate SDK stderr into logging
            # model defaults to latest sonnet with extended context
        )

        # V3 Features
        self.enable_v3_features = enable_v3_features
        self.message_collectors = message_collectors or []

        if enable_v3_features:
            self.interceptor = MessageInterceptor(logger=self.logger)
            self.stream_handler = StreamHandler(
                enable_buffering=False,  # Buffering optional, disabled by default
                logger=self.logger
            )
            self.logger.info("V3 features enabled: message interception and stream handling")
        else:
            self.interceptor = None
            self.stream_handler = None

        self.logger.info("ShannonSDKClient initialized")
        self.logger.debug(f"  Plugin: {self.framework_path}")
        self.logger.debug(f"  Setting sources: user, project")
        self.logger.debug(f"  Model: sonnet[1m]")
        self.logger.debug(f"  V3 features: {enable_v3_features}")

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
            # Get base query iterator
            query_iterator = query(prompt=prompt, options=self.base_options)

            # V3 Enhancement: Wrap with interceptor if enabled
            if self.enable_v3_features and self.interceptor:
                # Apply message interception
                query_iterator = self.interceptor.intercept(
                    query_iterator,
                    self.message_collectors
                )

                # Apply stream handling if configured
                if self.stream_handler:
                    query_iterator = self.stream_handler.handle(query_iterator)

            # Iterate messages (V2 behavior or V3 enhanced)
            async for msg in query_iterator:
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

        except CLINotFoundError as e:
            self.logger.error("Claude Code CLI not found")
            raise RuntimeError(
                "Claude Code not installed. Install with:\n"
                "  npm install -g @anthropic-ai/claude-code"
            ) from e
        except ProcessError as e:
            self.logger.error(f"Process failed (exit {e.exit_code}): {e.stderr}")
            raise RuntimeError(
                f"Claude Code process failed with exit code {e.exit_code}\n"
                f"Error: {e.stderr}"
            ) from e
        except CLIConnectionError as e:
            self.logger.error(f"Connection failed: {e}")
            raise RuntimeError(f"Failed to connect to Claude Code: {e}") from e
        except CLIJSONDecodeError as e:
            self.logger.error(f"JSON parse error: {e.line}")
            raise RuntimeError(f"Failed to parse Claude Code response: {e}") from e
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

        except CLINotFoundError as e:
            self.logger.error("Claude Code CLI not found")
            raise RuntimeError(
                "Claude Code not installed. Install with:\n"
                "  npm install -g @anthropic-ai/claude-code"
            ) from e
        except ProcessError as e:
            self.logger.error(f"Process failed (exit {e.exit_code}): {e.stderr}")
            raise RuntimeError(
                f"Claude Code process failed with exit code {e.exit_code}\n"
                f"Error: {e.stderr}"
            ) from e
        except CLIConnectionError as e:
            self.logger.error(f"Connection failed: {e}")
            raise RuntimeError(f"Failed to connect to Claude Code: {e}") from e
        except CLIJSONDecodeError as e:
            self.logger.error(f"JSON parse error: {e.line}")
            raise RuntimeError(f"Failed to parse Claude Code response: {e}") from e
        except Exception as e:
            self.logger.error(f"Command invocation failed: {e}")
            raise

    async def invoke_command_with_enhancements(
        self,
        command: str,
        args: str = "",
        system_prompt_enhancements: str = "",
        progress_callback: Optional[Callable[[Any], None]] = None
    ) -> AsyncIterator[Any]:
        """
        Invoke Shannon command with enhanced system prompts (V3.5)
        
        This method allows injecting custom system prompt instructions
        via ClaudeAgentOptions.system_prompt.append. Used by V3.5
        autonomous executor to inject library discovery, validation,
        and git workflow instructions.
        
        Args:
            command: Command name (e.g., '/shannon:exec')
            args: Command arguments
            system_prompt_enhancements: Additional system prompt text to inject
            progress_callback: Optional callback for progress
            
        Yields:
            SDK messages
            
        Example:
            enhancements = build_exec_enhancements(task, project_type)
            async for msg in client.invoke_command_with_enhancements(
                '/shannon:exec',
                'fix iOS login',
                enhancements
            ):
                print(msg)
        """
        self.logger.info(f"Invoking command with enhancements: {command} {args}")
        self.logger.debug(f"  System prompt enhancements: {len(system_prompt_enhancements)} chars")
        
        # Format command with args
        prompt = f"{command} {args}".strip()
        
        # Create enhanced options
        enhanced_options = ClaudeAgentOptions(
            plugins=self.base_options.plugins,
            setting_sources=self.base_options.setting_sources,
            permission_mode=self.base_options.permission_mode,
            allowed_tools=self.base_options.allowed_tools,
            system_prompt={
                "type": "preset",
                "preset": "claude_code",
                "append": system_prompt_enhancements
            } if system_prompt_enhancements else self.base_options.system_prompt
        )
        
        try:
            # Query with enhanced options
            query_iterator = query(prompt=prompt, options=enhanced_options)
            
            # V3 Enhancement: Wrap with interceptor if enabled
            if self.enable_v3_features and self.interceptor:
                query_iterator = self.interceptor.intercept(
                    query_iterator,
                    self.message_collectors
                )
                if self.stream_handler:
                    query_iterator = self.stream_handler.handle(query_iterator)
            
            # Iterate messages
            async for msg in query_iterator:
                if progress_callback:
                    try:
                        progress_callback(msg)
                    except Exception as e:
                        self.logger.warning(f"Progress callback error: {e}")
                
                yield msg
        
        except CLINotFoundError as e:
            self.logger.error("Claude Code CLI not found")
            raise RuntimeError(
                "Claude Code not installed. Install with:\n"
                "  npm install -g @anthropic-ai/claude-code"
            ) from e
        except ProcessError as e:
            self.logger.error(f"Process failed (exit {e.exit_code}): {e.stderr}")
            raise RuntimeError(
                f"Claude Code process failed with exit code {e.exit_code}\n"
                f"Error: {e.stderr}"
            ) from e
        except CLIConnectionError as e:
            self.logger.error(f"Connection failed: {e}")
            raise RuntimeError(f"Failed to connect to Claude Code: {e}") from e
        except CLIJSONDecodeError as e:
            self.logger.error(f"JSON parse error: {e.line}")
            raise RuntimeError(f"Failed to parse Claude Code response: {e}") from e
        except Exception as e:
            self.logger.error(f"Enhanced command invocation failed: {e}")
            raise

    async def generate_code_changes(
        self,
        task: str,
        enhanced_prompts: str,
        working_directory: Path,
        libraries: Optional[List[Any]] = None
    ) -> AsyncIterator[Any]:
        """
        Generate code changes using Claude with enhanced prompts.
        
        Specifically designed for autonomous code generation in Shannon V3.5.
        Uses system_prompt.append to inject library discovery and validation instructions.
        
        Args:
            task: Task description
            enhanced_prompts: System prompt enhancements (library discovery, validation, git)
            working_directory: Project directory for file operations
            libraries: Optional discovered libraries to mention in prompt
            
        Yields:
            SDK messages (ToolUseBlock, AssistantMessage, etc.)
        """
        from claude_agent_sdk import ClaudeAgentOptions, query
        
        # Build library context
        library_context = ""
        if libraries:
            library_context = "\\n\\nRECOMMENDED LIBRARIES (use these):\\n"
            for lib in libraries[:3]:
                library_context += f"- {lib.name}: {lib.why_recommended}\\n"
                library_context += f"  Install: {lib.install_command}\\n"
        
        # Build task prompt
        prompt = f"""Execute this task in the current directory:

TASK: {task}
{library_context}

REQUIREMENTS:
1. Use recommended libraries (don't build custom if library exists)
2. Make focused, minimal changes
3. Use Write tool to create files, Edit tool to modify existing files
4. Ensure code works (proper syntax, imports, etc.)
5. Follow project conventions

Execute the task now."""

        # Create options with enhanced prompts
        options = ClaudeAgentOptions(
            cwd=str(working_directory),
            allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
            permission_mode="acceptEdits",  # Auto-accept file edits
            system_prompt={
                "type": "preset",
                "preset": "claude_code",
                "append": enhanced_prompts  # INJECT enhanced prompts
            },
            max_turns=10,
            setting_sources=["user", "project"]
        )
        
        # Query Claude for code generation
        async for message in query(prompt=prompt, options=options):
            yield message

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

    # V3 Feature Management Methods

    def add_collector(self, collector: MessageCollector) -> None:
        """
        Add a message collector for V3 interception

        Args:
            collector: MessageCollector instance to add

        Example:
            client = ShannonSDKClient(enable_v3_features=True)
            client.add_collector(MetricsCollector())
            client.add_collector(ContextCollector())
        """
        if not self.enable_v3_features:
            self.logger.warning("V3 features not enabled - collector will have no effect")

        self.message_collectors.append(collector)
        self.logger.debug(f"Added collector: {collector.__class__.__name__}")

    def remove_collector(self, collector: MessageCollector) -> None:
        """
        Remove a message collector

        Args:
            collector: Collector instance to remove
        """
        if collector in self.message_collectors:
            self.message_collectors.remove(collector)
            self.logger.debug(f"Removed collector: {collector.__class__.__name__}")

    def clear_collectors(self) -> None:
        """Clear all message collectors"""
        self.message_collectors.clear()
        self.logger.debug("Cleared all collectors")

    def get_stream_stats(self) -> Optional[dict[str, Any]]:
        """
        Get stream handler statistics (if V3 enabled)

        Returns:
            Dictionary with stream stats, or None if V3 disabled
        """
        if self.stream_handler:
            return self.stream_handler.get_stats()
        return None

    async def start_interactive_session(
        self,
        initial_prompt: Optional[str] = None,
        enable_partial_messages: bool = True,
        enable_thinking_display: bool = True
    ) -> 'InteractiveSession':
        """
        Start an interactive conversation session with Shannon Framework
        
        Uses ClaudeSDKClient for continuous conversation (maintains context across turns).
        This enables multi-turn interactions where Claude remembers previous exchanges.
        
        Args:
            initial_prompt: Optional initial message to start the conversation
            enable_partial_messages: Enable character-by-character streaming
            enable_thinking_display: Show ThinkingBlock content from thinking models
            
        Returns:
            InteractiveSession instance for managing the conversation
            
        Example:
            async with client.start_interactive_session() as session:
                # First turn
                await session.send("Analyze spec.md")
                async for msg in session.receive():
                    print(msg)
                
                # Follow-up (Claude remembers spec.md context!)
                await session.send("What API endpoints did you find?")
                async for msg in session.receive():
                    print(msg)
                    
                # Another follow-up (still remembers everything)
                await session.send("Generate code for the user endpoint")
                async for msg in session.receive():
                    print(msg)
        """
        # Create interactive options (extends base options)
        interactive_options = ClaudeAgentOptions(
            plugins=self.base_options.plugins,
            setting_sources=self.base_options.setting_sources,
            permission_mode=self.base_options.permission_mode,
            allowed_tools=self.base_options.allowed_tools,
            max_turns=self.base_options.max_turns,
            hooks=self.base_options.hooks,
            stderr=self.base_options.stderr,
            include_partial_messages=enable_partial_messages,  # KEY: Enable character-by-character streaming
        )
        
        # Create interactive session
        session = InteractiveSession(
            options=interactive_options,
            logger=self.logger,
            enable_thinking_display=enable_thinking_display,
            initial_prompt=initial_prompt
        )
        
        return session


class InteractiveSession:
    """
    Interactive conversation session using ClaudeSDKClient
    
    Maintains conversation context across multiple user inputs, enabling:
    - Multi-turn conversations where Claude remembers previous exchanges
    - Follow-up questions that build on previous context
    - Continuous workflow (analyze → understand → generate → refine)
    - Real-time streaming with partial message updates
    - ThinkingBlock display for models with thinking capability
    
    Usage:
        async with session:
            await session.send("Analyze spec.md")
            async for msg in session.receive():
                # Process first response
                if isinstance(msg, TextBlock):
                    print(msg.text)
            
            # Follow-up (context preserved!)
            await session.send("What API endpoints did you find?")
            async for msg in session.receive():
                # Claude remembers the spec analysis
                if isinstance(msg, TextBlock):
                    print(msg.text)
    """
    
    def __init__(
        self,
        options: ClaudeAgentOptions,
        logger: logging.Logger,
        enable_thinking_display: bool = True,
        initial_prompt: Optional[str] = None
    ):
        """
        Initialize interactive session
        
        Args:
            options: ClaudeAgentOptions with interactive settings
            logger: Logger instance
            enable_thinking_display: Show thinking content from ThinkingBlock
            initial_prompt: Optional initial message
        """
        self.options = options
        self.logger = logger
        self.enable_thinking_display = enable_thinking_display
        self.initial_prompt = initial_prompt
        
        self.client: Optional[ClaudeSDKClient] = None
        self.turn_count = 0
        self.is_connected = False
    
    async def __aenter__(self) -> 'InteractiveSession':
        """Async context manager entry - connects to Claude"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit - disconnects from Claude"""
        await self.disconnect()
    
    async def connect(self) -> None:
        """
        Connect to Claude and start session
        
        Raises:
            RuntimeError: If Claude Code not installed or connection fails
        """
        if self.is_connected:
            self.logger.warning("Already connected")
            return
        
        try:
            self.client = ClaudeSDKClient(options=self.options)
            await self.client.connect(prompt=self.initial_prompt)
            self.is_connected = True
            self.logger.info("Interactive session connected")
            
            # If initial prompt was provided, we already sent first message
            if self.initial_prompt:
                self.turn_count = 1
                self.logger.debug(f"Initial prompt sent: {self.initial_prompt[:100]}...")
                
        except CLINotFoundError as e:
            raise RuntimeError(
                "Claude Code not installed. Install with:\n"
                "  npm install -g @anthropic-ai/claude-code"
            ) from e
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            raise RuntimeError(f"Failed to start interactive session: {e}") from e
    
    async def disconnect(self) -> None:
        """Disconnect from Claude and end session"""
        if not self.is_connected or not self.client:
            return
        
        try:
            await self.client.disconnect()
            self.is_connected = False
            self.logger.info(f"Interactive session ended after {self.turn_count} turns")
        except Exception as e:
            self.logger.warning(f"Error during disconnect: {e}")
    
    async def send(self, message: str) -> None:
        """
        Send a message to Claude
        
        Args:
            message: User message to send
            
        Raises:
            RuntimeError: If not connected
        """
        if not self.is_connected or not self.client:
            raise RuntimeError("Not connected. Call connect() first or use async with.")
        
        self.turn_count += 1
        self.logger.info(f"[Turn {self.turn_count}] Sending: {message[:100]}...")
        
        try:
            await self.client.query(message)
        except CLINotFoundError as e:
            raise RuntimeError(
                "Claude Code not installed. Install with:\n"
                "  npm install -g @anthropic-ai/claude-code"
            ) from e
        except ProcessError as e:
            raise RuntimeError(
                f"Claude Code process failed with exit code {e.exit_code}\n"
                f"Error: {e.stderr}"
            ) from e
        except CLIConnectionError as e:
            raise RuntimeError(f"Connection failed: {e}") from e
        except CLIJSONDecodeError as e:
            raise RuntimeError(f"Failed to parse response: {e}") from e
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            raise
    
    async def receive(self) -> AsyncIterator[Any]:
        """
        Receive response messages from Claude
        
        Yields messages until ResultMessage (end of turn).
        Handles TextBlock, ThinkingBlock, ToolUseBlock, ToolResultBlock, etc.
        
        Yields:
            SDK message objects (TextBlock, ThinkingBlock, ToolUseBlock, etc.)
            
        Example:
            async for msg in session.receive():
                if isinstance(msg, TextBlock):
                    print(f"Text: {msg.text}")
                elif isinstance(msg, ThinkingBlock):
                    print(f"Thinking: {msg.thinking}")
                elif isinstance(msg, ToolUseBlock):
                    print(f"Tool: {msg.name}")
        """
        if not self.is_connected or not self.client:
            raise RuntimeError("Not connected. Call connect() first or use async with.")
        
        self.logger.debug(f"[Turn {self.turn_count}] Receiving response...")
        message_count = 0
        
        try:
            async for message in self.client.receive_response():
                message_count += 1
                msg_type = type(message).__name__
                self.logger.debug(f"[Turn {self.turn_count}] Message {message_count}: {msg_type}")
                
                # Handle different message types
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            self.logger.debug(f"  Text: {block.text[:100]}...")
                            yield block
                        elif isinstance(block, ThinkingBlock):
                            if self.enable_thinking_display:
                                self.logger.debug(f"  Thinking: {block.thinking[:100]}...")
                                yield block
                        elif isinstance(block, ToolUseBlock):
                            self.logger.debug(f"  Tool use: {block.name}")
                            yield block
                        elif isinstance(block, ToolResultBlock):
                            self.logger.debug(f"  Tool result for: {block.tool_use_id}")
                            yield block
                        else:
                            # Unknown block type - yield it anyway
                            yield block
                
                elif isinstance(message, ResultMessage):
                    # Final message - log stats
                    self.logger.info(
                        f"[Turn {self.turn_count}] Complete: "
                        f"{message.num_turns} turns, "
                        f"{message.duration_ms}ms, "
                        f"${message.total_cost_usd:.4f}" if message.total_cost_usd else ""
                    )
                    yield message
                
                else:
                    # Other message types (SystemMessage, etc.)
                    yield message
        
        except Exception as e:
            self.logger.error(f"Error receiving messages: {e}")
            raise
    
    async def interrupt(self) -> None:
        """
        Send interrupt signal to stop Claude mid-execution
        
        Useful for stopping long-running operations.
        After interrupting, you can send a new message.
        """
        if not self.is_connected or not self.client:
            raise RuntimeError("Not connected")
        
        self.logger.info(f"[Turn {self.turn_count}] Sending interrupt...")
        try:
            await self.client.interrupt()
            self.logger.info("Interrupt sent successfully")
        except Exception as e:
            self.logger.error(f"Failed to send interrupt: {e}")
            raise
    
    def get_turn_count(self) -> int:
        """Get current turn count"""
        return self.turn_count
    
    def is_active(self) -> bool:
        """Check if session is active"""
        return self.is_connected
