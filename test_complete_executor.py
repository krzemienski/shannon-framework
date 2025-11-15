#!/usr/bin/env python3
"""
Test CompleteExecutor with fixed code generation
"""

import asyncio
import logging
from pathlib import Path
import sys
import shutil

# Setup path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from shannon.executor.complete_executor import CompleteExecutor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_complete_executor():
    """Test the complete executor with a simple file creation task"""

    # Create test directory
    test_dir = Path("/tmp/shannon-test-executor")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir()

    # Initialize git repo
    import subprocess
    subprocess.run(["git", "init"], cwd=test_dir, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=test_dir, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=test_dir, capture_output=True)

    # Create .gitignore
    gitignore = test_dir / ".gitignore"
    gitignore.write_text(".shannon_cache/\n__pycache__/\n*.pyc\n")

    # Create initial commit
    readme = test_dir / "README.md"
    readme.write_text("# Test Project\n")
    subprocess.run(["git", "add", "."], cwd=test_dir, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=test_dir, capture_output=True)

    logger.info(f"Test directory: {test_dir}")

    # Initialize executor
    executor = CompleteExecutor(
        project_root=test_dir,
        logger=logger,
        max_iterations=1  # Only try once for testing
    )

    # Test task
    task = "create calculator.py with add and subtract functions"

    logger.info(f"Task: {task}")
    logger.info("=" * 80)

    # Execute
    result = await executor.execute_autonomous(
        task=task,
        auto_commit=True
    )

    # Check results
    logger.info("=" * 80)
    logger.info(f"RESULTS:")
    logger.info(f"  Success: {result.success}")
    logger.info(f"  Task: {result.task_description}")
    logger.info(f"  Steps completed: {result.steps_completed}/{result.steps_total}")
    logger.info(f"  Commits: {len(result.commits_created)}")
    logger.info(f"  Duration: {result.duration_seconds:.2f}s")
    logger.info(f"  Iterations: {result.iterations_total}")
    logger.info(f"  Validations passed: {result.validations_passed}")
    logger.info(f"  Validations failed: {result.validations_failed}")

    if result.error_message:
        logger.error(f"  Error: {result.error_message}")

    # Check if file was created
    calc_file = test_dir / "calculator.py"
    if calc_file.exists():
        logger.info(f"\nSUCCESS: calculator.py was created!")
        logger.info(f"Content:\n{calc_file.read_text()[:500]}")
        return True
    else:
        logger.error(f"\nFAILURE: calculator.py was NOT created")
        # List files
        logger.info(f"Files in {test_dir}:")
        for f in test_dir.rglob("*"):
            if f.is_file():
                logger.info(f"  - {f.relative_to(test_dir)}")
        return False

if __name__ == '__main__':
    try:
        success = asyncio.run(test_complete_executor())
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Test failed with exception: {e}", exc_info=True)
        sys.exit(1)
