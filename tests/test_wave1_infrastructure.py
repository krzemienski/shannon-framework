#!/usr/bin/env python3
"""
Wave 1 Task 1.1 Functional Test: Skills Directory Structure

Tests that skills/ directory exists with proper structure.
Following TDD: This test will FAIL initially, then pass after implementation.
"""

import os
import sys
from pathlib import Path

def test_skills_directory_exists():
    """Test: shannon-plugin/skills/ directory exists"""
    skills_dir = Path("shannon-plugin/skills")

    if not skills_dir.exists():
        print("❌ FAIL: shannon-plugin/skills/ directory does not exist")
        return False

    if not skills_dir.is_dir():
        print("❌ FAIL: shannon-plugin/skills/ exists but is not a directory")
        return False

    print("✅ PASS: shannon-plugin/skills/ directory exists")
    return True

def test_skills_readme_exists():
    """Test: skills/README.md exists and has required content"""
    readme = Path("shannon-plugin/skills/README.md")

    if not readme.exists():
        print("❌ FAIL: shannon-plugin/skills/README.md does not exist")
        return False

    content = readme.read_text()

    required_sections = [
        "# Shannon Framework V4 Skills",
        "## Skill Structure",
        "## Available Skills",
        "## Core Shannon Skills",
    ]

    for section in required_sections:
        if section not in content:
            print(f"❌ FAIL: README.md missing section: {section}")
            return False

    print("✅ PASS: skills/README.md exists with all required sections")
    return True

def test_git_tracking():
    """Test: Skills directory is git-tracked"""
    skills_dir = Path("shannon-plugin/skills")

    if not skills_dir.exists():
        print("⚠️  SKIP: Directory doesn't exist yet")
        return True  # Will fail in earlier test

    # Check .gitkeep exists OR README.md exists (either makes it tracked)
    gitkeep = skills_dir / ".gitkeep"
    readme = skills_dir / "README.md"

    if not gitkeep.exists() and not readme.exists():
        print("❌ FAIL: Skills directory has no tracked files (.gitkeep or README.md)")
        return False

    print("✅ PASS: Skills directory is git-tracked")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Wave 1 Task 1.1 Functional Tests")
    print("=" * 60)
    print()

    results = [
        test_skills_directory_exists(),
        test_skills_readme_exists(),
        test_git_tracking(),
    ]

    print()
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)

    sys.exit(0 if all(results) else 1)
