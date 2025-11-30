# Shannon Framework v5.6 - Installation System Audit

**Version**: 5.6.0  
**Last Updated**: November 29, 2025  

---

## Overview

This document provides a complete audit of Shannon Framework's installation system, including scripts, flow, and verification.

---

## Installation Scripts Inventory

| Script | Purpose | Lines | Status |
|--------|---------|-------|--------|
| install_local.sh | Install to ~/.claude/ | ~400 | ✅ |
| install_universal.sh | Install for Claude + Cursor | ~200 | ✅ |
| test_install.sh | Verify installation | ~100 | ✅ |
| test_universal_install.sh | Verify universal install | ~100 | ✅ |

---

## 1. Local Installation (install_local.sh)

### 1.1 Script Purpose

Installs Shannon Framework directly to `~/.claude/` directory structure, bypassing the plugin marketplace for more reliable discovery.

### 1.2 Command Line Options

| Option | Description |
|--------|-------------|
| `--install` | Fresh installation |
| `--update` | Update existing installation |
| `--uninstall` | Remove installation |
| `--help` | Show usage information |

### 1.3 Installation Flow

```
┌────────────────────────────────────────────────────────────┐
│                  INSTALLATION FLOW                          │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  1. PLUGIN DETECTION                                        │
│     ├── Check ~/.claude/plugins/shannon                     │
│     ├── If exists: offer removal                            │
│     └── If removed: proceed to step 2                       │
│                                                             │
│  2. DIRECTORY CREATION                                      │
│     ├── ~/.claude/skills/shannon/                           │
│     ├── ~/.claude/commands/shannon/                         │
│     ├── ~/.claude/agents/shannon/                           │
│     ├── ~/.claude/core/shannon/                             │
│     ├── ~/.claude/modes/shannon/                            │
│     ├── ~/.claude/templates/shannon/                        │
│     └── ~/.claude/hooks/shannon/                            │
│                                                             │
│  3. CONTENT INSTALLATION                                    │
│     ├── Copy 42 skills                                      │
│     ├── Copy 23 commands                                    │
│     ├── Copy 24 agents                                      │
│     ├── Copy 10 core files                                  │
│     ├── Copy 2 modes                                        │
│     ├── Copy 1 template                                     │
│     └── Copy 9 hooks                                        │
│                                                             │
│  4. PATH REFERENCE UPDATES                                  │
│     ├── Replace 'shannon-plugin/' with '~/.claude/'         │
│     ├── Update all internal references                      │
│     └── Update hooks.json paths                             │
│                                                             │
│  5. HOOK CONFIGURATION                                      │
│     ├── Create ~/.claude/hooks.json                         │
│     ├── Make hooks executable                               │
│     ├── Embed using-shannon in session_start.sh             │
│     └── Configure hook timeouts                             │
│                                                             │
│  6. VERIFICATION                                            │
│     ├── Check all directories populated                     │
│     ├── Verify hook scripts executable                      │
│     ├── Validate hooks.json structure                       │
│     └── Count installed components                          │
│                                                             │
│  7. POST-INSTALL                                            │
│     ├── Display success message                             │
│     ├── Show restart instructions                           │
│     ├── List verification commands                          │
│     └── Log installation details                            │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### 1.4 Key Code Sections

#### Plugin Detection
```bash
check_plugin() {
    PLUGIN_DIR="${HOME}/.claude/plugins/shannon"
    if [[ -d "${PLUGIN_DIR}" ]]; then
        print_warning "Shannon plugin detected at ${PLUGIN_DIR}"
        print_info "Local installation conflicts with plugin installation."
        read -p "Remove plugin installation? (y/n): " -n 1 -r
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "${PLUGIN_DIR}"
            print_success "Plugin removed"
        else
            print_error "Cannot proceed with plugin installed"
            exit 1
        fi
    fi
}
```

#### Directory Creation
```bash
create_directories() {
    local dirs=(
        "${CLAUDE_DIR}/skills/shannon"
        "${CLAUDE_DIR}/commands/shannon"
        "${CLAUDE_DIR}/agents/shannon"
        "${CLAUDE_DIR}/core/shannon"
        "${CLAUDE_DIR}/modes/shannon"
        "${CLAUDE_DIR}/templates/shannon"
        "${HOOKS_DIR}"
    )
    
    for dir in "${dirs[@]}"; do
        mkdir -p "${dir}"
        print_success "Created ${dir}"
    done
}
```

#### Skill Installation
```bash
install_skills() {
    print_info "Installing skills..."
    
    for skill_dir in "${SHANNON_ROOT}/skills/"*/; do
        skill_name=$(basename "${skill_dir}")
        target_dir="${SKILLS_DIR}/${skill_name}"
        
        mkdir -p "${target_dir}"
        cp -r "${skill_dir}"* "${target_dir}/"
        
        # Update path references
        find "${target_dir}" -type f -name "*.md" -exec \
            sed -i.bak "s|shannon-plugin/|${HOME}/.claude/|g" {} \;
        
        print_success "  Installed skill: ${skill_name}"
    done
}
```

#### Hook Installation with Embedded using-shannon
```bash
install_hooks() {
    print_info "Installing hooks..."
    
    # Copy Python hooks
    cp "${SHANNON_ROOT}/hooks/precompact.py" "${HOOKS_DIR}/"
    cp "${SHANNON_ROOT}/hooks/post_tool_use.py" "${HOOKS_DIR}/"
    cp "${SHANNON_ROOT}/hooks/stop.py" "${HOOKS_DIR}/"
    cp "${SHANNON_ROOT}/hooks/user_prompt_submit.py" "${HOOKS_DIR}/"
    
    # Create session_start.sh with EMBEDDED using-shannon content
    print_info "  Creating session_start.sh with embedded using-shannon..."
    
    cat > "${HOOKS_DIR}/session_start.sh" << 'HOOK_HEADER'
#!/bin/bash
# Shannon Framework V5 - SessionStart Hook
# Loads using-shannon meta-skill to establish Shannon workflows

echo "<EXTREMELY_IMPORTANT>"
echo "You are using Shannon Framework V5."
echo ""
echo "**The content below is the using-shannon skill:**"
echo ""
cat << 'SKILL_EOF'
HOOK_HEADER

    # Embed actual using-shannon content
    cat "${SHANNON_ROOT}/skills/using-shannon/SKILL.md" >> "${HOOKS_DIR}/session_start.sh"
    
    cat >> "${HOOKS_DIR}/session_start.sh" << 'HOOK_FOOTER'
SKILL_EOF
echo ""
echo "</EXTREMELY_IMPORTANT>"
HOOK_FOOTER

    # Make all hooks executable
    chmod +x "${HOOKS_DIR}"/*.py
    chmod +x "${HOOKS_DIR}"/*.sh
    
    print_success "  Hooks installed and made executable"
}
```

### 1.5 Installed Component Paths

| Component | Source | Destination |
|-----------|--------|-------------|
| Skills | `skills/*` | `~/.claude/skills/shannon/*` |
| Commands | `commands/*.md` | `~/.claude/commands/shannon/*.md` |
| Agents | `agents/*.md` | `~/.claude/agents/shannon/*.md` |
| Core | `core/*.md` | `~/.claude/core/shannon/*.md` |
| Modes | `modes/*.md` | `~/.claude/modes/shannon/*.md` |
| Templates | `templates/*.md` | `~/.claude/templates/shannon/*.md` |
| Hooks | `hooks/*` | `~/.claude/hooks/shannon/*` |
| Hook Config | Generated | `~/.claude/hooks.json` |

---

## 2. Universal Installation (install_universal.sh)

### 2.1 Script Purpose

Installs Shannon Framework for both Claude Code and Cursor IDE.

### 2.2 Platform Detection

```bash
detect_platform() {
    if command -v claude &> /dev/null; then
        HAS_CLAUDE=true
    fi
    
    if command -v cursor &> /dev/null; then
        HAS_CURSOR=true
    fi
    
    # Also check for Cursor settings directory
    if [[ -d "${HOME}/.cursor" ]]; then
        HAS_CURSOR=true
    fi
}
```

### 2.3 Claude Code Installation

For Claude Code, the universal installer calls `install_local.sh`:

```bash
install_claude_code() {
    print_info "Installing for Claude Code..."
    
    # Use local installer
    bash "${SHANNON_ROOT}/install_local.sh" --install
}
```

### 2.4 Cursor IDE Installation

For Cursor, the installer creates `.cursorrules` and updates settings:

```bash
install_cursor() {
    print_info "Installing for Cursor IDE..."
    
    CURSOR_DIR="${HOME}/.cursor"
    CURSORRULES="${HOME}/.cursorrules"
    
    # Generate .cursorrules from Shannon content
    cat > "${CURSORRULES}" << 'RULES_HEADER'
# Shannon Framework v5.6 - Cursor Integration
# Auto-generated by install_universal.sh

## Shannon Methodology

RULES_HEADER

    # Append key Shannon skills as rules
    cat "${SHANNON_ROOT}/skills/using-shannon/SKILL.md" >> "${CURSORRULES}"
    cat "${SHANNON_ROOT}/core/SPEC_ANALYSIS.md" >> "${CURSORRULES}"
    cat "${SHANNON_ROOT}/core/TESTING_PHILOSOPHY.md" >> "${CURSORRULES}"
    
    # Update Cursor settings
    update_cursor_settings
}

update_cursor_settings() {
    CURSOR_SETTINGS="${CURSOR_DIR}/settings.json"
    
    # Add Shannon-specific settings
    # - Enable project rules loading
    # - Configure recommended extensions
    # - Set up MCP server references
}
```

### 2.5 Platform Differences

| Feature | Claude Code | Cursor IDE |
|---------|-------------|------------|
| Skills | Loaded via hooks | Embedded in .cursorrules |
| Commands | ~/.claude/commands/ | N/A |
| Agents | ~/.claude/agents/ | N/A |
| Hooks | hooks.json lifecycle | N/A |
| Enforcement | Runtime hooks | Rules guidance |

---

## 3. Verification Scripts

### 3.1 test_install.sh

```bash
#!/bin/bash
# Shannon Framework - Installation Verification

verify_installation() {
    ERRORS=0
    
    # Check directories
    for dir in skills commands agents core modes templates hooks; do
        if [[ ! -d "${HOME}/.claude/${dir}/shannon" ]]; then
            print_error "Missing: ~/.claude/${dir}/shannon"
            ((ERRORS++))
        fi
    done
    
    # Check skill count
    SKILL_COUNT=$(ls -d "${HOME}/.claude/skills/shannon/"*/ 2>/dev/null | wc -l)
    if [[ ${SKILL_COUNT} -lt 40 ]]; then
        print_warning "Expected 42+ skills, found ${SKILL_COUNT}"
    fi
    
    # Check hooks executable
    for hook in precompact.py post_tool_use.py stop.py user_prompt_submit.py session_start.sh; do
        if [[ ! -x "${HOME}/.claude/hooks/shannon/${hook}" ]]; then
            print_error "Not executable: ${hook}"
            ((ERRORS++))
        fi
    done
    
    # Check hooks.json
    if [[ ! -f "${HOME}/.claude/hooks.json" ]]; then
        print_error "Missing: ~/.claude/hooks.json"
        ((ERRORS++))
    fi
    
    return ${ERRORS}
}
```

### 3.2 Verification Checklist

| Check | Command | Expected |
|-------|---------|----------|
| Skills dir | `ls ~/.claude/skills/shannon/ \| wc -l` | 42+ |
| Commands dir | `ls ~/.claude/commands/shannon/ \| wc -l` | 23 |
| Agents dir | `ls ~/.claude/agents/shannon/ \| wc -l` | 24 |
| Core dir | `ls ~/.claude/core/shannon/ \| wc -l` | 10 |
| Hooks dir | `ls ~/.claude/hooks/shannon/ \| wc -l` | 9 |
| hooks.json | `cat ~/.claude/hooks.json \| jq .hooks` | Valid JSON |
| Hook perms | `ls -l ~/.claude/hooks/shannon/*.py` | -rwx... |

---

## 4. Rollback and Uninstallation

### 4.1 Uninstall Command

```bash
./install_local.sh --uninstall
```

### 4.2 Uninstall Flow

```bash
uninstall() {
    print_warning "Uninstalling Shannon Framework..."
    
    # Remove Shannon directories
    rm -rf "${HOME}/.claude/skills/shannon"
    rm -rf "${HOME}/.claude/commands/shannon"
    rm -rf "${HOME}/.claude/agents/shannon"
    rm -rf "${HOME}/.claude/core/shannon"
    rm -rf "${HOME}/.claude/modes/shannon"
    rm -rf "${HOME}/.claude/templates/shannon"
    rm -rf "${HOME}/.claude/hooks/shannon"
    
    # Remove hooks.json if Shannon-only
    if grep -q "shannon" "${HOME}/.claude/hooks.json" 2>/dev/null; then
        # Check if other hooks exist
        if ! grep -q -v "shannon" "${HOME}/.claude/hooks.json"; then
            rm "${HOME}/.claude/hooks.json"
        fi
    fi
    
    print_success "Shannon Framework uninstalled"
}
```

### 4.3 Manual Uninstall

If automatic uninstall fails:

```bash
# Remove Shannon directories
rm -rf ~/.claude/skills/shannon
rm -rf ~/.claude/commands/shannon
rm -rf ~/.claude/agents/shannon
rm -rf ~/.claude/core/shannon
rm -rf ~/.claude/modes/shannon
rm -rf ~/.claude/templates/shannon
rm -rf ~/.claude/hooks/shannon

# Edit hooks.json to remove Shannon hooks
# or delete entirely if Shannon-only
rm ~/.claude/hooks.json

# Restart Claude Code
```

---

## 5. Troubleshooting

### 5.1 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Skills not loading | hooks.json missing | Run `--install` again |
| Hooks not firing | Not executable | `chmod +x ~/.claude/hooks/shannon/*` |
| NO MOCKS not working | post_tool_use.py missing | Verify hook installation |
| Context not saving | Serena not configured | Configure Serena MCP |
| Version conflict | Plugin and local both installed | Uninstall plugin first |

### 5.2 Diagnostic Commands

```bash
# Check installation
./install_local.sh --verify

# List installed components
tree ~/.claude/skills/shannon | head -50
tree ~/.claude/commands/shannon
tree ~/.claude/agents/shannon

# Check hooks.json
cat ~/.claude/hooks.json | jq .

# Verify hook permissions
ls -la ~/.claude/hooks/shannon/

# Check for plugin conflict
ls ~/.claude/plugins/shannon 2>/dev/null && echo "Plugin exists - conflict!"
```

### 5.3 Log File

Installation logs are written to:
```
~/.claude/shannon_install.log
```

---

## 6. Migration from Plugin Installation

### 6.1 Migration Steps

```bash
# 1. Backup existing work (if any)
cp -r ~/.claude/plugins/shannon ~/shannon_backup

# 2. Remove plugin
rm -rf ~/.claude/plugins/shannon

# 3. Remove plugin marketplace entry
# Edit ~/.claude/plugins/marketplace.json and remove shannon entry

# 4. Run local installer
./install_local.sh --install

# 5. Restart Claude Code completely
# Quit and reopen

# 6. Verify
/shannon:status
```

### 6.2 What Changes

| Aspect | Plugin Install | Local Install |
|--------|----------------|---------------|
| Location | ~/.claude/plugins/shannon/ | ~/.claude/{type}/shannon/ |
| Discovery | Via marketplace | Direct loading |
| Reliability | Sometimes flaky | More reliable |
| Updates | Marketplace refresh | Re-run installer |
| Hooks | Plugin-relative paths | Absolute paths |

---

## 7. Prerequisites

### 7.1 System Requirements

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| macOS/Linux | Any | `uname -s` |
| Bash | 4.0+ | `bash --version` |
| Claude Code | Latest | `claude --version` |
| Git | Any | `git --version` |

### 7.2 MCP Requirements

| MCP | Requirement | Purpose |
|-----|-------------|---------|
| Serena | MANDATORY | Context preservation |
| Sequential | MANDATORY | Deep reasoning |
| Context7 | RECOMMENDED | Documentation |
| Tavily | RECOMMENDED | Research |
| Puppeteer | RECOMMENDED | Browser testing |

---

**Installation Audit Complete**: November 29, 2025
