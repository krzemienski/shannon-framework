#!/usr/bin/env python3
"""
Wave 1 Task 1.5 Functional Test: Plugin Manifest Update

Tests that plugin.json is updated to v4.0.0-alpha.1 with new keywords.
Following TDD: This test will FAIL initially.
"""

import json
import sys
from pathlib import Path

def test_manifest_exists():
    """Test: plugin.json exists"""
    manifest = Path("shannon-plugin/.claude-plugin/plugin.json")

    if not manifest.exists():
        print("❌ FAIL: shannon-plugin/.claude-plugin/plugin.json does not exist")
        return False

    print("✅ PASS: plugin.json exists")
    return True

def test_version_updated():
    """Test: Version is 4.0.0-alpha.1"""
    manifest = Path("shannon-plugin/.claude-plugin/plugin.json")

    if not manifest.exists():
        print("⚠️  SKIP: Manifest doesn't exist")
        return True

    try:
        data = json.loads(manifest.read_text())
        version = data.get("version", "")

        if not version.startswith("4.0.0"):
            print(f"❌ FAIL: Version is '{version}', expected '4.0.0-alpha.1'")
            return False

        if "alpha" not in version:
            print(f"❌ FAIL: Version missing 'alpha' designation: '{version}'")
            return False

        print(f"✅ PASS: Version updated to {version}")
        return True

    except Exception as e:
        print(f"❌ FAIL: Error reading manifest: {e}")
        return False

def test_new_keywords_added():
    """Test: V4 keywords present"""
    manifest = Path("shannon-plugin/.claude-plugin/plugin.json")

    if not manifest.exists():
        print("⚠️  SKIP: Manifest doesn't exist")
        return True

    try:
        data = json.loads(manifest.read_text())
        keywords = data.get("keywords", [])

        required_new_keywords = [
            "skill-based-architecture",
            "sitrep-protocol",
            "mcp-integration",
        ]

        missing = []
        for keyword in required_new_keywords:
            if keyword not in keywords:
                missing.append(keyword)

        if missing:
            print(f"❌ FAIL: Missing V4 keywords: {', '.join(missing)}")
            print(f"   Current keywords: {keywords}")
            return False

        print("✅ PASS: All V4 keywords present")
        return True

    except Exception as e:
        print(f"❌ FAIL: Error reading keywords: {e}")
        return False

def test_description_updated():
    """Test: Description mentions V4 and skills"""
    manifest = Path("shannon-plugin/.claude-plugin/plugin.json")

    if not manifest.exists():
        print("⚠️  SKIP: Manifest doesn't exist")
        return True

    try:
        data = json.loads(manifest.read_text())
        description = data.get("description", "")

        if "V4" not in description and "v4" not in description:
            print(f"❌ FAIL: Description doesn't mention V4")
            return False

        if "skill" not in description.lower():
            print(f"❌ FAIL: Description doesn't mention skills")
            return False

        print("✅ PASS: Description updated for V4")
        return True

    except Exception as e:
        print(f"❌ FAIL: Error reading description: {e}")
        return False

def test_json_valid():
    """Test: JSON is valid and parseable"""
    manifest = Path("shannon-plugin/.claude-plugin/plugin.json")

    if not manifest.exists():
        print("⚠️  SKIP: Manifest doesn't exist")
        return True

    try:
        json.loads(manifest.read_text())
        print("✅ PASS: JSON is valid")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ FAIL: Invalid JSON: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Wave 1 Task 1.5 Functional Tests")
    print("=" * 60)
    print()

    results = [
        test_manifest_exists(),
        test_json_valid(),
        test_version_updated(),
        test_new_keywords_added(),
        test_description_updated(),
    ]

    print()
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)

    sys.exit(0 if all(results) else 1)
