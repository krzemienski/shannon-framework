#!/usr/bin/env python3
"""
Tests for spec-analysis skill

These are VALIDATION tests (not functional tests).
They validate the skill file structure and content.

Functional testing happens in Claude Code with real execution.
"""

import sys
from pathlib import Path
from validate_skills import validate_skill_file


def test_spec_analysis_skill_structure():
    """Test spec-analysis skill has valid structure"""

    skill_path = Path(__file__).parent.parent / "skills" / "spec-analysis" / "SKILL.md"

    is_valid, errors = validate_skill_file(skill_path)

    if not is_valid:
        print(f"❌ spec-analysis skill validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False

    print("✅ spec-analysis skill structure valid")
    return True


def test_spec_analysis_has_algorithm():
    """Test spec-analysis skill includes 8D algorithm"""

    skill_path = Path(__file__).parent.parent / "skills" / "spec-analysis" / "SKILL.md"

    with open(skill_path, 'r') as f:
        content = f.read()

    # Check for all 8 dimensions
    dimensions = [
        'Structural Complexity',
        'Cognitive Complexity',
        'Coordination Complexity',
        'Temporal Complexity',
        'Technical Complexity',
        'Scale Complexity',
        'Uncertainty Complexity',
        'Dependency Complexity'
    ]

    missing = []
    for dim in dimensions:
        if dim not in content:
            missing.append(dim)

    if missing:
        print(f"❌ spec-analysis missing dimensions: {', '.join(missing)}")
        return False

    print("✅ spec-analysis includes all 8 dimensions")
    return True


def test_spec_analysis_has_examples():
    """Test spec-analysis has required examples"""

    examples_dir = Path(__file__).parent.parent / "skills" / "spec-analysis" / "examples"

    if not examples_dir.exists():
        print("❌ spec-analysis examples directory missing")
        return False

    example_files = list(examples_dir.glob("*.md"))

    if len(example_files) < 2:
        print(f"❌ spec-analysis has only {len(example_files)} examples (minimum 2)")
        return False

    print(f"✅ spec-analysis has {len(example_files)} examples")
    return True


def main():
    """Run all tests for spec-analysis skill"""

    print("Testing spec-analysis Skill")
    print("=" * 60)

    tests = [
        test_spec_analysis_skill_structure,
        test_spec_analysis_has_algorithm,
        test_spec_analysis_has_examples
    ]

    results = [test() for test in tests]

    if all(results):
        print("\n✅ All spec-analysis tests passed")
        return 0
    else:
        failed = len([r for r in results if not r])
        print(f"\n❌ {failed}/{len(tests)} tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
