#!/usr/bin/env python3
"""
Shannon v4: Convert v3 commands to progressive disclosure format

This script converts Shannon v3 commands (single large .md files) into
Shannon v4 progressive disclosure format:
- Tier 1: Metadata + summary (~200 tokens, always loaded)
- Tier 2: Full content (on-demand via resources/FULL.md)

Target: 60-80% token reduction
"""

import os
import re
import yaml
from pathlib import Path

# Directories
V3_COMMANDS_DIR = Path("shannon-plugin/commands")
V4_COMMANDS_DIR = Path("shannon-v4-plugin/commands")
V4_RESOURCES_DIR = V4_COMMANDS_DIR / "resources"

# Ensure directories exist
V4_COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
V4_RESOURCES_DIR.mkdir(parents=True, exist_ok=True)


def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown file."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    if match:
        frontmatter_text = match.group(1)
        body = content[match.end():]
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            return frontmatter, body
        except yaml.YAMLError as e:
            print(f"YAML parse error: {e}")
            return {}, content
    return {}, content


def extract_sections(body):
    """Extract key sections from command body."""
    sections = {}

    # Extract title (first # heading)
    title_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    if title_match:
        sections['title'] = title_match.group(1)

    # Extract purpose/description (content after first heading until ## heading)
    purpose_match = re.search(
        r'^#\s+.+?\n\n(.*?)\n\n##',
        body,
        re.DOTALL | re.MULTILINE
    )
    if purpose_match:
        sections['purpose'] = purpose_match.group(1).strip()

    # Extract usage patterns section
    usage_match = re.search(
        r'##\s+Usage.*?\n\n(.*?)\n\n##',
        body,
        re.DOTALL | re.MULTILINE
    )
    if usage_match:
        sections['usage'] = usage_match.group(0).strip()

    # Extract activation/triggers section
    activation_match = re.search(
        r'##\s+Activation.*?\n\n(.*?)\n\n##',
        body,
        re.DOTALL | re.MULTILINE
    )
    if activation_match:
        sections['activation'] = activation_match.group(0).strip()

    return sections


def estimate_tokens(text):
    """Rough token estimation (1 token ≈ 4 characters)."""
    return len(text) // 4


def suggest_linked_skills(command_name, frontmatter):
    """Suggest appropriate skills based on command characteristics."""
    skills = []

    # Map commands to likely skills
    skill_map = {
        'sh:spec': ['shannon-spec-analyzer', 'shannon-skill-generator'],
        'sh:plan': ['shannon-phase-planner', 'shannon-skill-generator'],
        'sh:wave': ['shannon-wave-orchestrator', 'shannon-context-loader'],
        'sh:checkpoint': ['shannon-serena-manager'],
        'sh:test': ['shannon-test-coordinator'],
        'sh:deploy': ['shannon-deployment-manager'],
    }

    cmd_name = frontmatter.get('name', command_name)

    # Get mapped skills
    for pattern, mapped_skills in skill_map.items():
        if pattern in cmd_name:
            skills.extend(mapped_skills)

    # Add domain-specific skills based on MCP servers
    mcp_servers = frontmatter.get('mcp_servers', [])
    if 'puppeteer' in mcp_servers or 'playwright' in mcp_servers:
        skills.append('shannon-browser-test')
    if any('postgres' in mcp.lower() for mcp in mcp_servers):
        skills.append('shannon-postgres-prisma')

    return list(set(skills))  # Remove duplicates


def create_progressive_disclosure(v3_file_path):
    """Convert v3 command to v4 progressive disclosure format."""

    # Read v3 file
    with open(v3_file_path, 'r', encoding='utf-8') as f:
        v3_content = f.read()

    # Extract frontmatter and body
    frontmatter, body = extract_frontmatter(v3_content)
    sections = extract_sections(body)

    # Enhance frontmatter for v4
    frontmatter['progressive_disclosure'] = {
        'tier': 1,
        'full_content': 'resources/FULL.md',
        'estimated_tokens': 200
    }

    # Suggest linked skills
    command_name = v3_file_path.stem
    linked_skills = suggest_linked_skills(command_name, frontmatter)
    if linked_skills:
        frontmatter['linked_skills'] = linked_skills

    # Create v4 summary (Tier 1 - always loaded)
    v4_summary = f"""---
{yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True).strip()}
---

{sections.get('title', '# Command')}

> **Shannon V4 Skill-Based Framework**: Progressive disclosure command with linked skills

## Purpose

{sections.get('purpose', 'Command description')}

{sections.get('usage', '')}

## Skill Integration

**v4 NEW**: This command activates skills:

"""

    # Add linked skills section
    for skill in linked_skills:
        v4_summary += f"- `{skill}`\n"

    v4_summary += """
## Quick Reference

📚 **Full Documentation**: See [resources/FULL.md](./resources/FULL.md) for:
- Complete execution algorithms
- Detailed examples
- Integration patterns
- Validation rules

---

**Shannon V4** - Skill-Based Progressive Disclosure 🚀
"""

    # Save v4 summary
    v4_file_path = V4_COMMANDS_DIR / v3_file_path.name
    with open(v4_file_path, 'w', encoding='utf-8') as f:
        f.write(v4_summary)

    # Save full content to resources/
    full_file_path = V4_RESOURCES_DIR / f"{v3_file_path.stem}_FULL.md"
    with open(full_file_path, 'w', encoding='utf-8') as f:
        f.write(f"# {sections.get('title', 'Command')} - Full Documentation\n\n")
        f.write("> This is the complete reference loaded on-demand (Tier 2)\n\n")
        f.write(body)

    # Calculate token reduction
    v3_tokens = estimate_tokens(v3_content)
    v4_tokens = estimate_tokens(v4_summary)
    reduction_pct = ((v3_tokens - v4_tokens) / v3_tokens) * 100

    return {
        'command': command_name,
        'v3_tokens': v3_tokens,
        'v4_tokens': v4_tokens,
        'reduction_pct': reduction_pct,
        'linked_skills': linked_skills
    }


def convert_all_commands():
    """Convert all v3 commands to v4 progressive disclosure format."""

    results = []

    # Get all v3 command files
    v3_commands = list(V3_COMMANDS_DIR.glob("*.md"))

    print(f"Converting {len(v3_commands)} commands from v3 to v4...\n")

    for v3_file in sorted(v3_commands):
        try:
            result = create_progressive_disclosure(v3_file)
            results.append(result)

            print(f"✅ {result['command']}")
            print(f"   Tokens: {result['v3_tokens']} → {result['v4_tokens']} "
                  f"({result['reduction_pct']:.1f}% reduction)")
            if result['linked_skills']:
                print(f"   Skills: {', '.join(result['linked_skills'])}")
            print()

        except Exception as e:
            print(f"❌ Error converting {v3_file.name}: {e}\n")

    # Summary statistics
    total_v3_tokens = sum(r['v3_tokens'] for r in results)
    total_v4_tokens = sum(r['v4_tokens'] for r in results)
    overall_reduction = ((total_v3_tokens - total_v4_tokens) / total_v3_tokens) * 100

    print("=" * 60)
    print("CONVERSION SUMMARY")
    print("=" * 60)
    print(f"Commands converted: {len(results)}")
    print(f"Total v3 tokens: {total_v3_tokens:,}")
    print(f"Total v4 tokens (Tier 1): {total_v4_tokens:,}")
    print(f"Overall reduction: {overall_reduction:.1f}%")
    print(f"Target achieved: {'✅ YES' if overall_reduction >= 60 else '❌ NO'} "
          f"(target: 60-80%)")
    print("=" * 60)

    # Save report
    report_path = V4_COMMANDS_DIR / "CONVERSION_REPORT.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Shannon v4 Command Conversion Report\n\n")
        f.write(f"**Date**: Generated automatically\n")
        f.write(f"**Commands**: {len(results)}\n")
        f.write(f"**Overall Token Reduction**: {overall_reduction:.1f}%\n\n")
        f.write("## Per-Command Results\n\n")
        f.write("| Command | v3 Tokens | v4 Tokens | Reduction | Linked Skills |\n")
        f.write("|---------|-----------|-----------|-----------|---------------|\n")

        for r in sorted(results, key=lambda x: x['reduction_pct'], reverse=True):
            skills_str = ', '.join(r['linked_skills']) if r['linked_skills'] else 'None'
            f.write(f"| {r['command']} | {r['v3_tokens']:,} | {r['v4_tokens']:,} | "
                   f"{r['reduction_pct']:.1f}% | {skills_str} |\n")

        f.write(f"\n## Summary\n\n")
        f.write(f"- **Total v3 tokens**: {total_v3_tokens:,}\n")
        f.write(f"- **Total v4 tokens**: {total_v4_tokens:,}\n")
        f.write(f"- **Overall reduction**: {overall_reduction:.1f}%\n")
        f.write(f"- **Target (60-80%)**: {'✅ ACHIEVED' if overall_reduction >= 60 else '❌ NOT ACHIEVED'}\n")

    print(f"\n📊 Report saved to: {report_path}")


if __name__ == "__main__":
    convert_all_commands()
