#!/usr/bin/env python3
"""
Apply Shannon V4 enhancements to domain agents.
Adds: SITREP protocol, Serena MCP context loading, wave awareness
"""

import re
import sys
from pathlib import Path

V4_CONTEXT_LOADING = """
## MANDATORY CONTEXT LOADING PROTOCOL

**Before ANY {domain} task**, execute this protocol:

```
STEP 1: Discover available context
list_memories()

STEP 2: Load required context (in order)
read_memory("spec_analysis")           # REQUIRED - understand project requirements
read_memory("phase_plan_detailed")     # REQUIRED - know execution structure
read_memory("architecture_complete")   # If Phase 2 complete - system design
read_memory("{domain}_context")        # If exists - domain-specific context
read_memory("wave_N_complete")         # Previous wave results (if in wave execution)

STEP 3: Verify understanding
✓ What we're building (from spec_analysis)
✓ How it's designed (from architecture_complete)
✓ What's been built (from previous waves)
✓ Your specific {domain} task

STEP 4: Load wave-specific context (if in wave execution)
read_memory("wave_execution_plan")     # Wave structure and dependencies
read_memory("wave_[N-1]_complete")     # Immediate previous wave results
```

**If missing required context**:
```
ERROR: Cannot perform {domain} tasks without spec analysis and architecture
INSTRUCT: "Run /sh:analyze-spec and /sh:plan-phases before {domain} implementation"
```
"""

V4_SITREP_PROTOCOL = """
## SITREP REPORTING PROTOCOL

When coordinating with WAVE_COORDINATOR or during wave execution, use structured SITREP format:

### Full SITREP Format

```markdown
═══════════════════════════════════════════════════════════
🎯 SITREP: {{agent_name}}
═══════════════════════════════════════════════════════════

**STATUS**: {{🟢 ON TRACK | 🟡 AT RISK | 🔴 BLOCKED}}
**PROGRESS**: {{0-100}}% complete
**CURRENT TASK**: {{description}}

**COMPLETED**:
- ✅ {{completed_item_1}}
- ✅ {{completed_item_2}}

**IN PROGRESS**:
- 🔄 {{active_task_1}} (XX% complete)
- 🔄 {{active_task_2}} (XX% complete)

**REMAINING**:
- ⏳ {{pending_task_1}}
- ⏳ {{pending_task_2}}

**BLOCKERS**: {{None | Issue description with 🔴 severity}}
**DEPENDENCIES**: {{What you're waiting for}}
**ETA**: {{Time estimate}}

**NEXT ACTIONS**:
1. {{Next step 1}}
2. {{Next step 2}}

**HANDOFF**: {{HANDOFF-{{agent_name}}-YYYYMMDD-HASH | Not ready}}
═══════════════════════════════════════════════════════════
```

### Brief SITREP Format

Use for quick updates (every 30 minutes during wave execution):

```
🎯 {{agent_name}}: 🟢 XX% | Task description | ETA: Xh | No blockers
```

### SITREP Trigger Conditions

**Report IMMEDIATELY when**:
- 🔴 BLOCKED: Cannot proceed without external input
- 🟡 AT RISK: Timeline or quality concerns
- ✅ COMPLETED: Ready for handoff to next wave
- 🆘 URGENT: Critical issue requiring coordinator attention

**Report every 30 minutes during wave execution**
"""

V4_WAVE_COORDINATION = """
## Wave Coordination

### Wave Execution Awareness

**When spawned in a wave**:
1. **Load ALL previous wave contexts** via Serena MCP
2. **Report status using SITREP protocol** every 30 minutes
3. **Save deliverables to Serena** with descriptive keys
4. **Coordinate with parallel agents** via shared Serena context
5. **Request handoff approval** before marking complete

### Wave-Specific Behaviors

**{{domain}} Waves**:
```yaml
typical_wave_tasks:
  - {{task_1}}
  - {{task_2}}
  - {{task_3}}

wave_coordination:
  - Load requirements from Serena
  - Share {{domain}} updates with other agents
  - Report progress to WAVE_COORDINATOR via SITREP
  - Save deliverables for future waves
  - Coordinate with dependent agents

parallel_agent_coordination:
  frontend: "Load UI requirements, share integration points"
  backend: "Load API contracts, share data requirements"
  qa: "Share test results, coordinate validation"
```

### Context Preservation

**Save to Serena after completion**:
```yaml
{{domain}}_deliverables:
  key: "{{domain}}_wave_[N]_complete"
  content:
    components_implemented: [list]
    decisions_made: [key choices]
    tests_created: [count]
    integration_points: [dependencies]
    next_wave_needs: [what future waves need to know]
```
"""

def enhance_frontmatter(content: str, agent_name: str, domain: str) -> str:
    """Add V4 capabilities to frontmatter."""
    # Find frontmatter block
    match = re.search(r'^---\n(.*?)\n---', content, re.MULTILINE | re.DOTALL)
    if not match:
        print(f"  ⚠️  No frontmatter found in {agent_name}")
        return content

    frontmatter = match.group(1)

    # Add V4 capabilities if capabilities section exists
    if 'capabilities:' in frontmatter:
        capabilities_additions = f'''  - "Coordinate with wave execution using SITREP protocol for multi-agent {domain} development"
  - "Load complete project context via Serena MCP before {domain} tasks"
  - "Report structured progress during wave execution with status codes and quantitative metrics"'''

        # Find the end of capabilities section
        capabilities_match = re.search(r'(capabilities:.*?)(\n\w+:|\n---)', frontmatter, re.DOTALL)
        if capabilities_match:
            capabilities_end = capabilities_match.end(1)
            frontmatter = frontmatter[:capabilities_end] + '\n' + capabilities_additions + frontmatter[capabilities_end:]

    # Update enhancement line to V4
    frontmatter = re.sub(r'enhancement:.*', f'enhancement: Shannon V4 - SITREP protocol, Serena context loading, wave awareness', frontmatter)

    # Add V4 metadata
    if 'shannon-version:' not in frontmatter:
        frontmatter += '\nshannon-version: ">=4.0.0"'

    # Add depends_on if not present
    if 'depends_on:' not in frontmatter:
        frontmatter += '\ndepends_on: [spec-analyzer, phase-planner]'

    # Ensure mcp_servers has serena as mandatory
    if 'mcp_servers:' not in frontmatter or 'mcp-servers:' not in frontmatter:
        frontmatter += '\nmcp_servers:\n  mandatory: [serena]'

    # Replace frontmatter in content
    content = content.replace(match.group(0), f'---\n{frontmatter}\n---')
    return content

def insert_v4_sections(content: str, agent_name: str, domain: str) -> str:
    """Insert V4 protocol sections after Agent Identity."""

    # Find insertion point (after Agent Identity section)
    insertion_patterns = [
        r'(## Agent Identity.*?\n\n)(## (?!MANDATORY|SITREP|Wave))',
        r'(## Core Identity.*?\n\n)(## (?!MANDATORY|SITREP|Wave))',
        r'(# ' + agent_name + r' Agent.*?\n\n)(## (?!MANDATORY|SITREP|Wave))'
    ]

    for pattern in insertion_patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            # Check if sections already exist
            if '## MANDATORY CONTEXT LOADING PROTOCOL' in content:
                print(f"  ℹ️  V4 sections already present in {agent_name}")
                return content

            # Prepare V4 sections
            context_section = V4_CONTEXT_LOADING.format(domain=domain, agent_name=agent_name)
            sitrep_section = V4_SITREP_PROTOCOL.format(agent_name=agent_name)

            # Insert sections
            insertion_point = match.end(1)
            content = (content[:insertion_point] +
                      context_section + '\n' +
                      sitrep_section + '\n' +
                      content[insertion_point:])
            return content

    print(f"  ⚠️  Could not find insertion point in {agent_name}")
    return content

def add_wave_coordination_section(content: str, agent_name: str, domain: str) -> str:
    """Add Wave Coordination section before Integration Points."""

    # Check if already exists
    if '## Wave Coordination' in content:
        print(f"  ℹ️  Wave Coordination section already exists in {agent_name}")
        return content

    # Find Integration Points section
    match = re.search(r'(## Integration Points)', content)
    if match:
        wave_section = V4_WAVE_COORDINATION.format(
            domain=domain,
            agent_name=agent_name,
            task_1=f"Implement {domain} features",
            task_2=f"Create {domain} tests",
            task_3=f"Validate {domain} quality"
        )

        insertion_point = match.start(1)
        content = content[:insertion_point] + wave_section + '\n' + content[insertion_point:]
        return content

    print(f"  ⚠️  Could not find Integration Points section in {agent_name}")
    return content

def enhance_agent(agent_path: Path, agent_name: str, domain: str):
    """Apply all V4 enhancements to an agent."""
    print(f"\n📝 Enhancing {agent_name} agent...")

    # Read content
    content = agent_path.read_text()

    # Apply enhancements
    content = enhance_frontmatter(content, agent_name, domain)
    content = insert_v4_sections(content, agent_name, domain)
    content = add_wave_coordination_section(content, agent_name, domain)

    # Write back
    agent_path.write_text(content)
    print(f"  ✅ {agent_name} enhanced with V4 patterns")

def main():
    agents_dir = Path(__file__).parent.parent / 'agents'

    # Define agents to enhance with their domains
    agents_to_enhance = {
        'BACKEND.md': ('BACKEND', 'backend'),
        'MOBILE_DEVELOPER.md': ('MOBILE_DEVELOPER', 'mobile'),
        'DEVOPS.md': ('DEVOPS', 'DevOps'),
        'SECURITY.md': ('SECURITY', 'security'),
        'QA.md': ('QA', 'QA'),
        'PERFORMANCE.md': ('PERFORMANCE', 'performance'),
        'DATA_ENGINEER.md': ('DATA_ENGINEER', 'data engineering'),
    }

    print("🚀 Starting Shannon V4 agent enhancement process...")
    print(f"📁 Agents directory: {agents_dir}")

    enhanced_count = 0
    for filename, (agent_name, domain) in agents_to_enhance.items():
        agent_path = agents_dir / filename
        if not agent_path.exists():
            print(f"\n⚠️  {filename} not found, skipping...")
            continue

        try:
            enhance_agent(agent_path, agent_name, domain)
            enhanced_count += 1
        except Exception as e:
            print(f"  ❌ Error enhancing {agent_name}: {e}")

    print(f"\n✅ Enhancement complete! Enhanced {enhanced_count} agents with V4 patterns.")
    print("\nV4 Enhancements Applied:")
    print("  • MANDATORY CONTEXT LOADING PROTOCOL")
    print("  • SITREP REPORTING PROTOCOL")
    print("  • Wave Coordination section")
    print("  • Updated frontmatter with V4 metadata")

if __name__ == '__main__':
    main()
