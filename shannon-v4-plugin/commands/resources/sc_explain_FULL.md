# /sc:explain - Enhanced Educational Explanation Command - Full Documentation

> This is the complete reference loaded on-demand (Tier 2)

# /sc:explain - Enhanced Educational Explanation Command

**Command Identity**: Structured educational explanation engine with progressive learning paths, Context7 integration, and cross-wave knowledge preservation

**Enhancement Type**: Enhanced from SuperClaude's /explain command with systematic teaching patterns, Shannon context awareness, and MCP coordination

**Base Command**: SuperClaude `/explain [topic] [flags]`

**Core Philosophy**: "Understanding enables independence | Progressive scaffolding builds capability | Methodology matters more than answers"

---

## 1. Command Overview

### Purpose Statement
Transform complex technical concepts into accessible, structured learning experiences through systematic knowledge transfer, progressive complexity layering, and context-aware educational content.

### Shannon V3 Enhancements

**1. Structured Explanation Framework**:
- 5-section progressive learning template
- Mental model formation with analogies
- Layered complexity (basic → intermediate → advanced)
- Real-world examples with inline commentary

**2. Context7 Integration**:
- Official documentation patterns for libraries/frameworks
- Version-specific API references and best practices
- Curated code examples from authoritative sources
- Pattern validation against official guidelines

**3. Progressive Learning Paths**:
- Skill level assessment and adaptation
- Prerequisite knowledge identification
- Learning checkpoint validation
- Next-step recommendations

**4. Cross-Wave Knowledge**:
- Reference previous explanations from wave memory
- Build on established mental models
- Maintain learning continuity across sessions
- Link explanations to project context

**5. Multi-Format Output**:
- Comprehensive explanations for deep learning
- Quick reference cards for rapid lookup
- Interactive examples for hands-on learning
- Visual diagrams for system understanding

### Command Signature
```
/sc:explain <topic> [flags] [@files]
```

**Parameters**:
- `<topic>` (required): Concept, technology, pattern, or system to explain
- `[flags]` (optional): Behavior modifiers for output format and depth
- `[@files]` (optional): Context files for project-specific explanations

---

## 2. Usage Patterns

### Basic Usage
```bash
/sc:explain "React hooks"
# Comprehensive explanation with examples, analogies, common mistakes

/sc:explain "event loop" --detailed
# Deep dive with advanced concepts and edge cases

/sc:explain "dependency injection" --beginner
# Simplified explanation focused on fundamentals
```

### Context-Aware Explanations
```bash
/sc:explain @auth.ts
# Explain the authentication pattern used in this specific file

/sc:explain "state management" @src/store/
# Explain state management in context of this project's implementation

/sc:explain "API design" @api_spec.yaml
# Explain API patterns with reference to this specification
```

### Learning Path Generation
```bash
/sc:explain "microservices" --learning-path
# Generate structured curriculum from beginner to advanced

/sc:explain "TypeScript" --prerequisites
# Identify prerequisite knowledge needed before learning TypeScript

/sc:explain "React" --roadmap
# Create learning roadmap with milestones and checkpoints
```

### Format Variations
```bash
/sc:explain "closures" --quick-ref
# Generate concise reference card for quick lookup

/sc:explain "async/await" --interactive
# Create interactive examples with step-by-step execution

/sc:explain "REST API" --visual
# Include architectural diagrams and visual representations

/sc:explain "OAuth 2.0" --comparison
# Compare with alternatives and explain trade-offs
```

---

## 3. Execution Flow

### Phase 1: Topic Analysis & Context Loading
```yaml
Step_1_Topic_Classification:
  action: "Analyze topic for domain, complexity, and learning level"
  tools: [Sequential MCP]
  output: "Domain classification, complexity score, prerequisite map"

Step_2_Context_Loading:
  action: "Load relevant context from Serena memory"
  tools: [Serena MCP]
  operations:
    - "search_nodes(query=topic)"
    - "read_memory('previous_explanations')"
    - "read_memory('project_context')"
  output: "Prior explanations, project patterns, user learning history"

Step_3_Framework_Discovery:
  action: "Identify if Context7 has official documentation"
  tools: [Context7 MCP]
  operations:
    - "resolve-library-id(libraryName=topic)"
    - "get-library-docs(context7CompatibleLibraryID, topic=subtopic)"
  output: "Official patterns, API references, version-specific docs"
  conditional: "Only if topic is library/framework"
```

### Phase 2: Explanation Structure Generation
```yaml
Step_1_Mental_Model:
  action: "Create core mental model and analogy"
  criteria:
    - "Single-sentence essence of concept"
    - "Real-world analogy for intuitive understanding"
    - "Visual representation if beneficial"

Step_2_Progressive_Layering:
  action: "Structure explanation in complexity layers"
  layers:
    basic: "Suitable for beginners, no prerequisites"
    intermediate: "Technical terminology, common patterns"
    advanced: "Implementation details, edge cases, optimization"

Step_3_Example_Creation:
  action: "Generate practical examples with inline commentary"
  requirements:
    - "Minimum 2 examples: common use case + real-world scenario"
    - "Inline comments explaining each significant line"
    - "Runnable code when applicable"
    - "Context7 patterns when available"

Step_4_Mistake_Identification:
  action: "Document common mistakes and solutions"
  sources:
    - "Context7 best practices"
    - "Sequential reasoning about error patterns"
    - "Previous wave learnings from Serena"

Step_5_Further_Learning:
  action: "Recommend next steps and advanced resources"
  output:
    - "Prerequisites if knowledge gaps exist"
    - "Next logical concepts to learn"
    - "Advanced topics for depth"
    - "Official documentation links"
```

### Phase 3: Output Generation & Preservation
```yaml
Step_1_Format_Application:
  action: "Apply requested output format"
  formats:
    comprehensive: "Full 5-section structured explanation"
    quick_ref: "Condensed reference card format"
    interactive: "Step-by-step walkthrough with examples"
    visual: "Diagrams and architectural representations"
    comparison: "Side-by-side with alternatives"

Step_2_Quality_Validation:
  action: "Validate explanation quality"
  criteria:
    - "Clarity: Accessible to target skill level"
    - "Completeness: Covers essential aspects"
    - "Accuracy: Validated against Context7 where applicable"
    - "Practicality: Includes actionable examples"

Step_3_Context_Preservation:
  action: "Save explanation to Serena for future reference"
  tools: [Serena MCP]
  operations:
    - "write_memory('explanation_[topic]', explanation_content)"
    - "create_entities([{name: topic, type: 'concept', observations: [key_points]}])"
    - "create_relations([{from: topic, to: related_concepts, type: 'prerequisite'}])"
```

---

## 4. Sub-Agent Integration

### Primary: MENTOR Agent

**Activation**: Automatic for all /sc:explain commands

**Responsibilities**:
- Educational content structure and pedagogy
- Progressive scaffolding based on learner assessment
- Learning path design and prerequisite identification
- Knowledge transfer methodology application

**Integration Pattern**:
```yaml
MENTOR_Workflow:
  step_1: "Assess user's current knowledge level"
  step_2: "Design explanation structure for target level"
  step_3: "Create mental models and analogies"
  step_4: "Generate progressive complexity layers"
  step_5: "Validate clarity and completeness"
  step_6: "Recommend learning progression"
```

**Context Requirements**:
- Previous explanations from Serena memory
- User's learning history and knowledge level
- Project context for relevance
- Phase-specific educational needs

### Secondary: ANALYST Agent

**Activation**: For technical concept analysis and pattern identification

**Responsibilities**:
- Technical accuracy validation
- Pattern recognition in code examples
- Complexity assessment and scoring
- Edge case identification

**Integration Pattern**:
```yaml
ANALYST_Support:
  technical_validation:
    - "Verify explanation accuracy"
    - "Identify technical edge cases"
    - "Assess complexity appropriately"

  pattern_analysis:
    - "Extract patterns from context files"
    - "Compare with best practices"
    - "Identify anti-patterns to warn against"
```

### Tertiary: SCRIBE Agent

**Activation**: For documentation formatting and clarity optimization

**Responsibilities**:
- Professional documentation formatting
- Message clarity and cognitive load optimization
- Structured content organization
- Audience-appropriate language

---

## 5. MCP Server Coordination

### Context7 MCP (Primary for Frameworks)

**Use Case**: Official documentation for libraries, frameworks, APIs

**Operations**:
```yaml
resolve_library_id:
  input: "Library or framework name from topic"
  output: "Context7-compatible library ID"
  example: "react → /facebook/react"

get_library_docs:
  input: "Library ID + specific topic focus"
  output: "Official documentation, patterns, examples"
  example: "get-library-docs('/facebook/react', topic='hooks')"
```

**Integration Pattern**:
1. Detect if topic is library/framework
2. Resolve to Context7 library ID
3. Fetch relevant official documentation
4. Extract patterns and examples
5. Incorporate into explanation with attribution
6. Validate explanation against official guidelines

**Fallback**: If library not in Context7, use WebSearch for official docs

### Sequential MCP (Primary for Complex Reasoning)

**Use Case**: Multi-step concept breakdown, systematic analysis

**Operations**:
```yaml
concept_decomposition:
  process: "Break complex topic into teachable components"
  output: "Hierarchical concept map with dependencies"

analogy_generation:
  process: "Create relatable real-world parallels"
  output: "Multiple analogy candidates with evaluation"

mistake_analysis:
  process: "Systematic identification of common errors"
  output: "Error patterns with root causes and solutions"
```

**Integration Pattern**:
1. Submit topic to Sequential for decomposition
2. Generate structured reasoning chain
3. Extract mental models and analogies
4. Identify learning checkpoints
5. Create progressive complexity layers
6. Validate logical flow and completeness

### Serena MCP (Context Preservation)

**Use Case**: Save explanations, track learning history, maintain continuity

**Operations**:
```yaml
save_explanation:
  action: "write_memory('explanation_[topic]', content)"
  purpose: "Future reference and building on prior knowledge"

track_learning:
  action: "create_entities([{name: topic, type: 'concept'}])"
  purpose: "Map knowledge graph for learning path optimization"

link_concepts:
  action: "create_relations([{from: A, to: B, type: 'prerequisite'}])"
  purpose: "Establish learning dependencies and progression"
```

---

## 6. Output Formats

### Comprehensive Explanation (Default)
```markdown
# [Topic Name] - Educational Explanation

## Core Idea (Mental Model)
[Single-sentence essence]

**Analogy**: [Real-world parallel]

## Fundamental Principles
1. [Key principle 1]
2. [Key principle 2]
3. [Key principle 3]

## How It Works (Progressive Detail)

### Basic Level
[Simplified explanation for beginners]

### Intermediate Level
[Technical details with terminology]

### Advanced Level
[Implementation specifics and edge cases]

## Practical Examples

### Example 1: [Common Use Case]
```[language]
[Code with inline comments]
```
**Explanation**: [Line-by-line walkthrough]

### Example 2: [Real-World Scenario]
[Production context application]

## Common Mistakes & Solutions

**Mistake 1**: [Error description]
- **Why It Happens**: [Root cause]
- **Solution**: [How to fix]

**Mistake 2**: [Error description]
- **Why It Happens**: [Root cause]
- **Solution**: [How to fix]

## Further Learning

**Prerequisites**: [Required knowledge if gaps exist]
**Next Steps**: [Logical next concepts]
**Advanced Topics**: [Depth expansion]
**Resources**: [Official docs, authoritative sources]

---
*Explained by MENTOR agent | Shannon Framework V3*
```

### Quick Reference Card
```markdown
# [Topic] - Quick Reference

## Key Concept
[1-2 sentence summary]

## Essential Syntax/Pattern
```[language]
[Minimal working example]
```

## Common Use Cases
1. [Use case 1]: `[code snippet]`
2. [Use case 2]: `[code snippet]`

## Watch Out For
- [Common mistake 1]
- [Common mistake 2]

## Learn More
[Official docs link]
```

### Learning Path Format
```markdown
# Learning Path: [Topic]

## Prerequisites
- [Prerequisite 1]: [Why needed]
- [Prerequisite 2]: [Why needed]

## Stage 1: Fundamentals
**Goal**: [Learning objective]
**Concepts**: [List of concepts]
**Practice**: [Exercises]
**Validation**: [How to know you're ready]

## Stage 2: Intermediate
**Goal**: [Learning objective]
**Concepts**: [List of concepts]
**Practice**: [Exercises]
**Validation**: [How to know you're ready]

## Stage 3: Advanced
**Goal**: [Learning objective]
**Concepts**: [List of concepts]
**Practice**: [Exercises]
**Validation**: [How to know you're ready]

## Capstone Project
[Real-world project to demonstrate mastery]
```

---

## 7. Command Flags

### Depth Control
```bash
--beginner        # Focus on fundamentals, avoid advanced concepts
--intermediate    # Balance basics and technical details
--advanced        # Deep dive with edge cases and optimization
--detailed        # Maximum depth across all complexity levels
```

### Format Control
```bash
--quick-ref       # Condensed reference card format
--interactive     # Step-by-step walkthrough with examples
--visual          # Include diagrams and architectural views
--comparison      # Compare with alternatives and explain trade-offs
--learning-path   # Generate structured curriculum
```

### Context Control
```bash
--project-context # Explain in context of current project patterns
--prerequisites   # Focus on identifying required prior knowledge
--roadmap         # Create learning milestone progression
--examples-only   # Focus heavily on practical code examples
```

### Integration Control
```bash
--context7        # Prioritize official documentation sources
--no-analogy      # Skip analogies, focus on technical accuracy
--save-learning   # Explicitly save to Serena for future reference
```

---

## 8. Examples

### Example 1: Basic Concept Explanation
```bash
/sc:explain "closures"
```

**Output**: Comprehensive explanation with mental model ("functions that remember their environment"), progressive layering (basic → intermediate → advanced), practical examples, common mistakes, and further learning recommendations.

### Example 2: Framework-Specific Explanation
```bash
/sc:explain "React hooks" --context7
```

**Output**: Explanation using official React documentation from Context7, including official examples, best practices from React team, version-specific considerations, and links to authoritative resources.

### Example 3: Project Context Explanation
```bash
/sc:explain @src/auth/middleware.ts
```

**Output**: Explanation of the authentication pattern used in this specific file, how it fits into the project architecture, why this approach was chosen, and how it connects to related components.

### Example 4: Learning Path Generation
```bash
/sc:explain "microservices" --learning-path
```

**Output**: Structured curriculum from fundamentals (monoliths, service boundaries) through intermediate (communication patterns, data consistency) to advanced (service mesh, observability), with validation checkpoints and capstone project.

### Example 5: Quick Reference
```bash
/sc:explain "async/await" --quick-ref
```

**Output**: Condensed reference card with key concept summary, essential syntax, common use cases with code snippets, common mistakes, and official docs link.

---

## 9. Quality Standards

### Explanation Quality Metrics
```yaml
clarity:
  target: ">= 90%"
  measurement: "Accessible to target skill level without confusion"
  validation: "MENTOR agent review for pedagogical soundness"

completeness:
  target: ">= 85%"
  measurement: "Covers all essential aspects of topic"
  validation: "ANALYST agent review for technical completeness"

accuracy:
  target: ">= 95%"
  measurement: "Technically correct and validated against sources"
  validation: "Context7 validation where applicable"

practicality:
  target: ">= 80%"
  measurement: "Includes actionable examples and real-world application"
  validation: "Minimum 2 working examples required"
```

### Success Criteria
- User can explain concept back in own words
- User can identify when to apply concept
- User can recognize common mistakes
- User knows next learning steps
- Explanation builds on prior knowledge when available

---

## 10. Integration Workflows

### Workflow 1: Standalone Explanation
```yaml
1. User: "/sc:explain 'event loop'"
2. System: Activate MENTOR agent
3. MENTOR: Load previous explanations from Serena
4. MENTOR: Generate comprehensive explanation with Sequential
5. MENTOR: Save explanation to Serena memory
6. Output: Structured educational content
```

### Workflow 2: Framework Documentation
```yaml
1. User: "/sc:explain 'React hooks' --context7"
2. System: Activate MENTOR + Context7
3. Context7: resolve-library-id('react') → '/facebook/react'
4. Context7: get-library-docs('/facebook/react', topic='hooks')
5. MENTOR: Structure explanation using official patterns
6. MENTOR: Add progressive complexity layers
7. Output: Explanation with official documentation integration
```

### Workflow 3: Project-Specific Explanation
```yaml
1. User: "/sc:explain @auth.ts"
2. System: Activate MENTOR + ANALYST
3. ANALYST: Analyze file for patterns and complexity
4. MENTOR: Load project context from Serena
5. MENTOR: Explain pattern in project context
6. MENTOR: Link to related project components
7. Output: Context-aware explanation with project references
```

---

*Command Definition | Shannon Framework V3 | Enhanced from SuperClaude*