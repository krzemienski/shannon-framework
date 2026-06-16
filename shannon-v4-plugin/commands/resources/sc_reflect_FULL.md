# /sc:reflect - Enhanced Reflection Command - Full Documentation

> This is the complete reference loaded on-demand (Tier 2)

# /sc:reflect - Enhanced Reflection Command

> **Enhanced from SuperClaude's reflection capabilities with Shannon V3 structured retrospectives, learning storage via Serena MCP, and systematic improvement tracking.**

## Command Identity

**Name**: /sc:reflect
**Base Command**: SuperClaude's reflection and introspection capabilities
**Shannon Enhancement**: Structured retrospectives, learning storage, pattern recognition, cross-session improvement
**Primary Domain**: Task reflection, learning extraction, continuous improvement, knowledge retention
**Complexity Level**: Low to Moderate (systematic analysis of completed work)

---

## Purpose Statement

The `/sc:reflect` command transforms post-task analysis into systematic learning and continuous improvement. It provides:

- **Structured Retrospectives**: Systematic analysis of what worked, what didn't, and why
- **Learning Storage**: All insights stored in Serena for cross-session improvement and pattern reuse
- **Pattern Recognition**: Identify recurring successes and failures across tasks
- **Improvement Tracking**: Monitor effectiveness of changes over time
- **Knowledge Retention**: Build organizational memory of best practices and lessons learned
- **Evidence-Based Insights**: All conclusions supported by specific task evidence

**SuperClaude Foundation**: Built on introspection mode and meta-cognitive analysis capabilities

**Shannon V3 Enhancements**:
- Structured retrospective templates (Start/Stop/Continue, Rose/Bud/Thorn)
- Learning storage via Serena with categorization and tagging
- Pattern recognition across multiple task reflections
- Improvement effectiveness tracking
- Integration with other commands for context-aware reflection
- Automated reflection triggers at task completion

---

## Shannon V3 Enhancements

### 1. Structured Retrospective Framework

**Retrospective Templates**:

```yaml
start_stop_continue:
  start: "What should we START doing?"
  stop: "What should we STOP doing?"
  continue: "What should we CONTINUE doing?"
  effectiveness: 95%
  best_for: "Process improvements, habit formation"

rose_bud_thorn:
  rose: "What went well? (Successes)"
  bud: "What has potential? (Opportunities)"
  thorn: "What was challenging? (Problems)"
  effectiveness: 90%
  best_for: "Balanced emotional reflection, team retrospectives"

what_so_what_now_what:
  what: "What happened? (Observations)"
  so_what: "Why does it matter? (Analysis)"
  now_what: "What will we do? (Actions)"
  effectiveness: 92%
  best_for: "Learning extraction, action planning"

four_l_retrospective:
  liked: "What did we like?"
  learned: "What did we learn?"
  lacked: "What was lacking?"
  longed_for: "What did we long for?"
  effectiveness: 88%
  best_for: "Comprehensive team reflection"

mad_sad_glad:
  mad: "What made us frustrated?"
  sad: "What disappointed us?"
  glad: "What made us happy?"
  effectiveness: 85%
  best_for: "Emotional processing, team morale"
```

### 2. Learning Storage Architecture

**Serena Memory Schema**:

```yaml
reflection_structure:
  reflection_[timestamp]_[task]:
    task_context: "Original task description and goals"
    outcomes: "What was achieved"
    effectiveness: "Success rating and evidence"

    insights:
      what_worked: ["Specific successes with evidence"]
      what_failed: ["Specific failures with root causes"]
      unexpected: ["Surprises and emergent patterns"]

    patterns:
      tool_effectiveness: {tool: effectiveness_score}
      approach_success: {approach: success_rate}
      common_pitfalls: ["Recurring issues"]

    lessons_learned:
      technical: ["Technical insights"]
      process: ["Process improvements"]
      collaboration: ["Teamwork learnings"]

    improvements:
      immediate: ["Quick wins to implement now"]
      short_term: ["Changes to make within 1 week"]
      long_term: ["Strategic improvements"]

    evidence:
      metrics: {metric: value}
      artifacts: ["Links to outputs"]
      feedback: ["User/stakeholder feedback"]
```

**Pattern Recognition Storage**:

```yaml
pattern_[pattern_type]:
  occurrences:
    - {date, task, outcome, evidence}
  success_rate: float
  contexts: ["When this pattern appears"]
  recommendations: ["When to apply/avoid"]
  evolution: ["How pattern has changed over time"]
```

### 3. Automated Reflection Triggers

```yaml
trigger_conditions:
  task_completion:
    complexity: ">= moderate"
    duration: ">= 30 minutes"
    auto_trigger: true

  failure_detection:
    quality_gates_failed: true
    unexpected_outcomes: true
    auto_trigger: true
    priority: "high"

  milestone_completion:
    wave_completed: true
    phase_completed: true
    auto_trigger: true

  periodic:
    frequency: "end_of_session"
    condition: "tasks_completed >= 3"
    auto_trigger: optional
```

---

## Usage Patterns

### Basic Reflection
```bash
/sc:reflect @task_or_session

# Triggers structured retrospective on specified task or session
# Uses default template (Start/Stop/Continue)
# Stores insights in Serena
```

### Template-Specific Reflection
```bash
/sc:reflect @task --template rose_bud_thorn

# Uses specified retrospective template
# Options: start_stop_continue, rose_bud_thorn, what_so_what_now_what, four_l, mad_sad_glad
```

### Pattern Analysis
```bash
/sc:reflect --patterns "tool_effectiveness"

# Analyzes patterns across multiple reflections
# Identifies recurring successes and failures
# Provides recommendations based on pattern history
```

### Comparative Reflection
```bash
/sc:reflect @task1 @task2 --compare

# Compares approaches and outcomes across tasks
# Identifies what changed and why
# Extracts differential insights
```

### Learning Review
```bash
/sc:reflect --review-period "last_week"

# Synthesizes learnings from specified period
# Identifies improvement trends
# Validates effectiveness of implemented changes
```

---

## Execution Flow

### Phase 1: Context Gathering (10-15%)

**Step 1.1: Task Analysis**
```yaml
context_gathering:
  - Identify task scope and original goals
  - Review deliverables and outcomes
  - Collect metrics and evidence
  - Gather user/stakeholder feedback
  - Review tool usage and effectiveness
```

**Step 1.2: Previous Reflection Lookup (Serena)**
```bash
# Check for related previous reflections
serena.list_memories()
→ Filter for reflection_* and pattern_* memories
→ Load relevant previous insights
→ Identify recurring themes
```

**Step 1.3: Template Selection**
```yaml
template_selection:
  auto_select: true
  criteria:
    - Task complexity → Template depth
    - Emotional impact → Emotion-aware templates
    - Team context → Collaborative templates
    - Learning goals → Learning-focused templates
  fallback: "start_stop_continue"
```

### Phase 2: Structured Reflection (40-50%)

**Step 2.1: Template Application**
```yaml
reflection_process:
  - Apply selected template questions
  - Use Sequential MCP for systematic analysis
  - Collect evidence for each insight
  - Identify specific examples
  - Avoid generalizations without evidence
```

**Step 2.2: Evidence Collection**
```yaml
evidence_sources:
  quantitative:
    - Performance metrics
    - Time measurements
    - Quality scores
    - Success rates

  qualitative:
    - Code quality observations
    - User feedback
    - Process effectiveness
    - Tool performance

  artifacts:
    - Deliverable links
    - Test results
    - Documentation
    - Communication records
```

**Step 2.3: Root Cause Analysis**
```yaml
analysis_framework:
  what_worked:
    - Specific action or decision
    - Why it was effective
    - Context dependencies
    - Reusability assessment

  what_failed:
    - Specific issue or failure
    - Root cause identification
    - Contributing factors
    - Prevention strategies

  unexpected:
    - Surprising outcomes
    - Why unexpected
    - Lessons learned
    - Future applications
```

### Phase 3: Pattern Recognition (20-25%)

**Step 3.1: Pattern Identification**
```yaml
pattern_detection:
  tool_patterns:
    - Which tools worked best
    - Context dependencies
    - Efficiency gains/losses

  approach_patterns:
    - Successful methodologies
    - Failed approaches
    - Contextual effectiveness

  collaboration_patterns:
    - Effective communication
    - Delegation success
    - Team dynamics

  timing_patterns:
    - Optimal work periods
    - Deadline effectiveness
    - Pacing insights
```

**Step 3.2: Cross-Reflection Analysis**
```yaml
historical_comparison:
  - Load previous reflections from Serena
  - Identify recurring themes
  - Track improvement trends
  - Validate pattern consistency
  - Measure change effectiveness
```

**Step 3.3: Pattern Categorization**
```yaml
pattern_types:
  proven_success:
    success_rate: ">= 80%"
    occurrences: ">= 3"
    action: "Codify as best practice"

  emerging_pattern:
    success_rate: "60-80%"
    occurrences: "2-3"
    action: "Continue monitoring"

  anti_pattern:
    success_rate: "< 40%"
    occurrences: ">= 2"
    action: "Avoid or fix"

  context_dependent:
    success_rate: "Varies by context"
    action: "Document conditions"
```

### Phase 4: Learning Extraction (15-20%)

**Step 4.1: Insight Formulation**
```yaml
insight_structure:
  observation: "What happened (objective)"
  analysis: "Why it happened (root causes)"
  learning: "What we learned (takeaway)"
  application: "How to apply (actionable)"
  context: "When to apply (conditions)"
```

**Step 4.2: Improvement Planning**
```yaml
improvement_hierarchy:
  immediate:
    timeframe: "Next task"
    effort: "Low"
    impact: "Quick wins"

  short_term:
    timeframe: "Next week"
    effort: "Moderate"
    impact: "Process improvements"

  long_term:
    timeframe: "Next month+"
    effort: "High"
    impact: "Strategic changes"
```

**Step 4.3: Learning Storage (Serena)**
```yaml
serena_storage:
  # Store complete reflection
  - write_memory("reflection_[timestamp]_[task]", structured_reflection)

  # Update pattern records
  - write_memory("pattern_[type]", updated_pattern_data)

  # Store lessons learned
  - write_memory("lessons_[category]", categorized_lessons)

  # Track improvements
  - write_memory("improvements_[task]", improvement_plan)
```

### Phase 5: Synthesis & Output (10-15%)

**Step 5.1: Report Generation**
```yaml
report_structure:
  - Executive Summary (key insights)
  - Structured Retrospective (template results)
  - Pattern Analysis (recurring themes)
  - Lessons Learned (categorized)
  - Improvement Recommendations (prioritized)
  - Evidence Appendix (supporting data)
```

**Step 5.2: Actionable Recommendations**
```yaml
recommendation_format:
  recommendation: "Specific action to take"
  rationale: "Why this will help (evidence-based)"
  priority: "high|medium|low"
  effort: "low|moderate|high"
  impact: "low|moderate|high"
  owner: "Who should implement"
  timeline: "When to implement"
```

---

## Sub-Agent Integration

The `/sc:reflect` command activates specialized personas:

### ANALYZER Agent Profile
```yaml
identity: "Systematic investigator, pattern recognizer, evidence-based analyst"

priority_hierarchy: "Evidence > Patterns > Insights > Recommendations"

core_principles:
  - "All insights supported by specific evidence"
  - "Patterns require multiple occurrences"
  - "Root causes over symptoms"
  - "Actionable over theoretical"

behavioral_traits:
  - Systematic analysis of outcomes
  - Pattern recognition across tasks
  - Root cause identification
  - Evidence collection and validation

reflection_approach:
  - Objective observation first
  - Evidence-based conclusions
  - Pattern-focused analysis
  - Actionable recommendations
```

### MENTOR Agent Profile
```yaml
identity: "Learning facilitator, knowledge curator, improvement advisor"

priority_hierarchy: "Learning > Application > Retention > Sharing"

core_principles:
  - "Learning from every experience"
  - "Knowledge sharing for team benefit"
  - "Continuous improvement mindset"
  - "Psychological safety in reflection"

behavioral_traits:
  - Facilitative questioning
  - Learning extraction
  - Growth mindset encouragement
  - Knowledge organization

reflection_approach:
  - Focus on learning and growth
  - Encourage honest assessment
  - Extract transferable insights
  - Support improvement planning
```

### Agent Coordination
```yaml
collaboration_model:
  analyzer_leads:
    - Pattern identification
    - Evidence collection
    - Root cause analysis

  mentor_leads:
    - Learning extraction
    - Insight formulation
    - Improvement planning

  shared_responsibility:
    - Report synthesis
    - Recommendation prioritization
    - Knowledge storage
```

---

## Output Format

### Standard Reflection Report

```markdown
# Reflection Report: [Task Name]
**Date**: [Timestamp]
**Template**: [Template Used]
**Duration**: [Task Duration]

## Executive Summary
[2-3 sentence high-level summary of key insights and recommendations]

## Structured Retrospective: [Template Name]

### [Template Section 1]
**Observations**:
- [Specific observation with evidence]
- [Specific observation with evidence]

**Analysis**:
[Why these observations matter]

### [Template Section 2]
**Observations**:
- [Specific observation with evidence]
- [Specific observation with evidence]

**Analysis**:
[Why these observations matter]

## Pattern Analysis

### Proven Patterns (Continue Using)
| Pattern | Success Rate | Occurrences | Context |
|---------|--------------|-------------|---------|
| [Pattern] | 85% | 5 tasks | [When effective] |

### Emerging Patterns (Monitor)
| Pattern | Success Rate | Occurrences | Context |
|---------|--------------|-------------|---------|
| [Pattern] | 65% | 3 tasks | [Initial observations] |

### Anti-Patterns (Avoid)
| Pattern | Failure Rate | Occurrences | Root Cause |
|---------|--------------|-------------|------------|
| [Pattern] | 70% | 4 tasks | [Why it fails] |

## Lessons Learned

### Technical Insights
- **[Insight]**: [Evidence] → [Application]
- **[Insight]**: [Evidence] → [Application]

### Process Improvements
- **[Insight]**: [Evidence] → [Application]
- **[Insight]**: [Evidence] → [Application]

### Collaboration Learnings
- **[Insight]**: [Evidence] → [Application]
- **[Insight]**: [Evidence] → [Application]

## Improvement Recommendations

### Immediate Actions (Next Task)
1. **[Action]**: [Rationale] | Priority: High | Effort: Low
2. **[Action]**: [Rationale] | Priority: High | Effort: Low

### Short-Term Changes (Next Week)
1. **[Action]**: [Rationale] | Priority: Medium | Effort: Moderate
2. **[Action]**: [Rationale] | Priority: Medium | Effort: Moderate

### Long-Term Improvements (Next Month+)
1. **[Action]**: [Rationale] | Priority: Medium | Effort: High
2. **[Action]**: [Rationale] | Priority: Low | Effort: High

## Evidence Appendix

### Metrics
- [Metric]: [Value] ([Source])
- [Metric]: [Value] ([Source])

### Artifacts
- [Deliverable]: [Link/Location]
- [Test Results]: [Link/Location]

### Feedback
- [Source]: "[Quoted feedback]"
- [Source]: "[Quoted feedback]"

---

**Stored in Serena**: reflection_[timestamp]_[task]
**Related Patterns Updated**: [List of pattern memories updated]
```

---

## Integration with Shannon Commands

### With /sc:task
```yaml
integration_pattern:
  - /sc:task completes major milestone
  - Auto-trigger /sc:reflect for milestone
  - Store insights for next task planning
  - Update task patterns in Serena
```

### With /sc:research
```yaml
integration_pattern:
  - /sc:research completes investigation
  - /sc:reflect analyzes research process
  - Store search patterns and source strategies
  - Improve future research effectiveness
```

### With /sc:build
```yaml
integration_pattern:
  - /sc:build completes implementation
  - /sc:reflect analyzes development process
  - Store successful patterns and pitfalls
  - Inform future architecture decisions
```

### With Wave Operations
```yaml
integration_pattern:
  - Wave operation completes
  - /sc:reflect analyzes wave effectiveness
  - Store orchestration patterns
  - Optimize future wave strategies
```

---

## Examples

### Example 1: Basic Task Reflection
```bash
/sc:reflect @authentication_implementation

# Triggers Start/Stop/Continue retrospective
# Analyzes what worked and what didn't
# Stores insights in Serena
# Provides improvement recommendations
```

### Example 2: Pattern Analysis
```bash
/sc:reflect --patterns "mcp_tool_effectiveness"

# Reviews tool usage across tasks
# Identifies which MCP servers worked best
# Provides context-specific recommendations
# Updates tool usage patterns in Serena
```

### Example 3: Comparative Reflection
```bash
/sc:reflect @sprint1 @sprint2 --compare

# Compares two sprint outcomes
# Identifies improvements implemented
# Validates effectiveness of changes
# Extracts lessons for next sprint
```

### Example 4: Learning Review
```bash
/sc:reflect --review-period "last_month" --focus "process_improvements"

# Synthesizes process learnings from last month
# Tracks improvement implementation
# Validates effectiveness
# Plans next improvements
```

---

## Quality Standards

### Reflection Quality Metrics
```yaml
evidence_requirement:
  - Every insight has specific example
  - Patterns have >= 2 occurrences
  - Recommendations are actionable
  - All conclusions evidence-based

objectivity_standard:
  - Separate observation from interpretation
  - Avoid blame or judgment
  - Focus on systems over individuals
  - Balanced positive and negative

actionability_requirement:
  - Recommendations are specific
  - Prioritization is clear
  - Effort and impact estimated
  - Implementation path defined

learning_effectiveness:
  - Insights are transferable
  - Patterns are documented
  - Knowledge is stored
  - Improvement tracked over time
```

---

## Advanced Features

### Automated Improvement Tracking
```yaml
tracking_mechanism:
  - Store improvement recommendations
  - Monitor implementation
  - Measure effectiveness
  - Adjust future recommendations
```

### Team Reflection Support
```yaml
team_features:
  - Aggregate individual reflections
  - Identify shared patterns
  - Facilitate team retrospectives
  - Build team knowledge base
```

### Continuous Learning Loop
```yaml
learning_cycle:
  reflect → learn → apply → reflect

  effectiveness_validation:
    - Track recommended changes
    - Measure impact on outcomes
    - Adjust recommendations
    - Evolve patterns over time
```