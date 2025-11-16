#!/usr/bin/env python3
"""Quick validation script for orchestration layer.

Runs smoke tests to verify all components are working correctly.
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from shannon.orchestration import (
    TaskParser,
    ExecutionPlanner,
    StateManager,
    Orchestrator,
    ParsedTask,
    ExecutionPlan,
    Checkpoint
)
from shannon.orchestration.task_parser import TaskIntent
from shannon.skills.registry import SkillRegistry


def print_test(name: str, passed: bool):
    """Print test result"""
    symbol = "✓" if passed else "✗"
    color = "\033[92m" if passed else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{symbol}{reset} {name}")


async def main():
    """Run validation tests"""
    print("\n" + "="*60)
    print("Shannon Orchestration Layer - Validation")
    print("="*60 + "\n")

    all_passed = True

    # Test 1: Imports
    print("[1/6] Testing imports...")
    try:
        from shannon.orchestration import TaskParser, ExecutionPlanner, StateManager, Orchestrator
        print_test("All orchestration imports successful", True)
    except Exception as e:
        print_test(f"Import failed: {e}", False)
        all_passed = False

    # Test 2: TaskParser
    print("\n[2/6] Testing TaskParser...")
    registry = None
    try:
        # Create a minimal registry for testing
        from pathlib import Path
        schema_path = Path(__file__).parent.parent / 'src' / 'shannon' / 'skills' / 'schema.json'
        registry = await SkillRegistry.get_instance(schema_path=schema_path)
        parser = TaskParser(registry)

        parsed = await parser.parse("create authentication system with JWT")

        checks = [
            parsed.raw_task == "create authentication system with JWT",
            parsed.intent.goal == "create",
            "authentication" in parsed.intent.domain or "auth" in [kw for kw in parsed.intent.keywords],
            len(parsed.candidate_skills) > 0,
            parsed.confidence > 0.0
        ]

        print_test("TaskParser extracts intent correctly", all(checks))
        print(f"    Goal: {parsed.intent.goal}")
        print(f"    Domain: {parsed.intent.domain}")
        print(f"    Keywords: {', '.join(parsed.intent.keywords[:3])}")
        print(f"    Confidence: {parsed.confidence:.2%}")

        if not all(checks):
            all_passed = False

    except Exception as e:
        print_test(f"TaskParser failed: {e}", False)
        all_passed = False

    # Test 3: ExecutionPlanner
    print("\n[3/6] Testing ExecutionPlanner...")
    try:
        from shannon.skills.dependencies import DependencyResolver

        resolver = DependencyResolver(registry)
        planner = ExecutionPlanner(registry, resolver)

        # Use the parsed task from above
        plan = await planner.create_plan(parsed)

        checks = [
            plan.plan_id is not None,
            plan.task == parsed.raw_task,
            len(plan.steps) > 0,
            plan.estimated_duration > 0
        ]

        print_test("ExecutionPlanner creates valid plans", all(checks))
        print(f"    Steps: {len(plan.steps)}")
        print(f"    Checkpoints: {len(plan.checkpoints)}")
        print(f"    Duration estimate: {plan.estimated_duration:.0f}s")

        if not all(checks):
            all_passed = False

    except Exception as e:
        print_test(f"ExecutionPlanner failed: {e}", False)
        all_passed = False

    # Test 4: StateManager
    print("\n[4/6] Testing StateManager...")
    try:
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)

            manager = StateManager(project_root)

            # Create test file
            test_file = project_root / "test.txt"
            test_file.write_text("initial content")
            manager.add_tracked_file(test_file)

            # Create checkpoint
            checkpoint = await manager.create_checkpoint("test_checkpoint")

            checks = [
                checkpoint.id is not None,
                checkpoint.label == "test_checkpoint",
                len(checkpoint.file_snapshots) > 0
            ]

            print_test("StateManager creates checkpoints", all(checks))
            print(f"    Checkpoint ID: {checkpoint.id[:8]}...")
            print(f"    Files tracked: {len(checkpoint.file_snapshots)}")

            if not all(checks):
                all_passed = False

    except Exception as e:
        print_test(f"StateManager failed: {e}", False)
        all_passed = False

    # Test 5: Orchestrator
    print("\n[5/6] Testing Orchestrator...")
    try:
        from shannon.orchestration.orchestrator import Orchestrator, OrchestratorResult

        print_test("Orchestrator class loads correctly", True)
        print("    (Full execution test requires registered skills)")

    except Exception as e:
        print_test(f"Orchestrator failed: {e}", False)
        all_passed = False

    # Test 6: CLI Command
    print("\n[6/6] Testing CLI command registration...")
    try:
        from shannon.cli.commands import cli
        from click.testing import CliRunner

        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])

        has_do_command = 'do ' in result.output

        print_test("shannon do command registered", has_do_command)

        if has_do_command:
            # Extract description
            import re
            match = re.search(r'do\s+(.+)', result.output)
            if match:
                print(f"    Description: {match.group(1).strip()}")

        if not has_do_command:
            all_passed = False

    except Exception as e:
        print_test(f"CLI command test failed: {e}", False)
        all_passed = False

    # Summary
    print("\n" + "="*60)
    if all_passed:
        print("\033[92m✓ ALL VALIDATION TESTS PASSED\033[0m")
        print("="*60 + "\n")
        print("The orchestration layer is working correctly!")
        print("\nNext steps:")
        print("  1. Run integration tests: pytest tests/integration/test_orchestration.py")
        print("  2. Try the command: shannon do \"create simple feature\" --dry-run")
        print()
        return 0
    else:
        print("\033[91m✗ SOME VALIDATION TESTS FAILED\033[0m")
        print("="*60 + "\n")
        print("Please review the errors above.")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
