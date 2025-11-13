# Contributing to Shannon Framework

**Version**: 4.1.0
**Last Updated**: 2025-11-09

---

## Welcome Contributors!

Shannon Framework is open source and welcomes contributions. Whether you're fixing bugs, adding features, improving documentation, or creating new skills, your contributions help make AI development more rigorous.

---

## Quick Start for Contributors

### 1. Fork and Clone

```bash
# Fork on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/shannon-framework
cd shannon-framework
```

### 2. Install Locally for Testing

```bash
# In Claude Code:
/plugin marketplace add /path/to/shannon-framework
/plugin install shannon@shannon

# Restart Claude Code
```

### 3. Make Changes

Edit plugin files in root directory:
- Commands: `commands/`
- Skills: `skills/`
- Agents: `agents/`
- Hooks: `hooks/`
- Core patterns: `core/`

### 4. Test Your Changes

```bash
# Reinstall plugin to test
/plugin uninstall shannon@shannon
/plugin install shannon@shannon

# Restart Claude Code

# Test your changes
/shannon:status  # Verify Shannon loads
/your_new_command  # Test new features
```

### 5. Submit Pull Request

```bash
git checkout -b feature/your-feature-name
git add .
git commit -m "feat: description of your changes"
git push origin feature/your-feature-name

# Create PR on GitHub
```

---

## Contribution Areas

### High-Value Contributions

**1. New Skills**
- Domain-specific workflows
- Integration patterns
- Testing methodologies
- Analysis frameworks

**2. Enhanced Anti-Rationalization Patterns**
- Document new violation scenarios
- Add pressure test cases
- Expand enforcement mechanisms

**3. Additional Command Guides**
- Comprehensive examples (10-15 per command)
- Anti-patterns with Shannon counters
- Integration workflows

**4. Agent Enhancements**
- New specialized agents
- Enhanced agent prompts
- Agent coordination patterns

### Medium-Value Contributions

**5. Documentation Improvements**
- Clarifications and examples
- Troubleshooting scenarios
- Tutorial videos/walkthroughs

**6. MCP Integrations**
- New MCP recommendations
- Setup guides
- Fallback chain definitions

**7. Testing & Validation**
- Pressure test scenarios
- Validation scripts
- CI/CD integration

### Code Quality Standards

**Follow Shannon Principles**:
- Apply FORCED_READING_PROTOCOL to code you're changing
- Use Shannon's own tools (run /shannon:spec on your changes)
- Follow NO MOCKS for any tests you add
- Document anti-rationalization patterns you discover

**Commit Message Format**:
```
type(scope): description

Examples:
feat(skill): add performance-optimization skill
fix(hooks): correct PreCompact checkpoint timing
docs(commands): add /shannon:wave comprehensive guide
test(skills): add pressure test for using-shannon
```

**Types**: feat, fix, docs, test, refactor, chore

---

## Development Workflow

### For New Skills

1. **Use skill-creator skill**:
   ```
   Skill("skill-creator")
   # Follow the 6-step process
   ```

2. **Required Elements**:
   - YAML frontmatter (name, description, skill-type)
   - When to Use section
   - Anti-Rationalization section (if patterns exist)
   - Workflow with steps
   - Examples (minimum 2)
   - Success criteria

3. **Test Your Skill**:
   - RED test: Without skill, agent behavior
   - GREEN test: With skill, agent behavior
   - Verify behavioral difference

4. **Document in PR**:
   - What problem the skill solves
   - Evidence of need (baseline violation data)
   - Test results (RED vs GREEN)

### For Command Enhancements

1. **Follow existing pattern** (see commands/guides/):
   - Overview with core value
   - 10-15 comprehensive examples
   - Anti-patterns with Shannon counters
   - Integration workflows
   - Troubleshooting + FAQ

2. **Test command works**:
   - Install Shannon locally
   - Execute command
   - Verify expected behavior
   - Document actual vs expected

### For Hook Additions

1. **Read hooks/README.md** completely
2. **Follow hook development guide** (section in hooks/README.md)
3. **Test hook fires**:
   - Install locally
   - Trigger hook event
   - Verify hook executes
   - Verify decision enforcement (block/allow)

4. **Required**:
   - Python/Bash script in hooks/
   - Entry in hooks/hooks.json
   - Executable permissions (chmod +x)
   - Documentation in hooks/README.md

---

## Testing Requirements

**All contributions must include testing**:

**For Skills**:
- RED/GREEN comparison with sub-agents
- Same input for both tests
- Document behavioral difference
- Include pressure test scenario (if Iron Law)

**For Commands**:
- Example executions with outputs
- Error handling verification
- Integration with other commands

**For Hooks**:
- Hook fires on correct event
- Enforcement works (blocks when should block)
- Error handling graceful

**For Documentation**:
- All links validated (target files exist)
- Code examples tested
- Procedures followed step-by-step

---

## Review Process

### What We Look For

**Quality**:
- Follows Shannon principles
- Complete, not partial
- Tested, not theoretical
- Honest about limitations

**Documentation**:
- Clear examples
- Anti-patterns documented
- Integration explained
- Success criteria defined

**Testing**:
- Proper methodology (same inputs for comparisons)
- Real scenarios (pressure tests)
- Evidence included
- Results reproducible

### Review Timeline

- PRs reviewed within 1 week
- Feedback provided for improvements
- Approved PRs merged to main
- Contributors credited in CHANGELOG.md

---

## Community Guidelines

**Be Rigorous**:
- Shannon is for mission-critical development
- Maintain high quality standards
- Test thoroughly
- Document completely

**Be Honest**:
- Acknowledge gaps
- Don't overclaim
- Validate assertions
- Correct errors transparently

**Be Collaborative**:
- Provide constructive feedback
- Help other contributors
- Share learnings
- Improve together

---

## Getting Help

**Questions**:
- GitHub Discussions: https://github.com/krzemienski/shannon-framework/discussions
- Issues: https://github.com/krzemienski/shannon-framework/issues

**Documentation**:
- Read: README.md
- Architecture: SHANNON_SYSTEM_ARCHITECTURE_SYNTHESIS.md
- Hooks: hooks/README.md

**Testing**:
- Guide: SHANNON_PLUGIN_TESTING_GUIDE.md
- Pressure tests: PRESSURE_TEST_RESULTS.md

---

## Recognition

Contributors are recognized in:
- CHANGELOG.md (feature credits)
- README.md (contributor list)
- Git history (author attribution)

**Significant contributions** may result in:
- Maintainer status
- Direct commit access
- Shannon Framework team membership

---

## License

By contributing, you agree that your contributions will be licensed under MIT License.

---

## Thank You!

Every contribution makes Shannon better for mission-critical development.

**Questions?** Open an issue or discussion on GitHub.
**Ready to contribute?** Fork, code, test, and submit a PR!

---

**Shannon Framework Team**
**Version**: 4.1.0
**Contact**: info@shannon-framework.dev
