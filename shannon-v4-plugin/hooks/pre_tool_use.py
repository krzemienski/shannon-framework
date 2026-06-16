#!/usr/bin/env python3
"""
Shannon v4: PreToolUse Hook

NEW in v4: Executes BEFORE any tool is used

Responsibilities:
1. Check if skill should activate for this tool use
2. Validate MCP server availability
3. Suggest alternative approaches if MCP unavailable
4. Block tool use if prerequisites not met
"""

import json
import sys


def pre_tool_use_hook():
    """
    PreToolUse hook - Skill activation and MCP availability checks
    """

    result = {
        "success": True,
        "tool_allowed": True,
        "skill_activated": None,
        "mcp_checked": False,
        "mcp_available": True,
        "alternatives": [],
        "blocks": []
    }

    try:
        # Get tool being used from environment or args
        # tool_name = get_tool_from_context()

        # 1. Check if skill should activate
        # Example: Write tool + test file → shannon-browser-test skill
        # if tool_name == "Write" and "test" in file_path:
        #     result["skill_activated"] = "shannon-browser-test"

        # 2. Check MCP availability
        # Example: Puppeteer tool requires puppeteer MCP
        # if tool_name.startswith("puppeteer"):
        #     mcp_available = check_mcp_available("puppeteer")
        #     result["mcp_checked"] = True
        #     result["mcp_available"] = mcp_available
        #
        #     if not mcp_available:
        #         result["blocks"].append("Puppeteer MCP not available")
        #         result["alternatives"].append("Use Playwright MCP")
        #         result["alternatives"].append("Use Read tool to analyze existing tests")

        # 3. Validate tool prerequisites
        # Example: Write tool requires Read tool used first (for existing files)

        # 4. Block tool use if prerequisites not met
        if result["blocks"]:
            result["tool_allowed"] = False
            result["success"] = False
            result["message"] = f"Tool use blocked: {', '.join(result['blocks'])}"
            if result["alternatives"]:
                result["message"] += f" | Alternatives: {', '.join(result['alternatives'])}"
        else:
            result["message"] = "Tool use allowed"

        print(json.dumps(result), file=sys.stderr)

        return 0 if result["tool_allowed"] else 1

    except Exception as e:
        result["success"] = False
        result["message"] = f"PreToolUse hook error: {str(e)}"
        print(json.dumps(result), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(pre_tool_use_hook())
