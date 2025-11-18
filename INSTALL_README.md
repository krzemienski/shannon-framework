# Shannon Framework - Installation Quick Guide

## One-Command Installation

```bash
./install_universal.sh
```

That's it! This installs Shannon Framework for both Claude Code and Cursor IDE.

---

## What You Get

### Claude Code
- ✅ 19 commands (`/shannon:do`, `/shannon:spec`, `/shannon:wave`, etc.)
- ✅ 17 skills (auto-loaded at session start)
- ✅ 24 agents (referenced by commands/skills)
- ✅ 5 hooks (automatic workflow enforcement)
- ✅ Complete integration with plugin system

**Usage**: `/shannon:status` to verify

### Cursor IDE
- ✅ 19 commands in `~/.cursor/commands/` (referenceable in Chat)
- ✅ 7 VS Code tasks (Cmd+Shift+P → "Tasks: Run Task")
- ✅ Global rules file (2000+ lines of Shannon methodology)
- ✅ Settings safely merged (your config preserved!)
- ✅ Quick start guide

**Usage**: Cmd+Shift+P → "Tasks: Run Task" → Select "Shannon:" task

---

## Installation Options

### Both Platforms (Recommended)
```bash
./install_universal.sh
```

### Cursor Only
```bash
./install_universal.sh --cursor
```

### Claude Code Only
```bash
./install_universal.sh --claude
# or
./install_local.sh
```

### Update Existing Installation
```bash
./install_universal.sh --update
```

### Remove Installation
```bash
./install_universal.sh --uninstall
```

---

## Safety Features

✅ **Automatic Backups**: All configuration files backed up before changes
✅ **Safe Merge**: Never overwrites your Cursor settings (merges safely)
✅ **Plugin Detection**: Automatically finds and removes conflicting plugin installations
✅ **Verification**: Checks installation integrity before completing
✅ **Rollback**: Uninstall mode cleanly removes everything

---

## After Installation

### Claude Code

1. **Restart Claude Code**
2. Verify:
   ```
   /shannon:status
   ```
3. Start using:
   ```
   /shannon:prime
   /shannon:spec "Build a task manager app"
   ```

### Cursor IDE

1. **Restart Cursor**
2. Verify commands:
   ```bash
   ls ~/.cursor/commands/
   ```
3. Access tasks:
   ```
   Cmd+Shift+P → "Tasks: Run Task"
   ```
4. Use in Chat:
   ```
   "Analyze this specification using Shannon Framework 8D complexity scoring:
   [paste your specification]"
   ```

---

## Troubleshooting

### Commands Not Found (Claude Code)
```bash
# Verify installation
ls ~/.claude/commands/shannon/

# If empty, re-run:
./install_universal.sh --claude --update
```

### Commands Not Found (Cursor)
```bash
# Verify installation
ls ~/.cursor/commands/

# If empty, re-run:
./install_universal.sh --cursor --update
```

### Settings Not Merged (Cursor)
```bash
# Check if Shannon settings present
grep "cursor.shannon" ~/Library/Application\ Support/Cursor/User/settings.json

# If not found, check for separate file
ls ~/Library/Application\ Support/Cursor/User/shannon_settings.json

# Manual merge if separate file exists (follow instructions in terminal)
```

### Hooks Not Firing (Claude Code)
```bash
# Check hooks installed
ls -l ~/.claude/hooks/shannon/

# Check hooks.json configured
cat ~/.claude/hooks.json

# If issues, reinstall:
./install_local.sh --update
```

---

## Documentation

**Quick Start**:
- This file (INSTALL_README.md)

**Complete Guides**:
- Universal Installation: INSTALL_UNIVERSAL.md
- Local Installation (Claude Code): INSTALL_LOCAL.md

**Technical Details**:
- Bug Fixes: CRITICAL_FIXES_v2.md
- Implementation: INSTALLATION_SYSTEM_FINAL.md

**Log Files**:
- Claude Code: `~/.claude/shannon_install.log`
- Universal: `~/.shannon_install.log`

---

## Quick Commands Reference

### Installation
```bash
./install_universal.sh              # Install both
./install_universal.sh --cursor     # Cursor only
./install_universal.sh --claude     # Claude Code only
```

### Update
```bash
cd shannon-framework
git pull
./install_universal.sh --update
```

### Uninstall
```bash
./install_universal.sh --uninstall
```

### Test
```bash
./test_universal_install.sh   # Test before installing
./test_install.sh             # Test Claude sources
```

### Help
```bash
./install_universal.sh --help
```

---

## What's Installed Where

### Claude Code Locations
```
~/.claude/
├── skills/shannon/
├── commands/shannon/
├── agents/shannon/
├── core/shannon/
├── modes/shannon/
├── templates/shannon/
├── hooks/shannon/
└── hooks.json
```

### Cursor Locations
```
~/.cursor/
├── commands/              (19 Shannon commands)
├── .vscode/tasks.json     (7 Shannon tasks)
├── shannon/               (Reference docs)
├── global.cursorrules     (Methodology)

~/Library/Application Support/Cursor/User/  (macOS)
└── settings.json          (Shannon config merged)

~/.config/Cursor/User/     (Linux)
└── settings.json          (Shannon config merged)
```

---

## Support

**Issues**: https://github.com/shannon-framework/shannon/issues

**Questions**: Review documentation files listed above

**Installation Problems**: Check log files:
- `~/.shannon_install.log`
- `~/.claude/shannon_install.log`

---

## Version

**Shannon Framework**: v5.0.0
**Installation System**: v1.0.0 (Production)
**Last Updated**: 2025-11-18

---

**Get started now**: `./install_universal.sh` 🚀

