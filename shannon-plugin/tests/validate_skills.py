#!/usr/bin/env python3
"""
Shannon V4 Skill Validation Script

Validates skill files for structural correctness:
- Frontmatter presence and format
- Required sections
- Skill type classification
- Success criteria presence
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Tuple


def validate_skill_file(skill_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate single skill file

    Returns:
        (is_valid, error_messages)
    """
    errors = []

    if not skill_path.exists():
        return False, [f"File not found: {skill_path}"]

    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check 1: Frontmatter exists
    if not content.startswith('---'):
        errors.append("Missing frontmatter (must start with ---)")
        return False, errors

    # Extract frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        errors.append("Invalid frontmatter format (must be --- YAML ---)")
        return False, errors

    try:
        frontmatter = yaml.safe_load(frontmatter_match.group(1))
    except yaml.YAMLError as e:
        errors.append(f"YAML parse error: {e}")
        return False, errors

    # Check 2: Required frontmatter fields
    required_fields = ['name', 'skill-type', 'description']
    for field in required_fields:
        if field not in frontmatter:
            errors.append(f"Missing required frontmatter field: {field}")

    # Check 3: Valid skill type
    valid_types = ['QUANTITATIVE', 'RIGID', 'PROTOCOL', 'FLEXIBLE']
    skill_type = frontmatter.get('skill-type', '').upper()
    if skill_type not in valid_types:
        errors.append(f"Invalid skill-type: {skill_type}. Must be one of: {', '.join(valid_types)}")

    # Check 4: Description length
    description = frontmatter.get('description', '')
    if isinstance(description, str):
        desc_len = len(description.strip())
        if desc_len < 50:
            errors.append(f"Description too short: {desc_len} chars (minimum 50)")
        elif desc_len > 500:
            errors.append(f"Description too long: {desc_len} chars (maximum 500)")

    # Check 5: Required sections present
    required_sections = [
        ('## Purpose', '## Overview'),  # Accept either
        '## When to Use',
        '## Inputs',
        ('## Workflow', '## Process'),  # Accept either
        '## Outputs',
        '## Success Criteria',
        '## Examples'
    ]

    for section in required_sections:
        if isinstance(section, tuple):
            # Accept any variant
            if not any(variant in content for variant in section):
                primary = section[0]
                alternates = ', '.join(section[1:])
                errors.append(f"Missing required section: {primary} (or alternates: {alternates})")
        else:
            if section not in content:
                errors.append(f"Missing required section: {section}")

    # Check 6: Success criteria has validation code
    if '## Success Criteria' in content:
        success_section = content.split('## Success Criteria')[1].split('##')[0]
        if 'assert' not in success_section and 'validate' not in success_section.lower():
            errors.append("Success criteria should include validation code/assertions")

    # Check 7: Examples present (minimum 2)
    if '## Examples' in content:
        examples_section = content.split('## Examples')[1]
        example_count = len(re.findall(r'### Example \d+:', examples_section))
        if example_count < 2:
            errors.append(f"Insufficient examples: {example_count} found, minimum 2 required")

    # Check 8: Common Pitfalls for RIGID/QUANTITATIVE skills
    if skill_type in ['RIGID', 'QUANTITATIVE']:
        if '## Common Pitfalls' not in content:
            errors.append(f"{skill_type} skills must document common pitfalls")

    return len(errors) == 0, errors


def validate_all_skills(skills_dir: Path) -> Dict[str, List[str]]:
    """
    Validate all skills in directory

    Returns:
        {skill_name: [error_messages]} (only skills with errors)
    """
    results = {}

    if not skills_dir.exists():
        return {"_directory": [f"Skills directory not found: {skills_dir}"]}

    # Find all SKILL.md files recursively
    skill_files = list(skills_dir.rglob('SKILL.md'))

    # Also check for skills in root of skills/ directory
    root_skills = list(skills_dir.glob('*.md'))
    skill_files.extend([f for f in root_skills if f.name != 'TEMPLATE.md'])

    if not skill_files:
        return {"_directory": ["No skill files found (looking for SKILL.md or *.md)"]}

    for skill_file in skill_files:
        is_valid, errors = validate_skill_file(skill_file)
        if not is_valid:
            relative_path = skill_file.relative_to(skills_dir)
            results[str(relative_path)] = errors

    return results


def main():
    """Run all validations"""

    print("Shannon V4 Skill Validation")
    print("=" * 60)

    # Determine skills directory
    script_dir = Path(__file__).parent
    plugin_dir = script_dir.parent
    skills_dir = plugin_dir / "skills"

    print(f"\nValidating skills in: {skills_dir}")

    # Validate all skills
    results = validate_all_skills(skills_dir)

    if not results:
        print("\n✅ All skills valid")
        return 0
    else:
        print(f"\n❌ Validation errors found in {len(results)} file(s):\n")
        for skill_name, errors in results.items():
            print(f"  {skill_name}:")
            for error in errors:
                print(f"    - {error}")
        print(f"\n❌ Validation failed: {len(results)} file(s) with errors")
        return 1


if __name__ == "__main__":
    sys.exit(main())
