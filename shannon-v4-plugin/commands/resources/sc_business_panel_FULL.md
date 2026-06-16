# /sc:business-panel - Strategic Business Analysis Command - Full Documentation

> This is the complete reference loaded on-demand (Tier 2)

# /sc:business-panel - Strategic Business Analysis Command

## Purpose Statement

Multi-expert business analysis engine combining 9 renowned business thought leaders for comprehensive strategic evaluation. Shannon V3 enhances SuperClaude's business panel mode with Serena-powered strategic insight storage, pattern learning, and cross-session business intelligence.

**Core Capability**: Orchestrate collaborative, adversarial, or Socratic analysis from business experts (Christensen, Porter, Drucker, Godin, Kim/Mauborgne, Collins, Taleb, Meadows, Doumont) with persistent strategic memory.

## Shannon V3 Enhancements

### Strategic Intelligence Layer
```yaml
serena_integration:
  insight_storage:
    - Store expert analyses as retrievable patterns
    - Build strategic knowledge base across sessions
    - Track successful framework applications
    - Learn from business decision outcomes

  pattern_recognition:
    - Identify recurring strategic themes
    - Map expert consensus/disagreement patterns
    - Track framework effectiveness by domain
    - Build organizational intelligence

  memory_schema:
    business_analyses: "Panel outputs with metadata"
    strategic_patterns: "Cross-framework insights"
    expert_effectiveness: "Framework success metrics"
    decision_outcomes: "Strategy results tracking"
```

### Cross-Session Learning
- **Pattern Reuse**: Retrieve similar past analyses for context
- **Expert Selection Optimization**: Learn which expert combinations work best
- **Framework Evolution**: Track which frameworks prove most valuable
- **Strategic Continuity**: Maintain business context across sessions

## Usage Patterns

### Basic Invocation
```bash
/sc:business-panel @strategy_document.pdf
# Auto-selects 3-5 relevant experts, discussion mode

/sc:business-panel "analyze our market entry strategy"
# Natural language analysis request
```

### Expert Selection
```bash
/sc:business-panel @doc.pdf --experts "porter,christensen,meadows"
# Explicit expert selection

/sc:business-panel @doc.pdf --focus innovation
# Auto-select innovation-focused experts

/sc:business-panel @doc.pdf --all-experts
# Include all 9 experts (comprehensive analysis)
```

### Mode Control
```bash
/sc:business-panel @doc.pdf --mode discussion
# Collaborative analysis (default)

/sc:business-panel @doc.pdf --mode debate
# Adversarial analysis for stress-testing

/sc:business-panel @doc.pdf --mode socratic
# Question-driven strategic learning
```

### Output Control
```bash
/sc:business-panel @doc.pdf --structured
# Structured synthesis format

/sc:business-panel @doc.pdf --synthesis-only
# Skip individual expert outputs, show integration only

/sc:business-panel @doc.pdf --verbose
# Include detailed framework application
```

### Memory Integration
```bash
/sc:business-panel @doc.pdf --store-insights
# Save analysis to Serena memory (default: true)

/sc:business-panel @doc.pdf --recall-similar
# Retrieve similar past analyses for context

/sc:business-panel @doc.pdf --pattern-compare
# Compare against historical strategic patterns
```

## Execution Flow

### Phase 1: Planning & Context
```yaml
step_1_document_analysis:
  - Parse input document or query
  - Identify business domains and strategic themes
  - Classify document type (strategy, market, risk, etc.)
  - Check Serena memory for similar past analyses

step_2_expert_selection:
  - Score expert relevance to content
  - Optimize for framework diversity
  - Consider interaction dynamics
  - Validate panel completeness
  - Load expert personas and frameworks

step_3_mode_determination:
  - Analyze content for discussion/debate/socratic indicators
  - Check user explicit mode flags
  - Select optimal interaction strategy
  - Configure output templates
```

### Phase 2: Multi-Expert Analysis
```yaml
discussion_mode:
  sequential_analysis:
    - Expert 1: Apply framework to content
    - Expert 2: Build on Expert 1's insights
    - Expert 3: Connect both perspectives
    - Continue cross-pollination

  parallel_opportunities:
    - Independent framework application
    - Simultaneous document sections
    - Convergent insight extraction

debate_mode:
  structured_disagreement:
    - Identify areas of expert conflict
    - Position articulation with evidence
    - Respectful challenge and rebuttal
    - Systems view of tensions (Meadows)
    - Higher-order synthesis

socratic_mode:
  question_generation:
    - Each expert formulates probing questions
    - Cluster questions by strategic themes
    - Present to user for reflection
    - Follow-up based on responses
    - Extract strategic thinking patterns
```

### Phase 3: Synthesis & Storage
```yaml
cross_framework_integration:
  - Identify convergent insights (expert agreement)
  - Extract productive tensions (strategic trade-offs)
  - Map system patterns (Meadows analysis)
  - Optimize communication clarity (Doumont)
  - Flag blind spots and gaps
  - Generate strategic questions

serena_storage:
  write_memory:
    - "business_panel_[timestamp]": Full analysis output
    - "strategic_insights_[domain]": Key findings by domain
    - "expert_patterns_[expert]": Framework application patterns
    - "synthesis_[topic]": Cross-framework integrations

  metadata_tracking:
    - Experts used and relevance scores
    - Mode applied and effectiveness
    - Convergent vs. divergent insights
    - User feedback if available
    - Outcome tracking if follow-up occurs
```

## Sub-Agent Integration

### Business Expert Personas

**Innovation Experts**:
```yaml
christensen:
  framework: "Jobs-to-be-Done, Disruption Theory"
  voice: "Academic, methodical, hypothesis-driven"
  symbol: "🔨"
  focus: "Customer jobs, innovation opportunities, disruption potential"

drucker:
  framework: "Management by Objectives, Customer Focus"
  voice: "Wise, fundamental, questioning assumptions"
  symbol: "🧭"
  focus: "What business should we be in, customer value, effectiveness"
```

**Strategy Experts**:
```yaml
porter:
  framework: "Five Forces, Value Chain, Competitive Strategy"
  voice: "Analytical, data-driven, structure-focused"
  symbol: "⚔️"
  focus: "Industry structure, competitive advantage, positioning"

kim_mauborgne:
  framework: "Blue Ocean Strategy, Value Innovation"
  voice: "Strategic, value-focused, opportunity-oriented"
  symbol: "🌊"
  focus: "Uncontested markets, value innovation, strategic moves"
```

**Marketing & Communication Experts**:
```yaml
godin:
  framework: "Purple Cow, Permission Marketing, Tribes"
  voice: "Conversational, provocative, remarkable-focused"
  symbol: "🎪"
  focus: "Remarkability, viral potential, tribe building"

doumont:
  framework: "Trees, Maps, and Theorems (Communication)"
  voice: "Precise, clarity-focused, audience-centric"
  symbol: "💬"
  focus: "Message clarity, cognitive load, actionable communication"
```

**Organizational & Risk Experts**:
```yaml
collins:
  framework: "Good to Great, Flywheel, Level 5 Leadership"
  voice: "Research-driven, disciplined, evidence-based"
  symbol: "🚀"
  focus: "Organizational excellence, disciplined execution, flywheel momentum"

taleb:
  framework: "Antifragility, Black Swan, Skin in the Game"
  voice: "Contrarian, risk-aware, fragility-detector"
  symbol: "🛡️"
  focus: "Robustness, hidden risks, asymmetric outcomes"

meadows:
  framework: "Systems Thinking, Leverage Points"
  voice: "Holistic, systems-focused, interconnection-aware"
  symbol: "🕸️"
  focus: "System structure, feedback loops, leverage points"
```

### Expert Coordination Patterns

**Complementary Collaboration**:
- Porter (structure) + Christensen (disruption) → Competitive innovation analysis
- Collins (execution) + Drucker (strategy) → Organizational effectiveness
- Godin (marketing) + Doumont (communication) → Message optimization
- Taleb (risk) + Meadows (systems) → Resilience design

**Productive Tension**:
- Taleb challenges Collins on execution vs. antifragility
- Christensen challenges Porter on disruption vs. positioning
- Godin challenges Drucker on remarkable vs. systematic

**Systems Integration**:
- Meadows provides meta-view of all expert frameworks
- Identifies leverage points across strategic dimensions
- Maps feedback loops in business strategies
- Reveals unintended consequences

## Tool Orchestration

### Primary Tools
```yaml
sequential_mcp:
  role: "Multi-expert coordination and complex reasoning"
  usage: "Moderate debate, synthesize frameworks, analyze tensions"

serena_mcp:
  role: "Strategic memory and pattern learning"
  usage: "Store analyses, retrieve patterns, track effectiveness"

read:
  role: "Document ingestion and content parsing"
  usage: "Load strategy docs, reports, plans for analysis"
```

### Supporting Tools
```yaml
context7_mcp:
  role: "Business framework documentation"
  usage: "Retrieve official framework patterns and case studies"

grep:
  role: "Document section extraction"
  usage: "Find specific strategic sections for focused analysis"

write:
  role: "Analysis output generation"
  usage: "Generate formatted business panel reports"
```

## Output Format

### Discussion Mode Template
```markdown
# Business Panel Analysis: [Document Title]

## 📋 Analysis Context
**Document Type**: [strategy/market/risk/innovation]
**Experts Convened**: [Expert list with symbols]
**Analysis Mode**: Discussion (Collaborative)
**Timestamp**: [ISO-8601]

## 🎯 Expert Analysis

**📊 PORTER - Competitive Strategy**:
[Industry structure analysis, five forces assessment, positioning recommendations]

**🔨 CHRISTENSEN building on PORTER**:
[Jobs-to-be-done perspective, disruption opportunities connecting to competitive dynamics]

**🕸️ MEADOWS - Systems View**:
[System structure analysis, feedback loops, leverage points across frameworks]

**💬 DOUMONT - Communication Clarity**:
[Message optimization, implementation priorities, stakeholder communication]

## 🧩 SYNTHESIS ACROSS FRAMEWORKS

**🤝 Convergent Insights**: [Where multiple experts agree and why]
- 🎯 Strategic alignment on [key area]
- 💰 Economic consensus around [financial drivers]
- 🏆 Shared view of competitive advantage

**⚖️ Productive Tensions**: [Strategic trade-offs revealed]
- 📈 Growth vs 🛡️ Risk management (Taleb ⚡ Collins)
- 🌊 Innovation vs 📊 Market positioning (Kim/Mauborgne ⚡ Porter)

**🔄 System Patterns** (Meadows):
- Leverage points: [Key intervention opportunities]
- Feedback loops: [Reinforcing/balancing dynamics]
- Unintended consequences: [Watch-outs]

**💬 Communication Clarity** (Doumont):
- Core message: [Essential strategic insight]
- Action priorities: [1, 2, 3 in order]
- Stakeholder messaging: [Audience-specific framing]

**⚠️ Blind Spots**: [What no framework captured adequately]

**🤔 Strategic Questions**: [Next exploration priorities]

## 💾 Strategic Insights Stored
- business_panel_[ID]: Full analysis
- strategic_patterns_[domain]: Cross-framework insights
- expert_effectiveness: Framework success tracking
```

### Debate Mode Template
```markdown
# Business Panel Debate: [Document Title]

## ⚡ PRODUCTIVE TENSIONS

**Initial Conflict**: [Primary disagreement area]

**🚀 COLLINS position**:
[Evidence-based organizational perspective with research backing]

**🛡️ TALEB challenges COLLINS**:
[Risk-focused challenge: "Your flywheel assumes stability, but..."]

**🚀 COLLINS responds**:
[Defense or concession with supporting logic]

**🕸️ MEADOWS on system dynamics**:
[How the debate reveals deeper system structure and both perspectives' validity]

## 🧩 Higher-Order Solution
[Strategy that honors multiple frameworks and transcends the tension]
```

### Socratic Mode Template
```markdown
# Strategic Inquiry Session: [Document Title]

## 🎓 Panel Questions for You

**Round 1 - Framework Foundations**:
- **🔨 CHRISTENSEN**: "What job is this being hired to do?"
- **⚔️ PORTER**: "What creates sustainable competitive advantage here?"
- **🧭 DRUCKER**: "What business should we actually be in?"

**[Await user responses]**

**Round 2 - Deeper Exploration**:
[Follow-up questions based on user answers, progressive depth]

## 💡 Strategic Thinking Development
[Insights about reasoning patterns and framework application]
```

## Examples

### Example 1: Market Entry Strategy Analysis
```bash
/sc:business-panel @market_entry_plan.pdf --experts "porter,christensen,taleb,meadows"

# Output:
# - Porter: Industry structure and competitive positioning
# - Christensen: Jobs-to-be-done and disruption potential
# - Taleb: Risk assessment and antifragility design
# - Meadows: System dynamics and unintended consequences
# - Synthesis: Integrated market entry recommendations
# - Storage: Strategic patterns stored in Serena memory
```

### Example 2: Innovation Strategy Debate
```bash
/sc:business-panel "Should we disrupt ourselves?" --mode debate --experts "christensen,collins,taleb"

# Output:
# - Christensen: Argues for self-disruption to avoid displacement
# - Collins: Challenges with disciplined execution and flywheel
# - Taleb: Adds antifragility perspective on optionality
# - Meadows: Systems view of the strategic tension
# - Synthesis: Conditions-based decision framework
```

### Example 3: Strategic Learning Session
```bash
/sc:business-panel @competitive_analysis.pdf --mode socratic --focus strategy

# Output:
# - Porter, Kim/Mauborgne, Meadows generate strategic questions
# - User responds to probing questions
# - Experts follow up based on responses
# - Strategic thinking patterns extracted
# - Learning insights stored for future sessions
```

### Example 4: Comprehensive Business Audit
```bash
/sc:business-panel @business_plan.pdf --all-experts --structured --store-insights

# Output:
# - All 9 experts provide framework-specific analysis
# - Structured synthesis across all frameworks
# - Comprehensive strategic recommendations
# - Full analysis stored in Serena memory
# - Pattern comparison with historical analyses
```

## Integration with SuperClaude Framework

### Persona Coordination
- **Auto-Activation**: Analyzer (investigation), Architect (systems), Mentor (learning)
- **Complementary**: Business experts inform technical decisions, technical personas ground business analysis

### MCP Server Integration
- **Sequential**: Multi-expert coordination, debate moderation, synthesis reasoning
- **Serena**: Strategic memory, pattern storage, cross-session learning
- **Context7**: Business framework documentation, case studies
- **Magic**: Business model visualization, strategic diagrams

### Wave Mode Support
```yaml
wave_enabled_operations:
  comprehensive_audit: "Multiple documents, stakeholder analysis, competitive landscape"
  strategic_planning: "Multi-phase development with expert validation"
  organizational_transformation: "Complete business system evaluation"
  market_entry_analysis: "Multi-market, multi-competitor assessment"
```

## Quality Standards

### Analysis Fidelity
- **Framework Authenticity**: ≥90% true-to-source methodology
- **Voice Consistency**: Each expert maintains characteristic communication style
- **Evidence-Based**: All conclusions supported by framework logic
- **Actionable Insights**: ≥80% recommendations are implementable

### Strategic Value
- **Multi-Perspective**: Minimum 3 complementary frameworks
- **Synthesis Quality**: Integration exceeds individual analyses
- **Blind Spot Detection**: Identify gaps requiring additional analysis
- **Pattern Learning**: Successful analyses stored for future reuse

### Performance Metrics
- **Token Efficiency**: 15-30K tokens for comprehensive analysis
- **Processing Time**: <2 minutes for discussion, <5 minutes for debate
- **Memory Utilization**: Efficient Serena storage with metadata
- **Learning Impact**: Improve expert selection over time (track effectiveness)