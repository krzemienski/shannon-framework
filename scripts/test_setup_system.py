#!/usr/bin/env python3
"""Test setup system components.

Quick verification that the setup system is properly integrated.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


def test_imports():
    """Test that all setup components can be imported."""
    print("Testing imports...")

    try:
        from shannon.setup import FrameworkDetector, SetupWizard
        print("  ✓ shannon.setup imports successfully")

        from shannon.setup.framework_detector import FrameworkDetector
        print("  ✓ FrameworkDetector imports successfully")

        from shannon.setup.wizard import SetupWizard
        print("  ✓ SetupWizard imports successfully")

        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_framework_detector():
    """Test FrameworkDetector functionality."""
    print("\nTesting FrameworkDetector...")

    from shannon.setup import FrameworkDetector

    # Test find_framework
    print("  Searching for framework...")
    framework_path = FrameworkDetector.find_framework()
    if framework_path:
        print(f"  ✓ Framework found: {framework_path}")

        # Test verify_framework
        is_valid, message = FrameworkDetector.verify_framework(framework_path)
        if is_valid:
            print(f"  ✓ Verification passed: {message}")
        else:
            print(f"  ⚠ Verification warning: {message}")

        # Test get_framework_info
        info = FrameworkDetector.get_framework_info(framework_path)
        print(f"  ✓ Info extracted: {len(info['skills'])} skills, {len(info['commands'])} commands")

    else:
        print("  ℹ No framework found (this is OK for clean install)")

    # Test search_all_locations
    print("  Searching all locations...")
    locations = FrameworkDetector.search_all_locations()
    print(f"  ✓ Searched {len(locations)} locations")

    for loc in locations:
        status = "✓ Valid" if loc.get('is_valid') else ("⚠ Invalid" if loc['exists'] else "✗ Not Found")
        print(f"    {status:12} {loc['location_name']}")

    return True


def test_config_integration():
    """Test ShannonConfig framework_path support."""
    print("\nTesting ShannonConfig integration...")

    from shannon.config import ShannonConfig

    config = ShannonConfig()

    # Check framework_path attribute exists
    if hasattr(config, 'framework_path'):
        print(f"  ✓ framework_path attribute exists: {config.framework_path}")
    else:
        print("  ✗ framework_path attribute missing")
        return False

    # Test save/load cycle
    test_path = "/test/path/to/framework"
    config.framework_path = test_path
    config.save()

    # Reload and verify
    config2 = ShannonConfig()
    if config2.framework_path == test_path:
        print("  ✓ Save/load cycle successful")

        # Cleanup - reset to None
        config2.framework_path = None
        config2.save()
        return True
    else:
        print(f"  ✗ Save/load failed: expected {test_path}, got {config2.framework_path}")
        return False


def test_cli_commands():
    """Test CLI command registration."""
    print("\nTesting CLI commands...")

    from shannon.cli.commands import cli

    # Check setup command exists
    setup_cmd = None
    diagnostics_cmd = None

    for cmd in cli.commands.values():
        if cmd.name == 'setup':
            setup_cmd = cmd
        elif cmd.name == 'diagnostics':
            diagnostics_cmd = cmd

    if setup_cmd:
        print("  ✓ 'shannon setup' command registered")
    else:
        print("  ✗ 'shannon setup' command missing")
        return False

    if diagnostics_cmd:
        print("  ✓ 'shannon diagnostics' command registered")
    else:
        print("  ✗ 'shannon diagnostics' command missing")
        return False

    # Check require_framework decorator exists
    from shannon.cli.commands import require_framework
    print("  ✓ require_framework decorator available")

    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Shannon CLI Setup System Tests")
    print("=" * 60)
    print()

    results = []

    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("FrameworkDetector", test_framework_detector()))
    results.append(("Config Integration", test_config_integration()))
    results.append(("CLI Commands", test_cli_commands()))

    # Summary
    print()
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {name}")

    print()
    if passed == total:
        print(f"✅ All {total} tests passed!")
        return 0
    else:
        print(f"⚠️  {passed}/{total} tests passed ({total - passed} failed)")
        return 1


if __name__ == '__main__':
    sys.exit(main())
