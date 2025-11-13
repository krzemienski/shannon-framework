---
name: analyze
description: Shannon-aware project analysis with complexity assessment and confidence validation
usage: /shannon:analyze [aspect] [--deep]
---

# Project Analysis Command (V4)

## Overview

Performs comprehensive Shannon-aware project analysis using the shannon-analysis skill. Provides multi-dimensional analysis of codebase, architecture, patterns, and technical debt with objective scoring. Optionally validates findings with confidence checking.

## Prerequisites

- Project context available (run from project root)
- Serena MCP recommended for saving analysis results
- Sequential MCP recommended for --deep analysis (complexity >= 0.70)

## Workflow

### Step 1: Validate Input

Check analysis scope:
- If no aspect specified: Analyze entire project (full analysis)
- If aspect provided: Focus on specific component/domain
- If --deep flag: Activate confidence validation

### Step 2: Invoke shannon-analysis Skill

Use the `@skill shannon-analysis` skill to perform analysis:

**Invocation:**
```
@skill shannon-analysis
- Input:
  * scope: "full" | "aspect_name"
  * depth: "standard" | "deep" (if --deep flag)
  * aspect: User-provided aspect (optional)
- Options:
  * include_architecture: true
  * include_patterns: true
  * include_technical_debt: true
  * save_to_serena: true
- Output: analysis_result
```

The shannon-analysis skill will:
1. Scan project structure
2. Detect technologies and frameworks
3. Analyze architectural patterns
4. Assess technical debt
5. Identify complexity hot spots
6. Generate recommendations

### Step 3: Invoke confidence-check (if --deep)

If --deep flag provided, validate analysis confidence:

**Invocation:**
```
@skill confidence-check
- Input: analysis_result from Step 2
- Options:
  * validation_depth: "thorough"
  * check_assumptions: true
  * verify_metrics: true
- Output: confidence_score
```

The confidence-check skill will:
1. Validate metric accuracy
2. Check assumption validity
3. Verify data completeness
4. Score confidence (0.0-1.0)
5. Flag low-confidence findings

### Step 4: Present Results

Format and display analysis results:

```markdown
📊 Shannon Project Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Scope**: {scope}
**Analysis Depth**: {standard | deep}
{if confidence_score}
**Confidence**: {confidence_score}/1.0 ({high | medium | low})
{end if}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Architecture Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Pattern**: {architectural_pattern}
**Complexity**: {complexity_score}/1.0

Structure:
{architecture_breakdown}

Strengths:
{for each strength}
✅ {strength_description}

Weaknesses:
{for each weakness}
⚠️  {weakness_description}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Technology Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Primary Languages:
{for each language}
├─ {language}: {percentage}%

Frameworks:
{for each framework}
├─ {framework_name} ({framework_version})

Dependencies:
├─ Total: {dependency_count}
├─ Outdated: {outdated_count}
└─ Vulnerable: {vulnerable_count}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Technical Debt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Overall Score**: {debt_score}/100

Hot Spots:
{for each hot_spot}
🔴 {file_path}
   - Complexity: {complexity_metric}
   - Issues: {issue_count}
   - Priority: {priority}

Areas of Concern:
{for each concern}
├─ {concern_category}: {concern_description}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommendations
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

High Priority:
{for each high_priority}
1. {recommendation}
   Impact: {impact_level}
   Effort: {effort_estimate}

Medium Priority:
{for each medium_priority}
- {recommendation}

Low Priority:
{for each low_priority}
- {recommendation}

{if saved_to_serena}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💾 Analysis saved to Serena MCP
Key: {analysis_key}
Retrieve: /shannon:restore {timestamp}
{else}
⚠️  Analysis not saved (Serena MCP unavailable)
{end if}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps:
{if complexity_score >= 0.70}
- Run /shannon:wave to create implementation plan
- Consider wave-based execution for refactoring
- Create checkpoint: /shannon:wave before-refactor

{else if technical_debt_score >= 0.60}
- Address high-priority technical debt items
- Run functional tests to validate improvements
- Create checkpoint: /shannon:wave debt-baseline

{else}
- Codebase in good health
- Continue with standard development workflow
{end if}
```

{if deep_analysis}
### Step 5: Present Confidence Report

Display confidence validation results:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Confidence Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Overall Confidence**: {confidence_score}/1.0 ({confidence_label})

Metric Accuracy: {metric_accuracy_score}
Assumption Validity: {assumption_validity_score}
Data Completeness: {data_completeness_score}

{if low_confidence_findings}
⚠️  Low Confidence Findings:
{for each finding}
- {finding_description}
  Confidence: {finding_confidence}
  Reason: {reason}
  Recommendation: {recommendation}
{end for}
{end if}

{if high_confidence}
✅ High confidence in all findings
Analysis results are reliable
{end if}
```
{end if}

## Output Format

See Step 4 presentation template above.

## Skill Dependencies

- shannon-analysis (REQUIRED)
- confidence-check (OPTIONAL, activated with --deep flag)

## MCP Dependencies

- Serena MCP (recommended for saving analysis results)
- Sequential MCP (recommended for deep analysis, complexity >= 0.70)

## Examples

### Example 1: Full Project Analysis

```bash
/shannon:analyze
```

Analyzes entire project with standard depth.

### Example 2: Component-Specific Analysis

```bash
/shannon:analyze authentication
```

Focuses on authentication component/module.

### Example 3: Deep Analysis with Confidence Check

```bash
/shannon:analyze --deep
```

Performs thorough analysis with confidence validation.

### Example 4: Deep Component Analysis

```bash
/shannon:analyze api-layer --deep
```

Deep analysis of API layer with confidence scoring.

## Notes

- **NEW in V4**: This is a new command that delegates to shannon-analysis skill
- **Purpose**: Shannon-aware analysis (not generic code analysis)
- **When to use**: Understanding project complexity, planning refactors, assessing technical health
- **vs. sc_analyze**: sc_analyze is SuperClaude generic analysis; sh_analyze is Shannon-specific with 8D framework awareness
