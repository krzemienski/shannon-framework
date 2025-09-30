# Section 8: Documentation Guide

Shannon includes comprehensive documentation organized by topic and purpose. All documentation follows the NO MOCKS principle - real examples, real evidence, real results.

## Documentation Files

| File | Purpose | Size | Key Topics |
|------|---------|------|------------|
| [INSTALLATION.md](INSTALLATION.md) | Complete setup guide | 13KB | Claude Desktop config, MCP server setup, verification steps |
| [SHADCN_INTEGRATION.md](SHADCN_INTEGRATION.md) | shadcn/ui complete guide | 49KB | Component installation, customization, theming, CLI usage |
| [DOCKER_TESTING.md](DOCKER_TESTING.md) | Docker validation guide | 9KB | Container setup, test execution, CI/CD integration |
| [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md) | 100% test pass proof | 11KB | Complete test results, NO MOCKS evidence, artifact validation |
| [CHANGELOG.md](CHANGELOG.md) | Release history | Variable | Version changes, new features, breaking changes |

## Quick Reference: Where to Find What

### Getting Started
- **First-time setup**: Start with [INSTALLATION.md](INSTALLATION.md)
- **Claude Desktop config**: [INSTALLATION.md](INSTALLATION.md) → "Claude Desktop Configuration"
- **Verification**: [INSTALLATION.md](INSTALLATION.md) → "Verification Steps"

### Using Shannon
- **Available commands**: See [Section 4: Core Commands](#section-4-core-commands) in main README
- **Agent system**: See [Section 5: Agent System](#section-5-agent-system) in main README
- **Examples**: Each command includes usage examples in frontmatter

### Component Integration
- **shadcn/ui setup**: [SHADCN_INTEGRATION.md](SHADCN_INTEGRATION.md) → "Installation"
- **Adding components**: [SHADCN_INTEGRATION.md](SHADCN_INTEGRATION.md) → "Component Installation"
- **Customization**: [SHADCN_INTEGRATION.md](SHADCN_INTEGRATION.md) → "Customization Guide"
- **Theming**: [SHADCN_INTEGRATION.md](SHADCN_INTEGRATION.md) → "Theme Configuration"

### Testing & Validation
- **Running tests**: [DOCKER_TESTING.md](DOCKER_TESTING.md) → "Running Tests"
- **Test results**: [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md)
- **CI/CD setup**: [DOCKER_TESTING.md](DOCKER_TESTING.md) → "CI/CD Integration"

### Development
- **Adding commands**: See [Section 10: Contributing](#section-10-contributing--development)
- **Adding agents**: See [Section 10: Contributing](#section-10-contributing--development)
- **Testing requirements**: See [Section 9: Testing & Validation](#section-9-testing--validation)

## Documentation Organization

Shannon's documentation follows a hierarchical structure:

```
shannon/
├── README.md                    # Main documentation (this file)
├── INSTALLATION.md              # Setup and configuration
├── SHADCN_INTEGRATION.md        # Component system guide
├── DOCKER_TESTING.md            # Testing infrastructure
├── VERIFICATION_REPORT.md       # Test evidence
├── CHANGELOG.md                 # Release history
├── docs/
│   ├── commands/               # Command-specific guides
│   ├── agents/                 # Agent behavioral documentation
│   └── examples/               # Usage examples and patterns
└── tests/
    ├── fixtures/               # Test data and examples
    └── validation/             # Validation scripts
```

### Documentation Principles

1. **Evidence-Based**: All claims backed by real examples or test results
2. **NO MOCKS**: Only real, working examples - never placeholder code
3. **Verification**: Every feature includes verification steps
4. **Completeness**: Comprehensive coverage of setup, usage, and troubleshooting

### Finding Information Quickly

**By Task:**
- Setting up Shannon → [INSTALLATION.md](INSTALLATION.md)
- Installing components → [SHADCN_INTEGRATION.md](SHADCN_INTEGRATION.md)
- Running tests → [DOCKER_TESTING.md](DOCKER_TESTING.md)
- Verifying results → [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md)

**By Technology:**
- Claude Desktop → [INSTALLATION.md](INSTALLATION.md) → "Claude Desktop Configuration"
- MCP Servers → [INSTALLATION.md](INSTALLATION.md) → "MCP Server Configuration"
- shadcn/ui → [SHADCN_INTEGRATION.md](SHADCN_INTEGRATION.md)
- Docker → [DOCKER_TESTING.md](DOCKER_TESTING.md)

**By Concern:**
- "How do I...?" → Check command examples in README or relevant guide
- "Is this tested?" → [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md)
- "What changed?" → [CHANGELOG.md](CHANGELOG.md)
- "How do I contribute?" → [Section 10: Contributing](#section-10-contributing--development)

### Documentation Updates

Documentation is updated with each release. See [CHANGELOG.md](CHANGELOG.md) for documentation changes in each version.

For documentation issues or suggestions, please open an issue on GitHub.

---

# Section 9: Testing & Validation

Shannon uses **Docker-based testing** to ensure **100% real-world validation**. Every test runs in an isolated container with actual Claude Desktop configuration - **NO MOCKS, NO STUBS, NO FAKE DATA**.

## Test Results: 46/46 Tests Pass (100%)

Complete test validation across all Shannon components:

```
✅ 46/46 TESTS PASSED (100%)

Test Categories:
├── PreCompact Hook Tests (7 tests) ................... 100%
├── NO MOCKS Detection Tests (6 tests) ................ 100%
├── Artifact Validation Tests (23 tests) .............. 100%
└── Framework Integration Tests (10 tests) ............ 100%

Evidence: VERIFICATION_REPORT.md
```

## NO MOCKS Philosophy

Shannon's testing philosophy is simple: **Real examples or nothing**.

### What This Means

**NO MOCKS**:
- ❌ No placeholder code
- ❌ No fake data generators
- ❌ No stub implementations
- ❌ No "TODO: implement"
- ❌ No commented-out functionality

**YES REAL**:
- ✅ Real Claude Desktop configs
- ✅ Real MCP server definitions
- ✅ Real component installations
- ✅ Real Docker environments
- ✅ Real test evidence

### Why This Matters

1. **Trust**: Tests prove Shannon actually works, not just that mocks pass
2. **Reality**: Catches real-world issues that mocks would hide
3. **Documentation**: Test results are proof of functionality
4. **Confidence**: 100% pass rate means 100% working features

### Detection System

Shannon includes **automatic NO MOCKS detection** that validates:

```yaml
no_mocks_validation:
  placeholder_detection:
    - "TODO"
    - "FIXME"
    - "placeholder"
    - "mock"
    - "stub"

  fake_code_patterns:
    - "NotImplementedError"
    - "pass  # implement"
    - "throw new Error('Not implemented')"

  incomplete_implementations:
    - Empty function bodies
    - Commented-out logic
    - Conditional bypasses
```

**Test Results**: 6/6 NO MOCKS detection tests pass (100%)

See [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md) → "NO MOCKS Detection Tests"

## Running Tests Locally

### Prerequisites

- Docker installed and running
- Repository cloned locally
- No other Claude Desktop instances running (to avoid conflicts)

### Quick Test Run

```bash
# Clone repository
git clone https://github.com/yourusername/shannon.git
cd shannon

# Run all tests
docker-compose -f tests/docker-compose.test.yml up --abort-on-container-exit

# View results
cat tests/results/test-results.json
```

### Test Categories

#### 1. PreCompact Hook Tests (7 tests)

Validates PreCompact executable configuration and behavior:

```bash
# Run PreCompact tests only
docker-compose -f tests/docker-compose.test.yml run --rm test-precompact
```

**Tests:**
- Executable installation verification
- Hook configuration validation
- Claude Desktop integration
- Command routing functionality
- Error handling
- Performance benchmarks
- Cross-platform compatibility

#### 2. NO MOCKS Detection Tests (6 tests)

Ensures no placeholder code in production:

```bash
# Run NO MOCKS tests only
docker-compose -f tests/docker-compose.test.yml run --rm test-no-mocks
```

**Tests:**
- Placeholder keyword detection
- Fake code pattern scanning
- Incomplete implementation checks
- Documentation verification
- Example code validation
- Test fixture authenticity

#### 3. Artifact Validation Tests (23 tests)

Validates all framework artifacts and configurations:

```bash
# Run artifact tests only
docker-compose -f tests/docker-compose.test.yml run --rm test-artifacts
```

**Tests:**
- Command YAML frontmatter validation
- Agent behavioral instruction validation
- File structure verification
- Documentation completeness
- Configuration integrity
- Example accuracy
- Cross-reference validation

#### 4. Framework Integration Tests (10 tests)

End-to-end framework functionality validation:

```bash
# Run integration tests only
docker-compose -f tests/docker-compose.test.yml run --rm test-integration
```

**Tests:**
- Claude Desktop MCP integration
- Command execution flow
- Agent coordination
- File system operations
- Error propagation
- Performance under load
- Multi-command sequences

### Test Output

Tests produce structured JSON output with detailed results:

```json
{
  "test_suite": "Shannon Framework Tests",
  "total_tests": 46,
  "passed": 46,
  "failed": 0,
  "pass_rate": "100%",
  "execution_time": "47.3s",
  "categories": {
    "precompact_hook": {"tests": 7, "passed": 7},
    "no_mocks_detection": {"tests": 6, "passed": 6},
    "artifact_validation": {"tests": 23, "passed": 23},
    "framework_integration": {"tests": 10, "passed": 10}
  }
}
```

## CI/CD Integration

Shannon tests run automatically on every commit and pull request using GitHub Actions with Docker-based validation.

### GitHub Actions Workflow

```yaml
name: Shannon Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Docker Tests
        run: docker-compose -f tests/docker-compose.test.yml up --abort-on-container-exit
      - name: Verify Results
        run: |
          if [ $(cat tests/results/test-results.json | jq '.failed') -gt 0 ]; then
            exit 1
          fi
```

### Local CI Simulation

Test exactly what CI will run:

```bash
# Simulate CI environment
docker-compose -f tests/docker-compose.test.yml down --volumes
docker-compose -f tests/docker-compose.test.yml build --no-cache
docker-compose -f tests/docker-compose.test.yml up --abort-on-container-exit

# Check results like CI does
jq '.failed' tests/results/test-results.json
# Output: 0 (success)
```

## Test Evidence & Reports

All test runs produce evidence in [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md):

- **Test Execution Logs**: Complete output from all tests
- **Pass/Fail Breakdown**: Results by category and individual test
- **NO MOCKS Evidence**: Proof of real implementations
- **Performance Metrics**: Execution times and resource usage
- **Environment Details**: Docker versions, system info, test conditions

**Current Report**: 100% pass rate across 46 tests - see [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md)

---

# Section 10: Contributing & Development

Shannon is a **documentation framework**, not a code project. Contributions involve writing clear behavioral instructions in markdown and YAML, not implementing features.

## How to Extend Shannon

### Understanding the Architecture

Shannon consists of:
1. **Commands** (YAML frontmatter + markdown documentation)
2. **Agents** (Behavioral instruction documents)
3. **Templates** (Reusable instruction patterns)
4. **Tests** (Docker-based validation)

**Key Principle**: You're writing *instructions for Claude*, not code for execution.

### Adding New Commands

Commands are markdown files with YAML frontmatter that define behavior for Claude.

#### 1. Create Command File

```bash
# Create new command file
touch commands/my-command.md
```

#### 2. Add YAML Frontmatter

Required frontmatter structure:

```yaml
---
name: my-command
description: Brief description of what this command does
category: command
triggers:
  - /my-command
  - specific keywords that activate this command
behavior:
  primary_goal: Main objective of this command
  task_sequence:
    - Step 1 of execution
    - Step 2 of execution
    - Step 3 of execution
  success_criteria:
    - How to know the command succeeded
  error_handling:
    - How to handle failures
examples:
  - description: Example use case 1
    input: "/my-command @file.txt"
    expected_output: What Claude should produce
  - description: Example use case 2
    input: "/my-command --flag"
    expected_output: Alternative output format
integration:
  personas: [analyzer, architect]  # Compatible personas
  mcp_servers: [sequential, context7]  # Required MCP servers
  modes: [task-management, introspection]  # Compatible modes
---
```

#### 3. Write Behavioral Instructions

After frontmatter, write clear instructions for Claude:

```markdown
# My Command

## Purpose
Clear explanation of what this command does and when to use it.

## Behavioral Instructions

### Pre-Execution
1. Validate inputs
2. Check prerequisites
3. Load necessary context

### Execution Flow
1. First action with specific guidance
2. Second action with decision criteria
3. Third action with output format

### Post-Execution
1. Validation steps
2. Cleanup operations
3. Status reporting

## Examples

### Example 1: Basic Usage
**Input**: `/my-command @file.txt`

**Expected Behavior**:
1. Read file.txt
2. Process according to instructions
3. Output formatted results

**Output Format**:
```
[Specific output structure]
```

### Example 2: Advanced Usage
[Additional examples with different scenarios]

## Integration Notes

### With Personas
- **Analyzer**: Use for investigation tasks
- **Architect**: Use for design decisions

### With MCP Servers
- **Sequential**: Required for complex reasoning
- **Context7**: Optional for documentation lookup

## Error Handling

### Common Issues
1. **Issue**: Description
   **Solution**: Resolution steps

2. **Issue**: Another problem
   **Solution**: Fix instructions
```

#### 4. Add Tests

Create validation tests for your command:

```bash
# Add test file
touch tests/validation/test-my-command.sh
```

```bash
#!/bin/bash
# Test: my-command basic functionality

set -e

# Test 1: Command triggers correctly
echo "Testing command trigger..."
# Validation logic

# Test 2: Output format matches specification
echo "Testing output format..."
# Validation logic

# Test 3: Error handling works
echo "Testing error handling..."
# Validation logic

echo "✅ All my-command tests passed"
```

#### 5. Document the Command

Add entry to README.md command list:

```markdown
### `/my-command`

**Purpose**: Brief description

**Usage**: `/my-command [arguments]`

**Key Features**:
- Feature 1
- Feature 2
- Feature 3

**See**: [commands/my-command.md](commands/my-command.md)
```

### Adding New Agents

Agents are behavioral instruction documents that define specialized expertise.

#### 1. Create Agent File

```bash
touch agents/my-agent.md
```

#### 2. Define Agent Behavior

```yaml
---
name: my-agent
description: Specialized agent for specific domain
category: agent
expertise:
  - Domain expertise 1
  - Domain expertise 2
  - Domain expertise 3
activation_triggers:
  keywords: [specific, domain, terms]
  contexts: [when this agent should activate]
  complexity_threshold: 0.7  # Complexity score 0.0-1.0
behavioral_principles:
  - Core principle 1
  - Core principle 2
  - Core principle 3
decision_framework:
  priority_hierarchy: [highest priority first]
  trade_off_preferences: [how to resolve conflicts]
integration:
  compatible_agents: [other agents that work well with this one]
  mcp_preferences: [preferred MCP servers]
---
```

#### 3. Write Behavioral Instructions

```markdown
# My Agent

## Identity
Clear statement of agent's role and expertise domain.

## Core Principles
1. **Principle 1**: Explanation and application
2. **Principle 2**: Explanation and application
3. **Principle 3**: Explanation and application

## Decision Framework

### Priority Hierarchy
1. Highest priority consideration
2. Secondary priority
3. Tertiary priority

### Trade-off Resolution
When facing conflicts:
- Scenario 1: Resolution approach
- Scenario 2: Alternative approach

## Behavioral Patterns

### Analysis Approach
1. First step in analysis
2. Second step in analysis
3. Synthesis and recommendations

### Communication Style
- How this agent communicates
- Tone and terminology preferences
- Output formatting standards

## Integration Patterns

### With Other Agents
- **Agent A**: Complementary collaboration pattern
- **Agent B**: Sequential handoff pattern

### With MCP Servers
- **Server 1**: Primary usage pattern
- **Server 2**: Secondary usage pattern

## Examples

### Example 1: Typical Use Case
[Detailed example of agent behavior]

### Example 2: Complex Scenario
[Advanced example showing decision-making]
```

#### 4. Add Agent Tests

Validate agent behavior and integration:

```bash
touch tests/validation/test-my-agent.sh
```

### Testing Requirements

**ALL contributions must include tests that follow NO MOCKS principles.**

#### Test Requirements Checklist

- [ ] Tests run in Docker (isolated environment)
- [ ] No placeholder code or mock data
- [ ] Real examples with actual expected output
- [ ] Validation of YAML frontmatter structure
- [ ] Integration testing with other components
- [ ] Error handling verification
- [ ] Documentation completeness check

#### Running Tests Before Submission

```bash
# Run all tests
docker-compose -f tests/docker-compose.test.yml up --abort-on-container-exit

# Check results
cat tests/results/test-results.json | jq '.failed'
# Must output: 0
```

**Required**: All tests must pass before submitting pull request.

## Pull Request Process

### 1. Fork and Branch

```bash
# Fork repository on GitHub
# Clone your fork
git clone https://github.com/YOUR-USERNAME/shannon.git
cd shannon

# Create feature branch
git checkout -b feature/my-contribution
```

### 2. Make Changes

Follow the guides above for adding commands or agents.

### 3. Test Thoroughly

```bash
# Run full test suite
docker-compose -f tests/docker-compose.test.yml up --abort-on-container-exit

# Verify NO MOCKS compliance
docker-compose -f tests/docker-compose.test.yml run --rm test-no-mocks

# Check specific component
docker-compose -f tests/docker-compose.test.yml run --rm test-artifacts
```

### 4. Update Documentation

- Add entry to README.md command list
- Update CHANGELOG.md with your changes
- Include examples in your component documentation
- Add any new dependencies to INSTALLATION.md

### 5. Submit Pull Request

```bash
# Commit changes
git add .
git commit -m "Add [feature]: Brief description"

# Push to your fork
git push origin feature/my-contribution
```

Create pull request on GitHub with:
- **Title**: Clear, concise description
- **Description**:
  - What this adds/changes
  - Why it's needed
  - Test results (paste from test-results.json)
  - Screenshots/examples if applicable

### 6. PR Review Criteria

PRs are evaluated on:
- ✅ All tests pass (100%)
- ✅ NO MOCKS compliance verified
- ✅ Documentation complete and clear
- ✅ Examples are real and working
- ✅ Follows existing patterns and style
- ✅ Integration tested with existing components

## Code Standards (It's Markdown!)

Shannon is documentation, not code. Standards focus on clarity and consistency.

### Markdown Style

```markdown
# Headers use sentence case
## Not Title Case Like This

- Lists use consistent formatting
- Items are complete sentences when needed
- Or fragments when appropriate

**Bold** for emphasis on key terms.
*Italic* for subtle emphasis or terms.

Code blocks always specify language:
```yaml
key: value
```

Links use descriptive text: [installation guide](INSTALLATION.md)
Not: [click here](INSTALLATION.md)
```

### YAML Style

```yaml
# Use consistent indentation (2 spaces)
key: value
nested:
  key: value

# Lists with hyphens
items:
  - First item
  - Second item

# Use descriptive keys
triggers:
  - /command
  - keyword

# Not cryptic abbreviations
t:
  - /cmd
  - kw
```

### File Organization

```
shannon/
├── commands/          # One command per file
│   └── my-cmd.md
├── agents/            # One agent per file
│   └── my-agent.md
├── templates/         # Reusable patterns
│   └── template.md
└── tests/
    └── validation/    # One test file per component
        └── test-my-cmd.sh
```

### Naming Conventions

- **Files**: lowercase-with-hyphens.md
- **YAML keys**: snake_case_names
- **Headers**: Sentence case headers
- **Commands**: /lowercase-commands
- **Agents**: lowercase-agent-names

## Getting Help

### Questions About Contributing

- **General questions**: Open a GitHub Discussion
- **Specific issues**: Open a GitHub Issue
- **Documentation unclear**: Open an issue labeled "documentation"

### Before You Start

1. Read [INSTALLATION.md](INSTALLATION.md) to understand setup
2. Review existing commands and agents for patterns
3. Run tests locally to understand validation
4. Check open issues for contribution ideas

### Contribution Ideas

Looking for ways to contribute? Check:
- **GitHub Issues** labeled "good first issue"
- **Enhancement requests** from users
- **Documentation gaps** in existing components
- **Test coverage** opportunities

## Recognition

Contributors are recognized in:
- CHANGELOG.md for each release
- GitHub contributors page
- Individual file attribution in frontmatter

Thank you for contributing to Shannon!
