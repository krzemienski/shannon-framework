#!/usr/bin/env python3
"""
Wave 1 Task 1.2 Functional Test: Skill Template

Tests that SKILL_TEMPLATE.md exists with all required sections.
Following TDD: This test will FAIL initially.
"""

import sys
from pathlib import Path

def test_template_exists():
    """Test: SKILL_TEMPLATE.md exists"""
    template = Path("shannon-plugin/templates/SKILL_TEMPLATE.md")

    if not template.exists():
        print("❌ FAIL: shannon-plugin/templates/SKILL_TEMPLATE.md does not exist")
        return False

    print("✅ PASS: SKILL_TEMPLATE.md exists")
    return True

def test_template_has_frontmatter():
    """Test: Template has YAML frontmatter"""
    template = Path("shannon-plugin/templates/SKILL_TEMPLATE.md")

    if not template.exists():
        print("⚠️  SKIP: Template doesn't exist yet")
        return True

    content = template.read_text()

    if not content.startswith("---"):
        print("❌ FAIL: Template missing YAML frontmatter (should start with ---)")
        return False

    if content.count("---") < 2:
        print("❌ FAIL: Template missing closing --- for frontmatter")
        return False

    print("✅ PASS: Template has valid YAML frontmatter structure")
    return True

def test_template_has_required_sections():
    """Test: Template has all Shannon V4 required sections"""
    template = Path("shannon-plugin/templates/SKILL_TEMPLATE.md")

    if not template.exists():
        print("⚠️  SKIP: Template doesn't exist yet")
        return True

    content = template.read_text()

    required_sections = [
        "## Overview",
        "## Core Competencies",
        "## Workflow",
        "## Examples",
        "## Success Criteria",
        "## Common Pitfalls",
        "## Validation",
        "## Progressive Disclosure",
        "## References",
    ]

    missing = []
    for section in required_sections:
        if section not in content:
            missing.append(section)

    if missing:
        print(f"❌ FAIL: Template missing sections: {', '.join(missing)}")
        return False

    print("✅ PASS: Template has all required sections")
    return True

def test_template_has_frontmatter_fields():
    """Test: Template frontmatter has Shannon V4 fields"""
    template = Path("shannon-plugin/templates/SKILL_TEMPLATE.md")

    if not template.exists():
        print("⚠️  SKIP: Template doesn't exist yet")
        return True

    content = template.read_text()

    required_fields = [
        "name:",
        "description:",
        "skill-type:",
        "shannon-version:",
        "mcp-requirements:",
        "required-sub-skills:",
        "allowed-tools:",
    ]

    missing = []
    for field in required_fields:
        if field not in content[:1000]:  # Check first 1000 chars (frontmatter area)
            missing.append(field)

    if missing:
        print(f"❌ FAIL: Template missing frontmatter fields: {', '.join(missing)}")
        return False

    print("✅ PASS: Template has all Shannon V4 frontmatter fields")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Wave 1 Task 1.2 Functional Tests")
    print("=" * 60)
    print()

    results = [
        test_template_exists(),
        test_template_has_frontmatter(),
        test_template_has_required_sections(),
        test_template_has_frontmatter_fields(),
    ]

    print()
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)

    sys.exit(0 if all(results) else 1)
