# Shannon Framework Plugin

> Specification-driven development framework for Claude Code featuring 8-dimensional complexity analysis, wave orchestration, and NO MOCKS testing.

## ✨ Key Features

### 🎯 8-Dimensional Complexity Analysis
Quantitative specification analysis across structural, cognitive, coordination, temporal, technical, scale, uncertainty, and dependency dimensions.

### 🌊 Wave Orchestration
Multi-stage execution with compound intelligence and parallel sub-agent coordination for complex projects.

### 💾 Context Preservation
Automatic checkpointing via Serena MCP prevents information loss during auto-compaction and enables seamless session resumption.

### 🚫 NO MOCKS Testing
Enforced functional testing with real browsers (Playwright), real devices (iOS Simulator), and real databases.

### 📊 Domain Intelligence
Automatic domain detection (frontend, backend, database, mobile, devops, security) with percentage quantification and appropriate MCP server recommendations.

### 📋 5-Phase Planning
Structured implementation planning with validation gates, resource allocation, and timeline estimation.

## 🚀 Quick Start

### Prerequisites
- Claude Code v1.0.0 or higher
- Serena MCP server configured (required)

### Installation

1. **Add Shannon Marketplace**
   ```bash
   /plugin marketplace add shannon-framework/shannon
   ```

2. **Install Shannon Plugin**
   ```bash
   /plugin install shannon@shannon-framework
   ```

3. **Restart Claude Code**
   Required to load the plugin

4. **Verify Installation**
   ```bash
   /sh_status
   ```

5. **Configure MCP Servers** (if needed)
   ```bash
   /sh_check_mcps
   ```
   Follow the instructions to configure required MCPs.

### First Steps

Try Shannon's specification analysis:
```bash
/sh_spec "Build a task management web application with React frontend, Node.js backend, and PostgreSQL database"
```

You'll see:
- 8-dimensional complexity analysis
- Domain breakdown with percentages
- MCP server recommendations
- 5-phase implementation plan
- Comprehensive todo list (20-50 items)
- Timeline estimation with buffers

## 📚 Commands

### Shannon Commands (9)
- `/sh_spec` - Specification analysis with 8D complexity scoring
- `/sh_checkpoint` - Save session context to Serena MCP
- `/sh_restore` - Restore previous session context
- `/sh_status` - Framework status and health check
- `/sh_check_mcps` - MCP server verification and setup guidance
- `/sh_analyze` - Shannon-specific analysis workflows
- `/sh_memory` - Memory coordination tracking
- `/sh_north_star` - North Star goal management
- `/sh_wave` - Wave-based planning and execution

### Enhanced SuperClaude Commands (24)
Shannon enhances SuperClaude commands with wave orchestration, Serena integration, and structured patterns:
- `/sc_analyze`, `/sc_implement`, `/sc_build`, `/sc_test` - and 20 more enhanced commands

Run `/help` to see all available commands.

## 🤖 Agents

### Shannon Agents (5)
- **SPEC_ANALYZER** - 8D complexity scoring
- **PHASE_ARCHITECT** - 5-phase planning
- **WAVE_COORDINATOR** - Multi-stage orchestration
- **CONTEXT_GUARDIAN** - Context preservation
- **TEST_GUARDIAN** - NO MOCKS enforcement

### Enhanced SuperClaude Agents (14)
- **ANALYZER**, **ARCHITECT**, **FRONTEND**, **BACKEND**, **PERFORMANCE**, **SECURITY**, **QA**, **REFACTORER**, **DEVOPS**, **MENTOR**, **SCRIBE**, **DATA_ENGINEER**, **MOBILE_DEVELOPER**, **IMPLEMENTATION_WORKER**

Run `/agents` to see detailed agent capabilities.

## 🔌 MCP Requirements

### Required
- **Serena MCP** - Context preservation and checkpoint/restore functionality

### Recommended
- **Sequential MCP** - Complex multi-step reasoning and analysis
- **Context7 MCP** - Official framework patterns and documentation
- **Puppeteer MCP** - Real browser testing for NO MOCKS philosophy

### Conditional
- **shadcn-ui MCP** - Required for React/Next.js projects (Shannon enforces shadcn for React UI)

Run `/sh_check_mcps` for detailed setup instructions.

## 📖 Documentation

- **[Installation Guide](../../docs/PLUGIN_INSTALL.md)** - Detailed installation instructions
- **[Commands Reference](../../SHANNON_COMMANDS_GUIDE.md)** - Complete command documentation
- **[V3 Specification](../../SHANNON_V3_SPECIFICATION.md)** - Technical architecture details
- **[Migration Guide](../../docs/MIGRATION_GUIDE.md)** - Upgrade from legacy CLAUDE.md system
- **[Team Setup](../../docs/TEAM_SETUP.md)** - Team and enterprise configuration

## 🏗️ Plugin Structure

```
shannon-plugin/
├── .claude-plugin/
│   └── plugin.json        # Plugin manifest
├── commands/               # 33 slash commands
├── agents/                 # 19 specialized agents
├── hooks/                  # PreCompact context preservation
├── core/                   # Behavioral patterns (reference docs)
├── modes/                  # Execution modes (reference docs)
└── README.md              # This file
```

## 🤝 Contributing

Shannon Framework is open source. Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

See repository root for full contribution guidelines.

## 📜 License

MIT License - See LICENSE file for details

## 🔗 Links

- **Repository**: https://github.com/shannon-framework/shannon
- **Documentation**: https://github.com/shannon-framework/shannon#readme
- **Issues**: https://github.com/shannon-framework/shannon/issues
- **Changelog**: https://github.com/shannon-framework/shannon/blob/main/CHANGELOG.md

---

**Shannon Framework v3.0.0** - Specification-driven development for Claude Code
