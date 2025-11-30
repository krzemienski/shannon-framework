# Shannon Framework v5.6 - Hooks System Audit

**Version**: 5.6.0  
**Hooks Count**: 9 files  
**Last Updated**: November 29, 2025  

---

## Overview

Shannon Framework uses Claude Code's lifecycle hooks system to enforce workflows and preserve context automatically. This document provides a complete audit of all hook implementations.

---

## Hook Inventory

| Hook | Trigger | Purpose | File |
|------|---------|---------|------|
| SessionStart | Session begins | Load using-shannon skill | session_start.sh |
| UserPromptSubmit | User sends prompt | North Star + Forced Reading | user_prompt_submit.py |
| PreCompact | Before compaction | Auto-checkpoint to Serena | precompact.py |
| PostToolUse | After Write/Edit | NO MOCKS enforcement | post_tool_use.py |
| Stop | Task completion | Wave validation gates | stop.py |

---

## 1. SessionStart Hook

### File: `session_start.sh`

**Purpose**: Loads the `using-shannon` meta-skill at the start of every session to establish Shannon workflows.

**Trigger**: When a new Claude Code session begins

**Implementation**:
```bash
#!/bin/bash
# Shannon Framework V5 - SessionStart Hook
# Loads using-shannon meta-skill to establish Shannon workflows

echo "<EXTREMELY_IMPORTANT>"
echo "You are using Shannon Framework V5."
echo ""
echo "**The content below is the using-shannon skill:**"
echo ""

# Embedded using-shannon skill content
cat << 'SKILL_EOF'
[Full using-shannon SKILL.md content embedded here]
SKILL_EOF

echo ""
echo "</EXTREMELY_IMPORTANT>"
```

**Key Features**:
- Embeds using-shannon content directly (not file reference)
- Uses `<EXTREMELY_IMPORTANT>` tag for visibility
- Executes in <5 seconds

**Configuration** (hooks.json):
```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/session_start.sh",
  "timeout": 5000
}
```

---

## 2. UserPromptSubmit Hook

### File: `user_prompt_submit.py`

**Purpose**: Injects North Star goal context and auto-activates forced reading protocol for large content.

**Trigger**: When user submits any prompt

**Version**: 5.4.0 (Enhanced with Forced Reading Detection)

**Implementation**:
```python
#!/usr/bin/env -S python3
"""
Shannon UserPromptSubmit Hook - Context Injection & Forced Reading Activation

Features:
1. North Star goal injection
2. Active wave context injection
3. Large prompt detection (>3000 chars)
4. Large file reference detection (>5000 lines)
5. Specification keyword detection
6. Forced reading protocol auto-activation
"""

def detect_large_prompt(prompt: str, threshold: int = 3000) -> bool:
    """Check if prompt exceeds character threshold."""
    return len(prompt) > threshold

def detect_file_references(prompt: str, working_dir: Path) -> List[Dict]:
    """Detect file path references and check if they're large."""
    # Regex patterns for file paths
    # Check file sizes and line counts
    # Return list of large files

def detect_specification_keywords(prompt: str) -> bool:
    """Detect specification/requirements keywords."""
    keywords = [
        'specification', 'requirements', 'design doc',
        'technical spec', 'SPEC_', 'PLAN_'
    ]
    return any(k.lower() in prompt.lower() for k in keywords)

def inject_forced_reading_protocol(large_items, is_large_prompt, has_spec_keywords):
    """Inject forced reading protocol activation."""
    print("=" * 80)
    print("📖 **SHANNON FORCED READING PROTOCOL - AUTO-ACTIVATED**")
    print("=" * 80)
    # Print activation details and protocol steps
```

**Detections**:
- Large prompts: >3000 characters
- Large files: >5000 lines or >50KB
- Specification keywords: "specification", "requirements", etc.

**Configuration** (hooks.json):
```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks/user_prompt_submit.py",
  "timeout": 3000
}
```

---

## 3. PreCompact Hook

### File: `precompact.py`

**Purpose**: Saves comprehensive checkpoint to Serena MCP before Claude Code auto-compaction to prevent context loss.

**Trigger**: When Claude Code prepares to auto-compact conversation

**Version**: 3.0.1

**Implementation**:
```python
#!/usr/bin/env -S python3
"""
Shannon PreCompact Hook - Critical Context Preservation

Flow:
1. Claude Code detects token limit approaching
2. PreCompact hook executes before compaction
3. Hook generates Serena checkpoint instructions
4. Instructions injected into system prompt
5. Claude saves all context to Serena
6. Auto-compact proceeds safely
7. Next session: context restored from checkpoint
"""

class ShannonPreCompactHook:
    VERSION = "3.0.1"
    TIMEOUT_MS = 15000

    def execute(self, input_data: Dict) -> Dict:
        """Main execution logic."""
        # Generate checkpoint instructions
        checkpoint_instructions = self._generate_checkpoint_instructions()
        
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreCompact",
                "checkpointKey": self.checkpoint_key,
                "additionalContext": checkpoint_instructions,
            }
        }

    def _generate_checkpoint_instructions(self) -> str:
        """Generate Serena checkpoint instructions."""
        # Comprehensive checkpoint template
        # Includes: session state, wave progress, todos,
        # decisions, integration status, next steps
```

**Checkpoint Data**:
```json
{
  "checkpoint_type": "auto_precompact",
  "timestamp": "ISO8601",
  "session_id": "...",
  "serena_memory_keys": ["..."],
  "active_wave_state": {
    "current_wave": 2,
    "wave_phase": "execution",
    "wave_progress": "60%",
    "active_sub_agents": ["FRONTEND", "BACKEND"]
  },
  "phase_state": {
    "current_phase": 3,
    "phase_name": "Implementation",
    "phase_progress": "..."
  },
  "project_context": {
    "north_star_goal": "...",
    "project_name": "...",
    "current_focus": "..."
  },
  "todo_state": {...},
  "decisions_made": [...],
  "integration_status": {...},
  "next_steps": [...]
}
```

**Configuration** (hooks.json):
```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks/precompact.py",
  "timeout": 15000,
  "continueOnError": false
}
```

---

## 4. PostToolUse Hook

### File: `post_tool_use.py`

**Purpose**: Detects and blocks mock usage in test files to enforce NO MOCKS philosophy.

**Trigger**: After any Write/Edit/MultiEdit tool use

**Version**: 3.0.1

**Implementation**:
```python
#!/usr/bin/env -S python3
"""
Shannon PostToolUse Hook - NO MOCKS Testing Philosophy Enforcement

Detects and blocks:
- jest.mock()
- jest.spyOn()
- unittest.mock
- @Mock annotations
- @patch decorators
- sinon.stub/mock/fake/spy
- mockImplementation
- mockReturnValue
- vi.mock() (vitest)
"""

MOCK_PATTERNS = [
    (r'jest\.mock\(', 'jest.mock()'),
    (r'jest\.spyOn', 'jest.spyOn()'),
    (r'unittest\.mock', 'unittest.mock'),
    (r'from\s+unittest\.mock\s+import', 'unittest.mock imports'),
    (r'@[Mm]ock\b', '@Mock annotation'),
    (r'@[Pp]atch\b', '@patch decorator'),
    (r'sinon\.(stub|mock|fake|spy)', 'sinon mocking'),
    (r'mockImplementation', 'mockImplementation'),
    (r'mockReturnValue', 'mockReturnValue'),
    (r'vi\.mock\(', 'vitest mock'),
]

def detect_mocks(content: str) -> list:
    """Detect mock usage patterns in content."""
    violations = []
    for pattern, name in MOCK_PATTERNS:
        if re.search(pattern, content, re.MULTILINE):
            violations.append(name)
    return violations

def is_test_file(file_path: str) -> bool:
    """Check if file is a test file."""
    test_indicators = [
        '/test/', '/__tests__/', '/tests/',
        '.test.', '.spec.', '_test.', '_spec.'
    ]
    return any(i in file_path for i in test_indicators)
```

**Blocked Response**:
```
🚨 **Shannon NO MOCKS Violation Detected**

**File**: tests/auth.test.js
**Violations**: jest.mock(), mockImplementation

**Shannon Testing Philosophy**: Tests must validate REAL system 
behavior with real components, not mocked responses.

**Required Actions**:
1. Remove all mock usage
2. Implement functional test using:
   - Web/Frontend: Puppeteer MCP
   - Backend/API: Real HTTP requests
   - Database: Real database instance
```

**Configuration** (hooks.json):
```json
{
  "matcher": "Write|Edit|MultiEdit",
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks/post_tool_use.py",
  "timeout": 3000
}
```

---

## 5. Stop Hook

### File: `stop.py`

**Purpose**: Blocks completion until wave validation gates are satisfied.

**Trigger**: When Claude attempts to stop/complete

**Version**: 3.0.1

**Implementation**:
```python
#!/usr/bin/env -S python3
"""
Shannon Stop Hook - Wave Validation Gate Enforcement

Checks:
1. Pending wave validation marker
2. Incomplete critical tasks
"""

def main():
    # Check for pending wave validation
    validation_pending_file = serena_root / ".serena" / "wave_validation_pending"
    
    if validation_pending_file.exists():
        output = {
            "decision": "block",
            "reason": """⚠️ Shannon Wave Validation Required
            
            **Required Actions**:
            1. Present wave synthesis to user
            2. Request explicit approval
            3. Create checkpoint
            4. Mark validation complete
            """
        }
        return output
    
    # Check for incomplete critical todos
    critical_todos_file = serena_root / ".serena" / "critical_todos_incomplete"
    
    if critical_todos_file.exists():
        output = {
            "decision": "block",
            "reason": """⚠️ Shannon Critical Tasks Incomplete"""
        }
        return output
    
    # Allow normal completion
    sys.exit(0)
```

**Validation Gates**:
- Wave synthesis must be presented to user
- User must explicitly approve wave results
- Critical tasks must be completed or explicitly deferred

**Configuration** (hooks.json):
```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks/stop.py",
  "timeout": 2000
}
```

---

## 6. Additional Hook Files

### 6.1 user-prompt-submit-hook.sh

**Purpose**: Alternative shell-based implementation of UserPromptSubmit

**Use Case**: Simpler environments without Python

### 6.2 hooks.json

**Purpose**: Central hook configuration file

**Structure**:
```json
{
  "hooks": {
    "SessionStart": [...],
    "UserPromptSubmit": [...],
    "PreCompact": [...],
    "PostToolUse": [...],
    "Stop": [...]
  }
}
```

### 6.3 README.md

**Purpose**: Hook system documentation

### 6.4 HOOK_VERIFICATION_RESULTS.md

**Purpose**: Test results for hook functionality

---

## Hook Lifecycle Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     SESSION START                            │
│                           │                                  │
│                           ▼                                  │
│              ┌────────────────────────┐                      │
│              │   session_start.sh     │                      │
│              │  (Load using-shannon)  │                      │
│              └────────────────────────┘                      │
│                           │                                  │
│                           ▼                                  │
│              ┌────────────────────────┐                      │
│              │   USER PROMPT SUBMIT   │◄─────────────────┐   │
│              │  user_prompt_submit.py │                  │   │
│              │  - North Star inject   │                  │   │
│              │  - Forced reading      │                  │   │
│              └────────────────────────┘                  │   │
│                           │                              │   │
│                           ▼                              │   │
│              ┌────────────────────────┐                  │   │
│              │     CLAUDE WORKS       │                  │   │
│              │   (Write/Edit/etc)     │                  │   │
│              └────────────────────────┘                  │   │
│                           │                              │   │
│                           ▼                              │   │
│              ┌────────────────────────┐                  │   │
│              │    POST TOOL USE       │                  │   │
│              │   post_tool_use.py     │                  │   │
│              │  (NO MOCKS check)      │                  │   │
│              └────────────────────────┘                  │   │
│                           │                              │   │
│              ┌────────────┼────────────┐                 │   │
│              │            │            │                 │   │
│              ▼            ▼            ▼                 │   │
│      ┌───────────┐ ┌───────────┐ ┌───────────┐          │   │
│      │ Continue  │ │ PreCompact│ │   Stop    │          │   │
│      │           │ │  Trigger  │ │  Attempt  │          │   │
│      └─────┬─────┘ └─────┬─────┘ └─────┬─────┘          │   │
│            │             │             │                 │   │
│            │             ▼             ▼                 │   │
│            │     ┌───────────┐ ┌───────────┐            │   │
│            │     │precompact │ │  stop.py  │            │   │
│            │     │   .py     │ │(Validation│            │   │
│            │     │(Checkpoint│ │   Gate)   │            │   │
│            │     │ to Serena)│ └─────┬─────┘            │   │
│            │     └───────────┘       │                  │   │
│            │                         │                  │   │
│            └─────────────────────────┼──────────────────┘   │
│                                      │                      │
│                                      ▼                      │
│                          ┌────────────────────┐             │
│                          │   SESSION END      │             │
│                          └────────────────────┘             │
└─────────────────────────────────────────────────────────────┘
```

---

## Hook Configuration Reference

### Complete hooks.json

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "description": "Shannon context injection and forced reading activation",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/user_prompt_submit.py",
            "description": "Injects North Star goal, active wave context, auto-activates forced-reading-protocol",
            "timeout": 3000
          }
        ]
      }
    ],

    "PreCompact": [
      {
        "description": "Shannon context preservation",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/precompact.py",
            "description": "Triggers CONTEXT_GUARDIAN to create Serena checkpoint",
            "timeout": 15000,
            "continueOnError": false
          }
        ]
      }
    ],

    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "description": "Shannon NO MOCKS enforcement",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/post_tool_use.py",
            "description": "Detects and blocks mock usage in test files",
            "timeout": 3000
          }
        ]
      }
    ],

    "Stop": [
      {
        "description": "Shannon wave validation gate enforcement",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/stop.py",
            "description": "Blocks completion until validation gates satisfied",
            "timeout": 2000
          }
        ]
      }
    ],

    "SessionStart": [
      {
        "description": "Shannon V5 meta-skill loader",
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/session_start.sh",
            "description": "Loads using-shannon meta-skill",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

---

## Troubleshooting

### Hook Not Firing

1. **Check hooks.json exists**: `cat ~/.claude/hooks.json`
2. **Verify hook scripts executable**: `ls -l ~/.claude/hooks/shannon/`
3. **Restart Claude Code completely**
4. **Check installation log**: `cat ~/.claude/shannon_install.log`

### Mock Detection Not Working

1. **Verify post_tool_use.py executable**: `chmod +x ~/.claude/hooks/shannon/post_tool_use.py`
2. **Check matcher pattern**: Should be `Write|Edit|MultiEdit`
3. **Verify file is recognized as test file**: Must contain `/test/`, `.test.`, etc.

### PreCompact Not Saving

1. **Verify Serena MCP configured**: `/shannon:check_mcps`
2. **Check .serena directory exists**: `ls ~/.serena` or project-level
3. **Increase timeout if needed**: Change from 15000 to 30000ms

---

**Hooks Audit Complete**: November 29, 2025
