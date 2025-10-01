#!/usr/bin/env python3
"""
Shannon Framework Functional Test Runner

Executes comprehensive functional tests and generates detailed reports.
Provides test discovery, execution, result collection, and failure analysis.
"""

import sys
import argparse
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import re


@dataclass
class TestResult:
    """Container for individual test results"""
    test_name: str
    category: str
    status: str  # passed, failed, skipped, error
    duration: float
    message: Optional[str] = None
    traceback: Optional[str] = None


@dataclass
class TestSummary:
    """Overall test execution summary"""
    total: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errors: int = 0
    duration: float = 0.0
    success_rate: float = 0.0


class TestRunner:
    """
    Comprehensive test runner for Shannon Framework functional tests.

    Features:
    - Automatic test discovery
    - Parallel execution support
    - Coverage reporting
    - HTML and markdown report generation
    - Artifact preservation
    - Detailed failure analysis
    """

    def __init__(
        self,
        project_dir: Path,
        verbose: bool = False,
        category: str = "all",
        parallel: bool = False
    ):
        self.project_dir = project_dir
        self.verbose = verbose
        self.category = category
        self.parallel = parallel
        self.test_dir = project_dir / "tests" / "functional"
        self.results_dir = project_dir / "test-results"
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.test_results: List[TestResult] = []
        self.summary = TestSummary()

        # Ensure directories exist
        self.results_dir.mkdir(parents=True, exist_ok=True)
        (self.results_dir / "logs").mkdir(exist_ok=True)
        (self.results_dir / "html").mkdir(exist_ok=True)

    def discover_tests(self) -> List[Path]:
        """
        Discover all functional tests based on category filter.

        Returns:
            List of test file paths
        """
        if not self.test_dir.exists():
            print(f"⚠️  Test directory not found: {self.test_dir}")
            return []

        if self.category == "all":
            pattern = "test_*.py"
        else:
            # Map categories to test file patterns
            category_map = {
                "command": "test_01_*.py",
                "behavioral": "test_02_*.py",
                "integration": "test_03_*.py"
            }
            pattern = category_map.get(self.category, "test_*.py")

        tests = sorted(self.test_dir.glob(pattern))

        if self.verbose:
            print(f"📋 Discovered {len(tests)} test file(s):")
            for test in tests:
                print(f"   - {test.name}")

        return tests

    def run_all_tests(self) -> Dict:
        """
        Execute all functional tests with pytest.

        Returns:
            Dict containing test results and metadata
        """
        self.start_time = datetime.now()
        timestamp = self.start_time.strftime('%Y%m%d_%H%M%S')

        print("🧪 Shannon Framework Functional Test Suite")
        print("=" * 60)
        print(f"📅 Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Category: {self.category}")
        print(f"📂 Test Directory: {self.test_dir.relative_to(self.project_dir)}")
        print("=" * 60)

        # Discover tests
        test_files = self.discover_tests()
        if not test_files:
            print("\n❌ No tests found!")
            return {
                "success": False,
                "output": "No tests discovered",
                "errors": "No test files found",
                "duration": 0.0,
                "summary": asdict(self.summary)
            }

        # Build pytest command
        pytest_args = self._build_pytest_args(timestamp)

        if self.verbose:
            print(f"\n🔧 Running command: {' '.join(pytest_args)}")
            print()

        # Execute pytest
        result = subprocess.run(
            pytest_args,
            cwd=self.project_dir,
            capture_output=True,
            text=True
        )

        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()

        # Parse pytest output
        self._parse_pytest_output(result.stdout, result.stderr)

        # Calculate summary
        self.summary.duration = duration
        if self.summary.total > 0:
            self.summary.success_rate = (self.summary.passed / self.summary.total) * 100

        # Print summary
        self._print_summary()

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr,
            "duration": duration,
            "summary": asdict(self.summary),
            "results": [asdict(r) for r in self.test_results]
        }

    def _build_pytest_args(self, timestamp: str) -> List[str]:
        """Build pytest command arguments"""
        args = [
            sys.executable, "-m", "pytest",
            str(self.test_dir),
            "-v",
            "--tb=short",
            "--color=yes",
            f"--html={self.results_dir}/html/report_{timestamp}.html",
            "--self-contained-html",
            "--junit-xml=test-results/junit.xml"
        ]

        # Add coverage if available
        try:
            import pytest_cov
            args.extend([
                "--cov=shannon",
                f"--cov-report=html:{self.results_dir}/html/coverage_{timestamp}",
                "--cov-report=term"
            ])
        except ImportError:
            if self.verbose:
                print("ℹ️  pytest-cov not available, skipping coverage")

        # Add parallel execution if requested
        if self.parallel:
            try:
                import pytest_xdist
                args.extend(["-n", "auto"])
            except ImportError:
                if self.verbose:
                    print("ℹ️  pytest-xdist not available, running sequentially")

        # Add verbose output
        if self.verbose:
            args.append("-vv")

        # Filter by category if specified
        if self.category != "all":
            category_map = {
                "command": "test_01",
                "behavioral": "test_02",
                "integration": "test_03"
            }
            pattern = category_map.get(self.category)
            if pattern:
                args.extend(["-k", pattern])

        return args

    def _parse_pytest_output(self, stdout: str, stderr: str) -> None:
        """Parse pytest output to extract test results"""
        # Extract test results from output
        # Pattern: test_file.py::test_name PASSED/FAILED/SKIPPED [X%]
        pattern = r'(test_\w+\.py)::(test_\w+)\s+(PASSED|FAILED|SKIPPED|ERROR)'

        for match in re.finditer(pattern, stdout):
            test_file, test_name, status = match.groups()

            result = TestResult(
                test_name=f"{test_file}::{test_name}",
                category=self._extract_category(test_file),
                status=status.lower(),
                duration=0.0  # Would need more detailed parsing
            )

            self.test_results.append(result)

            # Update summary
            self.summary.total += 1
            if status == "PASSED":
                self.summary.passed += 1
            elif status == "FAILED":
                self.summary.failed += 1
            elif status == "SKIPPED":
                self.summary.skipped += 1
            elif status == "ERROR":
                self.summary.errors += 1

        # If no results parsed, try summary line
        if not self.test_results:
            summary_pattern = r'(\d+) passed(?:, (\d+) failed)?(?:, (\d+) skipped)?(?:, (\d+) error)?'
            match = re.search(summary_pattern, stdout)
            if match:
                passed, failed, skipped, errors = match.groups()
                self.summary.passed = int(passed) if passed else 0
                self.summary.failed = int(failed) if failed else 0
                self.summary.skipped = int(skipped) if skipped else 0
                self.summary.errors = int(errors) if errors else 0
                self.summary.total = sum([
                    self.summary.passed,
                    self.summary.failed,
                    self.summary.skipped,
                    self.summary.errors
                ])

    def _extract_category(self, test_file: str) -> str:
        """Extract test category from filename"""
        if "test_01" in test_file:
            return "command"
        elif "test_02" in test_file:
            return "behavioral"
        elif "test_03" in test_file:
            return "integration"
        return "unknown"

    def _print_summary(self) -> None:
        """Print test execution summary"""
        print("\n" + "=" * 60)
        print("📊 Test Execution Summary")
        print("=" * 60)
        print(f"Total Tests:    {self.summary.total}")
        print(f"✅ Passed:      {self.summary.passed}")
        print(f"❌ Failed:      {self.summary.failed}")
        print(f"⏭️  Skipped:     {self.summary.skipped}")
        print(f"💥 Errors:      {self.summary.errors}")
        print(f"⏱️  Duration:    {self.summary.duration:.2f}s")
        print(f"📈 Success:     {self.summary.success_rate:.1f}%")
        print("=" * 60)

    def generate_markdown_report(self, results: Dict) -> Path:
        """
        Generate comprehensive markdown test report.

        Args:
            results: Test execution results

        Returns:
            Path to generated report
        """
        timestamp = self.start_time.strftime('%Y%m%d_%H%M%S')
        report_path = self.results_dir / f"TEST_REPORT_{timestamp}.md"

        status_emoji = "✅" if results['success'] else "❌"
        status_text = "PASSED" if results['success'] else "FAILED"

        report = f"""# Shannon Framework Functional Test Report

**Date**: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
**Duration**: {results['duration']:.2f} seconds
**Status**: {status_emoji} {status_text}
**Category**: {self.category}

## Executive Summary

{self._generate_executive_summary(results)}

## Test Results

### Summary Statistics

| Metric | Count | Percentage |
|--------|-------|------------|
| Total Tests | {self.summary.total} | 100.0% |
| ✅ Passed | {self.summary.passed} | {(self.summary.passed/self.summary.total*100) if self.summary.total > 0 else 0:.1f}% |
| ❌ Failed | {self.summary.failed} | {(self.summary.failed/self.summary.total*100) if self.summary.total > 0 else 0:.1f}% |
| ⏭️ Skipped | {self.summary.skipped} | {(self.summary.skipped/self.summary.total*100) if self.summary.total > 0 else 0:.1f}% |
| 💥 Errors | {self.summary.errors} | {(self.summary.errors/self.summary.total*100) if self.summary.total > 0 else 0:.1f}% |

### Test Execution Details

{self._format_test_results()}

## Test Output

<details>
<summary>Click to expand full test output</summary>

```
{results['output']}
```

</details>

{self._format_error_output(results['errors'])}

## Artifacts Created

{self._list_artifacts()}

## Debug Logs

{self._list_debug_logs()}

## Code Coverage

{self._format_coverage_info(timestamp)}

## Failure Analysis

{self._analyze_failures()}

## Next Steps

{self._generate_next_steps(results['success'])}

---

*Report generated by Shannon Framework Test Runner*
*Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        report_path.write_text(report)
        return report_path

    def _generate_executive_summary(self, results: Dict) -> str:
        """Generate executive summary section"""
        if results['success']:
            return f"""
🎉 **All tests passed successfully!**

Shannon Framework validation completed with {self.summary.passed} tests passing.
The framework is functioning correctly and meets all functional requirements.
"""
        else:
            return f"""
⚠️ **Test failures detected!**

{self.summary.failed} test(s) failed out of {self.summary.total} total tests.
{self.summary.errors} error(s) occurred during execution.

**Action Required**: Review failed tests and address issues before deployment.
"""

    def _format_test_results(self) -> str:
        """Format individual test results as markdown table"""
        if not self.test_results:
            return "*No detailed test results available*"

        lines = ["| Test | Category | Status | Duration |", "|------|----------|--------|----------|"]

        for result in self.test_results:
            status_emoji = {
                "passed": "✅",
                "failed": "❌",
                "skipped": "⏭️",
                "error": "💥"
            }.get(result.status, "❓")

            lines.append(
                f"| `{result.test_name}` | {result.category} | "
                f"{status_emoji} {result.status.upper()} | {result.duration:.2f}s |"
            )

        return "\n".join(lines)

    def _format_error_output(self, errors: str) -> str:
        """Format error output section"""
        if not errors or errors.strip() == "":
            return ""

        return f"""
## Error Output

<details>
<summary>Click to expand error details</summary>

```
{errors}
```

</details>
"""

    def _list_artifacts(self) -> str:
        """List all artifacts created during tests"""
        shannon_dir = self.project_dir / ".shannon"
        if not shannon_dir.exists():
            return "*No artifacts created*"

        artifacts = []
        for item in sorted(shannon_dir.rglob("*")):
            if item.is_file():
                rel_path = item.relative_to(shannon_dir)
                size = item.stat().st_size
                artifacts.append(f"- `{rel_path}` ({size:,} bytes)")

        return "\n".join(artifacts) if artifacts else "*No artifacts*"

    def _list_debug_logs(self) -> str:
        """List all debug logs created"""
        log_dir = self.results_dir / "logs"
        if not log_dir.exists() or not any(log_dir.iterdir()):
            return "*No debug logs*"

        logs = []
        for log in sorted(log_dir.glob("*.log")):
            size = log.stat().st_size
            logs.append(f"- [`{log.name}`]({log.relative_to(self.results_dir)}) ({size:,} bytes)")

        return "\n".join(logs) if logs else "*No debug logs*"

    def _format_coverage_info(self, timestamp: str) -> str:
        """Format code coverage information"""
        coverage_dir = self.results_dir / "html" / f"coverage_{timestamp}"
        if coverage_dir.exists():
            return f"""
Code coverage report generated: [`coverage_{timestamp}/index.html`]({coverage_dir.relative_to(self.results_dir)}/index.html)

Run `open test-results/html/coverage_{timestamp}/index.html` to view detailed coverage.
"""
        return "*Coverage reporting not available*"

    def _analyze_failures(self) -> str:
        """Analyze and categorize test failures"""
        failed_tests = [r for r in self.test_results if r.status in ('failed', 'error')]

        if not failed_tests:
            return "✅ No failures to analyze"

        analysis = ["### Failed Test Details\n"]

        for result in failed_tests:
            analysis.append(f"#### `{result.test_name}`\n")
            analysis.append(f"- **Category**: {result.category}")
            analysis.append(f"- **Status**: {result.status.upper()}")

            if result.message:
                analysis.append(f"- **Message**: {result.message}")

            if result.traceback:
                analysis.append("\n**Traceback**:\n```python")
                analysis.append(result.traceback)
                analysis.append("```\n")

            analysis.append("")

        return "\n".join(analysis)

    def _generate_next_steps(self, success: bool) -> str:
        """Generate next steps based on test results"""
        if success:
            return """
### ✅ All Tests Passed

1. **Review Coverage**: Check code coverage report for any gaps
2. **Deploy**: Framework is validated and ready for deployment
3. **Documentation**: Update any documentation based on test insights
4. **Monitor**: Set up monitoring for production deployment
"""
        else:
            return f"""
### ⚠️ Action Required

1. **Review Failures**: Examine failed tests in detail above
2. **Check Logs**: Review debug logs for additional context
3. **Fix Issues**: Address root causes of test failures
4. **Retest**: Run tests again after fixes: `./run_tests.py`
5. **Validate**: Ensure all tests pass before deployment

**Failed Tests**: {self.summary.failed}
**Errors**: {self.summary.errors}
"""


def main():
    """Main entry point for test runner"""
    parser = argparse.ArgumentParser(
        description="Run Shannon Framework functional tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Run all tests
  %(prog)s --verbose                 # Run with detailed output
  %(prog)s --category command        # Run only command tests
  %(prog)s --parallel                # Run tests in parallel
  %(prog)s --category behavioral -v  # Run behavioral tests verbosely
        """
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--category",
        choices=["command", "behavioral", "integration", "all"],
        default="all",
        help="Test category to run (default: all)"
    )

    parser.add_argument(
        "--parallel", "-p",
        action="store_true",
        help="Run tests in parallel (requires pytest-xdist)"
    )

    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip markdown report generation"
    )

    args = parser.parse_args()

    # Determine project directory
    project_dir = Path(__file__).resolve().parent.parent.parent

    # Create and run test runner
    runner = TestRunner(
        project_dir=project_dir,
        verbose=args.verbose,
        category=args.category,
        parallel=args.parallel
    )

    # Execute tests
    results = runner.run_all_tests()

    # Generate report unless disabled
    if not args.no_report:
        report_path = runner.generate_markdown_report(results)
        print(f"\n📊 Report generated: {report_path.relative_to(project_dir)}")
        print(f"   View with: open {report_path}")

    # Exit with appropriate code
    sys.exit(0 if results['success'] else 1)


if __name__ == "__main__":
    main()
