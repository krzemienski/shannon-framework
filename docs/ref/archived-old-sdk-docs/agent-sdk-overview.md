# Agent SDK Overview

## Installation

```bash
npm install @anthropic-ai/claude-agent-sdk  # TypeScript
pip install claude-agent-sdk  # Python
```

## Why use the Claude Agent SDK?

Built on agent harness powering Claude Code, provides:

* **Context Management**: Automatic compaction
* **Rich tool ecosystem**: File operations, code execution, web search, MCP
* **Advanced permissions**: Fine-grained control
* **Production essentials**: Error handling, session management, monitoring
* **Optimized Claude integration**: Prompt caching, performance

## What can you build?

**Coding agents**: SRE, security review, code review, oncall assistants
**Business agents**: Legal, finance, customer support, content creation

## Core Concepts

### Authentication
Set `ANTHROPIC_API_KEY` environment variable or use Bedrock/Vertex AI.

### Full Claude Code Feature Support

Access to all Claude Code features via filesystem configuration:

* **Subagents**: `./.claude/agents/`
* **Agent Skills**: `./.claude/skills/`
* **Hooks**: `./.claude/settings.json`
* **Slash Commands**: `./.claude/commands/`
* **Plugins**: Load programmatically via `plugins` option
* **Memory (CLAUDE.md)**: Project context files

**CRITICAL**: To load filesystem features, must set `settingSources: ['project']` (TypeScript) or `setting_sources=["project"]` (Python).
