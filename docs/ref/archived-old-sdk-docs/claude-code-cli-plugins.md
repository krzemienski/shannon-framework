# Claude Code Plugins: Complete Overview

## Core Concept
Claude Code's plugin system allows users to "extend Claude Code with custom functionality that can be shared across projects and teams." Plugins can include custom commands, agents, hooks, Skills, and MCP servers.

## Plugin Structure
A basic plugin contains:
- **Plugin manifest** (`.claude-plugin/plugin.json`) with metadata
- **Commands directory** for slash commands
- **Optional components**: agents, Skills, hooks, and MCP servers

## Installation Methods

Users can install plugins through:
1. Interactive menu via `/plugin` command
2. Direct commands like `/plugin install formatter@your-org`
3. Repository-level configuration for team adoption

## Key Management Commands
- `/plugin marketplace add` - Add plugin catalogs
- `/plugin install` - Install specific plugins
- `/plugin enable/disable` - Toggle plugins without uninstalling
- `/plugin uninstall` - Remove plugins completely

## Development Workflow
Developers can create local test marketplaces, iterate on plugin components, and share plugins through distribution channels. The documentation emphasizes testing plugins locally before sharing.

## Team Implementation
Organizations can configure plugins at the repository level through `.claude/settings.json`, enabling automatic installation when team members trust the folder.
