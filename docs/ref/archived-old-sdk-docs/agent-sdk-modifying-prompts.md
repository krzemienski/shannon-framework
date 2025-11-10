# System Prompts Customization Guide

The Claude Agent SDK provides four approaches to customize system prompts:

## Key Methods

**Method 1: CLAUDE.md Files**
Project-level instruction files requiring `settingSources: ['project']` to load.

**Method 2: Output Styles**
Saved markdown configurations in `~/.claude/output-styles`

**Method 3: systemPrompt with Append**
Adds custom instructions to Claude Code's preset.

**Method 4: Custom System Prompts**
Complete replacement with custom string.

## Critical Implementation Detail

"The `claude_code` system prompt preset does NOT automatically load CLAUDE.md" — must explicitly specify setting sources.
