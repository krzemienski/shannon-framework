#!/usr/bin/env python3
"""
Test: confidence-check skill validation
Tests GREEN phase compliance with 5-check algorithm and threshold enforcement
"""

import json
import os
import sys
from pathlib import Path

# Add shannon-plugin to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_skill_structure():
    """Validate confidence-check skill has required structure"""
    skill_path = Path(__file__).parent.parent / "skills" / "confidence-check"

    print("✓ Testing skill structure...")

    # Check directories
    assert skill_path.exists(), "confidence-check/ directory missing"
    assert (skill_path / "examples").exists(), "examples/ directory missing"

    # Check files
    assert (skill_path / "SKILL.md").exists(), "SKILL.md missing"
    assert (skill_path / "examples" / "BASELINE_TEST.md").exists(), "BASELINE_TEST.md missing"
    assert (skill_path / "examples" / "85_PERCENT_CLARIFY.md").exists(), "85_PERCENT_CLARIFY.md missing"

    print("  ✓ All required files present")

def test_skill_frontmatter():
    """Validate SKILL.md frontmatter"""
    skill_path = Path(__file__).parent.parent / "skills" / "confidence-check" / "SKILL.md"

    print("✓ Testing frontmatter...")

    with open(skill_path, 'r') as f:
        content = f.read()

    # Check frontmatter markers
    assert content.startswith('---\n'), "Missing opening frontmatter marker"
    assert '\n---\n' in content, "Missing closing frontmatter marker"

    # Extract frontmatter
    frontmatter = content.split('\n---\n')[0].replace('---\n', '')

    # Check required fields
    assert 'name: confidence-check' in frontmatter, "Missing name field"
    assert 'skill-type: QUANTITATIVE' in frontmatter, "Missing or incorrect skill-type"
    assert 'shannon-version: ">=4.0.0"' in frontmatter, "Missing shannon-version"
    assert 'description:' in frontmatter, "Missing description field"

    # Check description mentions key features
    assert '5-check' in content.lower(), "Description missing 5-check mention"
    assert '90%' in content, "Description missing 90% threshold"
    assert '25-250x' in content, "Description missing ROI claim"

    print("  ✓ Frontmatter valid")

def test_5check_algorithm():
    """Validate 5-check algorithm is documented"""
    skill_path = Path(__file__).parent.parent / "skills" / "confidence-check" / "SKILL.md"

    print("✓ Testing 5-check algorithm documentation...")

    with open(skill_path, 'r') as f:
        content = f.read()

    # Check all 5 checks documented with correct weights
    assert 'No Duplicate Implementations (25%)' in content, "Missing duplicate check (25%)"
    assert 'Architecture Compliance (25%)' in content, "Missing architecture check (25%)"
    assert 'Official Docs Verified (20%)' in content, "Missing docs check (20%)"
    assert 'Working OSS Referenced (15%)' in content, "Missing OSS check (15%)"
    assert 'Root Cause Identified (15%)' in content, "Missing root cause check (15%)"

    # Verify total = 100%
    weights = [25, 25, 20, 15, 15]
    assert sum(weights) == 100, f"Weights sum to {sum(weights)}, expected 100"

    print("  ✓ All 5 checks documented with correct weights (25+25+20+15+15=100)")

def test_threshold_enforcement():
    """Validate threshold system is documented"""
    skill_path = Path(__file__).parent.parent / "skills" / "confidence-check" / "SKILL.md"

    print("✓ Testing threshold enforcement...")

    with open(skill_path, 'r') as f:
        content = f.read()

    # Check threshold values
    assert '≥90%' in content or '>=90%' in content, "Missing >=90% PROCEED threshold"
    assert '70-89%' in content or '70%-89%' in content, "Missing 70-89% CLARIFY threshold"
    assert '<70%' in content, "Missing <70% STOP threshold"

    # Check decisions
    assert 'PROCEED' in content, "Missing PROCEED decision"
    assert 'CLARIFY' in content, "Missing CLARIFY decision"
    assert 'STOP' in content, "Missing STOP decision"

    print("  ✓ Thresholds documented: ≥90% PROCEED, 70-89% CLARIFY, <70% STOP")

def test_anti_rationalization():
    """Validate anti-rationalization section exists"""
    skill_path = Path(__file__).parent.parent / "skills" / "confidence-check" / "SKILL.md"

    print("✓ Testing anti-rationalization section...")

    with open(skill_path, 'r') as f:
        content = f.read()

    # Check section exists
    assert 'Anti-Rationalization' in content or 'anti-rationalization' in content.lower(), \
           "Missing Anti-Rationalization section"

    # Check for common rationalizations
    rationalizations = [
        'seems confident',
        'simple task',
        'know the API',
        'can design this',
        'obvious problem',
        'close enough'
    ]

    found_count = sum(1 for r in rationalizations if r in content.lower())
    assert found_count >= 4, f"Only {found_count}/6 rationalizations documented"

    print(f"  ✓ Anti-rationalization section present with {found_count}/6 patterns")

def test_85_percent_example():
    """Validate 85% CLARIFY example"""
    example_path = Path(__file__).parent.parent / "skills" / "confidence-check" / "examples" / "85_PERCENT_CLARIFY.md"

    print("✓ Testing 85% CLARIFY example...")

    with open(example_path, 'r') as f:
        content = f.read()

    # Check score calculation
    assert '85' in content or '0.85' in content, "Missing 85% score"
    assert 'CLARIFY' in content, "Missing CLARIFY decision"

    # Check shows failed OSS check
    assert 'oss' in content.lower() or 'OSS' in content, "Missing OSS check discussion"
    assert '0/15' in content or 'FAIL' in content, "Missing failed check indication"

    # Check shows missing points
    assert 'missing' in content.lower() or 'need' in content.lower(), \
           "Missing explanation of what's needed to reach 90%"

    print("  ✓ 85% CLARIFY example demonstrates threshold enforcement")

def test_baseline_violations():
    """Validate RED phase baseline documented violations"""
    baseline_path = Path(__file__).parent.parent / "skills" / "confidence-check" / "examples" / "BASELINE_TEST.md"

    print("✓ Testing RED phase baseline...")

    with open(baseline_path, 'r') as f:
        content = f.read()

    # Check violation scenarios documented
    assert 'Scenario' in content, "Missing test scenarios"
    assert 'Violation' in content, "Missing violation documentation"

    # Check expected behaviors documented
    scenarios = content.lower().count('scenario')
    assert scenarios >= 5, f"Only {scenarios} scenarios documented, expected >=5"

    # Check token waste estimated
    assert 'token' in content.lower(), "Missing token waste analysis"
    assert 'ROI' in content or 'savings' in content.lower(), "Missing ROI calculation"

    print(f"  ✓ {scenarios} baseline violation scenarios documented with ROI")

def validate_confidence_score_calculation():
    """Test example: Validate confidence score calculation logic"""
    print("✓ Testing score calculation (simulation)...")

    # Example: 85% scenario
    checks = {
        'duplicate': {'points': 25, 'max': 25},
        'architecture': {'points': 25, 'max': 25},
        'docs': {'points': 20, 'max': 20},
        'oss': {'points': 0, 'max': 15},
        'root_cause': {'points': 15, 'max': 15}
    }

    total_points = sum(c['points'] for c in checks.values())
    confidence_score = total_points / 100.0

    assert total_points == 85, f"Points sum to {total_points}, expected 85"
    assert confidence_score == 0.85, f"Score {confidence_score}, expected 0.85"

    # Test threshold
    if confidence_score >= 0.90:
        decision = "PROCEED"
    elif confidence_score >= 0.70:
        decision = "CLARIFY"
    else:
        decision = "STOP"

    assert decision == "CLARIFY", f"Decision {decision}, expected CLARIFY for 85%"

    print("  ✓ Score calculation logic correct: 85/100 = 0.85 → CLARIFY")

def main():
    """Run all tests"""
    print("=" * 60)
    print("Confidence-Check Skill Validation (GREEN Phase)")
    print("=" * 60)
    print()

    try:
        test_skill_structure()
        test_skill_frontmatter()
        test_5check_algorithm()
        test_threshold_enforcement()
        test_anti_rationalization()
        test_85_percent_example()
        test_baseline_violations()
        validate_confidence_score_calculation()

        print()
        print("=" * 60)
        print("✅ ALL TESTS PASSED - GREEN Phase Complete")
        print("=" * 60)
        print()
        print("Confidence-check skill validated:")
        print("  • QUANTITATIVE skill-type ✓")
        print("  • 5-check algorithm (25+25+20+15+15=100) ✓")
        print("  • Thresholds (≥90% PROCEED, 70-89% CLARIFY, <70% STOP) ✓")
        print("  • Anti-rationalization section ✓")
        print("  • 85% CLARIFY example ✓")
        print("  • RED phase baseline violations ✓")
        print()
        print("Ready for REFACTOR phase (pressure scenarios).")
        print()

        return 0

    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"❌ TEST FAILED: {e}")
        print("=" * 60)
        return 1
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ ERROR: {e}")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
