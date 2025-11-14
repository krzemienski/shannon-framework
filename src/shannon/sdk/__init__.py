"""Shannon SDK integration - Claude Agent SDK wrapper.

Provides ShannonSDKClient for direct Shannon Framework skill invocation,
plus AgentFactory and PromptBuilder for template-based agent creation,
and MessageParser for extracting structured data from SDK message streams.
"""

from shannon.sdk.client import ShannonSDKClient, SDK_AVAILABLE
from shannon.sdk.message_parser import MessageParser

# Optional: AgentFactory and PromptBuilder (not yet implemented)
try:
    from shannon.sdk.agent_factory import AgentFactory, CLAUDE_SDK_AVAILABLE
    from shannon.sdk.prompt_builder import PromptBuilder
    FACTORY_AVAILABLE = True
except ImportError:
    FACTORY_AVAILABLE = False
    AgentFactory = None
    PromptBuilder = None
    CLAUDE_SDK_AVAILABLE = SDK_AVAILABLE

__all__ = [
    "ShannonSDKClient",
    "SDK_AVAILABLE",
    "AgentFactory",
    "PromptBuilder",
    "MessageParser",
    "CLAUDE_SDK_AVAILABLE",
    "FACTORY_AVAILABLE"
]
