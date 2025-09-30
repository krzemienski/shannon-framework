---
name: help
description: "Enhanced help system with Shannon documentation access and intelligent command discovery"
category: meta
complexity: simple
mcp-servers: [context7]
personas: [mentor, analyzer]
wave-enabled: false
shannon-v3-enhanced: true
base-command: SuperClaude /index
---

# /sc:help - Enhanced Help & Documentation System

## Purpose

Provide comprehensive help and documentation with enhanced Shannon V3 capabilities:
- **SuperClaude Base**: Command catalog browsing, usage patterns, command discovery
- **Shannon Enhancement**: Shannon-specific documentation access, component reference
- **Intelligent Discovery**: Context-aware command suggestions based on current task
- **Framework Navigation**: Access to Shannon specifications, patterns, and examples
- **Quick Reference**: Command syntax, flags, and integration patterns

## Activation Triggers

### Automatic
- User confusion detected (repeated similar queries)
- Invalid command syntax entered
- Unknown flag usage
- Mode or persona questions
- First-time Shannon usage

### Manual
- User types `/sc:help` or `/help`
- Command-specific help: `/sc:help [command]`
- Category browse: `/sc:help --category [name]`
- Shannon docs: `/sc:help --shannon`
- Quick reference: `/sc:help --quick`

## Usage Patterns

```bash
# General help (shows command overview)
/sc:help

# Command-specific help
/sc:help analyze-spec
/sc:help plan-phase
/sc:help wave-execute

# Browse commands by category
/sc:help --category development
/sc:help --category analysis
/sc:help --category shannon

# Shannon-specific documentation
/sc:help --shannon
/sc:help --shannon agents
/sc:help --shannon modes
/sc:help --shannon hooks

# Search commands by keyword
/sc:help search "specification analysis"
/sc:help search "wave orchestration"

# Quick reference card
/sc:help --quick

# Integration patterns
/sc:help --patterns
/sc:help --examples [command]

# Flag reference
/sc:help --flags
/sc:help --flags [command]
```

## Command Categories

### Shannon V3 Core Commands
- `/sc:analyze-spec` - Specification analysis and complexity scoring
- `/sc:plan-phase` - Phase planning with validation gates
- `/sc:wave-execute` - Parallel wave orchestration
- `/sc:suggest-mcps` - Dynamic MCP server recommendations

### Enhanced SuperClaude Commands (25)
- **Development**: build, implement, design
- **Analysis**: analyze, troubleshoot, explain
- **Quality**: improve, cleanup, test
- **Session**: load, save, index
- **Git**: git operations and workflows
- **Documentation**: document
- **Planning**: workflow, estimate, task
- **Meta**: spawn, help

### Session Management
- `/sc:load` - Project context loading with checkpoint restoration
- `/sc:save` - Context preservation with Serena integration
- `/sc:index` - Command catalog browsing

### Specialized Operations
- `/sc:business-panel` - Multi-expert business analysis
- `/sc:research` - Deep research investigations
- `/sc:git` - Git workflow assistance

## Shannon Documentation Access

### Component Reference
```bash
# Agent documentation
/sc:help --shannon agents
# Output: List of 19 Shannon agents (5 new + 14 enhanced)

# Mode documentation
/sc:help --shannon modes
# Output: 9 operational modes with activation patterns

# Hook documentation
/sc:help --shannon hooks
# Output: Hook system with PreCompact focus

# MCP integration
/sc:help --shannon mcps
# Output: MCP coordination patterns and fallback chains
```

### Specification Access
```bash
# Full Shannon V3 specification
/sc:help --shannon spec

# Architecture overview
/sc:help --shannon architecture

# Installation guide
/sc:help --shannon install

# Testing philosophy
/sc:help --shannon testing
```

## Execution Flow

### Basic Help Request
1. **Input Processing**: Parse help query and parameters
2. **Context Analysis**: Identify current task and project state
3. **Relevance Scoring**: Rank commands by relevance to context
4. **Documentation Retrieval**: Access command definitions and examples
5. **Format Output**: Present organized, actionable help content

### Command-Specific Help
1. **Command Lookup**: Find command definition in Commands/ directory
2. **Read Metadata**: Parse YAML frontmatter for command details
3. **Extract Documentation**: Pull purpose, usage, examples
4. **Related Commands**: Suggest complementary commands
5. **Present Help**: Formatted output with examples and flags

### Shannon Documentation
1. **Component Identification**: Determine requested Shannon component
2. **File Access**: Read from Shannon/ directory structure
3. **Context7 Integration**: Access curated Shannon patterns if available
4. **Format Content**: Present with syntax highlighting and structure
5. **Related Links**: Suggest related documentation sections

## Output Format

### General Help Output
```markdown
# Shannon V3 / SuperClaude Command Reference

## Shannon Core Commands (4)
🔍 /sc:analyze-spec - Automatic specification analysis
📋 /sc:plan-phase - Structured phase planning
🌊 /sc:wave-execute - Parallel wave orchestration
🔌 /sc:suggest-mcps - Dynamic MCP recommendations

## Enhanced SuperClaude Commands (25)
**Development**
  /build - Project builder with framework detection
  /implement - Feature implementation with persona activation
  /design - Design orchestration

**Analysis**
  /analyze - Multi-dimensional analysis
  /troubleshoot - Problem investigation
  /explain - Educational explanations

**Quality**
  /improve - Code enhancement
  /cleanup - Technical debt reduction
  /test - Testing workflows

**Session Management**
  /sc:load - Enhanced project loading
  /sc:save - Context preservation

[Additional categories...]

Type `/sc:help [command]` for detailed command help
Type `/sc:help --shannon` for Shannon documentation
Type `/sc:help --quick` for quick reference card
```

### Command-Specific Help Output
```markdown
# /sc:analyze-spec - Specification Analysis

**Purpose**: Automatic specification analysis with 8-dimensional complexity scoring

**Usage**:
  /sc:analyze-spec @spec.md
  /sc:analyze-spec @requirements/ --comprehensive

**Complexity Assessment**:
  - Technical complexity (0-1 scale)
  - Domain complexity
  - Testing complexity
  - Integration complexity

**Output**: Structured analysis with MCP suggestions

**Related Commands**:
  - /sc:plan-phase - Use analysis results for planning
  - /sc:suggest-mcps - Get MCP recommendations
  - /sc:wave-execute - Execute based on plan

**Examples**:
  [Detailed examples with expected output]
```

### Quick Reference Card
```markdown
# Shannon V3 Quick Reference

## Essential Commands
/sc:analyze-spec @file - Analyze specification
/sc:plan-phase [template] - Create phase plan
/sc:wave-execute @plan - Execute with waves
/sc:load - Load project context
/sc:save - Save session state

## Key Flags
--shannon - Shannon-specific features
--waves - Enable wave orchestration
--restore - Restore checkpoint
--comprehensive - Deep analysis

## Emergency Commands
/sc:load --restore - Recover from compact
/sc:help --shannon hooks - PreCompact guide
```

## Integration with SuperClaude

### Persona Coordination
- **Primary**: Mentor persona for educational guidance
- **Secondary**: Analyzer for command discovery and context analysis
- **Context-Aware**: Suggestions based on active persona and current task

### MCP Server Integration
- **Context7**: Access to Shannon documentation patterns and framework guides
- **Sequential**: Complex help query reasoning for multi-part questions
- **Fallback**: Native Claude knowledge when external docs unavailable

### Tool Orchestration
- **Read**: Access command definition files from Shannon/Commands/
- **Grep**: Search across documentation for keywords
- **Glob**: Find relevant documentation files
- **Context7**: Retrieve curated Shannon patterns and examples

## Examples

### Example 1: First-Time User
```bash
User: /sc:help
Output:
  # Shannon V3 Command Overview
  Shannon enhances SuperClaude with systematic intelligence...

  **Get Started**:
  1. /sc:analyze-spec @your-spec.md - Analyze requirements
  2. /sc:plan-phase - Create implementation plan
  3. /sc:wave-execute - Execute with parallel waves

  Type `/sc:help --shannon` for Shannon documentation
```

### Example 2: Command Discovery
```bash
User: /sc:help search "analyze requirements"
Output:
  # Matching Commands

  🔍 /sc:analyze-spec - Automatic specification analysis
  📊 /analyze - Multi-dimensional code analysis
  🔍 /troubleshoot - Problem investigation

  **Best match**: /sc:analyze-spec
  **Usage**: /sc:analyze-spec @requirements.md
```

### Example 3: Shannon Documentation
```bash
User: /sc:help --shannon agents
Output:
  # Shannon V3 Sub-Agent System

  **New Shannon Agents (5)**:
  - spec-analyzer-agent - Specification analysis
  - phase-planner-agent - Phase planning
  - wave-orchestrator-agent - Wave coordination
  - testing-philosopher-agent - Testing strategy
  - mcp-discoverer-agent - MCP suggestions

  **Enhanced SuperClaude Agents (14)**:
  - analyzer-agent - Investigation and root cause
  - architect-agent - System design
  [...]

  Type `/sc:help --shannon spec` for full specification
```

## Quality Standards

### Help Content Requirements
- **Clarity**: Clear, concise explanations without jargon
- **Completeness**: Cover all command aspects and variations
- **Examples**: Real-world usage examples with expected output
- **Context**: Explain when and why to use each command
- **Updates**: Synchronized with actual command implementations

### User Experience
- **Fast Access**: <2 second response for basic help queries
- **Progressive Disclosure**: Overview → Details → Examples
- **Search Quality**: Relevant results for keyword searches
- **Navigation**: Easy movement between related topics
- **Visual Hierarchy**: Clear structure with symbols and formatting

### Documentation Standards
- **Accuracy**: All information verified against implementations
- **Consistency**: Unified format across all command help
- **Maintenance**: Regular updates with framework changes
- **Accessibility**: Help available offline via local files
- **Discoverability**: Multiple paths to find needed information