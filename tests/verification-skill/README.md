# Shannon Execution Verifier - Usage Guide

**Comprehensive verification framework for Shannon Framework execution quality and completeness.**

## Overview

The Shannon Execution Verifier skill provides a systematic approach to validating that Shannon Framework executions meet production standards. It ensures:

- ✅ **Complete implementation** - All expected domains and features built
- ✅ **Runtime functionality** - Services start and respond correctly
- ✅ **Integration quality** - Cross-domain flows work end-to-end
- ✅ **Testing coverage** - Functional, integration, and cross-platform tests pass
- ✅ **Production readiness** - Deployable artifacts with proper configuration

## Directory Structure

```
shannon-execution-verifier/
├── SKILL.md                    # Main skill specification
├── README.md                   # This file - usage guide
├── scenarios/                  # Test scenario specifications
│   ├── prd_creator.yaml       # Full-stack web app (React + FastAPI + PostgreSQL)
│   ├── claude_code_expo.yaml  # Mobile app (React Native + Express + WebSocket)
│   ├── repo_nexus.yaml        # iOS app (React Native + FastAPI + PostgreSQL + Redis)
│   └── shannon_cli.yaml       # CLI tool (Python + Click + Claude SDK)
└── flow-specs/                 # Expected execution flows
    └── sh_wave_flow.yaml      # Shannon /shannon:wave command flow specification
```

## Scenario Files

### What are Scenario Files?

Scenario files are **declarative YAML specifications** that define:

1. **What should be built** - Complete technical requirements
2. **Expected execution flow** - Skills, agents, MCPs invoked
3. **Expected artifacts** - Files that must be created with required content
4. **Runtime verification** - How to start services and verify they work
5. **Functional tests** - API endpoints, UI interactions, command-line operations
6. **Integration tests** - Cross-domain flows and data synchronization
7. **Cross-platform tests** - Viewports, devices, browsers, shells
8. **Performance tests** - Response times, resource usage thresholds
9. **Validation criteria** - Must-pass, should-pass, nice-to-have requirements

### Available Scenarios

#### 1. PRD Creator (`prd_creator.yaml`)

**Type:** Full-stack web application
**Complexity:** High
**Duration:** 45-60 minutes

**Architecture:**
- Frontend: React + TypeScript + TailwindCSS + shadcn/ui
- Backend: FastAPI + SQLAlchemy + Alembic
- Database: PostgreSQL + Redis
- Features: Real-time collaboration, AI-powered PRD generation, WebSocket updates

**Use this scenario to verify:**
- Multi-domain orchestration (frontend + backend + database)
- Real-time features with WebSocket
- AI integration with Claude API
- Authentication and authorization flows
- File upload and export functionality

#### 2. Claude Code Expo (`claude_code_expo.yaml`)

**Type:** Mobile event management app
**Complexity:** High
**Duration:** 50-70 minutes

**Architecture:**
- Mobile: React Native (iOS + Android)
- Backend: Express + Socket.io
- Database: MongoDB + Redis
- Features: QR check-in, real-time updates, push notifications, offline sync

**Use this scenario to verify:**
- React Native mobile app implementation
- Cross-platform compatibility (iOS + Android)
- Native module integration (QR scanner, biometrics)
- Real-time WebSocket features
- Offline-first architecture with sync

#### 3. Repo Nexus (`repo_nexus.yaml`)

**Type:** iOS repository manager
**Complexity:** Very High
**Duration:** 60-90 minutes

**Architecture:**
- Mobile: React Native (iOS only) with native modules
- Backend: FastAPI + async/await
- Database: PostgreSQL + Redis + ElasticSearch
- Features: Code search, AI insights, widgets, Apple Watch companion

**Use this scenario to verify:**
- iOS-specific features (Face ID, widgets, haptics)
- Complex native bridge implementations
- ElasticSearch integration for code search
- Advanced UI (syntax highlighting, diff viewer)
- Multi-platform sync and search

#### 4. Shannon CLI (`shannon_cli.yaml`)

**Type:** Command-line tool
**Complexity:** Medium
**Duration:** 30-40 minutes

**Architecture:**
- Core: Python + Click + Rich
- API: Claude SDK integration
- Config: YAML/TOML with Pydantic validation
- Features: Interactive prompts, shell completion, plugin system

**Use this scenario to verify:**
- CLI command structure and help text
- Interactive prompt flows
- Configuration management
- API integration and error handling
- Cross-platform compatibility
- Testing with pytest and Click testing utilities

## Flow Specification Files

### What are Flow Specs?

Flow specifications define **expected execution patterns** for Shannon commands. They document:

1. **Command signature** - Arguments, flags, options
2. **Execution phases** - Step-by-step flow with timing
3. **Skill invocation patterns** - Which skills should be called and when
4. **Agent coordination** - How agents orchestrate parallel work
5. **MCP usage patterns** - When and how MCPs are utilized
6. **Error handling strategies** - Recovery procedures for failures
7. **Output artifacts** - Required and optional files
8. **Success criteria** - Validation checklist

### Available Flow Specs

#### 1. Shannon Wave Flow (`sh_wave_flow.yaml`)

Defines the complete execution flow for the `/shannon:wave` command:

**Phases:**
1. **Initialization** (2-5 min) - Load spec, prime session, discover skills
2. **Analysis & Planning** (5-10 min) - Architect and plan implementation
3. **Implementation** (20-60 min) - Parallel domain execution
4. **Integration** (10-20 min) - Cross-domain integration
5. **Testing** (10-15 min) - Unit, integration, E2E tests
6. **Verification** (5-10 min) - Runtime checks and functional tests
7. **Reporting** (2-5 min) - Generate documentation and handoff

**Use this spec to verify:**
- Correct phase ordering and timing
- Appropriate skill selection for project type
- Parallel vs sequential execution patterns
- Agent coordination strategies
- MCP usage at decision points
- Error recovery mechanisms

## How to Use This Skill

### 1. As a Verification Framework

After a Shannon execution completes, use the appropriate scenario file to verify quality:

```bash
# Example verification workflow
/skill shannon-execution-verifier

# The skill will:
# 1. Analyze the generated artifacts
# 2. Compare against scenario expectations
# 3. Run functional tests
# 4. Execute integration tests
# 5. Generate verification report
```

### 2. As a Testing Specification

Use scenarios as test specifications for automated testing:

```python
# Example: Load scenario and run tests
from shannon_verifier import ScenarioLoader, TestRunner

scenario = ScenarioLoader.load('scenarios/prd_creator.yaml')
runner = TestRunner(scenario)

# Run all tests
results = runner.run_all_tests()

# Or run specific test suites
results = runner.run_functional_tests()
results = runner.run_integration_tests()
results = runner.run_performance_tests()
```

### 3. As Implementation Requirements

Use scenarios as comprehensive requirements during implementation:

- **Architects**: Reference expected_flow and expected_artifacts
- **Developers**: Implement against functional_tests specifications
- **QA Engineers**: Execute validation_criteria as acceptance tests

### 4. As Documentation

Scenarios serve as living documentation of:

- Complete technical requirements for each project type
- Expected behavior and verification procedures
- Performance benchmarks and quality thresholds

## Scenario File Structure

Each scenario YAML contains these sections:

```yaml
metadata:
  name: scenario_name
  description: "What this scenario tests"
  architecture: "Tech stack summary"
  complexity: low|medium|high|very_high
  domains: [frontend, backend, database, ...]
  estimated_duration: "Time estimate"

specification:
  user_request: |
    Original user requirements
  technical_requirements:
    domain_name:
      - "Requirement 1"
      - "Requirement 2"

expected_flow:
  skills_invoked:
    - name: skill_name
      phase: phase_name
      expected_output: "What skill produces"

  agents_invoked:
    - name: agent_name
      trigger: "When agent activates"
      expected_actions: [...]

  mcps_used:
    - name: mcp_name
      usage: "How MCP is used"

expected_artifacts:
  directory_structure: |
    project/
    ├── domain1/
    └── domain2/

  domain_files:
    required:
      - path: "path/to/file"
        must_contain: ["code pattern 1", "code pattern 2"]

runtime_verification:
  services:
    - name: "Service Name"
      check_command: "verification command"
      expected_status: "expected result"

  startup_sequence:
    - step: "description"
      command: "command to run"
      wait_seconds: N

functional_tests:
  api_endpoints:
    - name: "test name"
      method: GET|POST|PUT|DELETE
      url: "endpoint URL"
      headers: {...}
      body: {...}
      expected_status: 200
      expected_body_contains: [...]

  ui_interactions:
    playwright_actions:
      - name: "interaction name"
        steps:
          - action: "action type"
            selector: "CSS selector"
            value: "input value"

integration_tests:
  cross_domain_flows:
    - name: "flow name"
      description: "what the flow tests"
      steps:
        - domain: domain_name
          action: "what happens"
          verification: "how to verify"

cross_platform_tests:
  viewports: [...]
  browsers: [...]
  devices: [...]
  shells: [...]

performance_tests:
  metrics:
    - name: "metric name"
      measurement: "what to measure"
      max_response_time_ms: N

validation_criteria:
  must_pass: [...]
  should_pass: [...]
  nice_to_have: [...]
```

## Best Practices

### When Creating Scenarios

1. **Be Comprehensive** - Cover all expected behaviors and edge cases
2. **Use Real Requirements** - Base on actual Shannon executions
3. **Define Clear Criteria** - Make validation criteria unambiguous
4. **Include Examples** - Provide concrete API requests, commands, interactions
5. **Specify Timing** - Include performance thresholds and timeouts
6. **Document Failures** - Specify expected error handling

### When Using Scenarios

1. **Start with Dry Run** - Use `--dry-run` to understand the verification plan
2. **Run Incrementally** - Verify each phase as implementation progresses
3. **Collect Evidence** - Save logs, screenshots, test results
4. **Iterate on Failures** - Use verification failures to improve implementation
5. **Update Scenarios** - Keep scenarios in sync with Shannon Framework evolution

### When Extending

1. **Follow the Template** - Use existing scenarios as templates
2. **Cover New Patterns** - Add scenarios for new project types
3. **Test Thoroughly** - Validate scenarios against real Shannon executions
4. **Document Rationale** - Explain why specific tests are included
5. **Version Control** - Track scenario changes with the framework

## Integration with Shannon Framework

### Automatic Invocation

Shannon Framework will automatically invoke this skill when:

- User requests verification: `/shannon:verify`
- Shannon Wave completes with `--verify` flag
- Quality gates are configured in session

### Manual Invocation

Invoke manually for ad-hoc verification:

```bash
/skill shannon-execution-verifier
```

Then specify:
- Scenario to use
- Tests to run
- Report format

### CI/CD Integration

Integrate into automated pipelines:

```yaml
# .github/workflows/verify-shannon.yml
- name: Verify Shannon Execution
  run: |
    python verify.py \
      --scenario scenarios/prd_creator.yaml \
      --artifacts ./output \
      --report junit
```

## Troubleshooting

### Scenario Validation Errors

**Error:** "Invalid scenario structure"
- Check YAML syntax with `yamllint`
- Validate against scenario schema
- Reference working scenarios for structure

**Error:** "Missing required fields"
- Ensure all required top-level keys present
- Check that file paths use correct format
- Verify test specifications are complete

### Runtime Verification Failures

**Error:** "Service failed to start"
- Check service logs for root cause
- Verify dependencies installed
- Ensure ports available
- Review startup sequence ordering

**Error:** "Tests failed"
- Examine test output for specific failures
- Verify expected vs actual behavior
- Check if implementation matches scenario
- Update scenario if requirements changed

### Integration Test Failures

**Error:** "Cross-domain flow failed"
- Verify each domain works independently
- Check integration points (APIs, databases)
- Validate configuration (env vars, URLs)
- Test with manual integration steps

## Contributing

To add new scenarios or improve existing ones:

1. **Create scenario file** in `scenarios/` directory
2. **Follow naming convention**: `project_type.yaml`
3. **Use existing scenarios as templates**
4. **Test thoroughly** against real Shannon executions
5. **Update this README** with scenario details
6. **Submit PR** with rationale and test results

## Related Documentation

- [Shannon Framework README](../../shannon-plugin/README.md)
- [Shannon V4.1 Summary](../../SHANNON_V4.1_FINAL_SUMMARY.md)
- [Shannon V5 Plan](../../SHANNON_V5_FUNCTIONAL_TESTING_PLAN.md)

## Version History

**v1.0.0** (2025-01-09)
- Initial release with 4 comprehensive scenarios
- Complete verification framework
- Shannon Wave flow specification
- Integration with Shannon Framework v4.1+

---

**Need help?** Invoke the skill and ask questions about verification procedures, scenario structure, or how to add custom test cases.
