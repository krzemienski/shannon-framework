#!/usr/bin/env python3
"""
Final comprehensive test of code generation fix
"""

import asyncio
import logging
from pathlib import Path
import sys
import shutil
import subprocess

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from shannon.executor.complete_executor import CompleteExecutor

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

async def run_test(test_name: str, task: str, expected_files: list) -> bool:
    """Run a single test case"""

    logger.info(f"\n{'='*70}")
    logger.info(f"TEST: {test_name}")
    logger.info(f"{'='*70}")

    # Setup test directory
    test_dir = Path(f"/tmp/shannon-test-{test_name.replace(' ', '-').lower()}")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir()

    # Init git
    subprocess.run(["git", "init"], cwd=test_dir, capture_output=True, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=test_dir, capture_output=True, check=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=test_dir, capture_output=True, check=True)

    # Create .gitignore
    (test_dir / ".gitignore").write_text(".shannon_cache/\n")
    (test_dir / "README.md").write_text("# Test\n")
    subprocess.run(["git", "add", "."], cwd=test_dir, capture_output=True, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=test_dir, capture_output=True, check=True)

    # Execute task
    executor = CompleteExecutor(test_dir, logger=logger, max_iterations=1)

    logger.info(f"Task: {task}")
    logger.info(f"Expected files: {expected_files}")

    result = await executor.execute_autonomous(task, auto_commit=True)

    # Check results
    success = True
    if not result.success:
        logger.error(f"❌ Execution failed: {result.error_message}")
        success = False
    else:
        logger.info(f"✅ Execution succeeded")

        # Check files
        for expected_file in expected_files:
            file_path = test_dir / expected_file
            if not file_path.exists():
                logger.error(f"❌ Expected file not found: {expected_file}")
                success = False
            else:
                logger.info(f"✅ Found file: {expected_file}")
                content = file_path.read_text()
                logger.info(f"   Content preview: {content[:100]}...")

        # Check commit
        git_log = subprocess.run(
            ["git", "log", "--oneline"],
            cwd=test_dir,
            capture_output=True,
            text=True
        )
        commits = git_log.stdout.strip().split('\n')
        if len(commits) >= 2:
            logger.info(f"✅ Commit created: {commits[0]}")
        else:
            logger.error(f"❌ No commit created")
            success = False

    logger.info(f"\nResult: {'✅ PASS' if success else '❌ FAIL'}")
    return success

async def main():
    """Run all tests"""

    logger.info("\n" + "="*70)
    logger.info("CODE GENERATION FIX - COMPREHENSIVE TEST SUITE")
    logger.info("="*70)

    tests = [
        ("Simple File Creation", "create hello.py that prints hello", ["hello.py"]),
        ("Multiple Functions", "create utils.py with capitalize and lowercase functions", ["utils.py"]),
        ("With Docstrings", "create math_ops.py with multiply and divide functions with docstrings", ["math_ops.py"]),
    ]

    results = []
    for test_name, task, expected_files in tests:
        try:
            success = await run_test(test_name, task, expected_files)
            results.append((test_name, success))
        except Exception as e:
            logger.error(f"❌ Test crashed: {e}")
            results.append((test_name, False))

    # Summary
    logger.info("\n" + "="*70)
    logger.info("TEST SUMMARY")
    logger.info("="*70)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status}: {test_name}")

    logger.info(f"\n{passed}/{total} tests passed")

    return passed == total

if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
