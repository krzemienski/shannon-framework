#!/usr/bin/env python3
"""
Wave 1 Task 1.3 Functional Test: Validation Infrastructure

Tests that validate_skills.py exists and can validate skills.
Following TDD: This test will FAIL initially.
"""

import sys
import subprocess
from pathlib import Path

def test_validator_exists():
    """Test: validate_skills.py exists"""
    validator = Path("shannon-plugin/tests/validate_skills.py")

    if not validator.exists():
        print("❌ FAIL: shannon-plugin/tests/validate_skills.py does not exist")
        return False

    print("✅ PASS: validate_skills.py exists")
    return True

def test_validator_is_executable():
    """Test: validate_skills.py runs without errors"""
    validator = Path("shannon-plugin/tests/validate_skills.py")

    if not validator.exists():
        print("⚠️  SKIP: Validator doesn't exist yet")
        return True

    try:
        result = subprocess.run(
            ["python3", str(validator)],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Should exit 0 (even with 0 skills, script should run)
        if result.returncode != 0:
            print(f"❌ FAIL: Validator exited with code {result.returncode}")
            print(f"stderr: {result.stderr}")
            return False

        print("✅ PASS: Validator runs successfully")
        return True

    except Exception as e:
        print(f"❌ FAIL: Validator execution error: {e}")
        return False

def test_validator_output_format():
    """Test: Validator produces expected output format"""
    validator = Path("shannon-plugin/tests/validate_skills.py")

    if not validator.exists():
        print("⚠️  SKIP: Validator doesn't exist yet")
        return True

    try:
        result = subprocess.run(
            ["python3", str(validator)],
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout

        # Should contain results summary
        if "Shannon V4 Skill Validation Results" not in output:
            print("❌ FAIL: Validator missing results header")
            return False

        if "Results:" not in output:
            print("❌ FAIL: Validator missing results summary")
            return False

        print("✅ PASS: Validator produces correct output format")
        return True

    except Exception as e:
        print(f"❌ FAIL: Validator execution error: {e}")
        return False

def test_validator_detects_invalid_skills():
    """Test: Validator can detect invalid skill structure"""
    # This will be tested once we have a sample skill
    # For now, just check the validator has validation logic
    validator = Path("shannon-plugin/tests/validate_skills.py")

    if not validator.exists():
        print("⚠️  SKIP: Validator doesn't exist yet")
        return True

    content = validator.read_text()

    # Check for key validation functions
    if "def validate_skill" not in content:
        print("❌ FAIL: Validator missing validate_skill function")
        return False

    if "frontmatter" not in content.lower():
        print("❌ FAIL: Validator doesn't check frontmatter")
        return False

    print("✅ PASS: Validator has validation logic")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Wave 1 Task 1.3 Functional Tests")
    print("=" * 60)
    print()

    results = [
        test_validator_exists(),
        test_validator_is_executable(),
        test_validator_output_format(),
        test_validator_detects_invalid_skills(),
    ]

    print()
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)

    sys.exit(0 if all(results) else 1)
