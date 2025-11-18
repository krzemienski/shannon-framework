#!/usr/bin/env python3
"""
Shannon v5.0 - Master Test Runner

Runs all verification tests sequentially:
- Tier 1: Analysis only (4 specs)
- Tier 2: Full builds (4 applications)

Usage: python tests/run_all_verification.py [--tier1-only] [--tier2-only]

Cost: ~$150-200 for complete suite
Duration: 4-6 hours for complete suite
Exit: 0 (all pass) or 1 (any fail)
"""

import sys
import subprocess
import time
from pathlib import Path
from typing import List, Tuple
import argparse


# Test configuration
TIER1_TESTS = [
    {
        'name': 'Tier 1: Analysis Only',
        'script': 'tier1_verify_analysis.py',
        'description': 'Test /shannon:spec on 4 specifications',
        'cost': '$2-3',
        'duration': '5-10 min',
    }
]

TIER2_TESTS = [
    {
        'name': 'Tier 2: PRD Creator',
        'script': 'tier2_build_prd_creator.py',
        'description': 'Build PRD Creator web app',
        'cost': '$20-25',
        'duration': '30-45 min',
    },
    {
        'name': 'Tier 2: Claude Code Expo',
        'script': 'tier2_build_mobile_expo.py',
        'description': 'Build mobile app with React Native',
        'cost': '$35-40',
        'duration': '60-75 min',
    },
    {
        'name': 'Tier 2: Repo Nexus',
        'script': 'tier2_build_repo_nexus.py',
        'description': 'Build full-stack iOS app',
        'cost': '$40-45',
        'duration': '60-75 min',
    },
    {
        'name': 'Tier 2: Shannon CLI',
        'script': 'tier2_build_shannon_cli.py',
        'description': 'Build Shannon CLI (meta-circular)',
        'cost': '$50-60',
        'duration': '90-120 min',
    }
]


def run_test(test_config: dict, test_dir: Path) -> Tuple[bool, float]:
    """
    Run a single test script

    Returns: (success: bool, elapsed_seconds: float)
    """
    script_path = test_dir / test_config['script']

    if not script_path.exists():
        print(f"❌ ERROR: Test script not found: {script_path}")
        return False, 0.0

    print(f"\n{'='*80}")
    print(f"Running: {test_config['name']}")
    print(f"Script:  {test_config['script']}")
    print(f"Cost:    {test_config['cost']}")
    print(f"Time:    {test_config['duration']}")
    print('='*80)

    start_time = time.time()

    try:
        # Run test script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=test_dir.parent,  # Run from repo root
            capture_output=False,  # Show output in real-time
            text=True
        )

        elapsed = time.time() - start_time
        success = result.returncode == 0

        if success:
            print(f"\n✅ {test_config['name']} PASSED ({elapsed:.1f}s)")
        else:
            print(f"\n❌ {test_config['name']} FAILED (exit code: {result.returncode})")

        return success, elapsed

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ {test_config['name']} EXCEPTION: {e}")
        return False, elapsed


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f} min"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} hours"


def main():
    """Run all verification tests"""

    parser = argparse.ArgumentParser(description='Shannon v5.0 Master Test Runner')
    parser.add_argument('--tier1-only', action='store_true',
                       help='Run only Tier 1 (analysis) tests')
    parser.add_argument('--tier2-only', action='store_true',
                       help='Run only Tier 2 (build) tests')
    args = parser.parse_args()

    # Determine which tiers to run
    run_tier1 = not args.tier2_only
    run_tier2 = not args.tier1_only

    print("="*80)
    print("SHANNON v5.0 - MASTER VERIFICATION SUITE")
    print("="*80)

    # Test directory
    test_dir = Path(__file__).parent

    # Cost and time estimates
    tier1_cost = "$2-3"
    tier1_time = "5-10 min"
    tier2_cost = "$145-170"
    tier2_time = "240-315 min (4-5 hours)"

    if run_tier1 and run_tier2:
        print("\nRunning: COMPLETE SUITE (Tier 1 + Tier 2)")
        print(f"Estimated cost: ~$150-200")
        print(f"Estimated time: 4-6 hours")
    elif run_tier1:
        print("\nRunning: TIER 1 ONLY (Analysis)")
        print(f"Estimated cost: {tier1_cost}")
        print(f"Estimated time: {tier1_time}")
    elif run_tier2:
        print("\nRunning: TIER 2 ONLY (Builds)")
        print(f"Estimated cost: {tier2_cost}")
        print(f"Estimated time: {tier2_time}")

    # Confirmation
    print("\nPress Ctrl+C to cancel, or wait 5 seconds to continue...")
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        return 0

    # Run tests
    overall_start = time.time()
    all_results = []

    # Tier 1: Analysis
    if run_tier1:
        print(f"\n{'='*80}")
        print("TIER 1: SPECIFICATION ANALYSIS")
        print('='*80)

        for test_config in TIER1_TESTS:
            success, elapsed = run_test(test_config, test_dir)
            all_results.append((test_config['name'], success, elapsed))

            if not success:
                print(f"\n⚠️  Tier 1 failed. Stopping before Tier 2.")
                print(f"   Fix Tier 1 issues before running expensive Tier 2 tests.")
                run_tier2 = False
                break

    # Tier 2: Builds
    if run_tier2:
        print(f"\n{'='*80}")
        print("TIER 2: FULL BUILD VERIFICATION")
        print('='*80)
        print("\nNote: Each build takes 30-120 minutes and costs $20-60")

        for test_config in TIER2_TESTS:
            success, elapsed = run_test(test_config, test_dir)
            all_results.append((test_config['name'], success, elapsed))

            # Don't stop on Tier 2 failures - run all builds to get complete picture
            if not success:
                print(f"\n⚠️  {test_config['name']} failed, continuing with remaining tests...")

    # Summary
    total_elapsed = time.time() - overall_start

    print(f"\n{'='*80}")
    print("VERIFICATION SUITE SUMMARY")
    print('='*80)

    # Results table
    passed_count = 0
    for test_name, success, elapsed in all_results:
        status = "✅ PASSED" if success else "❌ FAILED"
        duration = format_duration(elapsed)
        print(f"{status}  {test_name} ({duration})")
        if success:
            passed_count += 1

    total_count = len(all_results)
    all_passed = passed_count == total_count

    print(f"\nResult: {passed_count}/{total_count} tests passed")
    print(f"Total duration: {format_duration(total_elapsed)}")

    # Recommendations
    if all_passed:
        print("\n✅ ALL VERIFICATION TESTS PASSED")
        print("\nShannon Framework v5.4 is working correctly:")
        if run_tier1:
            print("  - Analysis algorithm validated on 4 real specs")
        if run_tier2:
            print("  - Full build capability validated on 4 applications")
        print("\nReady for production use.")
    else:
        print(f"\n❌ {total_count - passed_count} TESTS FAILED")
        print("\nRecommended actions:")
        if not run_tier1 or not all([r[1] for r in all_results if 'Tier 1' in r[0]]):
            print("  1. Fix Tier 1 failures first (cheaper to iterate)")
            print("  2. Re-run: python tests/tier1_verify_analysis.py")
            print("  3. Debug Shannon plugin (see logs above)")
        else:
            print("  1. Review verification reports in test-builds/*/verification_report.txt")
            print("  2. Check build outputs for missing components")
            print("  3. Iterate on Shannon plugin or specifications")

    # Exit code
    return 0 if all_passed else 1


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test suite interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
