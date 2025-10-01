"""
Iteration Debugger - Systematic debugging for test iteration cycles.

Provides failure analysis, artifact comparison, log analysis, fix suggestions,
and regression detection to help iterate tests until they pass.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import difflib
import json
import re


@dataclass
class FailureAnalysis:
    """Analysis of a test failure"""
    test_name: str
    iteration: int
    failure_type: str
    root_cause: str
    suggested_fixes: List[str]
    related_issues: List[str]
    error_message: str
    traceback: Optional[str] = None
    artifacts_diff: Optional[str] = None
    log_issues: List[str] = field(default_factory=list)


class FailureClassifier:
    """Classifies test failures into categories"""

    FAILURE_PATTERNS = {
        'assertion_failure': [
            r'AssertionError',
            r'assert .* failed',
            r'Expected .* but got'
        ],
        'artifact_missing': [
            r'FileNotFoundError',
            r'No such file',
            r'Artifact not found',
            r'Missing artifact'
        ],
        'artifact_invalid': [
            r'KeyError',
            r'Missing required field',
            r'Invalid artifact structure',
            r'YAML parse error'
        ],
        'timeout': [
            r'TimeoutError',
            r'timeout exceeded',
            r'Command timed out'
        ],
        'command_failure': [
            r'Command failed',
            r'Non-zero exit code',
            r'Execution error'
        ],
        'magic_mcp_misuse': [
            r'Magic MCP.*React',
            r'Should use shadcn',
            r'Component library mismatch'
        ],
        'behavioral_pattern_missing': [
            r'Pattern not activated',
            r'CLAUDE\.md not loaded',
            r'Behavioral instruction missing'
        ]
    }

    @classmethod
    def classify(cls, error_msg: str, traceback: Optional[str] = None) -> str:
        """Classify failure type from error message and traceback"""
        text = f"{error_msg}\n{traceback or ''}"

        for failure_type, patterns in cls.FAILURE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return failure_type

        return 'unknown'


class RootCauseAnalyzer:
    """Identifies root causes of failures"""

    ROOT_CAUSES = {
        'assertion_failure': [
            "Output format doesn't match specification",
            "Command behavior differs from expected pattern",
            "Artifact content doesn't match requirements",
            "Missing or incorrect YAML frontmatter"
        ],
        'artifact_missing': [
            "Command didn't execute successfully",
            "Artifact not created in expected location",
            ".shannon/ directory permissions issue",
            "Artifact naming pattern mismatch"
        ],
        'artifact_invalid': [
            "Required field missing from artifact",
            "Field type doesn't match specification",
            "YAML structure invalid",
            "Frontmatter parsing failed"
        ],
        'timeout': [
            "Command execution too slow",
            "Infinite loop in command logic",
            "Network request hanging",
            "Resource contention"
        ],
        'command_failure': [
            "Command logic error",
            "Invalid arguments or parameters",
            "Dependency missing",
            "Runtime exception"
        ],
        'magic_mcp_misuse': [
            "Using Magic MCP for React instead of shadcn",
            "Component library selection incorrect",
            "Shannon behavioral pattern not followed"
        ],
        'behavioral_pattern_missing': [
            "CLAUDE.md not loaded or found",
            "Behavioral instructions not activated",
            "Shannon context missing",
            "Pattern matching failed"
        ]
    }

    @classmethod
    def identify(cls, failure_type: str, error_msg: str) -> str:
        """Identify probable root cause"""
        causes = cls.ROOT_CAUSES.get(failure_type, ["Unknown root cause"])

        # Try to match specific causes based on error message
        for cause in causes:
            keywords = cause.lower().split()[:3]  # First few keywords
            if any(kw in error_msg.lower() for kw in keywords):
                return cause

        # Return first cause as default
        return causes[0] if causes else "Unknown root cause - review logs and error details"


class FixSuggester:
    """Suggests fixes for common failure types"""

    FIX_SUGGESTIONS = {
        'assertion_failure': [
            "Compare actual vs expected output using artifact_differ",
            "Review Shannon behavioral patterns in Shannon/*.md",
            "Verify CLAUDE.md instructions loaded correctly",
            "Check command implementation matches specification",
            "Update test expectations if behavior is correct"
        ],
        'artifact_missing': [
            "Verify command executed without errors (check exit code)",
            "Check .shannon/ directory exists and is writable",
            "Review command output for error messages",
            "Confirm artifact naming matches test expectations",
            "Check command creates artifacts in correct location"
        ],
        'artifact_invalid': [
            "Update artifact structure in Shannon specs",
            "Check YAML frontmatter format and fields",
            "Verify required fields match specification",
            "Review field naming conventions",
            "Validate YAML syntax"
        ],
        'timeout': [
            "Increase timeout threshold in test configuration",
            "Check for infinite loops in command logic",
            "Optimize command execution performance",
            "Review long-running operations",
            "Check for hanging network requests"
        ],
        'command_failure': [
            "Review command implementation in Shannon/*.md",
            "Check error handling logic",
            "Verify dependencies are installed",
            "Review argument parsing and validation",
            "Check for runtime exceptions in logs"
        ],
        'magic_mcp_misuse': [
            "Use shadcn for React component generation",
            "Remove Magic MCP tool selection for React",
            "Update COMMANDS.md to specify shadcn for React",
            "Review component library selection logic",
            "Check MCP integration configuration"
        ],
        'behavioral_pattern_missing': [
            "Verify CLAUDE.md exists and is readable",
            "Check Shannon context loading in setup",
            "Review behavioral pattern activation logic",
            "Confirm pattern matching works correctly",
            "Update behavioral instructions if needed"
        ]
    }

    @classmethod
    def suggest(cls, failure_type: str, context: Optional[Dict] = None) -> List[str]:
        """Generate fix suggestions for failure type"""
        suggestions = cls.FIX_SUGGESTIONS.get(failure_type, [
            "Review debug logs for details",
            "Check error message and traceback",
            "Compare with passing tests",
            "Verify test setup and prerequisites"
        ])

        # Add context-specific suggestions
        if context:
            if context.get('iteration', 0) > 3:
                suggestions.append("Consider if test expectations need adjustment")
            if context.get('related_failures'):
                suggestions.append("Check related failures for patterns")

        return suggestions


class ArtifactDiffer:
    """Compares expected vs actual artifacts"""

    def __init__(self):
        self.diff_cache: Dict[Tuple[str, str], str] = {}

    def compare(self, expected: Path, actual: Path, context_lines: int = 3) -> str:
        """Generate unified diff between artifacts"""
        cache_key = (str(expected), str(actual))
        if cache_key in self.diff_cache:
            return self.diff_cache[cache_key]

        # Check existence
        if not expected.exists():
            result = f"Expected artifact missing: {expected}"
        elif not actual.exists():
            result = f"Actual artifact missing: {actual}"
        else:
            # Generate diff
            expected_lines = expected.read_text().splitlines(keepends=True)
            actual_lines = actual.read_text().splitlines(keepends=True)

            diff = difflib.unified_diff(
                expected_lines,
                actual_lines,
                fromfile=f"expected/{expected.name}",
                tofile=f"actual/{actual.name}",
                n=context_lines
            )

            result = ''.join(diff)
            if not result:
                result = "Files are identical"

        self.diff_cache[cache_key] = result
        return result

    def compare_json(self, expected: Path, actual: Path) -> Dict[str, Any]:
        """Compare JSON artifacts with structured diff"""
        if not expected.exists() or not actual.exists():
            return {"error": "One or both files missing"}

        try:
            expected_data = json.loads(expected.read_text())
            actual_data = json.loads(actual.read_text())

            differences = self._deep_diff(expected_data, actual_data)
            return {
                "has_differences": bool(differences),
                "differences": differences
            }
        except json.JSONDecodeError as e:
            return {"error": f"JSON parse error: {e}"}

    def _deep_diff(self, expected: Any, actual: Any, path: str = "") -> List[Dict]:
        """Recursively find differences in nested structures"""
        differences = []

        if type(expected) != type(actual):
            differences.append({
                "path": path,
                "issue": "type_mismatch",
                "expected": type(expected).__name__,
                "actual": type(actual).__name__
            })
            return differences

        if isinstance(expected, dict):
            all_keys = set(expected.keys()) | set(actual.keys())
            for key in all_keys:
                key_path = f"{path}.{key}" if path else key
                if key not in expected:
                    differences.append({
                        "path": key_path,
                        "issue": "unexpected_key",
                        "actual": actual[key]
                    })
                elif key not in actual:
                    differences.append({
                        "path": key_path,
                        "issue": "missing_key",
                        "expected": expected[key]
                    })
                else:
                    differences.extend(
                        self._deep_diff(expected[key], actual[key], key_path)
                    )

        elif isinstance(expected, list):
            if len(expected) != len(actual):
                differences.append({
                    "path": path,
                    "issue": "length_mismatch",
                    "expected": len(expected),
                    "actual": len(actual)
                })
            else:
                for i, (exp_item, act_item) in enumerate(zip(expected, actual)):
                    differences.extend(
                        self._deep_diff(exp_item, act_item, f"{path}[{i}]")
                    )

        elif expected != actual:
            differences.append({
                "path": path,
                "issue": "value_mismatch",
                "expected": expected,
                "actual": actual
            })

        return differences


class LogAnalyzer:
    """Analyzes command logs for issues"""

    ISSUE_PATTERNS = {
        'error': [
            (r'ERROR', 'Error found in execution'),
            (r'Exception', 'Exception occurred'),
            (r'Failed to', 'Operation failed'),
            (r'Could not', 'Operation could not complete')
        ],
        'warning': [
            (r'WARNING', 'Warning detected'),
            (r'WARN', 'Warning detected'),
            (r'Deprecated', 'Using deprecated feature')
        ],
        'mcp_issue': [
            (r'Magic MCP.*React', 'Magic MCP used for React (should use shadcn)'),
            (r'MCP server.*unavailable', 'MCP server unavailable'),
            (r'MCP.*timeout', 'MCP operation timed out')
        ],
        'behavioral': [
            (r'CLAUDE\.md.*not found', 'CLAUDE.md not found'),
            (r'Pattern.*not activated', 'Behavioral pattern not activated'),
            (r'Context.*missing', 'Shannon context missing')
        ]
    }

    def analyze(self, log_path: Path) -> Dict[str, Any]:
        """Analyze command execution log"""
        if not log_path.exists():
            return {
                'issues': ['Log file not found'],
                'log_file': str(log_path),
                'requires_attention': True
            }

        log_content = log_path.read_text()
        issues = []

        # Check for patterns
        for category, patterns in self.ISSUE_PATTERNS.items():
            for pattern, description in patterns:
                if re.search(pattern, log_content, re.IGNORECASE):
                    issues.append({
                        'category': category,
                        'description': description,
                        'pattern': pattern
                    })

        # Extract error lines
        error_lines = [
            line.strip()
            for line in log_content.splitlines()
            if any(keyword in line.upper() for keyword in ['ERROR', 'EXCEPTION', 'FAILED'])
        ]

        return {
            'issues': issues,
            'error_lines': error_lines[:10],  # First 10 errors
            'log_file': str(log_path),
            'requires_attention': len(issues) > 0 or len(error_lines) > 0,
            'log_size': len(log_content)
        }


class RegressionDetector:
    """Detects when fixes break other tests"""

    def __init__(self):
        self.test_history: Dict[str, List[bool]] = {}

    def record_result(self, test_name: str, passed: bool):
        """Record test result"""
        if test_name not in self.test_history:
            self.test_history[test_name] = []
        self.test_history[test_name].append(passed)

    def detect_regressions(self) -> List[Dict[str, Any]]:
        """Detect tests that regressed (passed before, fail now)"""
        regressions = []

        for test_name, history in self.test_history.items():
            if len(history) >= 2:
                # Check if test passed before but fails now
                if history[-2] and not history[-1]:
                    regressions.append({
                        'test': test_name,
                        'previous_result': 'pass',
                        'current_result': 'fail',
                        'iterations_since_regression': 1
                    })

        return regressions

    def get_test_stability(self, test_name: str) -> float:
        """Calculate test stability (% of times it passed)"""
        history = self.test_history.get(test_name, [])
        if not history:
            return 0.0
        return sum(history) / len(history)


class IterationDebugger:
    """Systematic debugging for test iteration"""

    def __init__(self, test_results_dir: Path):
        self.results_dir = test_results_dir
        self.results_dir.mkdir(parents=True, exist_ok=True)

        self.iteration_count = 0
        self.failures: List[FailureAnalysis] = []
        self.passing_count = 0
        self.total_count = 0

        self.classifier = FailureClassifier()
        self.root_cause_analyzer = RootCauseAnalyzer()
        self.fix_suggester = FixSuggester()
        self.artifact_differ = ArtifactDiffer()
        self.log_analyzer = LogAnalyzer()
        self.regression_detector = RegressionDetector()

    def start_iteration(self) -> int:
        """Start new iteration"""
        self.iteration_count += 1
        self.failures = []
        self.passing_count = 0
        self.total_count = 0
        return self.iteration_count

    def analyze_failure(
        self,
        test_name: str,
        failure_info: Dict[str, Any]
    ) -> FailureAnalysis:
        """Analyze test failure and suggest fixes"""
        error_msg = failure_info.get('error', '')
        traceback = failure_info.get('traceback')

        # Classify failure
        failure_type = self.classifier.classify(error_msg, traceback)

        # Identify root cause
        root_cause = self.root_cause_analyzer.identify(failure_type, error_msg)

        # Generate fix suggestions
        context = {
            'iteration': self.iteration_count,
            'related_failures': self._find_related_failures(test_name)
        }
        suggested_fixes = self.fix_suggester.suggest(failure_type, context)

        # Analyze artifacts if paths provided
        artifacts_diff = None
        if 'expected_artifact' in failure_info and 'actual_artifact' in failure_info:
            artifacts_diff = self.artifact_differ.compare(
                Path(failure_info['expected_artifact']),
                Path(failure_info['actual_artifact'])
            )

        # Analyze logs if path provided
        log_issues = []
        if 'log_path' in failure_info:
            log_analysis = self.log_analyzer.analyze(Path(failure_info['log_path']))
            log_issues = [issue['description'] for issue in log_analysis.get('issues', [])]

        # Create analysis
        analysis = FailureAnalysis(
            test_name=test_name,
            iteration=self.iteration_count,
            failure_type=failure_type,
            root_cause=root_cause,
            suggested_fixes=suggested_fixes,
            related_issues=self._find_related_failures(test_name),
            error_message=error_msg,
            traceback=traceback,
            artifacts_diff=artifacts_diff,
            log_issues=log_issues
        )

        self.failures.append(analysis)
        self._save_analysis(test_name, analysis)

        # Record for regression detection
        self.regression_detector.record_result(test_name, False)

        return analysis

    def record_pass(self, test_name: str):
        """Record test pass"""
        self.passing_count += 1
        self.regression_detector.record_result(test_name, True)

    def _find_related_failures(self, test_name: str) -> List[str]:
        """Find related test failures"""
        related = []
        for failure in self.failures:
            if failure.test_name != test_name:
                # Check for common patterns
                if (failure.failure_type == self.failures[-1].failure_type if self.failures else None):
                    related.append(failure.test_name)
        return related[:5]  # Limit to 5

    def _save_analysis(self, test_name: str, analysis: FailureAnalysis):
        """Save analysis to file"""
        analysis_file = self.results_dir / f"{test_name}_iteration_{self.iteration_count}.json"
        analysis_file.write_text(json.dumps({
            'test': analysis.test_name,
            'iteration': analysis.iteration,
            'failure_type': analysis.failure_type,
            'root_cause': analysis.root_cause,
            'suggested_fixes': analysis.suggested_fixes,
            'related_issues': analysis.related_issues,
            'error_message': analysis.error_message,
            'log_issues': analysis.log_issues
        }, indent=2))

    def generate_iteration_report(self) -> Path:
        """Generate report for current iteration"""
        self.total_count = self.passing_count + len(self.failures)
        pass_rate = (self.passing_count / self.total_count * 100) if self.total_count > 0 else 0

        # Check for regressions
        regressions = self.regression_detector.detect_regressions()

        report = f"""# Test Iteration {self.iteration_count} Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Tests Passing**: {self.passing_count}
- **Tests Failing**: {len(self.failures)}
- **Total Tests**: {self.total_count}
- **Pass Rate**: {pass_rate:.1f}%
- **Regressions**: {len(regressions)}

## Failures Analyzed

{self._format_failures()}

## Suggested Fixes by Priority

{self._format_fixes()}

## Regressions Detected

{self._format_regressions(regressions)}

## Progress Tracking

- Iteration: {self.iteration_count}
- Previous Pass Rate: {self._get_previous_pass_rate():.1f}%
- Current Pass Rate: {pass_rate:.1f}%
- Improvement: {pass_rate - self._get_previous_pass_rate():+.1f}%

## Next Actions

{self._suggest_next_actions()}
"""

        report_path = self.results_dir / f"iteration_{self.iteration_count}_report.md"
        report_path.write_text(report)
        return report_path

    def _format_failures(self) -> str:
        """Format failure details"""
        if not self.failures:
            return "No failures to analyze.\n"

        sections = []
        for i, failure in enumerate(self.failures, 1):
            section = f"""
### {i}. {failure.test_name}

**Failure Type**: {failure.failure_type}
**Root Cause**: {failure.root_cause}

**Error**:
```
{failure.error_message[:200]}...
```

**Log Issues**: {', '.join(failure.log_issues) if failure.log_issues else 'None'}
"""
            sections.append(section)

        return '\n'.join(sections)

    def _format_fixes(self) -> str:
        """Format suggested fixes"""
        if not self.failures:
            return "No fixes needed - all tests passing!\n"

        # Group fixes by failure type
        fixes_by_type: Dict[str, List[str]] = {}
        for failure in self.failures:
            if failure.failure_type not in fixes_by_type:
                fixes_by_type[failure.failure_type] = []
            fixes_by_type[failure.failure_type].extend(failure.suggested_fixes)

        sections = []
        for failure_type, fixes in fixes_by_type.items():
            unique_fixes = list(dict.fromkeys(fixes))  # Remove duplicates
            section = f"""
### {failure_type.replace('_', ' ').title()}

{chr(10).join(f'{i}. {fix}' for i, fix in enumerate(unique_fixes, 1))}
"""
            sections.append(section)

        return '\n'.join(sections)

    def _format_regressions(self, regressions: List[Dict]) -> str:
        """Format regression details"""
        if not regressions:
            return "No regressions detected.\n"

        sections = []
        for reg in regressions:
            section = f"- **{reg['test']}**: Was passing, now failing"
            sections.append(section)

        return '\n'.join(sections)

    def _get_previous_pass_rate(self) -> float:
        """Get pass rate from previous iteration"""
        if self.iteration_count <= 1:
            return 0.0

        prev_report = self.results_dir / f"iteration_{self.iteration_count - 1}_report.md"
        if not prev_report.exists():
            return 0.0

        content = prev_report.read_text()
        match = re.search(r'Pass Rate:\s+([\d.]+)%', content)
        return float(match.group(1)) if match else 0.0

    def _suggest_next_actions(self) -> str:
        """Suggest next actions based on current state"""
        if not self.failures:
            return "✅ All tests passing! Ready to proceed.\n"

        actions = []

        # Most common failure type
        failure_types = [f.failure_type for f in self.failures]
        most_common = max(set(failure_types), key=failure_types.count)
        actions.append(
            f"1. Focus on {most_common.replace('_', ' ')} issues "
            f"({failure_types.count(most_common)} tests affected)"
        )

        # Check for regressions
        regressions = self.regression_detector.detect_regressions()
        if regressions:
            actions.append(f"2. Fix {len(regressions)} regressed test(s) immediately")

        # Iteration strategy
        if self.iteration_count > 5:
            actions.append("3. Consider if test expectations need adjustment")
        else:
            actions.append("3. Apply suggested fixes and re-run tests")

        return '\n'.join(actions) + '\n'
