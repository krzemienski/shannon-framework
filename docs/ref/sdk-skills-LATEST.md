# Agent Skills in the SDK

**CRITICAL:** Skills require `setting_sources=["user", "project"]` to load from filesystem.

## Quick Reference

```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    cwd="/path/to/project",
    setting_sources=["user", "project"],  # REQUIRED!
    allowed_tools=["Skill", "Read", "Write"]
)

async for message in query(prompt="...", options=options):
    print(message)
```

## How Skills Work

1. **Filesystem artifacts**: Created as `SKILL.md` in `.claude/skills/`
2. **Loaded via setting_sources**: Default is NO loading
3. **Auto-discovered**: Metadata discovered at startup
4. **Model-invoked**: Claude chooses when to use
5. **Enabled via allowed_tools**: Add `"Skill"` to `allowed_tools`

## Skill Locations

Based on `setting_sources` configuration:

* **Project Skills** (`.claude/skills/`): Loaded when `setting_sources` includes `"project"`
* **User Skills** (`~/.claude/skills/`): Loaded when `setting_sources` includes `"user"`
* **Plugin Skills**: Bundled with plugins

## Troubleshooting

### Skills Not Found

**Most common**: Missing `setting_sources`

```python
# WRONG - Skills won't load
options = ClaudeAgentOptions(
    allowed_tools=["Skill"]
)

# CORRECT - Skills will load
options = ClaudeAgentOptions(
    setting_sources=["user", "project"],  # Required!
    allowed_tools=["Skill"]
)
```
