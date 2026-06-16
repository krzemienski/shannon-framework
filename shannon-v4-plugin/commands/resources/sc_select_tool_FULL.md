# /sc:select-tool - Intelligent Tool Selection Command - Full Documentation

> This is the complete reference loaded on-demand (Tier 2)

# /sc:select-tool - Intelligent Tool Selection Command

> **Enhanced from SuperClaude's `/select-tool` command with Shannon V3 MCP server awareness, comprehensive tool selection matrix, and intelligent recommendations based on operation context.**

## Command Identity

**Name**: /sc:select-tool
**Base Command**: SuperClaude's `/select-tool`
**Shannon Enhancement**: MCP server matrix, dynamic tool suggestions, context-aware recommendations
**Primary Domain**: Tool optimization, workflow efficiency, MCP coordination
**Complexity Level**: Low to Moderate (intelligent routing and suggestion)

---

## Purpose Statement

The `/sc:select-tool` command provides intelligent recommendations for optimal tool and MCP server selection based on operation context. It helps developers:

- **Choose the Right Tools**: Native tools vs MCP servers based on task complexity
- **Optimize MCP Usage**: Select most appropriate MCP servers for specific operations
- **Understand Trade-offs**: Clear explanations of tool selection rationale
- **Improve Efficiency**: Reduce trial-and-error through smart recommendations
- **Learn Patterns**: Build understanding of tool capabilities and use cases

**SuperClaude Foundation**: Built on SuperClaude's tool selection intelligence and MCP coordination patterns

**Shannon V3 Enhancements**:
- Comprehensive MCP server awareness matrix
- Context-based dynamic suggestions
- Shannon-specific tool patterns (Serena, Puppeteer focus)
- Integration with Wave orchestration recommendations
- Operation complexity scoring for tool selection

---

## Shannon V3 Enhancements

### 1. MCP Server Awareness Matrix

Shannon V3 adds comprehensive awareness of ALL available MCP servers:

**Core Shannon MCPs**:
- **Serena**: Memory, context preservation, symbol operations, project knowledge
- **Puppeteer**: Browser automation, E2E testing, visual validation, user workflows

**SuperClaude MCPs**:
- **Context7**: Documentation, framework patterns, official guides
- **Sequential**: Complex reasoning, multi-step analysis, systematic thinking
- **Magic**: UI component generation, design system integration
- **Morphllm**: Pattern-based code edits, bulk transformations
- **Playwright**: Advanced browser testing, cross-browser validation
- **Tavily**: Web search, research, current information

### 2. Dynamic MCP Suggestion Engine

Shannon analyzes operation context and suggests optimal MCP combinations:

```yaml
analysis_factors:
  operation_type: [read, write, analyze, test, research, generate]
  complexity_level: [simple, moderate, complex, comprehensive]
  domain: [frontend, backend, testing, documentation, research]
  scope: [file, module, project, system]

suggestion_logic:
  - Match operation patterns to MCP capabilities
  - Consider complexity thresholds
  - Evaluate performance trade-offs
  - Recommend fallback options
  - Provide usage examples
```

### 3. Tool Selection Matrix

Comprehensive matrix mapping operations to optimal tools:

| Operation Type | Complexity | Best Tool | Alternative | MCP Enhancement |
|----------------|-----------|-----------|-------------|-----------------|
| Code reading | Simple | Read | Grep | - |
| Pattern search | Moderate | Grep | Read + manual | - |
| Symbol ops | Complex | Serena | Manual search | Memory integration |
| UI generation | Moderate | Magic | Manual code | Context7 patterns |
| Browser testing | Complex | Puppeteer | Playwright | Serena test context |
| Analysis | Complex | Sequential | Native reasoning | Serena findings |
| Research | Moderate | Tavily | WebSearch | Sequential synthesis |
| Documentation | Simple | Context7 | WebSearch | - |
| Bulk edits | Moderate | Morphllm | MultiEdit | Serena validation |
| Memory ops | Simple | Serena | Manual tracking | Always primary |

### 4. Context-Aware Recommendations

Shannon considers current project context:

- **Active Wave**: Recommend tools that integrate with wave context
- **Project Phase**: Align tool suggestions with current development phase
- **Available MCPs**: Only suggest installed and configured servers
- **Performance State**: Consider resource usage and token limits
- **Previous Patterns**: Learn from project-specific tool usage

---

## Usage Patterns

### Basic Usage

```bash
# Get tool recommendations for an operation
/sc:select-tool "analyze authentication flow"

# Get MCP server suggestions for testing
/sc:select-tool "E2E test user registration" --focus mcp

# Compare tool options
/sc:select-tool "bulk rename functions" --compare

# Get recommendations with examples
/sc:select-tool "research best practices" --examples
```

### Advanced Usage

```bash
# Context-aware suggestions
/sc:select-tool "improve performance" --context @current-wave

# Multi-operation recommendations
/sc:select-tool "analyze + refactor + test authentication"

# Domain-specific guidance
/sc:select-tool --domain frontend --operation "component testing"

# MCP combination suggestions
/sc:select-tool "comprehensive code review" --mcp-strategy
```

### Integration Patterns

```bash
# With analyze command
/sc:analyze @auth.js --suggest-tools

# With implement command
/sc:implement "login form" --tools auto-select

# With wave orchestration
/sh:spec analyze @spec.md --tool-recommendations
```

---

## Execution Flow

### Phase 1: Context Analysis

1. **Operation Parsing**
   - Extract operation type (read, write, analyze, test, research, generate)
   - Identify complexity level (simple, moderate, complex)
   - Determine domain (frontend, backend, testing, infrastructure)
   - Assess scope (file, module, project, system)

2. **Project Context Loading**
   - Check active wave state via Serena
   - Review project phase and goals
   - Identify available MCP servers
   - Consider resource constraints

3. **Pattern Matching**
   - Match operation to tool matrix patterns
   - Consider historical usage patterns (if Serena data available)
   - Evaluate complexity thresholds
   - Identify potential MCP enhancements

### Phase 2: Recommendation Generation

1. **Primary Tool Selection**
   - Select optimal native tool or MCP server
   - Provide clear rationale for selection
   - Explain capability match to operation

2. **Alternative Options**
   - List fallback tools with trade-offs
   - Explain when alternatives are better
   - Provide switching criteria

3. **MCP Enhancement Suggestions**
   - Identify MCP servers that enhance primary tool
   - Explain integration benefits
   - Provide usage examples

4. **Anti-Pattern Warnings**
   - Flag common tool misuse patterns
   - Explain why certain tools are suboptimal
   - Suggest correct alternatives

### Phase 3: Output Formatting

Present recommendations in structured format:

```markdown
## Tool Recommendation: [Operation]

### Primary Recommendation
**Tool**: [Selected Tool/MCP]
**Rationale**: [Why this is optimal]
**Example**: [Usage example]

### Alternative Options
1. **[Alternative 1]**: [Trade-offs and use cases]
2. **[Alternative 2]**: [Trade-offs and use cases]

### MCP Enhancements
- **[MCP Server]**: [How it enhances primary tool]
- **[MCP Server]**: [Integration benefit]

### Anti-Patterns to Avoid
- ❌ [Common mistake] → ✅ [Correct approach]

### Integration Example
[Complete workflow example]
```

---

## Tool Selection Matrix

### Native Claude Code Tools

**Read Tool**:
- **Best For**: Single file reading, code inspection, configuration review
- **Complexity**: Simple
- **Performance**: Fast, low token cost
- **When to Use**: Known file path, straightforward content needs
- **Avoid When**: Need pattern matching, symbol operations, or bulk operations

**Grep Tool**:
- **Best For**: Pattern searching, code discovery, finding references
- **Complexity**: Simple to Moderate
- **Performance**: Fast, efficient searching
- **When to Use**: Finding patterns across codebase, unknown file locations
- **Avoid When**: Need semantic understanding or symbol relationships

**Glob Tool**:
- **Best For**: File discovery by name pattern, directory traversal
- **Complexity**: Simple
- **Performance**: Fast, filesystem operations
- **When to Use**: Finding files by name/extension, directory structure discovery
- **Avoid When**: Need content-based search

**Edit Tool**:
- **Best For**: Single file edits, targeted changes
- **Complexity**: Moderate
- **Performance**: Efficient for small changes
- **When to Use**: Editing specific content in known locations
- **Avoid When**: Bulk operations, pattern-based edits across files

**MultiEdit Tool**:
- **Best For**: Multiple file edits in parallel
- **Complexity**: Moderate
- **Performance**: Efficient batch editing
- **When to Use**: Related changes across multiple files
- **Avoid When**: Pattern-based transformations (use Morphllm)

**Bash Tool**:
- **Best For**: System commands, build operations, git operations
- **Complexity**: Variable
- **Performance**: Direct system access
- **When to Use**: System-level operations, toolchain execution
- **Avoid When**: File operations (use specialized tools)

### Shannon MCP Servers

**Serena (Memory & Context)**:
```yaml
capabilities:
  - Project memory management
  - Context preservation across sessions
  - Symbol-level operations
  - Code navigation
  - Wave context storage
  - Evidence tracking

best_for:
  - Storing analysis findings
  - Cross-wave context sharing
  - Symbol rename/refactor
  - Project knowledge management
  - Session state preservation

when_to_use:
  - ALL wave operations (mandatory)
  - Complex refactoring requiring symbol tracking
  - Long-running analysis needing evidence trail
  - Multi-session project work

avoid_when:
  - Simple one-off operations
  - Temporary debugging
  - Read-only inspection

performance:
  - Setup cost: Moderate (initial indexing)
  - Operation cost: Low (cached symbols)
  - Token efficiency: High (structured data)

integration_patterns:
  - Checkpoint before risky operations
  - Store findings from analysis
  - Load wave context for sub-agents
  - Track project evolution
```

**Puppeteer (Browser Automation)**:
```yaml
capabilities:
  - Browser automation and control
  - E2E testing workflows
  - Visual validation and screenshots
  - User interaction simulation
  - Form testing
  - Navigation and page state management

best_for:
  - E2E user workflow testing
  - Form submission validation
  - Visual regression testing
  - Browser-based feature testing
  - Real user behavior simulation

when_to_use:
  - Testing requires real browser
  - Visual validation needed
  - User workflows critical
  - Integration testing

avoid_when:
  - Unit tests sufficient
  - No UI interaction needed
  - Pure API testing
  - Static code analysis

performance:
  - Setup cost: High (browser launch)
  - Operation cost: Moderate (page loads)
  - Token efficiency: Moderate (screenshots increase tokens)

integration_patterns:
  - Store test results in Serena
  - Coordinate with Sequential for test planning
  - Integrate with Context7 for framework testing patterns
```

### SuperClaude MCP Servers

**Context7 (Documentation)**:
```yaml
capabilities:
  - Official library documentation
  - Framework patterns and guides
  - API reference lookup
  - Best practices access

best_for:
  - Learning framework APIs
  - Finding official examples
  - Understanding library patterns
  - Version-specific guidance

when_to_use:
  - Working with external libraries
  - Need official documentation
  - Framework-specific questions
  - API integration

avoid_when:
  - General coding questions
  - Project-specific logic
  - No external dependencies

shannon_integration:
  - Complements Serena (Context7: official docs, Serena: project patterns)
  - Use with Sequential for framework analysis
```

**Sequential (Complex Reasoning)**:
```yaml
capabilities:
  - Multi-step systematic analysis
  - Complex problem decomposition
  - Structured reasoning chains
  - Hypothesis testing

best_for:
  - Complex debugging
  - Architectural analysis
  - Multi-component problems
  - Systematic investigation

when_to_use:
  - Problem has >3 interacting components
  - Need structured analysis
  - Root cause investigation
  - Design decisions

avoid_when:
  - Simple straightforward tasks
  - Clear single-step operations
  - Well-defined processes

shannon_integration:
  - Store reasoning chains in Serena
  - Primary tool for spec analysis
  - Wave planning coordination
```

**Magic (UI Components)**:
```yaml
capabilities:
  - Modern UI component generation
  - Design system integration
  - Framework-specific patterns
  - Accessibility compliance

best_for:
  - React/Vue/Angular components
  - Design system implementation
  - Accessible UI creation
  - Modern web patterns

when_to_use:
  - Building UI components
  - Need design system consistency
  - Accessibility requirements
  - Framework best practices

avoid_when:
  - Backend development
  - API implementation
  - Database operations

shannon_integration:
  - Generate components for Shannon CLI
  - Integrate with Context7 for framework patterns
  - Store component patterns in Serena
```

**Morphllm (Bulk Edits)**:
```yaml
capabilities:
  - Pattern-based code transformations
  - Bulk editing across files
  - Style enforcement
  - Consistent refactoring

best_for:
  - Applying patterns across codebase
  - Style guide enforcement
  - Framework migration
  - Consistent refactoring

when_to_use:
  - Need consistent changes across files
  - Pattern-based transformations
  - Style/convention enforcement
  - Large-scale refactoring

avoid_when:
  - Single file changes
  - Symbol-level operations (use Serena)
  - Semantic refactoring

shannon_integration:
  - Coordinate with Serena for validation
  - Store transformation patterns
```

**Playwright (Advanced Browser Testing)**:
```yaml
capabilities:
  - Multi-browser testing
  - Advanced browser automation
  - Visual regression
  - Performance monitoring

best_for:
  - Cross-browser compatibility
  - Advanced testing scenarios
  - Visual regression testing
  - Performance validation

when_to_use:
  - Need multi-browser support
  - Complex testing scenarios
  - Visual regression important
  - Performance monitoring

shannon_relationship:
  - Alternative to Puppeteer
  - Use Puppeteer for Shannon projects (simpler, more focused)
  - Playwright for cross-browser needs
```

**Tavily (Web Research)**:
```yaml
capabilities:
  - Web search and discovery
  - Current information retrieval
  - Research aggregation
  - Source credibility assessment

best_for:
  - Researching best practices
  - Finding current information
  - Technology comparison
  - External knowledge gathering

when_to_use:
  - Need current information
  - External knowledge required
  - Multiple sources needed
  - Research and discovery

avoid_when:
  - Project-specific questions
  - Internal codebase issues
  - Well-known patterns

shannon_integration:
  - Research framework patterns
  - Store findings in Serena
  - Coordinate with Sequential for synthesis
```

---

## Output Format

### Standard Recommendation

```markdown
# Tool Selection Recommendation

## Operation Analysis
**Type**: [read|write|analyze|test|research|generate]
**Complexity**: [simple|moderate|complex|comprehensive]
**Domain**: [frontend|backend|testing|infrastructure|documentation]
**Scope**: [file|module|project|system]

## Primary Recommendation

### Recommended Tool: [Tool/MCP Name]

**Rationale**:
- [Key reason 1]
- [Key reason 2]
- [Key reason 3]

**Capabilities Match**:
- ✅ [Operation requirement] → [Tool capability]
- ✅ [Operation requirement] → [Tool capability]

**Usage Example**:
```bash
[Concrete example command or workflow]
```

**Expected Outcome**:
[What user should expect from using this tool]

## Alternative Options

### Option 1: [Alternative Tool]
**Trade-offs**: [When this might be better/worse]
**Use When**: [Specific scenarios]

### Option 2: [Alternative Tool]
**Trade-offs**: [When this might be better/worse]
**Use When**: [Specific scenarios]

## MCP Enhancement Recommendations

### [MCP Server 1]
**Enhancement Value**: [How it improves primary tool]
**Integration Pattern**: [How to use together]
**Example**: [Concrete integration example]

### [MCP Server 2]
**Enhancement Value**: [How it improves workflow]
**Integration Pattern**: [How to use together]

## Anti-Patterns & Common Mistakes

❌ **Avoid**: [Common mistake]
✅ **Instead**: [Correct approach]
**Why**: [Explanation]

❌ **Avoid**: [Common mistake]
✅ **Instead**: [Correct approach]
**Why**: [Explanation]

## Complete Workflow Example

[Step-by-step example showing recommended tools in action]

## Performance Considerations

**Token Cost**: [low|moderate|high]
**Time Complexity**: [fast|moderate|slow]
**Setup Required**: [none|minimal|moderate|extensive]
**Best For Scale**: [small|medium|large projects]

## Shannon Integration Notes

[How this recommendation fits with Shannon's Wave orchestration, Serena memory, etc.]
```

---

## Examples

### Example 1: Simple File Reading

```bash
/sc:select-tool "read authentication configuration"
```

**Output**:
```markdown
# Tool Recommendation: Read Authentication Configuration

## Primary Recommendation: Read Tool

**Rationale**:
- Simple file reading operation
- Known configuration file location
- No pattern matching required
- Low complexity, fast execution

**Usage**: `Read @config/auth.js`

**MCP Enhancement**: Not needed for this operation

**Anti-Pattern**: ❌ Using Grep when file path is known
```

### Example 2: Pattern Search

```bash
/sc:select-tool "find all API endpoint definitions"
```

**Output**:
```markdown
# Tool Recommendation: Find API Endpoints

## Primary Recommendation: Grep Tool

**Rationale**:
- Pattern-based search across codebase
- Unknown file locations
- Need to find all matches
- Efficient for text pattern matching

**Usage**: `Grep pattern="app\\.get|app\\.post" path=./`

**MCP Enhancement**:
- **Serena**: Store endpoint inventory in project memory
- **Sequential**: Analyze endpoint patterns and inconsistencies

**Anti-Pattern**: ❌ Reading files one-by-one → ✅ Pattern search
```

### Example 3: Complex Refactoring

```bash
/sc:select-tool "rename getUserData function across project"
```

**Output**:
```markdown
# Tool Recommendation: Rename Function Across Project

## Primary Recommendation: Serena MCP (Symbol Operations)

**Rationale**:
- Symbol-level operation requiring semantic understanding
- Need to track all references and usages
- Maintain code correctness through symbol tracking
- Cross-file dependency management

**Usage**:
```bash
# Via Serena MCP
find_symbol(name_path="getUserData")
→ Analyze all references
→ Safe rename with dependency tracking
```

**Alternative**: Morphllm (if simple text replacement sufficient)

**MCP Enhancement**: Serena is primary, not enhancement

**Anti-Pattern**: ❌ Manual search-replace → ✅ Symbol-aware refactoring
```

### Example 4: E2E Testing

```bash
/sc:select-tool "test user registration flow"
```

**Output**:
```markdown
# Tool Recommendation: Test User Registration

## Primary Recommendation: Puppeteer MCP

**Rationale**:
- Real browser interaction required
- User workflow simulation
- Form submission and validation
- Visual feedback important
- Shannon's primary testing MCP

**Usage**:
```bash
# Test workflow with Puppeteer
1. Navigate to registration page
2. Fill form fields
3. Submit form
4. Validate success state
5. Verify user in system
```

**MCP Enhancements**:
- **Serena**: Store test results and patterns
- **Sequential**: Test planning and scenario analysis

**Alternative**: Playwright (for cross-browser testing)

**Anti-Pattern**: ❌ Mocked testing → ✅ Real browser validation
```

### Example 5: Research Operation

```bash
/sc:select-tool "research React testing best practices 2024"
```

**Output**:
```markdown
# Tool Recommendation: Research React Testing

## Primary Recommendation: Tavily MCP

**Rationale**:
- Current information needed (2024)
- External knowledge required
- Multiple source aggregation
- Best practices discovery

**Usage**:
```bash
Tavily search: "React testing best practices 2024"
→ Aggregate multiple sources
→ Identify consensus patterns
→ Extract actionable recommendations
```

**MCP Enhancements**:
- **Sequential**: Synthesize findings into structured recommendations
- **Serena**: Store research findings in project memory
- **Context7**: Validate against official React documentation

**Anti-Pattern**: ❌ Outdated knowledge → ✅ Current research
```

---

## Integration with Shannon Commands

### With /sh:spec (Specification Analysis)

```bash
/sh:spec analyze @requirements.md --tool-suggestions
```

Shannon automatically suggests tools based on spec analysis:
- Serena for context preservation
- Sequential for complex analysis
- Context7 for framework patterns
- Puppeteer for testing requirements

### With /sc:analyze

```bash
/sc:analyze @codebase/ --suggest-tools
```

Provides tool recommendations for analysis tasks:
- Grep for pattern discovery
- Serena for symbol analysis
- Sequential for complex reasoning

### With /sc:implement

```bash
/sc:implement "feature" --tools auto-select
```

Automatically selects optimal tools:
- Magic for UI components
- Context7 for framework patterns
- Serena for context storage
- Puppeteer for testing

---

## Best Practices

### Tool Selection Principles

1. **Start Simple**: Use native tools for simple operations
2. **MCP for Complexity**: Graduate to MCPs when operations become complex
3. **Always Serena for Waves**: Mandatory memory integration in Wave operations
4. **Puppeteer for Testing**: Shannon's primary E2E testing MCP
5. **Context7 for Learning**: Official documentation for framework questions
6. **Sequential for Analysis**: Systematic reasoning for complex problems

### Performance Optimization

1. **Token Awareness**: Consider token costs of MCP operations
2. **Caching**: Leverage Serena caching for repeated operations
3. **Batch Operations**: Use MultiEdit for bulk changes when possible
4. **Progressive Enhancement**: Start with native tools, add MCPs as needed

### Anti-Patterns to Avoid

❌ **Using Grep on single known file** → ✅ Use Read
❌ **Manual refactoring without Serena** → ✅ Use symbol operations
❌ **Mocked E2E tests** → ✅ Use Puppeteer for real validation
❌ **Ignoring Serena in Waves** → ✅ Always use for context preservation
❌ **Using Playwright instead of Puppeteer** → ✅ Puppeteer for Shannon projects

---

## Configuration & Settings

### MCP Server Availability Check

Command checks for installed and configured MCP servers:

```yaml
check_sequence:
  1. Read ~/.claude/claude_desktop_config.json
  2. Identify configured MCP servers
  3. Test server availability
  4. Provide server-specific recommendations
  5. Warn about missing recommended servers
```

### Recommendation Tuning

Users can configure recommendation preferences:

```yaml
preferences:
  favor_native_tools: true          # Prefer native over MCP when equivalent
  token_optimization: true          # Consider token costs in recommendations
  performance_priority: moderate    # [low|moderate|high]
  learning_mode: false             # Show detailed explanations
```

---

## Summary

The `/sc:select-tool` command is Shannon's intelligent tool selection system, providing:

✅ **Smart Recommendations**: Context-aware tool and MCP suggestions
✅ **MCP Awareness**: Comprehensive understanding of all Shannon and SuperClaude MCPs
✅ **Clear Rationale**: Explanations for why specific tools are recommended
✅ **Integration Guidance**: How tools work together in workflows
✅ **Anti-Pattern Warnings**: Common mistakes and correct alternatives
✅ **Shannon Optimization**: Emphasis on Serena memory and Puppeteer testing

**Key Innovation**: Dynamic MCP suggestions based on operation analysis, complexity scoring, and Shannon's tool ecosystem awareness.