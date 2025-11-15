#!/usr/bin/env python3
"""
Debug script for CompleteExecutor code generation
Tests what messages are returned from Claude SDK
"""

import asyncio
import logging
from pathlib import Path
import sys

# Setup path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from shannon.sdk.client import ShannonSDKClient
from claude_agent_sdk import ToolUseBlock, AssistantMessage, TextBlock, ResultMessage

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_code_generation():
    """Test code generation and see what messages we get"""

    # Create test directory
    test_dir = Path("/tmp/shannon-test-codegen")
    test_dir.mkdir(exist_ok=True)

    logger.info(f"Test directory: {test_dir}")

    # Initialize SDK client
    client = ShannonSDKClient(logger=logger)

    # Simple task
    task = "create hello.py that prints hello world"

    # Enhanced prompts (minimal)
    enhanced_prompts = """
You are an expert software developer.
Follow best practices for code quality.
"""

    logger.info(f"Task: {task}")
    logger.info("Calling generate_code_changes...")

    # Track what we receive
    message_count = 0
    tool_uses = []
    assistant_messages = []
    files_changed = set()

    try:
        async for message in client.generate_code_changes(
            task=task,
            enhanced_prompts=enhanced_prompts,
            working_directory=test_dir,
            libraries=[]
        ):
            message_count += 1
            msg_type = type(message).__name__

            logger.info(f"Message {message_count}: {msg_type}")

            # Log details based on type
            if isinstance(message, ToolUseBlock):
                logger.info(f"  ToolUseBlock: {message.name}")
                logger.info(f"  Input: {message.input}")
                tool_uses.append(message)

                # Track file operations
                if message.name in ['Write', 'Edit']:
                    if 'file_path' in message.input:
                        file_path = message.input['file_path']
                        logger.info(f"  FILE OPERATION: {message.name} -> {file_path}")
                        files_changed.add(file_path)

            elif isinstance(message, AssistantMessage):
                logger.info(f"  AssistantMessage: {len(message.content)} content blocks")
                for i, block in enumerate(message.content):
                    block_type = type(block).__name__
                    logger.info(f"    Block {i}: {block_type}")

                    if isinstance(block, TextBlock):
                        logger.info(f"      Text: {block.text[:100]}...")
                    elif isinstance(block, ToolUseBlock):
                        logger.info(f"      ToolUse: {block.name}")
                        logger.info(f"      Input: {block.input}")

                        # Track file operations from nested tool uses
                        if block.name in ['Write', 'Edit']:
                            if 'file_path' in block.input:
                                file_path = block.input['file_path']
                                logger.info(f"      FILE OPERATION: {block.name} -> {file_path}")
                                files_changed.add(file_path)

                assistant_messages.append(message)

            elif isinstance(message, ResultMessage):
                logger.info(f"  ResultMessage: {message}")

            else:
                logger.info(f"  Unknown type: {message}")

    except Exception as e:
        logger.error(f"Error during code generation: {e}", exc_info=True)
        return False

    # Summary
    logger.info("=" * 80)
    logger.info(f"SUMMARY:")
    logger.info(f"  Total messages: {message_count}")
    logger.info(f"  Tool uses (top-level): {len(tool_uses)}")
    logger.info(f"  Assistant messages: {len(assistant_messages)}")
    logger.info(f"  Files changed: {len(files_changed)}")

    if files_changed:
        logger.info(f"  Files: {list(files_changed)}")
    else:
        logger.warning("  NO FILES CHANGED!")

    # Check if file was actually created
    hello_py = test_dir / "hello.py"
    if hello_py.exists():
        logger.info(f"SUCCESS: hello.py was created!")
        logger.info(f"Content:\n{hello_py.read_text()}")
        return True
    else:
        logger.error(f"FAILURE: hello.py was NOT created")
        # List what files exist
        logger.info(f"Files in {test_dir}:")
        for f in test_dir.iterdir():
            logger.info(f"  - {f.name}")
        return False

if __name__ == '__main__':
    success = asyncio.run(test_code_generation())
    sys.exit(0 if success else 1)
