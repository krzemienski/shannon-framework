# Claude Code Builder Autonomous - Architecture & Integration Specification

**Version**: 1.0.0
**Date**: December 2025
**Status**: Design Complete

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Source Material Analysis](#source-material-analysis)
3. [Comparative Analysis](#comparative-analysis)
4. [Unified Architecture Design](#unified-architecture-design)
5. [Technical Specifications](#technical-specifications)
6. [Implementation Roadmap](#implementation-roadmap)
7. [MCP Integration Strategy](#mcp-integration-strategy)
8. [XML Prompt System](#xml-prompt-system)

---

## Executive Summary

This document defines the architecture for an **Autonomous Claude Code Builder** that:
- Intelligently researches capabilities before execution
- Dynamically discovers and installs required MCPs
- Maintains full codebase context via Serena MCP
- Executes builds with awareness of existing code
- Handles both new projects and existing directory scenarios

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Memory System | Serena MCP (NOT open memory) | Semantic code understanding, LSP integration, 30+ language support |
| Agent Pattern | Two-Agent (Initializer + Coding) | Proven by Anthropic's long-running agent research |
| Context Bridge | `feature_list.json` + `claude-progress.txt` | Enables stateless session resumption |
| SDK Integration | ClaudeSDKClient (stateful) | Multi-turn conversations with context retention |
| Security Model | Allowlist + Sandbox | Defense-in-depth from Claude Quickstart |

---

## Source Material Analysis

### 1. Claude Quickstart (Autonomous Coding)

**Repository**: `github.com/anthropics/claude-quickstarts/autonomous-coding`

#### Architecture Components

| Component | Purpose | Key Feature |
|-----------|---------|-------------|
| `autonomous_agent_demo.py` | Main entry point | CLI args, session orchestration |
| `agent.py` | Session logic | Async query loop, message handling |
| `client.py` | SDK configuration | Security hooks, sandbox, MCP integration |
| `security.py` | Command validation | Allowlist-based bash security |
| `progress.py` | State persistence | Feature list tracking |
| `prompts/` | Agent instructions | Initializer + Coding agent prompts |

#### Two-Agent Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    SESSION 1 (Initializer)                  │
│  • Read app_spec.txt                                        │
│  • Generate feature_list.json (200+ features, all false)    │
│  • Create init.sh (environment setup)                       │
│  • Initialize git repository                                │
│  • Create directory structure                               │
│  • Write claude-progress.txt                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               SESSION 2+ (Coding Agent Loop)                │
│  • Read git logs + progress files                           │
│  • Read feature_list.json                                   │
│  • Select highest-priority incomplete feature               │
│  • Run init.sh, verify baseline                             │
│  • Implement ONE feature                                    │
│  • Test with Puppeteer (visual verification)                │
│  • Mark feature as passes: true                             │
│  • Git commit + update progress                             │
│  • Auto-continue to next session                            │
└─────────────────────────────────────────────────────────────┘
```

#### Security Model

```python
ALLOWED_COMMANDS = {
    # File inspection
    "ls", "cat", "head", "tail", "wc", "grep",
    # File operations
    "cp", "mkdir", "chmod",
    # Directory
    "pwd",
    # Development
    "npm", "node",
    # Version control
    "git",
    # Process management
    "ps", "lsof", "sleep", "pkill",
    # Scripts
    "init.sh"
}

# Extra validation for sensitive commands
COMMANDS_NEEDING_EXTRA_VALIDATION = {"pkill", "chmod", "init.sh"}
```

#### Key Patterns Extracted

1. **Immutable Feature Tracking**: Only `passes` field can change
2. **Session Continuity**: Fresh context per session, state via artifacts
3. **Auto-Continue**: 3-second delay between iterations
4. **Visual Verification**: Puppeteer screenshots for UI testing

---

### 2. Anthropic Blog: Effective Harnesses for Long-Running Agents

**URL**: `anthropic.com/engineering/effective-harnesses-for-long-running-agents`

#### Core Problem

> "Each new session begins with no memory of what came before. Imagine a software project staffed by engineers working in shifts, where each new engineer arrives with no memory of what happened on the previous shift."

#### Solution Architecture

| Component | First Session | Subsequent Sessions |
|-----------|--------------|---------------------|
| `init.sh` | Create | Read |
| `claude-progress.txt` | Write | Read + Update |
| `feature_list.json` | Generate (200+) | Read + Update `passes` |
| Git commits | Initial | Incremental |

#### Failure Patterns Identified

| Problem | Cause | Solution |
|---------|-------|----------|
| Early victory declaration | Agent thinks job is done | Comprehensive feature list (200+) |
| One-shot attempts | Tries to build everything at once | Sequential, one feature per session |
| Buggy/undocumented code | No verification | Progress notes + git commits |
| Premature feature completion | Skips testing | Visual verification with screenshots |

#### Session Startup Protocol

1. `pwd` - Verify working directory
2. Read git logs + `claude-progress.txt`
3. Read `feature_list.json`
4. Run `init.sh`
5. Execute baseline smoke test
6. Begin feature implementation

---

### 3. Claude Code Builder

**Repository**: `github.com/krzemienski/claude-code-builder`

#### Multi-Agent System

| Agent | Role | Output |
|-------|------|--------|
| SpecAnalyzer | Requirement extraction | Structured requirements |
| TaskGenerator | Task ordering | Dependency graph |
| InstructionBuilder | Claude instructions | Formatted prompts |
| CodeGenerator | Implementation | Source code |
| TestGenerator | Test creation | Test suites |
| ReviewAgent | Quality validation | Review report |

#### MCP Server Integration

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    },
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/puppeteer-mcp-server"]
    }
  }
}
```

#### Key Features

- **Checkpoint/Resume**: Automatic checkpointing after each phase
- **Cost Tracking**: Token usage and budget enforcement
- **Context Management**: 150K token handling with chunking
- **Phase-Based Processing**: Modular build stages

---

### 4. Shannon Framework (Current)

**Location**: `/home/user/shannon-framework`

#### Existing Infrastructure

| Component | Count | Status |
|-----------|-------|--------|
| Commands | 20 | Production |
| Skills | 21 | Production |
| Hooks | 5 | Production |
| Core Files | 9 | Production |
| Agent Guides | 25 | Production |
| Orchestrator | 1 | Production |
| Decision Engine | 1 | Production |

#### Relevant Components

**Orchestrator** (`orchestration/orchestrator.py`):
- HALT/RESUME/ROLLBACK controls
- Wave execution with snapshots
- <100ms halt response time
- State management with StateManager

**Decision Engine** (`orchestration/decision_engine.py`):
- Human-in-the-loop decisions
- Auto-approve high confidence (≥0.95)
- Pending decision tracking

**SDK Examples** (`tests/sdk-examples/`):
- Plugin loading patterns
- Message type checking (isinstance)
- Content block iteration
- Cost tracking

---

## Comparative Analysis

### Feature Comparison Matrix

| Feature | Quickstart | Code Builder | Shannon | Unified Design |
|---------|------------|--------------|---------|----------------|
| Two-agent pattern | ✅ | ❌ | ❌ | ✅ |
| Multi-agent phases | ❌ | ✅ | ✅ (waves) | ✅ |
| MCP dynamic install | ❌ | ❌ | ❌ | ✅ |
| Serena integration | ❌ | ❌ | ✅ (61%) | ✅ |
| Feature tracking | ✅ (JSON) | ✅ (phases) | ✅ (Serena) | ✅ (hybrid) |
| Visual verification | ✅ (Puppeteer) | ✅ | ❌ | ✅ |
| Security allowlist | ✅ | ❌ | ❌ | ✅ |
| Checkpoint/resume | ✅ (basic) | ✅ | ✅ | ✅ |
| Cost tracking | ❌ | ✅ | ❌ | ✅ |
| Context compaction | ❌ | ✅ | ✅ | ✅ |
| HALT/RESUME | ❌ | ❌ | ✅ | ✅ |
| Decision engine | ❌ | ❌ | ✅ | ✅ |
| XML prompts | ❌ | ❌ | ❌ | ✅ |
| Existing code awareness | ❌ | ❌ | ❌ | ✅ |

### Strengths to Adopt

#### From Claude Quickstart
1. **Two-agent pattern** - Proven for long-running tasks
2. **Feature list as progress tracker** - Immutable source of truth
3. **Security allowlist** - Defense-in-depth command validation
4. **Session startup protocol** - Consistent context recovery

#### From Claude Code Builder
1. **Multi-agent phases** - Specialized agents for specific tasks
2. **MCP server configuration** - Structured MCP management
3. **Cost tracking** - Budget enforcement and monitoring
4. **Context management** - Large spec handling

#### From Shannon Framework
1. **Serena MCP integration** - Semantic code understanding
2. **Orchestrator** - HALT/RESUME/ROLLBACK controls
3. **Decision engine** - Human-in-the-loop when needed
4. **Wave execution** - Parallel agent spawning
5. **Hooks system** - Lifecycle event handling

---

## Unified Architecture Design

### System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     AUTONOMOUS CLAUDE CODE BUILDER                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        USER INPUT LAYER                              │   │
│  │  • Natural language request                                          │   │
│  │  • Target directory specification                                    │   │
│  │  • Configuration overrides                                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                   XML PROMPT TRANSFORMER                             │   │
│  │  • Parse user request                                                │   │
│  │  • Structure into XML format                                         │   │
│  │  • Inject context from Serena                                        │   │
│  │  • Apply best practices                                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    RESEARCH & DISCOVERY PHASE                        │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐        │   │
│  │  │  Capability    │  │    MCP         │  │   Codebase     │        │   │
│  │  │  Research      │  │  Discovery     │  │   Analysis     │        │   │
│  │  └────────────────┘  └────────────────┘  └────────────────┘        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      MCP INSTALLATION LAYER                          │   │
│  │  • Match task requirements to MCPs                                   │   │
│  │  • Install required MCPs dynamically                                 │   │
│  │  • Generate usage skills for new MCPs                                │   │
│  │  • Verify MCP availability                                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    SERENA CONTEXT BACKBONE                           │   │
│  │  • Query existing codebase structure                                 │   │
│  │  • Build symbol-level understanding                                  │   │
│  │  • Store execution state                                             │   │
│  │  • Maintain cross-session memory                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      EXECUTION ORCHESTRATOR                          │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │              TWO-AGENT PATTERN                               │    │   │
│  │  │  ┌───────────────────┐    ┌───────────────────┐            │    │   │
│  │  │  │  Initializer      │ ─► │  Coding Agent     │            │    │   │
│  │  │  │  Agent            │    │  (Loop)           │            │    │   │
│  │  │  └───────────────────┘    └───────────────────┘            │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │              WAVE ORCHESTRATION                              │    │   │
│  │  │  • Parallel agent execution                                  │    │   │
│  │  │  • HALT/RESUME/ROLLBACK controls                             │    │   │
│  │  │  • Decision engine integration                               │    │   │
│  │  │  • Checkpoint management                                     │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     VERIFICATION LAYER                               │   │
│  │  • Visual testing (Puppeteer)                                       │   │
│  │  • Feature completion validation                                     │   │
│  │  • Security scanning                                                 │   │
│  │  • Cost tracking and reporting                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Architecture

#### 1. XML Prompt Transformer

```python
class XMLPromptTransformer:
    """
    Transforms user requests into structured XML prompts for Claude.

    XML Structure:
    <request>
        <context>
            <existing_codebase>...</existing_codebase>
            <project_type>...</project_type>
            <dependencies>...</dependencies>
        </context>
        <task>
            <objective>...</objective>
            <requirements>...</requirements>
            <constraints>...</constraints>
        </task>
        <instructions>
            <step>...</step>
            ...
        </instructions>
        <output_format>
            <structure>...</structure>
            <validation>...</validation>
        </output_format>
    </request>
    """
```

#### 2. MCP Discovery & Installation

```python
class MCPManager:
    """
    Manages dynamic MCP discovery, installation, and skill generation.
    """

    # Task-to-MCP mapping
    MCP_MAPPING = {
        "web_scraping": ["puppeteer"],
        "web_automation": ["puppeteer"],
        "database": ["sqlite", "postgres", "mysql"],
        "api_testing": ["fetch", "http-client"],
        "code_analysis": ["serena"],
        "file_operations": ["filesystem"],
        "version_control": ["github"],
        "memory": ["serena"],  # NOT open memory
        "search": ["tavily", "perplexity"],
        "documentation": ["context7"]
    }

    async def analyze_task(self, task: str) -> List[str]:
        """Determine required MCPs for task."""

    async def install_mcp(self, mcp_name: str) -> bool:
        """Install MCP if not present."""

    async def generate_usage_skill(self, mcp_name: str) -> str:
        """Generate skill documentation for MCP."""
```

#### 3. Serena Context Manager

```python
class SerenaContextManager:
    """
    Manages codebase context via Serena MCP (NOT open memory).

    Provides:
    - Symbol-level code understanding
    - Cross-session memory persistence
    - Semantic code search
    - Project structure awareness
    """

    async def analyze_existing_directory(self, path: str) -> CodebaseContext:
        """Build complete understanding of existing codebase."""

    async def find_symbol(self, symbol_name: str) -> List[SymbolLocation]:
        """Locate code symbols semantically."""

    async def read_memory(self, memory_name: str) -> Optional[str]:
        """Retrieve persistent memory from .serena/memories/"""

    async def write_memory(self, memory_name: str, content: str) -> bool:
        """Store memory for future sessions."""

    async def create_execution_summary(self) -> str:
        """Generate summary for session continuity."""
```

#### 4. Dual Scenario Handler

```python
class ScenarioHandler:
    """
    Handles both existing directory and new project scenarios.
    """

    async def detect_scenario(self, target_dir: str) -> Scenario:
        """
        Detect whether target is existing codebase or new project.

        Scenario A: Existing directory
        - Has existing files
        - May have package.json, requirements.txt, etc.
        - Requires codebase analysis before modification

        Scenario B: New project
        - Empty or non-existent directory
        - Requires full scaffolding
        - No existing patterns to preserve
        """

    async def handle_existing_directory(self, dir: str, task: str) -> ExecutionPlan:
        """
        Scenario A: Implementation in existing directory.

        1. Query Serena for complete codebase context
        2. Identify existing patterns and conventions
        3. Build dependency map
        4. Plan changes that respect existing architecture
        5. Generate feature list considering existing code
        """

    async def handle_new_project(self, dir: str, task: str) -> ExecutionPlan:
        """
        Scenario B: New project initialization.

        1. Analyze requirements for tooling
        2. Determine project type and stack
        3. Install required MCPs
        4. Scaffold project structure
        5. Generate comprehensive feature list
        """
```

#### 5. Security Manager

```python
class SecurityManager:
    """
    Implements defense-in-depth security from Claude Quickstart.
    """

    ALLOWED_COMMANDS = {
        # File inspection
        "ls", "cat", "head", "tail", "wc", "grep",
        # File operations
        "cp", "mkdir", "chmod", "rm", "mv",
        # Directory
        "pwd", "cd",
        # Development
        "npm", "node", "npx", "yarn", "pnpm",
        "python", "pip", "uv", "poetry",
        "cargo", "rustc",
        "go",
        "java", "gradle", "maven",
        # Version control
        "git",
        # Process management
        "ps", "lsof", "sleep", "pkill", "kill",
        # Scripts
        "init.sh", "setup.sh"
    }

    COMMANDS_NEEDING_EXTRA_VALIDATION = {
        "pkill", "kill",  # Must target dev processes only
        "chmod",          # Only +x allowed
        "rm",             # Validate paths
        "init.sh", "setup.sh"
    }

    def validate_command(self, cmd: str) -> ValidationResult:
        """Validate bash command against allowlist."""

    async def bash_security_hook(self, input_data: dict) -> HookResult:
        """Pre-tool-use hook for bash commands."""
```

---

## Technical Specifications

### Python SDK Integration

```python
from claude_agent_sdk import (
    query,
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    SystemMessage,
    ResultMessage
)

class AutonomousBuilder:
    """
    Main autonomous builder using Claude Agent SDK.
    """

    def __init__(self, config: BuilderConfig):
        self.config = config
        self.serena = SerenaContextManager()
        self.mcp_manager = MCPManager()
        self.xml_transformer = XMLPromptTransformer()
        self.security = SecurityManager()
        self.orchestrator = ExecutionOrchestrator()

    async def build(self, user_request: str, target_dir: str) -> BuildResult:
        """
        Execute autonomous build.

        Flow:
        1. Detect scenario (existing vs new)
        2. Transform request to XML prompt
        3. Research required capabilities
        4. Install necessary MCPs
        5. Build Serena context
        6. Execute two-agent pattern
        7. Verify completion
        """

        # Phase 1: Scenario Detection
        scenario = await self.scenario_handler.detect_scenario(target_dir)

        # Phase 2: Context Building
        if scenario.is_existing:
            context = await self.serena.analyze_existing_directory(target_dir)
        else:
            context = CodebaseContext.empty()

        # Phase 3: MCP Discovery & Installation
        required_mcps = await self.mcp_manager.analyze_task(user_request)
        for mcp in required_mcps:
            await self.mcp_manager.install_mcp(mcp)

        # Phase 4: XML Prompt Generation
        xml_prompt = self.xml_transformer.transform(
            request=user_request,
            context=context,
            scenario=scenario
        )

        # Phase 5: Two-Agent Execution
        # First: Initializer Agent
        await self._run_initializer_session(xml_prompt, target_dir)

        # Then: Coding Agent Loop
        while not await self._is_complete(target_dir):
            await self._run_coding_session(target_dir)

        # Phase 6: Verification
        result = await self._verify_completion(target_dir)

        return result

    async def _run_initializer_session(self, xml_prompt: str, target_dir: str):
        """
        Session 1: Initializer Agent

        Tasks:
        - Read specification
        - Generate feature_list.json (all passes: false)
        - Create init.sh
        - Initialize git
        - Create directory structure
        - Write claude-progress.txt
        """
        options = ClaudeAgentOptions(
            setting_sources=["user", "project"],
            permission_mode="acceptEdits",
            cwd=target_dir,
            allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
            hooks={"PreToolUse": [self.security.bash_security_hook]},
            mcp_servers=self._get_mcp_config()
        )

        prompt = self._create_initializer_prompt(xml_prompt)

        async with ClaudeSDKClient(options) as client:
            await client.connect(prompt)
            async for message in client.receive_messages():
                await self._process_message(message)

    async def _run_coding_session(self, target_dir: str):
        """
        Session 2+: Coding Agent

        Tasks:
        - Read progress files
        - Select next incomplete feature
        - Run init.sh
        - Implement feature
        - Test with Puppeteer
        - Update feature_list.json (passes: true)
        - Git commit
        - Update progress
        """
        options = ClaudeAgentOptions(
            setting_sources=["user", "project"],
            permission_mode="acceptEdits",
            cwd=target_dir,
            allowed_tools=[
                "Read", "Write", "Edit", "Bash", "Glob", "Grep",
                "mcp__puppeteer__*",  # Visual testing
                "mcp__serena__*"       # Code context
            ],
            hooks={"PreToolUse": [self.security.bash_security_hook]},
            mcp_servers=self._get_mcp_config()
        )

        prompt = self._create_coding_prompt(target_dir)

        async with ClaudeSDKClient(options) as client:
            await client.connect(prompt)
            async for message in client.receive_messages():
                if isinstance(message, AssistantMessage):
                    await self._handle_assistant_message(message)
                elif isinstance(message, ResultMessage):
                    await self._handle_result(message)
```

### Feature List Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "project_name": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" },
    "features": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "category": {
            "type": "string",
            "enum": ["functional", "style", "integration", "performance", "security"]
          },
          "description": { "type": "string" },
          "priority": { "type": "integer", "minimum": 1, "maximum": 10 },
          "steps": {
            "type": "array",
            "items": { "type": "string" }
          },
          "passes": { "type": "boolean", "default": false },
          "implemented_at": { "type": ["string", "null"], "format": "date-time" },
          "session_id": { "type": ["string", "null"] }
        },
        "required": ["id", "category", "description", "steps", "passes"]
      },
      "minItems": 50
    }
  }
}
```

### Prompt Templates

#### Initializer Prompt (XML Format)

```xml
<system>
You are an Initializer Agent for an autonomous code builder. Your task is to set up the foundation for a multi-session development project.

<context>
    <existing_codebase>{serena_context}</existing_codebase>
    <scenario>{scenario_type}</scenario>
    <mcps_available>{available_mcps}</mcps_available>
</context>

<task>
    <specification>{user_specification}</specification>
    <target_directory>{target_dir}</target_directory>
</task>

<required_outputs>
    <output name="feature_list.json">
        Generate comprehensive feature list with:
        - Minimum 50 features (more for complex projects)
        - ALL features start with "passes": false
        - IT IS CATASTROPHIC TO REMOVE OR EDIT FEATURES IN FUTURE SESSIONS
        - Categories: functional, style, integration, performance, security
        - Each feature has testable verification steps
    </output>

    <output name="init.sh">
        Environment setup script:
        - Install dependencies
        - Start development server
        - Print access instructions
    </output>

    <output name="claude-progress.txt">
        Session summary including:
        - What was accomplished
        - Current state
        - Next steps for coding agent
    </output>
</required_outputs>

<constraints>
    - Use Serena MCP for all codebase context queries
    - Respect existing code patterns if implementing in existing directory
    - Do not overwrite existing files without explicit instruction
    - Create git commit after initialization
</constraints>
</system>
```

#### Coding Agent Prompt (XML Format)

```xml
<system>
You are a Coding Agent continuing an autonomous development project. Work incrementally on one feature per session.

<session_startup>
    1. Run pwd to verify working directory
    2. Read git log and claude-progress.txt for context
    3. Read feature_list.json to find next incomplete feature
    4. Run init.sh to start development environment
    5. Execute baseline verification test
</session_startup>

<task>
    <objective>Implement the highest-priority incomplete feature</objective>
    <working_directory>{target_dir}</working_directory>
</task>

<verification_requirements>
    - Test like a human user with visual verification
    - Use Puppeteer MCP for browser-based testing
    - Take screenshots to verify UI changes
    - Do NOT mark feature complete without verification
</verification_requirements>

<session_closure>
    1. Update feature_list.json: ONLY change "passes" field to true after verification
    2. Git commit with descriptive message
    3. Update claude-progress.txt with accomplishments
    4. Leave codebase in mergeable state
</session_closure>

<important>
    - Complete ONE feature thoroughly, not many features partially
    - It's ok to complete only one feature - more sessions will follow
    - NEVER remove or edit feature definitions
    - Always verify with real testing before marking complete
</important>
</system>
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)

| Task | Description | Deliverables |
|------|-------------|--------------|
| 1.1 | Create project structure | `autonomous-builder/` directory |
| 1.2 | Implement XMLPromptTransformer | `xml_transformer.py` |
| 1.3 | Implement SecurityManager | `security.py` |
| 1.4 | Create prompt templates | `prompts/initializer.xml`, `prompts/coding.xml` |
| 1.5 | Setup configuration | `config.py`, `config.yaml` |

### Phase 2: MCP Integration (Week 2)

| Task | Description | Deliverables |
|------|-------------|--------------|
| 2.1 | Implement MCPManager | `mcp_manager.py` |
| 2.2 | Create task-to-MCP mapping | `mcp_mappings.py` |
| 2.3 | Implement SerenaContextManager | `serena_context.py` |
| 2.4 | MCP skill generation | `skill_generator.py` |
| 2.5 | MCP installation automation | `mcp_installer.py` |

### Phase 3: Agent Execution (Week 3)

| Task | Description | Deliverables |
|------|-------------|--------------|
| 3.1 | Implement ScenarioHandler | `scenario_handler.py` |
| 3.2 | Create InitializerAgent | `agents/initializer.py` |
| 3.3 | Create CodingAgent | `agents/coding.py` |
| 3.4 | Implement session loop | `session_manager.py` |
| 3.5 | Integrate with Shannon Orchestrator | `orchestrator_integration.py` |

### Phase 4: Verification & Polish (Week 4)

| Task | Description | Deliverables |
|------|-------------|--------------|
| 4.1 | Visual verification with Puppeteer | `verification/visual.py` |
| 4.2 | Feature completion validation | `verification/features.py` |
| 4.3 | Cost tracking | `tracking/costs.py` |
| 4.4 | End-to-end testing | `tests/e2e/` |
| 4.5 | Documentation | `README.md`, API docs |

---

## MCP Integration Strategy

### Core MCPs (Always Required)

| MCP | Purpose | Installation |
|-----|---------|--------------|
| Serena | Codebase context, memory | `uvx --from git+https://github.com/oraios/serena serena` |
| Filesystem | File operations | `npx @modelcontextprotocol/server-filesystem` |

### Conditional MCPs (Task-Dependent)

| Task Type | MCP | Installation |
|-----------|-----|--------------|
| Web UI | Puppeteer | `npx @anthropic-ai/puppeteer-mcp-server` |
| Web scraping | Puppeteer | `npx @anthropic-ai/puppeteer-mcp-server` |
| GitHub ops | GitHub | `npx @modelcontextprotocol/server-github` |
| API testing | Fetch | `npx @modelcontextprotocol/server-fetch` |
| Research | Tavily | `npx tavily-mcp-server` |
| Docs lookup | Context7 | Via marketplace |

### MCP Configuration Template

```json
{
  "mcpServers": {
    "serena": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server"],
      "env": {
        "SERENA_PROJECT_ROOT": "${workspaceFolder}"
      }
    },
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/puppeteer-mcp-server"],
      "env": {
        "PUPPETEER_HEADLESS": "true"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${workspaceFolder}"]
    }
  }
}
```

---

## XML Prompt System

### Design Principles

Based on [Claude's XML tag best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags):

1. **Consistency**: Use same tag names throughout
2. **Hierarchy**: Nest tags for layered information
3. **Meaningful naming**: Tags describe their content
4. **Parseability**: Enable easy response extraction

### Standard Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `<system>` | Top-level container | Wraps entire prompt |
| `<context>` | Background information | Existing code, project type |
| `<task>` | What to accomplish | Objective, requirements |
| `<instructions>` | Step-by-step guidance | Ordered steps |
| `<constraints>` | Limitations | Security, style rules |
| `<output_format>` | Expected response | Structure, validation |
| `<examples>` | Reference samples | Good/bad patterns |
| `<thinking>` | Reasoning process | Chain-of-thought |
| `<answer>` | Final response | Structured output |

### Transformation Pipeline

```
User Request → Parse Intent → Query Serena → Build Context → Format XML → Validate → Output
```

---

## Success Criteria

- [ ] System correctly identifies existing vs new project scenarios
- [ ] MCP discovery and installation works automatically
- [ ] Serena MCP maintains full codebase context
- [ ] Two-agent pattern executes correctly across sessions
- [ ] Feature list tracking works with immutable definitions
- [ ] Visual verification with Puppeteer validates UI
- [ ] Security allowlist blocks unauthorized commands
- [ ] XML prompts produce consistent Claude responses
- [ ] Cost tracking and budget enforcement functional
- [ ] HALT/RESUME/ROLLBACK controls work from Shannon orchestrator

---

## References

### Source Materials
- [Claude Quickstarts - Autonomous Coding](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)
- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Claude Code Builder](https://github.com/krzemienski/claude-code-builder)
- [Claude Agent SDK Python](https://platform.claude.com/docs/en/agent-sdk/python)
- [Serena MCP](https://github.com/oraios/serena)

### Claude Documentation
- [Building Agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [XML Tags for Prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags)
- [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)
