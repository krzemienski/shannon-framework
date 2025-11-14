# Shannon SDK Integration

This module provides integration with the Claude Agent SDK for wave-based agent orchestration.

## Components

### AgentFactory (`agent_factory.py`)

Builds Claude Agent SDK `AgentDefinition` objects for wave task execution.

**Key Features:**
- Loads and applies prompt templates
- Injects runtime context (spec analysis, previous waves)
- Validates agent definitions against WaveCoordinator contract
- Supports custom models and configurations

**Usage:**

```python
from shannon.sdk.agent_factory import AgentFactory
from shannon.storage.models import WaveTask

# Create factory
factory = AgentFactory()

# Define task
task = WaveTask(
    task_id="wave_1_task_1",
    name="Build Config",
    agent_type="infrastructure-specialist",
    description="Create pyproject.toml with Poetry",
    estimated_minutes=30,
    deliverables=["pyproject.toml"]
)

# Prepare context
context = {
    "previous_waves": "Session initialized",
    "spec_sections": "Section 7.1: Configuration",
    "save_key": "wave_1_agent_1_complete"
}

# Build agent
agent_def = factory.build_agent(
    agent_type="infrastructure-specialist",
    task=task,
    context=context
)

# agent_def is ready for SDK execution
```

### PromptBuilder (`prompt_builder.py`)

Loads prompt templates and injects runtime context.

**Key Features:**
- Template loading from markdown files
- Template caching for performance
- Context placeholder injection
- Validation formatting
- Task detail formatting

**Template Placeholders:**
- `{task_description}` - Task description from WaveTask
- `{task_details}` - Formatted task metadata
- `{wave_context}` - Previous wave results
- `{spec_sections}` - Relevant specification sections
- `{validation}` - Validation criteria
- `{save_key}` - Memory key for results
- `{task_name}` - Task name
- `{task_id}` - Task identifier
- `{agent_type}` - Agent type

**Usage:**

```python
from shannon.sdk.prompt_builder import PromptBuilder

# Create builder
builder = PromptBuilder()

# Load template directly
template = builder.load_template("python-expert")

# Or build complete prompt with context
prompt = builder.build_prompt(
    template_name="python-expert",
    task=task,
    context=context
)

# List available templates
templates = builder.list_available_templates()
```

## Available Templates

The following prompt templates are available in `templates/`:

1. **python-expert.md** - Python development with production quality standards
2. **frontend-builder.md** - React/TypeScript frontend development
3. **backend-builder.md** - Backend API and database development
4. **testing-specialist.md** - Comprehensive testing and coverage
5. **infrastructure-specialist.md** - Configuration and deployment
6. **data-storage-specialist.md** - Data modeling and persistence

## Template Structure

All templates follow this structure:

```markdown
# Shannon Wave Agent: {task_name}

## MANDATORY CONTEXT LOADING
{wave_context}
{spec_sections}
{task_details}

## YOUR TASK
{task_description}

### Requirements
[Agent-specific requirements]

### Code Quality Standards
[Quality expectations]

### Testing
[Testing requirements]

## VALIDATION
{validation}

## DELIVERABLES CHECKLIST
[Checklist items]

## SAVE RESULTS
write_memory("{save_key}", {...})

## NOTES
[Agent-specific notes]
```

## Creating Custom Templates

To create a new agent template:

1. Create a markdown file in `src/shannon/sdk/templates/`
2. Use the standard template structure above
3. Include all required placeholders
4. Document agent-specific requirements
5. Add to agent type mappings in WaveCoordinator

Example:

```markdown
# Shannon Wave Agent: {task_name}

You are a [Role] agent...

## MANDATORY CONTEXT LOADING
{wave_context}
{spec_sections}
{task_details}

## YOUR TASK
{task_description}

[Role-specific requirements]

## VALIDATION
{validation}

## SAVE RESULTS
write_memory("{save_key}", {{...}})
```

## Contract: WaveCoordinator ↔ AgentFactory

From TECHNICAL_SPEC.md Section 11.3:

**AgentFactory MUST return:**
- Valid `AgentDefinition` object
- `.description` attribute (str)
- `.prompt` attribute (str with context injected)
- Prompt containing task description
- Prompt containing context (spec analysis, previous waves)

**Validation is automatic:**
- `build_agent()` validates all requirements
- Raises `ValueError` if contract violated
- Logs warnings for missing optional sections

## Error Handling

```python
from shannon.sdk.agent_factory import AgentFactory

factory = AgentFactory()

# Template not found
try:
    agent_def = factory.build_agent("unknown-type", task, context)
except FileNotFoundError as e:
    print(f"Template missing: {e}")
    # Available: factory.prompt_builder.list_available_templates()

# SDK not installed
try:
    agent_def = factory.build_agent("python-expert", task, context)
except ImportError:
    print("Install Claude SDK: pip install claude-agent-sdk")

# Invalid placeholder
try:
    prompt = builder.build_prompt("bad-template", task, context)
except ValueError as e:
    print(f"Template error: {e}")
```

## Testing

Run SDK integration tests:

```bash
poetry run pytest tests/test_sdk_integration.py -v
```

Test coverage:
- PromptBuilder: 11 tests
- AgentFactory: 8 tests  
- Integration: 2 tests
- Total: 21 tests

## Dependencies

Required:
- `claude-agent-sdk` (optional - graceful fallback if not installed)
- `pydantic` (for WaveTask model)

Install:
```bash
pip install claude-agent-sdk
# or
poetry add claude-agent-sdk
```

## Implementation Notes

1. **Template Caching**: Templates are cached after first load for performance
2. **Graceful Degradation**: System works without SDK (raises error on build_agent)
3. **Type Safety**: Full type hints with TYPE_CHECKING guards
4. **Logging**: Comprehensive logging at INFO and DEBUG levels
5. **Validation**: Contract validation happens automatically in build_agent()

## Next Steps

This implementation supports:
- Wave 3 Agent 3: WaveCoordinator integration
- Wave 3 Agent 4: Wave execution and monitoring
- Production agent orchestration with real Claude SDK

## See Also

- TECHNICAL_SPEC.md Section 7.3: Layer 3 SDK Integration
- TECHNICAL_SPEC.md Section 11.3: WaveCoordinator ↔ AgentFactory Contract
- Wave 1 Complete: Infrastructure and Storage
- Wave 2 Complete: Core Analysis Engine
