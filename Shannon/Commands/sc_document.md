---
name: sc:document
description: Enhanced documentation creation with structured templates and localization
category: documentation
priority: high
triggers: [document, write-docs, api-docs, readme, guide, manual, technical-writing]
auto_activate: true
activation_threshold: 0.6
tools: [Write, Read, Edit, Grep, Context7, Serena]
mcp_servers: [context7, serena, sequential]
wave_eligible: true
enhanced_from: SuperClaude /document command
shannon_enhancements: [structured-templates, localization-support, context7-patterns, wave-synthesis]
---

# /sc:document - Enhanced Documentation Command

> **Context Framework**: This command creates professional technical documentation with structured templates, localization support, and best practice patterns from Context7.

## Purpose

Creates comprehensive, audience-appropriate technical documentation including API references, user guides, README files, and localized content. Enhanced from SuperClaude with structured templates, localization workflows, and integration with Context7 documentation patterns.

## Triggers

**Automatic Detection**:
- Documentation keywords: document, write, readme, guide, manual, docs, api-docs
- File patterns: README*, CONTRIBUTING*, docs/*, wiki/*
- Explicit requests for technical writing or documentation
- Localization requests: translate, localize, i18n, l10n
- Post-implementation documentation needs
- Wave synthesis documentation requirements

**Manual Activation**:
```
/sc:document [target] [options]
/sc:document README --template getting-started
/sc:document api/users --format openapi
/sc:document guides/setup --lang es
/sc:document wave-synthesis --comprehensive
```

## Shannon V3 Enhancements

### 1. Structured Documentation Templates

**Template Library**:
- **README Templates**: project-overview, getting-started, installation, contributing
- **API Documentation**: openapi, rest-api, graphql, sdk-reference
- **User Guides**: tutorial, how-to, concept-guide, troubleshooting
- **Developer Docs**: architecture, setup, testing, deployment
- **Wave Documentation**: synthesis, phase-reports, validation-gates

**Template Selection Logic**:
```yaml
readme_templates:
  project_overview:
    sections: [description, features, installation, usage, contributing]
    audience: users
    length: comprehensive

  getting_started:
    sections: [quick-start, prerequisites, installation, first-steps]
    audience: new_users
    length: concise

api_templates:
  openapi:
    format: OpenAPI 3.0
    sections: [paths, schemas, security, examples]
    validation: automated

  rest_api:
    sections: [endpoints, authentication, request-response, errors]
    format: markdown
    examples: curl_and_code

guide_templates:
  tutorial:
    structure: step_by_step
    includes: [prerequisites, steps, verification, next_steps]

  how_to:
    structure: task_oriented
    includes: [goal, steps, validation, troubleshooting]
```

### 2. Localization Support

**Language Support**:
- English (en) - default
- Spanish (es) - native quality
- French (fr) - professional
- German (de) - technical precision
- Japanese (ja) - honorific awareness
- Chinese (zh) - simplified/traditional
- Portuguese (pt) - Brazilian/European
- Italian (it) - standard
- Russian (ru) - professional
- Korean (ko) - formality levels

**Localization Workflow**:
```yaml
localization_process:
  step_1_analysis:
    - Detect source language
    - Identify technical terms
    - Note cultural considerations
    - Mark non-translatable elements

  step_2_translation:
    - Professional translation
    - Technical accuracy preservation
    - Cultural adaptation
    - Formatting consistency

  step_3_validation:
    - Technical term consistency
    - Cultural appropriateness
    - Format integrity
    - Link/reference updates

  step_4_delivery:
    - Organized directory structure
    - Language-specific conventions
    - Metadata preservation
```

### 3. Context7 Pattern Integration

**Documentation Pattern Lookup**:
- Official framework documentation styles (React, Vue, Express, etc.)
- API documentation best practices
- Code example patterns
- Error message formatting
- Configuration documentation standards

**Pattern Application**:
```yaml
context7_integration:
  framework_docs:
    trigger: "framework documentation needed"
    action: "resolve-library-id → get-library-docs"
    usage: "apply official documentation patterns"

  api_patterns:
    trigger: "api documentation request"
    action: "lookup rest-api patterns"
    usage: "structure endpoints with examples"

  best_practices:
    trigger: "any documentation task"
    action: "retrieve documentation standards"
    usage: "ensure professional quality"
```

### 4. Wave Synthesis Documentation

**Comprehensive Wave Documentation**:
- Synthesis reports combining all wave findings
- Phase-by-phase progress documentation
- Validation gate records
- Implementation decisions and rationale
- Testing results and coverage
- Deployment procedures

## Sub-Agent Activation

### Primary: SCRIBE Agent

**Activation Triggers**:
- All `/sc:document` command executions
- Technical writing requests
- Localization requirements
- API documentation needs
- README creation/updates

**SCRIBE Responsibilities**:
- Apply structured documentation templates
- Ensure clarity and professionalism
- Manage localization workflows
- Coordinate with Context7 for patterns
- Write culturally-sensitive content
- Optimize for audience understanding

**SCRIBE Integration**:
```yaml
scribe_workflow:
  content_planning:
    - Analyze documentation scope
    - Select appropriate template
    - Identify target audience
    - Determine depth and detail

  content_creation:
    - Apply template structure
    - Write clear, professional content
    - Include code examples
    - Add visual elements (diagrams, tables)

  quality_assurance:
    - Technical accuracy review
    - Clarity validation
    - Cultural sensitivity check
    - Format consistency

  localization:
    - Translation management
    - Cultural adaptation
    - Technical term preservation
    - Format standardization
```

### Secondary: MENTOR Agent

**Activation Triggers**:
- Educational documentation (tutorials, guides)
- How-to documentation
- Concept explanations
- Learning-focused content

**MENTOR Responsibilities**:
- Structure educational content progressively
- Provide clear explanations with examples
- Anticipate learner questions
- Include practice exercises where appropriate
- Validate instructional clarity

## Execution Flow

### Phase 1: Analysis & Planning

**Step 1: Context Understanding**
```yaml
analysis:
  target_identification:
    - What needs documentation?
    - Existing content to enhance?
    - New documentation required?

  audience_analysis:
    - Technical level (beginner, intermediate, expert)
    - Use case (learning, reference, troubleshooting)
    - Cultural context (if localization needed)

  scope_definition:
    - Content depth required
    - Template selection
    - Language(s) needed
    - Delivery format
```

**Step 2: Template Selection**
- Match documentation type to appropriate template
- Consider audience and purpose
- Select localization strategy if applicable
- Plan Context7 pattern integration

**Tools**:
- Read: Review existing documentation and codebase
- Grep: Analyze code patterns and structures
- Context7 MCP: Lookup documentation patterns
- Sequential MCP: Structure complex documentation

### Phase 2: Content Creation

**Step 1: Structure Generation**
```yaml
structure_creation:
  apply_template:
    - Load selected template
    - Customize for specific context
    - Organize sections logically

  content_scaffolding:
    - Section headers
    - Placeholder content
    - Example placeholders
    - Reference markers
```

**Step 2: Content Writing**
```yaml
content_development:
  technical_writing:
    - Clear, concise language
    - Active voice preference
    - Technical accuracy
    - Appropriate detail level

  examples_integration:
    - Code examples with syntax highlighting
    - Real-world use cases
    - Error handling examples
    - Best practice demonstrations

  visual_elements:
    - Tables for structured data
    - Diagrams for concepts (when needed)
    - Screenshots (reference only)
    - Code snippets with comments
```

**Step 3: Context7 Pattern Application**
- Retrieve official documentation styles
- Apply framework-specific conventions
- Integrate best practice patterns
- Ensure consistency with ecosystem standards

**Tools**:
- Write: Create documentation files
- Edit: Refine existing documentation
- Context7 MCP: Apply documentation patterns
- Sequential MCP: Complex content structuring

### Phase 3: Localization (If Required)

**Step 1: Translation**
```yaml
translation_workflow:
  source_preparation:
    - Extract translatable text
    - Mark technical terms
    - Note cultural considerations

  translation_execution:
    - Professional language translation
    - Technical term preservation
    - Cultural adaptation
    - Format maintenance

  validation:
    - Translation accuracy
    - Technical correctness
    - Cultural appropriateness
```

**Step 2: Directory Organization**
```yaml
localization_structure:
  documentation_organization:
    docs/
    ├── en/           # English (default)
    │   ├── README.md
    │   ├── guides/
    │   └── api/
    ├── es/           # Spanish
    │   ├── README.md
    │   ├── guias/
    │   └── api/
    └── i18n/         # Translation resources
        ├── en.json
        └── es.json
```

**Tools**:
- Write: Create localized files
- Edit: Update existing localizations
- Serena MCP: Store localization patterns

### Phase 4: Quality Assurance

**Step 1: Technical Review**
- Verify technical accuracy
- Test code examples
- Validate links and references
- Check version compatibility

**Step 2: Clarity Review**
- Assess readability (Flesch-Kincaid)
- Verify logical flow
- Confirm audience appropriateness
- Check for jargon or complexity

**Step 3: Format Validation**
- Markdown syntax correctness
- Heading hierarchy consistency
- Code block formatting
- Link functionality

**Tools**:
- Read: Review generated documentation
- Grep: Validate cross-references
- Sequential MCP: Comprehensive quality check

### Phase 5: Delivery & Integration

**Step 1: File Organization**
- Place files in appropriate directories
- Update table of contents
- Create index pages if needed
- Configure navigation

**Step 2: Integration**
- Link from main documentation
- Update repository README links
- Configure documentation site (if applicable)
- Set up versioning (if needed)

**Step 3: Serena Persistence**
```yaml
memory_storage:
  documentation_patterns:
    - Successful template applications
    - Localization workflows
    - Audience preferences
    - Organizational conventions

  project_context:
    - Documentation structure
    - Localization coverage
    - Update frequency
    - Maintenance patterns
```

**Tools**:
- Write: Final file creation
- Serena MCP: Store documentation patterns

## Output Format

### Standard Documentation Output

```markdown
# [Documentation Title]

> Brief description of what this document covers

## Table of Contents
- [Section 1](#section-1)
- [Section 2](#section-2)

## Overview
[Clear overview of topic]

## Prerequisites
- Requirement 1
- Requirement 2

## Installation
```bash
# Step-by-step installation
```

## Usage
```javascript
// Clear, working code examples
```

## API Reference
### Method Name
**Description**: What this method does
**Parameters**:
- `param1` (type): Description
**Returns**: Return type and description
**Example**:
```javascript
// Usage example
```

## Troubleshooting
### Common Issue 1
**Problem**: Description
**Solution**: Steps to resolve

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)

## License
[License information]
```

### Wave Synthesis Documentation

```markdown
# Wave [N] Synthesis Report

## Overview
**Wave Duration**: [X hours]
**Phase**: [Phase name]
**Status**: ✅ Complete | ⚠️ Issues | ❌ Blocked

## Objectives
- [Objective 1]
- [Objective 2]

## Activities Completed
### [Activity Category]
- ✅ [Completed item]
- ✅ [Completed item]

## Deliverables
| Deliverable | Status | Location |
|-------------|--------|----------|
| [Item] | ✅ | [Path] |

## Technical Decisions
### [Decision Area]
**Decision**: [What was decided]
**Rationale**: [Why this approach]
**Alternatives Considered**: [Other options]

## Testing Results
**Test Coverage**: [X%]
**Test Type**: [Functional/Integration/E2E]
**Results**: [Summary]

## Issues & Resolutions
| Issue | Severity | Resolution |
|-------|----------|------------|
| [Description] | [High/Med/Low] | [How resolved] |

## Next Wave Preparation
- [Preparation item 1]
- [Preparation item 2]

## Validation Gate
✅ All validation criteria met
- [Criterion 1]
- [Criterion 2]
```

## Usage Examples

### Example 1: Project README Creation

```bash
/sc:document README --template project-overview

# Output:
# - Analyzes project structure and purpose
# - Generates comprehensive README.md with:
#   - Project description
#   - Features list
#   - Installation instructions
#   - Usage examples
#   - Contributing guidelines
#   - License information
```

### Example 2: API Documentation

```bash
/sc:document api/users --format rest-api

# Output:
# - Analyzes user API endpoints
# - Creates api/users.md with:
#   - Endpoint descriptions
#   - Request/response examples
#   - Authentication requirements
#   - Error responses
#   - Code examples in multiple languages
```

### Example 3: Localized User Guide

```bash
/sc:document guides/getting-started --lang es,fr,de

# Output:
# - Creates English version first
# - Translates to Spanish, French, German
# - Organizes in docs/[lang]/ structure
# - Maintains technical accuracy
# - Adapts cultural context
# - Preserves formatting
```

### Example 4: Wave Synthesis Documentation

```bash
/sc:document wave-synthesis --wave 3 --comprehensive

# Output:
# - Reads Serena memory for wave 3
# - Compiles all activities and decisions
# - Documents testing results
# - Records validation gate status
# - Creates synthesis report
# - Stores in docs/waves/wave_3_synthesis.md
```

## Best Practices

### Technical Writing Standards

**Clarity**:
- Use active voice
- Short, clear sentences
- Define technical terms
- Avoid jargon when possible

**Structure**:
- Logical section organization
- Progressive detail (overview → specifics)
- Clear headings and subheadings
- Table of contents for long docs

**Examples**:
- Include working code examples
- Show real use cases
- Provide before/after comparisons
- Comment code appropriately

**Consistency**:
- Follow project style guide
- Maintain terminology consistency
- Use consistent formatting
- Standardize code examples

### Localization Standards

**Translation Quality**:
- Professional language level
- Technical accuracy preserved
- Cultural appropriateness
- Natural phrasing (not literal translation)

**Technical Terms**:
- Preserve English technical terms when standard
- Translate only when local equivalent exists
- Maintain consistency across documents
- Provide glossary for ambiguous terms

**Cultural Adaptation**:
- Date/time format conventions
- Number formatting (1,000 vs 1.000)
- Address formats
- Currency symbols
- Cultural references

### Context7 Integration

**Pattern Application**:
- Always check official framework docs first
- Apply ecosystem conventions
- Match documentation style of frameworks used
- Ensure compatibility with framework versions

**Best Practice Lookup**:
- API documentation standards
- Error message formatting
- Configuration examples
- Testing documentation

## Integration with SuperClaude

### Persona Coordination

**Primary Persona**: SCRIBE
- Technical writing expertise
- Localization workflows
- Documentation templates
- Professional communication

**Supporting Persona**: MENTOR
- Educational content structuring
- Tutorial development
- Concept explanations
- Learning-focused documentation

### MCP Server Usage

**Context7 MCP** (Primary):
- Framework documentation patterns
- API reference styles
- Best practice examples
- Official documentation standards

**Serena MCP** (Mandatory):
- Store documentation patterns
- Maintain localization workflows
- Track documentation structure
- Preserve organizational conventions

**Sequential MCP** (Complex Docs):
- Structure comprehensive documentation
- Organize multi-section content
- Plan documentation strategy
- Coordinate complex localization

## Quality Standards

**Technical Accuracy**: 100%
- All code examples must work
- Technical details must be correct
- Version compatibility verified
- Links and references validated

**Clarity Score**: ≥80 (Flesch-Kincaid)
- Appropriate for target audience
- Clear and concise language
- Logical information flow
- Well-structured content

**Completeness**: 100%
- All required sections included
- No placeholder text in final docs
- Examples provided for all features
- Cross-references complete

**Localization Quality** (if applicable):
- Professional translation level
- Technical accuracy preserved
- Cultural appropriateness validated
- Format consistency maintained

---

**Version**: 1.0.0 (Shannon V3)
**Enhanced From**: SuperClaude /document command
**Category**: Documentation & Communication
**Priority**: High