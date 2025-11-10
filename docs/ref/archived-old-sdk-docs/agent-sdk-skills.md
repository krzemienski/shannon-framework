# Agent Skills in the SDK - Complete Content

## Overview
"Agent Skills extend Claude with specialized capabilities that Claude autonomously invokes when relevant. Skills are packaged as `SKILL.md` files containing instructions, descriptions, and optional supporting resources."

## How Skills Work with the SDK

Skills operate through these mechanisms:

1. "Defined as filesystem artifacts": Created as `SKILL.md` files in `.claude/skills/` directories
2. "Loaded from filesystem": Requires explicit `settingSources` (TypeScript) or `setting_sources` (Python) configuration
3. "Automatically discovered": Skill metadata discovered at startup; full content loaded when triggered
4. "Model-invoked": Claude autonomously chooses when to use them based on context
5. "Enabled via allowed_tools": Add `"Skill"` to `allowed_tools` configuration

**Critical Note**: "By default, the SDK does not load any filesystem settings. To use Skills, you must explicitly configure `settingSources: ['user', 'project']` (TypeScript) or `setting_sources=["user", "project"]` (Python)."

## Required SDK Configuration

To enable Skills, implement:

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        cwd="/path/to/project",  # Project with .claude/skills/
        setting_sources=["user", "project"],  # Load Skills from filesystem
        allowed_tools=["Skill", "Read", "Write", "Bash"]  # Enable Skill tool
    )

    async for message in query(
        prompt="Help me process this PDF document",
        options=options
    ):
        print(message)

asyncio.run(main())
```

## Skill Locations

"Skills are loaded from filesystem directories based on your `settingSources`/`setting_sources` configuration":

* **Project Skills** (`.claude/skills/`): "Shared with your team via git - loaded when `setting_sources` includes `"project"`"
* **User Skills** (`~/.claude/skills/`): "Personal Skills across all projects - loaded when `setting_sources` includes `"user"`"
* **Plugin Skills**: Bundled with installed Claude Code plugins

## Troubleshooting

**Common Issue - Skills Not Found**: Most frequent problem is missing `setting_sources` configuration:

```python
# Wrong - Skills won't be loaded
options = ClaudeAgentOptions(
    allowed_tools=["Skill"]
)

# Correct - Skills will be loaded
options = ClaudeAgentOptions(
    setting_sources=["user", "project"],  # Required to load Skills
    allowed_tools=["Skill"]
)
```
