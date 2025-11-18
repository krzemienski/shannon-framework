#!/bin/bash

# Shannon Framework - Universal Installation Script
# Version: 5.4.0
# Purpose: Install Shannon Framework for both Claude Code and Cursor IDE
#          Translates components appropriately for each platform

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Script directory (Shannon Framework root)
SHANNON_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Configuration directories
CLAUDE_CONFIG_DIR="${HOME}/.claude"
CURSOR_CONFIG_DIR="${HOME}/.cursor"
CURSOR_SETTINGS_DIR="${HOME}/Library/Application Support/Cursor/User"  # macOS
CURSOR_SETTINGS_DIR_LINUX="${HOME}/.config/Cursor/User"  # Linux

# Installation targets
TARGET_PLATFORM="both"  # claude, cursor, or both
MODE="install"  # install, update, or uninstall

# Logging
LOG_FILE="${HOME}/.shannon_install.log"

# Function: Print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "${LOG_FILE}"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "${LOG_FILE}"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "${LOG_FILE}"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "${LOG_FILE}"
}

print_action() {
    echo -e "${CYAN}[ACTION]${NC} $1" | tee -a "${LOG_FILE}"
}

print_platform() {
    echo -e "${MAGENTA}[PLATFORM]${NC} $1" | tee -a "${LOG_FILE}"
}

# Function: Show usage
show_usage() {
    cat << EOF
Shannon Framework v5.4 - Universal Installation Script

Usage: $0 [OPTIONS]

OPTIONS:
    --claude        Install for Claude Code only
    --cursor        Install for Cursor IDE only
    --both          Install for both platforms (default)
    --install       Install Shannon Framework (default)
    --update        Update existing installation
    --uninstall     Remove Shannon Framework installation
    --help          Show this help message

EXAMPLES:
    $0                       # Install for both platforms
    $0 --cursor              # Install for Cursor only
    $0 --claude --update     # Update Claude Code installation
    $0 --both --uninstall    # Remove from both platforms

INSTALLATION TARGETS:

Claude Code:
    ~/.claude/skills/shannon/
    ~/.claude/commands/shannon/
    ~/.claude/agents/shannon/
    ~/.claude/core/shannon/
    ~/.claude/hooks/shannon/
    ~/.claude/hooks.json

Cursor IDE:
    ~/.cursor/commands/                          # Shannon commands (19 files)
    ~/.cursor/shannon/                           # Shannon framework files
    ~/.cursor/global.cursorrules                 # Global rules file
    ~/.cursor/.vscode/tasks.json                 # VS Code tasks
    ~/Library/Application Support/Cursor/User/   # Settings (macOS, merged safely)
    ~/.config/Cursor/User/                       # Settings (Linux, merged safely)

For detailed documentation, see: INSTALL_LOCAL.md

EOF
}

# Function: Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --claude)
                TARGET_PLATFORM="claude"
                shift
                ;;
            --cursor)
                TARGET_PLATFORM="cursor"
                shift
                ;;
            --both)
                TARGET_PLATFORM="both"
                shift
                ;;
            --install)
                MODE="install"
                shift
                ;;
            --update)
                MODE="update"
                shift
                ;;
            --uninstall)
                MODE="uninstall"
                shift
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
}

# Function: Detect installed platforms
detect_platforms() {
    local has_claude=false
    local has_cursor=false

    # Check for Claude Code
    if [ -d "${CLAUDE_CONFIG_DIR}" ] || command -v claude &> /dev/null; then
        has_claude=true
        print_info "Detected: Claude Code"
    fi

    # Check for Cursor
    if [ -d "${CURSOR_CONFIG_DIR}" ] || command -v cursor &> /dev/null; then
        has_cursor=true
        print_info "Detected: Cursor IDE"
    fi

    # Determine Cursor settings directory (OS-specific)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        CURSOR_SETTINGS_DIR="${HOME}/Library/Application Support/Cursor/User"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        CURSOR_SETTINGS_DIR="${HOME}/.config/Cursor/User"
    else
        print_warning "Unknown OS: $OSTYPE, using Linux path for Cursor settings"
        CURSOR_SETTINGS_DIR="${HOME}/.config/Cursor/User"
    fi

    # Adjust target based on detection
    if [ "${TARGET_PLATFORM}" = "both" ]; then
        if [ "${has_claude}" = false ] && [ "${has_cursor}" = true ]; then
            print_warning "Claude Code not detected, installing for Cursor only"
            TARGET_PLATFORM="cursor"
        elif [ "${has_cursor}" = false ] && [ "${has_claude}" = true ]; then
            print_warning "Cursor not detected, installing for Claude Code only"
            TARGET_PLATFORM="claude"
        elif [ "${has_claude}" = false ] && [ "${has_cursor}" = false ]; then
            print_warning "Neither Claude Code nor Cursor detected"
            print_warning "Installation will proceed, but you may need to install one of these editors"
        fi
    fi

    echo ""
    print_platform "Installation target: ${TARGET_PLATFORM}"
    echo ""
}

# Function: Generate Cursor global rules file
generate_cursor_global_rules() {
    local rules_file="$1"

cat > "${rules_file}" << 'EOF'
# Shannon Framework v5.4 - Global Cursor Rules
# This file integrates Shannon Framework's quantitative development methodology into Cursor

## Shannon Framework Overview

Shannon Framework is a rigorous, quantitative development methodology that replaces subjective judgments with objective measurements throughout the development lifecycle.

### Core Principles

1. **Quantitative Over Qualitative**: All complexity estimates use 8-dimensional scoring (0.0-1.0)
2. **NO MOCKS Testing**: All tests must use real components (real browsers, real databases, real APIs)
3. **Wave-Based Execution**: Complex projects (>=0.50 complexity) use parallel wave execution
4. **Automatic Checkpointing**: Context preservation before compaction (if MCP available)

---

## MANDATORY Workflows

### Before ANY Implementation

**REQUIRED**: Analyze specification complexity BEFORE starting work

```
1. Extract task features:
   - Count domains (Frontend, Backend, Database, DevOps, Security, etc.)
   - Count integrations (external APIs, services)
   - Estimate lines of code
   - Identify new concepts/technologies

2. Calculate 8D Complexity Score (0.0-1.0):
   Dimensions:
   - Scope (0-100): Number of features/components
   - Technical Complexity (0-100): Algorithm difficulty, new concepts
   - Integration Complexity (0-100): External dependencies
   - Domain Knowledge (0-100): Specialized expertise required
   - Uncertainty (0-100): Unknown requirements, research needed
   - Testing Complexity (0-100): E2E scenarios, edge cases
   - Deployment Complexity (0-100): Infrastructure, configuration
   - Documentation (0-100): User docs, API docs, architecture

   Formula: (Sum of 8 dimensions) / 800 = Complexity Score

3. Determine execution strategy:
   - 0.0-0.29 (Simple): Sequential execution, basic testing
   - 0.30-0.49 (Moderate): Sequential with comprehensive testing
   - 0.50-0.69 (Complex): Wave-based parallel execution (3-7 agents)
   - 0.70-0.89 (Very Complex): Wave-based with SITREP coordination (8-15 agents)
   - 0.90-1.00 (Critical): Maximum parallelization (16-31 agents) + formal validation
```

### During Implementation

**NO MOCKS Iron Law**: Tests MUST use real components

```
❌ NEVER use:
- jest.mock()
- unittest.mock
- Sinon stubs
- TestDouble
- Any mocking library

✅ ALWAYS use:
- Real browsers (Puppeteer, Playwright)
- Real databases (Docker containers with actual DB)
- Real APIs (staging environments, test accounts)
- Real file systems (temporary test directories)
- Real network calls (integration tests)
```

**Why NO MOCKS**:
- Mocks test mock behavior, not production behavior
- Production bugs aren't caught by mocked tests
- Integration issues missed
- False confidence in code quality

### Complexity-Based Execution

**If complexity >= 0.50**: Use wave-based parallel execution

```
Wave Structure:
1. Planning Wave: Architecture, component design, API contracts
2. Implementation Waves: Parallel development of components
3. Integration Waves: Connect components, resolve conflicts
4. Validation Wave: End-to-end testing, performance testing
5. Production Wave: Deployment, monitoring, documentation

Each wave:
- Has clear entry/exit criteria
- Produces checkpoints
- Validates against requirements
- Synthesizes results before next wave
```

---

## Testing Philosophy

### Functional Testing Requirements

ALL tests must be functional (end-to-end) using real systems:

**Frontend Testing**:
```javascript
// ❌ WRONG: Mock testing
const mockApi = jest.fn().mockResolvedValue({data: 'test'});

// ✅ CORRECT: Real browser testing
const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.goto('http://localhost:3000');
const response = await page.evaluate(() =>
  fetch('/api/data').then(r => r.json())
);
expect(response.data).toBe('test');
```

**Backend Testing**:
```python
# ❌ WRONG: Mock database
@patch('database.query')
def test_user_creation(mock_query):
    mock_query.return_value = {'id': 1}

# ✅ CORRECT: Real database (Docker)
def test_user_creation():
    # Use real PostgreSQL in Docker container
    db = connect_test_database()
    user = create_user(db, {'name': 'Test'})
    assert user.id > 0
    cleanup_test_database(db)
```

**API Testing**:
```javascript
// ❌ WRONG: Nock/MSW mocking
nock('https://api.example.com')
  .get('/users')
  .reply(200, {users: []});

// ✅ CORRECT: Real API calls (staging)
const response = await fetch('https://staging.api.example.com/users', {
  headers: {'Authorization': `Bearer ${TEST_API_KEY}`}
});
const data = await response.json();
expect(data.users).toBeInstanceOf(Array);
```

---

## Specification Analysis Template

When user provides requirements, ALWAYS analyze:

```markdown
# Specification Analysis

## Requirements Summary
[Extract key requirements]

## 8D Complexity Breakdown

1. **Scope**: [Score/100] - [Number of features, components]
2. **Technical Complexity**: [Score/100] - [Algorithm difficulty, new tech]
3. **Integration Complexity**: [Score/100] - [External dependencies, APIs]
4. **Domain Knowledge**: [Score/100] - [Specialized expertise needed]
5. **Uncertainty**: [Score/100] - [Unknown requirements, research]
6. **Testing Complexity**: [Score/100] - [E2E scenarios, edge cases]
7. **Deployment Complexity**: [Score/100] - [Infrastructure, config]
8. **Documentation**: [Score/100] - [User docs, API docs, architecture]

**Total**: [Sum]/800 = **[Complexity Score]** ([Simple/Moderate/Complex/Very Complex/Critical])

## Domain Breakdown
- Frontend: [Percentage]%
- Backend: [Percentage]%
- Database: [Percentage]%
- DevOps: [Percentage]%
- Other: [Percentage]%

## Execution Strategy
[Sequential OR Wave-Based with N waves]

## Recommended Tools/MCPs
[Based on domain percentages]

## Testing Strategy
[Functional tests required, specify tools: Puppeteer, pytest, etc.]

## Estimated Timeline
[Based on complexity and execution strategy]
```

---

## Code Quality Standards

### Architecture
- Modular design with clear separation of concerns
- Dependency injection for testability
- Interface-based contracts between components
- Configuration externalized from code

### Testing
- Minimum 80% code coverage (functional tests only)
- All critical paths covered by E2E tests
- Performance tests for key operations
- Accessibility tests for user-facing components (WCAG 2.1 AA)

### Documentation
- README with setup, usage, architecture
- API documentation (OpenAPI/Swagger for APIs)
- Architecture diagrams (component, sequence, deployment)
- Inline comments for complex logic only

### Security
- Input validation on all external data
- Authentication/authorization on protected endpoints
- Secrets in environment variables (never committed)
- Dependencies regularly updated (automated scanning)

---

## Common Rationalizations to AVOID

Shannon Framework testing revealed these common violations:

### ❌ "This is simple, skip complexity analysis"
**Reality**: "Simple" tasks often score 0.40-0.60 (Moderate to Complex)
**Rule**: ALWAYS run 8D analysis. Let quantitative scoring decide, not intuition.

### ❌ "Unit tests with mocks are faster"
**Reality**: Mocks test mock behavior, not production
**Rule**: Use real components. 2-3 functional tests > 20 mock tests.

### ❌ "Time pressure justifies shortcuts"
**Reality**: Shortcuts create technical debt and false confidence
**Rule**: Shannon workflows are non-negotiable regardless of timeline.

### ❌ "I can estimate complexity by feel"
**Reality**: Human intuition biased toward under-estimation (30-50% low on average)
**Rule**: 8D quantitative scoring removes bias.

### ❌ "Wave execution is overkill"
**Reality**: Wave execution provides proven 3.5x speedup for complexity >= 0.50
**Rule**: Trust the threshold. Use waves for Complex and above.

---

## MCP Integration

If Model Context Protocol (MCP) servers available:

### Required MCPs
- **Serena MCP**: Context preservation across sessions (MANDATORY for Shannon)
- **Sequential MCP**: Complex reasoning and debugging (recommended)

### Recommended MCPs (by domain)
- **Frontend (>= 20%)**: Puppeteer (browser testing), Magic (component generation)
- **Backend (>= 20%)**: Context7 (framework docs)
- **Database (>= 15%)**: PostgreSQL/MySQL MCP (database operations)
- **DevOps (>= 10%)**: GitHub MCP (version control, CI/CD)

### MCP Discovery
Before starting complex projects, check available MCPs and configure based on domain percentages from specification analysis.

---

## Project Structure

Recommended structure for Shannon-compliant projects:

```
project/
├── .cursorrules              # Project-specific Shannon rules
├── .shannon/                 # Shannon working directory
│   ├── specs/                # Analyzed specifications
│   ├── waves/                # Wave execution plans
│   ├── checkpoints/          # Context checkpoints
│   └── reports/              # Complexity analysis reports
├── src/                      # Source code
├── tests/                    # Functional tests (NO MOCKS)
│   ├── e2e/                  # End-to-end tests
│   ├── integration/          # Integration tests
│   └── fixtures/             # Test data and fixtures
├── docs/                     # Documentation
│   ├── architecture/         # Architecture diagrams
│   ├── api/                  # API documentation
│   └── user/                 # User guides
└── README.md                 # Project README
```

---

## Session Workflow

### Starting a Session

1. **Load Context**: Review previous checkpoints (if available)
2. **Set North Star**: Define overarching project goal
3. **Review Status**: Check active waves, pending tasks

### During Development

1. **Analyze Specs**: Run 8D analysis on new requirements
2. **Plan Execution**: Sequential or wave-based
3. **Implement**: Follow domain-specific best practices
4. **Test**: Functional tests only (NO MOCKS)
5. **Document**: Update architecture, API docs

### Ending a Session

1. **Checkpoint**: Save context to MCP (if available)
2. **Update Status**: Mark completed tasks
3. **Note Blockers**: Document unresolved issues
4. **Plan Next**: Define immediate next steps

---

## Red Flags - STOP Immediately

These thoughts indicate deviation from Shannon:

- "This is simple enough to skip analysis"
- "I know the complexity already"
- "Unit tests with mocks are fine for this"
- "Manual testing verified it works"
- "Wave execution seems like overkill"
- "I'll add proper tests later"
- "Time pressure justifies shortcuts"

**If any of these occur**: STOP. Follow Shannon mandatory workflows.

---

## Cursor-Specific Integration

### Composer Integration
When using Cursor Composer:
- Paste specification → Request 8D analysis first
- Reference Shannon complexity score in prompts
- Specify "functional tests only (NO MOCKS)" for test generation
- Request wave plans for complexity >= 0.50

### Chat Integration
When using Cursor Chat:
- Ask for complexity analysis before implementation
- Request MCP recommendations based on domains
- Specify testing requirements explicitly
- Ask for checkpoints before major changes

### Custom Commands
Consider adding Cursor tasks:
- "Analyze Specification": Runs 8D analysis
- "Generate Wave Plan": Creates wave execution plan
- "Validate Tests": Checks for mock usage
- "Create Checkpoint": Saves current context

---

## Version

**Shannon Framework**: v5.4.0
**Last Updated**: 2025-11-18
**License**: MIT

---

This file establishes Shannon Framework workflows in Cursor IDE.
For complete documentation, see Shannon Framework repository.
EOF

    print_success "Generated Cursor global rules: ${rules_file}"
}

# Function: Generate Cursor settings.json snippet (safely merge with existing)
generate_cursor_settings() {
    local settings_file="$1"
    
    print_info "Configuring Cursor settings..."
    
    # Shannon settings to add
    local shannon_settings='{
  "cursor.shannon.enabled": true,
  "cursor.shannon.version": "5.4.0",
  "cursor.shannon.enforceNoMocks": true,
  "cursor.shannon.requireComplexityAnalysis": true,
  "cursor.shannon.waveExecutionThreshold": 0.50,
  
  "cursor.chat.systemPrompt": "You are an AI assistant following Shannon Framework v5.4 quantitative development methodology. Before any implementation, analyze specifications using 8D complexity scoring. Enforce NO MOCKS testing philosophy (real browsers, real databases, real APIs only). Use wave-based execution for complexity >= 0.50. Reference global Cursor rules for complete Shannon workflows.",
  
  "cursor.composer.systemPrompt": "Follow Shannon Framework v5.4: Run 8D complexity analysis before implementation. NO MOCKS in tests (use real components). Wave-based execution for complexity >= 0.50. Check global .cursorrules for full methodology.",
  
  "editor.rulers": [80, 120],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true
  },
  
  "files.exclude": {
    "**/.shannon/checkpoints": false,
    "**/.shannon/waves": false
  }
}'
    
    # Check if settings.json exists
    if [ -f "${settings_file}" ]; then
        # Backup existing settings
        cp "${settings_file}" "${settings_file}.backup.$(date +%Y%m%d_%H%M%S)"
        print_success "Backed up existing settings.json"
        
        # Check if jq is available for JSON merging
        if command -v jq &> /dev/null; then
            print_info "Merging Shannon settings with existing settings (using jq)..."
            
            # Merge using jq (Shannon settings take precedence)
            # Disable set -e temporarily to allow fallback on jq failure
            set +e
            local merged_settings=$(jq -s '.[0] * .[1]' "${settings_file}" <(echo "${shannon_settings}") 2>&1)
            local jq_exit_code=$?
            set -e
            
            if [ ${jq_exit_code} -eq 0 ] && [ -n "${merged_settings}" ]; then
                echo "${merged_settings}" > "${settings_file}"
                print_success "Settings merged successfully (existing settings preserved)"
            else
                print_warning "jq merge failed (exit code: ${jq_exit_code}), falling back to Python..."
                
                # Fall through to Python fallback below
                command -v jq &> /dev/null && false  # Force fallback to else block
            fi
        fi
        
        # Python fallback (runs if jq unavailable OR if jq failed)
        if ! command -v jq &> /dev/null || [ ${jq_exit_code:-1} -ne 0 ]; then
            # Fallback: Manual merge using Python
            print_warning "jq not found, using Python for merge..."
            
            # Write Shannon settings to temporary file (safer than heredoc embedding)
            local temp_shannon_settings="/tmp/shannon_settings_$$.json"
            echo "${shannon_settings}" > "${temp_shannon_settings}"
            
            python3 << EOF
import json
import sys

# Read existing settings
try:
    with open("${settings_file}", 'r') as f:
        existing = json.load(f)
except Exception as e:
    print(f"Error reading existing settings: {e}", file=sys.stderr)
    existing = {}

# Read Shannon settings from temp file (safer than heredoc)
try:
    with open("${temp_shannon_settings}", 'r') as f:
        shannon = json.load(f)
except Exception as e:
    print(f"Error reading Shannon settings: {e}", file=sys.stderr)
    sys.exit(1)

# Merge (Shannon settings take precedence)
merged = {**existing, **shannon}

# Write merged settings
try:
    with open("${settings_file}", 'w') as f:
        json.dump(merged, f, indent=2)
    print("✓ Settings merged successfully")
except Exception as e:
    print(f"Error writing merged settings: {e}", file=sys.stderr)
    sys.exit(1)
EOF
            
            local python_exit_code=$?
            
            # Clean up temp file
            rm -f "${temp_shannon_settings}"
            
            if [ ${python_exit_code} -eq 0 ]; then
                print_success "Settings merged successfully (existing settings preserved)"
            else
                print_error "Failed to merge settings with Python"
                print_error "Cannot automatically merge settings.json"
                
                # Write Shannon settings to separate file for manual merge
                local shannon_settings_file="${CURSOR_SETTINGS_DIR}/shannon_settings.json"
                echo "${shannon_settings}" > "${shannon_settings_file}"
                
                print_warning "Shannon settings written to: ${shannon_settings_file}"
                print_warning "MANUAL ACTION REQUIRED:"
                echo ""
                echo "1. Open: ${settings_file}"
                echo "2. Open: ${shannon_settings_file}"
                echo "3. Copy settings from shannon_settings.json into settings.json"
                echo "4. Ensure valid JSON syntax (no trailing commas)"
                echo "5. Save settings.json"
                echo "6. Delete shannon_settings.json (optional)"
                echo ""
                print_error "Settings.json NOT modified to prevent corruption"
                print_info "Your existing settings are preserved and unchanged"
            fi
        fi
    else
        # No existing file, create new one
        print_info "No existing settings.json, creating new file..."
        echo "${shannon_settings}" > "${settings_file}"
        print_success "Created new settings.json with Shannon configuration"
    fi
}

# Function: Install for Claude Code (using existing logic from install_local.sh)
install_claude_code() {
    print_platform "Installing Shannon Framework for Claude Code..."
    echo ""

    # Run the existing install_local.sh script
    if [ -f "${SHANNON_ROOT}/install_local.sh" ]; then
        bash "${SHANNON_ROOT}/install_local.sh" --install
    else
        print_error "install_local.sh not found"
        return 1
    fi
}

# Function: Install Shannon commands for Cursor
install_cursor_commands() {
    print_info "Installing Shannon commands for Cursor..."
    
    # Create global commands directory
    local cursor_commands_dir="${CURSOR_CONFIG_DIR}/commands"
    mkdir -p "${cursor_commands_dir}"
    
    local command_count=0
    
    # Copy each command file and adapt for Cursor
    for command_file in "${SHANNON_ROOT}/commands"/*.md; do
        if [ -f "${command_file}" ]; then
            local command_name=$(basename "${command_file}")
            local cursor_command_file="${cursor_commands_dir}/${command_name}"
            
            # Adapt command for Cursor (add usage note at top)
            cat > "${cursor_command_file}" << 'CMD_HEADER'
> **Note**: This is a Shannon Framework command. In Cursor, reference this command in Chat/Composer by mentioning its purpose.
> Example: "Run Shannon 8D complexity analysis on this specification"

CMD_HEADER
            
            # Append original command content
            cat "${command_file}" >> "${cursor_command_file}"
            
            print_info "  Installed command: ${command_name}"
            ((command_count++))
        fi
    done
    
    print_success "Installed ${command_count} commands to Cursor"
}

# Function: Create Cursor tasks.json for Shannon
create_cursor_tasks() {
    print_info "Creating Cursor tasks for Shannon commands..."
    
    # Create tasks directory
    local cursor_tasks_dir="${CURSOR_CONFIG_DIR}/.vscode"
    mkdir -p "${cursor_tasks_dir}"
    
    local tasks_file="${cursor_tasks_dir}/tasks.json"
    
    # Generate tasks.json
    cat > "${tasks_file}" << 'TASKS_EOF'
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Shannon: Prime Session",
      "type": "shell",
      "command": "echo '💡 In Cursor Chat, type: Prime this session with Shannon Framework'",
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Shannon: Analyze Specification",
      "type": "shell",
      "command": "echo '💡 In Cursor Chat, paste your specification and add: Analyze using Shannon Framework 8D complexity scoring'",
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Shannon: Check MCP Status",
      "type": "shell",
      "command": "echo '💡 In Cursor Chat, type: Check Shannon Framework MCP server status and recommendations'",
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Shannon: Generate Wave Plan",
      "type": "shell",
      "command": "echo '💡 In Cursor Chat, type: Generate Shannon wave execution plan for this project'",
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Shannon: Validate Tests (NO MOCKS)",
      "type": "shell",
      "command": "echo '💡 In Cursor Chat, type: Validate all tests follow Shannon NO MOCKS philosophy'",
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Shannon: View Global Rules",
      "type": "shell",
      "command": "cat ~/.cursor/global.cursorrules | head -100",
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Shannon: View Quick Start",
      "type": "shell",
      "command": "cat ~/.cursor/shannon/QUICK_START.md",
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
TASKS_EOF
    
    print_success "Created Cursor tasks.json with Shannon tasks"
    print_info "Access tasks: Cmd+Shift+P → 'Tasks: Run Task' → Select Shannon task"
}

# Function: Install for Cursor IDE
install_cursor() {
    print_platform "Installing Shannon Framework for Cursor IDE..."
    echo ""
    
    # Create Cursor Shannon directory
    local cursor_shannon_dir="${CURSOR_CONFIG_DIR}/shannon"
    mkdir -p "${cursor_shannon_dir}"
    
    # Copy core documentation (for reference)
    print_info "Installing core documentation..."
    mkdir -p "${cursor_shannon_dir}/core"
    mkdir -p "${cursor_shannon_dir}/skills"
    mkdir -p "${cursor_shannon_dir}/agents"
    
    cp -r "${SHANNON_ROOT}/core"/*.md "${cursor_shannon_dir}/core/"
    cp -r "${SHANNON_ROOT}/skills"/* "${cursor_shannon_dir}/skills/"
    cp -r "${SHANNON_ROOT}/agents"/*.md "${cursor_shannon_dir}/agents/"
    
    print_success "Core documentation installed"
    echo ""
    
    # Install Shannon commands for Cursor
    install_cursor_commands
    echo ""
    
    # Create Cursor tasks
    create_cursor_tasks
    echo ""
    
    # Generate global Cursor rules
    print_info "Generating global Cursor rules..."
    generate_cursor_global_rules "${CURSOR_CONFIG_DIR}/global.cursorrules"
    echo ""
    
    # Generate Cursor settings (with safe merge)
    mkdir -p "${CURSOR_SETTINGS_DIR}"
    generate_cursor_settings "${CURSOR_SETTINGS_DIR}/settings.json"
    echo ""
    
    # Create Shannon working directory structure
    print_info "Creating Shannon working directory structure..."
    mkdir -p "${CURSOR_CONFIG_DIR}/shannon/.templates"
    
    # Copy templates
    if [ -d "${SHANNON_ROOT}/templates" ]; then
        cp -r "${SHANNON_ROOT}/templates"/* "${CURSOR_CONFIG_DIR}/shannon/.templates/"
    fi
    
    print_success "Shannon working directory created"
    echo ""

    # Create quick reference guide
    print_info "Creating quick reference guide..."
    cat > "${CURSOR_CONFIG_DIR}/shannon/QUICK_START.md" << 'EOF'
# Shannon Framework - Cursor Quick Start

## Session Workflow

### 1. Starting Any Task

Before coding, analyze the specification:

```
Complexity analysis request:
"Analyze this specification using Shannon Framework's 8D complexity scoring:
[paste specification here]"
```

### 2. Review Complexity Report

You'll receive:
- 8D breakdown (Scope, Technical, Integration, Domain, Uncertainty, Testing, Deployment, Documentation)
- Complexity score (0.0-1.0)
- Execution strategy (Sequential or Wave-based)
- MCP recommendations
- Testing strategy

### 3. Execute Based on Complexity

**Simple/Moderate (< 0.50)**: Sequential implementation
**Complex/Very Complex/Critical (>= 0.50)**: Request wave execution plan

### 4. Testing Requirements

**NO MOCKS** - All tests must use real components:
- Frontend: Puppeteer/Playwright (real browser)
- Backend: Real database (Docker container)
- APIs: Staging environment with test accounts

### 5. Common Prompts

**Complexity Analysis**:
"Run Shannon 8D complexity analysis on: [specification]"

**Wave Planning**:
"Generate Shannon wave execution plan for complexity 0.72"

**Test Generation**:
"Create functional tests (NO MOCKS) for [feature] using real [browser/database/API]"

**Checkpoint**:
"Create Shannon checkpoint for current session"

## Reference

- Global Rules: `~/.cursor/global.cursorrules`
- Core Docs: `~/.cursor/shannon/core/`
- Skills: `~/.cursor/shannon/skills/`
- Agents: `~/.cursor/shannon/agents/`

## Version

Shannon Framework v5.4.0
EOF

    print_success "Quick start guide created: ${CURSOR_CONFIG_DIR}/shannon/QUICK_START.md"
    echo ""
}

# Function: Update installations
update_installations() {
    print_action "Updating Shannon Framework installations..."
    echo ""

    if [ "${TARGET_PLATFORM}" = "claude" ] || [ "${TARGET_PLATFORM}" = "both" ]; then
        if [ -f "${SHANNON_ROOT}/install_local.sh" ]; then
            print_platform "Updating Claude Code installation..."
            bash "${SHANNON_ROOT}/install_local.sh" --update
            echo ""
        fi
    fi

    if [ "${TARGET_PLATFORM}" = "cursor" ] || [ "${TARGET_PLATFORM}" = "both" ]; then
        print_platform "Updating Cursor installation..."
        # Backup existing
        if [ -d "${CURSOR_CONFIG_DIR}/shannon" ]; then
            local backup_dir="${CURSOR_CONFIG_DIR}/shannon_backup_$(date +%Y%m%d_%H%M%S)"
            mv "${CURSOR_CONFIG_DIR}/shannon" "${backup_dir}"
            print_success "Backup created: ${backup_dir}"
        fi

        # Reinstall
        install_cursor
    fi
}

# Function: Uninstall installations
uninstall_installations() {
    print_action "Uninstalling Shannon Framework..."
    echo ""

    if [ "${TARGET_PLATFORM}" = "claude" ] || [ "${TARGET_PLATFORM}" = "both" ]; then
        if [ -f "${SHANNON_ROOT}/install_local.sh" ]; then
            print_platform "Uninstalling from Claude Code..."
            bash "${SHANNON_ROOT}/install_local.sh" --uninstall
            echo ""
        fi
    fi

    if [ "${TARGET_PLATFORM}" = "cursor" ] || [ "${TARGET_PLATFORM}" = "both" ]; then
        print_platform "Uninstalling from Cursor..."

        # Remove Shannon directories
        if [ -d "${CURSOR_CONFIG_DIR}/shannon" ]; then
            rm -rf "${CURSOR_CONFIG_DIR}/shannon"
            print_success "Removed Shannon directory"
        fi

        # Remove global rules
        if [ -f "${CURSOR_CONFIG_DIR}/global.cursorrules" ]; then
            mv "${CURSOR_CONFIG_DIR}/global.cursorrules" "${CURSOR_CONFIG_DIR}/global.cursorrules.backup.$(date +%Y%m%d_%H%M%S)"
            print_success "Backed up and removed global.cursorrules"
        fi

        # Note about settings.json
        print_warning "Cursor settings.json not automatically removed (may contain other settings)"
        print_info "Backup exists at: ${CURSOR_SETTINGS_DIR}/settings.json.backup.*"

        echo ""
    fi
}

# Function: Post-installation instructions
post_install_instructions() {
    cat << 'INSTRUCTIONS'

╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║      Shannon Framework v5.4 - Universal Installation Complete  ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

INSTRUCTIONS

    # Platform-specific instructions
    if [ "${TARGET_PLATFORM}" = "claude" ] || [ "${TARGET_PLATFORM}" = "both" ]; then
        cat << 'CLAUDE_INSTRUCTIONS'
Claude Code Installation:
─────────────────────────────────────────────────────────────────
  ✓ Skills:    ~/.claude/skills/shannon/
  ✓ Commands:  ~/.claude/commands/shannon/
  ✓ Agents:    ~/.claude/agents/shannon/
  ✓ Core:      ~/.claude/core/shannon/
  ✓ Hooks:     ~/.claude/hooks/shannon/
  ✓ Config:    ~/.claude/hooks.json

Next Steps (Claude Code):
  1. Restart Claude Code
  2. Verify: /shannon:status
  3. Begin session: /shannon:prime
  4. Analyze specs: /shannon:spec "your specification"

CLAUDE_INSTRUCTIONS
    fi

    if [ "${TARGET_PLATFORM}" = "cursor" ] || [ "${TARGET_PLATFORM}" = "both" ]; then
        cat << 'CURSOR_INSTRUCTIONS'

Cursor IDE Installation:
─────────────────────────────────────────────────────────────────
  ✓ Core Docs:        ~/.cursor/shannon/core/
  ✓ Skills:           ~/.cursor/shannon/skills/
  ✓ Agents:           ~/.cursor/shannon/agents/
  ✓ Global Rules:     ~/.cursor/global.cursorrules
  ✓ Settings:         ~/Library/Application Support/Cursor/User/settings.json
  ✓ Quick Start:      ~/.cursor/shannon/QUICK_START.md

Next Steps (Cursor):
  1. Restart Cursor
  2. Open any project
  3. In Chat or Composer, request:
     "Analyze this specification using Shannon Framework's 8D complexity scoring:
      [paste your specification]"
  4. Follow Shannon workflows per global.cursorrules

Quick Reference:
  - View rules: cat ~/.cursor/global.cursorrules
  - Quick start: cat ~/.cursor/shannon/QUICK_START.md
  - Core docs: ls ~/.cursor/shannon/core/

CURSOR_INSTRUCTIONS
    fi

    cat << 'FOOTER'
Documentation:
─────────────────────────────────────────────────────────────────
  Installation Log: ~/.shannon_install.log

Support:
─────────────────────────────────────────────────────────────────
  Repository: https://github.com/shannon-framework/shannon
  Issues:     https://github.com/shannon-framework/shannon/issues

═══════════════════════════════════════════════════════════════════

FOOTER
}

# Main execution
main() {
    # Parse command line arguments
    parse_args "$@"

    # Create log directory
    mkdir -p "$(dirname "${LOG_FILE}")"

    # Log start
    echo "=== Shannon Framework Universal Installation ===" >> "${LOG_FILE}"
    echo "Date: $(date)" >> "${LOG_FILE}"
    echo "Mode: ${MODE}" >> "${LOG_FILE}"
    echo "Target: ${TARGET_PLATFORM}" >> "${LOG_FILE}"
    echo "================================================" >> "${LOG_FILE}"
    echo "" >> "${LOG_FILE}"

    # Detect platforms
    detect_platforms

    # Execute based on mode
    case "${MODE}" in
        install)
            if [ "${TARGET_PLATFORM}" = "claude" ]; then
                install_claude_code
            elif [ "${TARGET_PLATFORM}" = "cursor" ]; then
                install_cursor
            else
                install_claude_code
                echo ""
                install_cursor
            fi
            echo ""
            print_success "Installation complete!"
            echo ""
            post_install_instructions
            ;;
        update)
            update_installations
            print_success "Update complete!"
            ;;
        uninstall)
            uninstall_installations
            print_success "Uninstallation complete!"
            ;;
        *)
            print_error "Invalid mode: ${MODE}"
            show_usage
            exit 1
            ;;
    esac
}

# Run main
main "$@"

