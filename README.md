# Shannon Framework V3

**Context Engineering Framework for Claude Code**

Shannon V3 is a markdown-based behavioral framework that enhances Claude Code with advanced orchestration, specification analysis, and wave-based execution capabilities.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Key Innovations](#key-innovations-over-superclaud)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Command Reference](#command-reference)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [Documentation](#documentation)

---

## Quick Start

```bash
# Install Shannon
pip install shannon-framework
shannon install

# Verify installation
ls ~/.claude/ | grep -E "(SPEC_ANALYSIS|PHASE_PLANNING|WAVE_ORCHESTRATION)"

# Use Shannon commands
/sh:analyze-spec @requirements.md
/sh:create-waves --count 3 --strategy progressive
```

**First-Time Usage**:
1. Start with `/sh:analyze-spec` to understand project complexity
2. Use `/sh:create-waves` to generate execution plan
3. Let Claude execute waves automatically
4. Use `/sh:checkpoint` before risky operations

---

## Architecture

Shannon is **NOT** a Python execution framework. It is a **context engineering system** that:

1. **Behavioral Programming**: Markdown files containing instructions Claude follows
2. **System Prompt Injection**: Claude Code reads .md files and follows behavioral patterns
3. **Python Installer**: Copies markdown files to `~/.claude/` for Claude Code to discover
4. **No Code Execution**: Framework configures behavior, doesn't execute code

### Directory Structure

```
Shannon/
├── Core/           # 8 core behavioral pattern files
│   ├── SPEC_ANALYSIS.md           # 8-dimensional complexity analysis
│   ├── PHASE_PLANNING.md          # 5-phase planning framework
│   ├── WAVE_ORCHESTRATION.md      # Parallel execution system
│   ├── CONTEXT_PRESERVATION.md    # Checkpoint/restore system
│   ├── TESTING_PATTERNS.md        # NO MOCKS testing mandate
│   ├── MCP_DISCOVERY.md           # Dynamic MCP suggestions
│   ├── SHANNON_INTEGRATION.md     # SuperClaude coordination
│   └── QUALITY_GATES.md           # Validation framework
│
├── Agents/         # 19 sub-agent definitions
│   ├── spec_analyzer_agent.md     # NEW: Spec analysis specialist
│   ├── wave_coordinator_agent.md  # NEW: Wave orchestration
│   ├── context_manager_agent.md   # NEW: Context preservation
│   ├── testing_enforcer_agent.md  # NEW: Testing compliance
│   ├── mcp_discovery_agent.md     # NEW: MCP recommendations
│   └── [14 enhanced SuperClaude agents]
│
├── Commands/       # 29 commands (4 new /sh: + 25 enhanced /sc:)
│   ├── sh_analyze_spec.md         # NEW: Spec analysis command
│   ├── sh_create_waves.md         # NEW: Wave generation
│   ├── sh_checkpoint.md           # NEW: Manual checkpoint
│   ├── sh_restore.md              # NEW: Restore from checkpoint
│   └── [25 enhanced /sc: commands]
│
├── Modes/          # 9 modes (2 new + 7 from SuperClaude)
│   ├── MODE_WaveOrchestration.md  # NEW: Multi-wave execution
│   ├── MODE_SpecAnalysis.md       # NEW: Deep spec analysis
│   └── [7 SuperClaude modes]
│
└── Hooks/          # 1 critical PreCompact hook
    └── pre_compact_hook.py        # Checkpoint/restore automation
```

### Component Overview

**8 Core Files**: Behavioral patterns defining Shannon's operation
**19 Agents**: Specialized sub-agents for targeted operations
**29 Commands**: 4 Shannon-specific + 25 enhanced SuperClaude commands
**9 Modes**: 2 Shannon-specific + 7 inherited from SuperClaude
**1 Hook**: PreCompact hook for automatic context preservation

---

## Key Innovations Over SuperClaude

### 1. 8-Dimensional Spec Analysis
Automatic complexity scoring across:
- Technical complexity
- Functional scope
- Integration requirements
- Testing needs
- Documentation requirements
- Architecture decisions
- Risk factors
- Timeline considerations

### 2. 5-Phase Planning Framework
Structured planning with validation gates:
1. **Discovery**: Requirements gathering and clarification
2. **Analysis**: Complexity assessment and feasibility
3. **Design**: Architecture and technical approach
4. **Planning**: Wave strategy and resource allocation
5. **Validation**: Plan review and approval gates

### 3. Wave Orchestration
Parallel sub-agent execution with:
- Independent wave execution
- Context sharing via Serena MCP
- Cross-wave learning and adaptation
- Progressive enhancement strategies
- Automatic checkpoint/restore

### 4. PreCompact Hook
Prevents context loss through:
- Automatic checkpoint creation before compaction
- State preservation with Serena MCP
- Seamless restoration after compaction
- No user intervention required

### 5. NO MOCKS Testing Mandate
Functional testing requirements:
- Puppeteer for web UI testing
- iOS simulator for mobile testing
- Real backend integration
- No mock objects or stub data
- Production-like test environments

### 6. Dynamic MCP Discovery
Suggests 6-15 MCPs based on:
- Domain analysis (frontend, backend, testing, etc.)
- Complexity requirements
- Project technology stack
- Testing needs
- Documentation requirements

### 7. Cross-Wave Context
All agents access previous wave results:
- Shared context via Serena memory
- Learning from previous waves
- Avoiding duplicate work
- Progressive refinement

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Claude Code CLI installed
- Git (for development installation)

### Standard Installation

```bash
# Install from PyPI
pip install shannon-framework

# Install Shannon files to ~/.claude/
shannon install

# Verify installation
shannon verify
```

### Development Installation

```bash
# Clone repository
git clone https://github.com/yourusername/shannon.git
cd shannon

# Install in development mode
pip install -e .

# Install Shannon files
shannon install --dev

# Run tests
pytest tests/
```

### Configuration

Shannon uses `~/.claude/` as its deployment target. Claude Code automatically discovers and loads all `.md` files from this directory.

**File Locations**:
- Core files: `~/.claude/Core/`
- Agent definitions: `~/.claude/Agents/`
- Command implementations: `~/.claude/Commands/`
- Mode definitions: `~/.claude/Modes/`
- PreCompact hook: `~/.claude/Hooks/pre_compact_hook.py`

---

## Usage Examples

### Example 1: Analyzing a Specification

```bash
# Analyze requirements document
/sh:analyze-spec @requirements.md

# Output includes:
# - Complexity scores (0.0-1.0) across 8 dimensions
# - Recommended wave count (1-5)
# - Suggested MCP servers (6-15)
# - Risk assessment
# - Timeline estimate
```

### Example 2: Creating Wave Execution Plan

```bash
# Generate waves with progressive strategy
/sh:create-waves --count 3 --strategy progressive

# Wave 1: Core implementation
# Wave 2: Integration and testing
# Wave 3: Polish and documentation

# Claude executes waves automatically with checkpoints
```

### Example 3: Manual Context Preservation

```bash
# Before risky refactoring
/sh:checkpoint "pre-refactoring state"

# Perform refactoring
/sc:refactor @src/ --aggressive

# If issues occur, restore
/sh:restore "pre-refactoring state"
```

### Example 4: Complete Project Workflow

```bash
# Step 1: Analyze specification
/sh:analyze-spec @product_spec.md

# Step 2: Create execution plan
/sh:create-waves --count 4 --strategy systematic

# Step 3: Execute waves (automatic)
# Claude runs each wave with:
# - Checkpoint before wave
# - Parallel sub-agent execution
# - Context sharing via Serena
# - Restore if errors occur

# Step 4: Validate results
/sc:test --coverage --e2e
```

### Example 5: Testing Workflow

```bash
# Shannon enforces NO MOCKS testing
/sc:test --mode e2e

# Automatically uses:
# - Puppeteer for web UI
# - iOS simulator for mobile
# - Real backend services
# - Production-like environment
```

---

## Command Reference

### Shannon Commands (`/sh:`)

**`/sh:analyze-spec @<spec-file>`**
- 8-dimensional complexity analysis
- Recommends wave count and strategy
- Suggests relevant MCP servers
- Provides risk assessment and timeline

**`/sh:create-waves [options]`**
- Generates wave execution plan
- Options:
  - `--count N`: Number of waves (1-5)
  - `--strategy <type>`: progressive|systematic|adaptive
  - `--validate`: Show plan for approval
  - `--auto`: Execute immediately

**`/sh:checkpoint <name>`**
- Manual context preservation
- Saves state to Serena MCP
- Enables rollback capability
- Use before risky operations

**`/sh:restore <name>`**
- Restore from checkpoint
- Loads saved state from Serena
- Recovers from failed operations
- Maintains work continuity

### Enhanced SuperClaude Commands (`/sc:`)

Shannon enhances 25 existing SuperClaude commands with:
- Automatic spec analysis integration
- Wave orchestration support
- Context preservation hooks
- Testing compliance enforcement

**Key Enhanced Commands**:
- `/sc:implement` - Wave-aware implementation
- `/sc:test` - NO MOCKS enforcement
- `/sc:refactor` - Automatic checkpointing
- `/sc:analyze` - Spec analysis integration
- `/sc:build` - Wave coordination

See [Commands/](Commands/) directory for detailed documentation.

---

## Development

### Project Structure

```
shannon/
├── setup/              # Installation scripts
│   ├── __init__.py
│   ├── installer.py    # Shannon installer
│   └── verifier.py     # Installation verification
│
├── tests/              # Test suite
│   ├── test_core/      # Core functionality tests
│   ├── test_agents/    # Agent behavior tests
│   ├── test_commands/  # Command execution tests
│   └── test_integration/ # End-to-end tests
│
├── Core/               # Core behavioral files
├── Agents/             # Agent definitions
├── Commands/           # Command implementations
├── Modes/              # Mode definitions
└── Hooks/              # PreCompact hook
```

### Building Shannon

```bash
# Clone repository
git clone https://github.com/yourusername/shannon.git
cd shannon

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Install Shannon files
shannon install --dev
```

### Code Standards

- **Markdown Formatting**: Follow consistent header hierarchy
- **YAML Frontmatter**: All files include metadata
- **Cross-References**: Use relative paths for internal links
- **Validation**: Run `shannon verify` before committing
- **Testing**: Ensure all tests pass with `pytest`

---

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_core/
pytest tests/test_agents/
pytest tests/test_commands/

# Run with coverage
pytest --cov=shannon tests/

# Run integration tests
pytest tests/test_integration/ -v
```

### Test Categories

**1. Core Functionality Tests**
- Spec analysis accuracy
- Wave generation logic
- Context preservation
- MCP discovery suggestions

**2. Agent Behavior Tests**
- Agent activation triggers
- Sub-agent coordination
- Context sharing verification
- Cross-wave learning

**3. Command Execution Tests**
- Command parsing and validation
- Option handling
- Error recovery
- Integration with SuperClaude

**4. Integration Tests**
- End-to-end workflows
- Multi-wave execution
- Checkpoint/restore cycles
- Real MCP interaction

### NO MOCKS Philosophy

Shannon mandates functional testing:
- **Web UI**: Use Puppeteer for real browser testing
- **Mobile**: Use iOS simulator for actual device testing
- **Backend**: Test against real services, not mocks
- **Integration**: Full stack testing with real dependencies

---

## Contributing

### How to Contribute

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/your-feature`
3. **Commit changes**: `git commit -m "Add your feature"`
4. **Push to branch**: `git push origin feature/your-feature`
5. **Submit pull request**

### Contribution Guidelines

**Code Contributions**:
- Follow existing markdown structure
- Include YAML frontmatter in all files
- Add tests for new functionality
- Update documentation

**Documentation Contributions**:
- Clear, concise writing
- Include usage examples
- Update relevant README sections
- Maintain consistent formatting

**Bug Reports**:
- Use GitHub Issues
- Include reproduction steps
- Provide system information
- Attach relevant logs

**Feature Requests**:
- Open GitHub Discussion first
- Describe use case and benefits
- Consider backward compatibility
- Propose implementation approach

### Development Workflow

1. **Discovery**: Discuss feature/fix in GitHub Issues or Discussions
2. **Planning**: Design approach and get feedback
3. **Implementation**: Write code/markdown with tests
4. **Testing**: Ensure all tests pass
5. **Documentation**: Update README and relevant docs
6. **Review**: Submit PR and address feedback
7. **Merge**: Maintainers merge approved PRs

---

## Documentation

### Core Documentation

- **[SHANNON_V3_SPECIFICATION.md](SHANNON_V3_SPECIFICATION.md)**: Complete technical specification
- **[Core/](Core/)**: Behavioral pattern documentation
- **[Agents/](Agents/)**: Sub-agent definitions and behaviors
- **[Commands/](Commands/)**: Command reference and usage
- **[Modes/](Modes/)**: Operational mode documentation
- **[Hooks/](Hooks/)**: PreCompact hook implementation

### Additional Resources

- **[CHANGELOG.md](CHANGELOG.md)**: Version history and updates
- **[MIGRATION.md](MIGRATION.md)**: SuperClaude → Shannon migration guide
- **[EXAMPLES.md](EXAMPLES.md)**: Comprehensive usage examples
- **[FAQ.md](FAQ.md)**: Frequently asked questions

---

## Current Status

**Version**: 3.0.0
**Stage**: Production Ready
**Branch**: master
**Specification**: SHANNON_V3_SPECIFICATION.md (approved)

### Environment Details

- **Agent CWD**: `/Users/nick/Documents/shannon`
- **Codebase Directory**: `/Users/nick/Documents/shannon`
- **Deployment Target**: `~/.claude/` (Claude Code reads from here)

### License

MIT License - See [LICENSE](LICENSE) for details

### Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/shannon/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/shannon/discussions)
- **Email**: support@shannon-framework.dev

---

**Shannon V3** - Context Engineering for Claude Code