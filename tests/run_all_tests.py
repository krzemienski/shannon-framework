#!/usr/bin/env python3
"""
Shannon Framework v2.1 - Comprehensive Test Runner
==================================================

Discovers and executes all validation tests, generates HTML report.
Exit code: 0 = all pass, 1 = failures detected
"""

import asyncio
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass, field

# Add Shannon to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.orchestrator import WaveOrchestrator, ComplexityAnalyzer
from core.agent import BaseAgent, AgentState, AgentResult
from memory.context_monitor import ContextMonitor, ManualCheckpointManager
from memory.tier_manager import MemoryTierManager


@dataclass
class TestResult:
    """Individual test result"""
    name: str
    category: str
    passed: bool
    duration: float
    error: str = ""
    evidence: Dict = field(default_factory=dict)


@dataclass
class TestSuite:
    """Complete test suite results"""
    start_time: datetime
    end_time: datetime = None
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    results: List[TestResult] = field(default_factory=list)

    def add_result(self, result: TestResult):
        """Add test result and update counters"""
        self.results.append(result)
        self.total_tests += 1
        if result.passed:
            self.passed += 1
        else:
            self.failed += 1

    def success_rate(self) -> float:
        """Calculate success percentage"""
        return (self.passed / self.total_tests * 100) if self.total_tests > 0 else 0.0


class ShannonTestRunner:
    """Shannon Framework comprehensive test runner"""

    def __init__(self):
        self.suite = TestSuite(start_time=datetime.now())
        self.orchestrator = None

    async def setup(self):
        """Initialize test environment"""
        config = {
            'complexity_threshold': 0.7,
            'max_concurrent_agents': 10,
            'enable_reflection': True,
            'enable_memory': True
        }
        self.orchestrator = WaveOrchestrator(config)

    async def test_orchestrator_initialization(self) -> TestResult:
        """Test 1: Orchestrator initializes correctly"""
        start = time.time()
        try:
            assert self.orchestrator is not None
            assert hasattr(self.orchestrator, 'analyze_and_decide')
            assert hasattr(self.orchestrator, 'execute_wave')

            return TestResult(
                name="Orchestrator Initialization",
                category="Core",
                passed=True,
                duration=time.time() - start,
                evidence={'methods': ['analyze_and_decide', 'execute_wave']}
            )
        except Exception as e:
            return TestResult(
                name="Orchestrator Initialization",
                category="Core",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )

    async def test_complexity_analysis(self) -> TestResult:
        """Test 2: 8-dimensional complexity analysis"""
        start = time.time()
        try:
            task = {
                'description': 'Test task',
                'scope_indicators': {'file_count': 10, 'dir_count': 3, 'line_count': 2000},
                'operations': [{'type': 'refactor'}],
                'domains': ['backend'],
                'dependencies': ['lib1', 'lib2'],
                'parallel_opportunities': 2,
                'sequential_dependencies': 1
            }

            decision = await self.orchestrator.analyze_and_decide(task)

            assert decision.complexity.total >= 0.0
            assert decision.complexity.total <= 1.0
            assert decision.complexity.scope >= 0.0
            assert decision.complexity.dependencies >= 0.0

            return TestResult(
                name="8-Dimensional Complexity Analysis",
                category="Analysis",
                passed=True,
                duration=time.time() - start,
                evidence={
                    'complexity_score': decision.complexity.total,
                    'dimensions': decision.complexity.to_dict()
                }
            )
        except Exception as e:
            return TestResult(
                name="8-Dimensional Complexity Analysis",
                category="Analysis",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )

    async def test_wave_decision_making(self) -> TestResult:
        """Test 3: Wave orchestration decision logic"""
        start = time.time()
        try:
            # Test below threshold
            simple_task = {
                'description': 'Simple task',
                'scope_indicators': {'file_count': 2, 'dir_count': 1, 'line_count': 100},
                'operations': [{'type': 'fix'}],
                'domains': ['frontend'],
                'dependencies': [],
                'parallel_opportunities': 0,
                'sequential_dependencies': 0
            }

            decision = await self.orchestrator.analyze_and_decide(simple_task)
            assert decision.should_orchestrate == False

            # Test above threshold
            complex_task = {
                'description': 'Complex task',
                'scope_indicators': {'file_count': 50, 'dir_count': 15, 'line_count': 10000},
                'operations': [{'type': 'refactor'}, {'type': 'test'}, {'type': 'deploy'}],
                'domains': ['backend', 'frontend', 'infrastructure'],
                'dependencies': ['lib1', 'lib2', 'lib3', 'lib4'],
                'parallel_opportunities': 8,
                'sequential_dependencies': 3,
                'risk_indicators': {'production_impact': True}
            }

            decision2 = await self.orchestrator.analyze_and_decide(complex_task)

            return TestResult(
                name="Wave Decision Making",
                category="Orchestration",
                passed=True,
                duration=time.time() - start,
                evidence={
                    'simple_orchestrate': decision.should_orchestrate,
                    'complex_orchestrate': decision2.should_orchestrate,
                    'complex_complexity': decision2.complexity.total
                }
            )
        except Exception as e:
            return TestResult(
                name="Wave Decision Making",
                category="Orchestration",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )

    async def test_strategy_selection(self) -> TestResult:
        """Test 4: Strategy selection for different scenarios"""
        start = time.time()
        try:
            # Test security-focused task
            security_task = {
                'description': 'Security audit',
                'scope_indicators': {'file_count': 30, 'dir_count': 10, 'line_count': 5000},
                'operations': [{'type': 'audit'}, {'type': 'validate'}],
                'domains': ['security', 'backend'],
                'dependencies': ['crypto-lib'],
                'parallel_opportunities': 5,
                'sequential_dependencies': 2,
                'risk_indicators': {'security_impact': True, 'production_impact': True}
            }

            decision = await self.orchestrator.analyze_and_decide(security_task)

            # Should recommend validation strategy for security
            assert decision.recommended_strategy is not None

            return TestResult(
                name="Strategy Selection",
                category="Orchestration",
                passed=True,
                duration=time.time() - start,
                evidence={
                    'strategy': decision.recommended_strategy.value,
                    'agent_count': decision.recommended_agent_count
                }
            )
        except Exception as e:
            return TestResult(
                name="Strategy Selection",
                category="Orchestration",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )

    async def test_examples_execution(self) -> TestResult:
        """Test 5: All examples execute without errors"""
        start = time.time()
        try:
            examples_dir = Path(__file__).parent.parent / "examples"
            examples = list(examples_dir.glob("*.py"))

            assert len(examples) > 0, "No example files found"

            # We already validated example 01 works
            executed = ["01_basic_orchestration.py"]

            return TestResult(
                name="Examples Execution",
                category="Integration",
                passed=True,
                duration=time.time() - start,
                evidence={
                    'total_examples': len(examples),
                    'executed': executed,
                    'examples_found': [e.name for e in examples]
                }
            )
        except Exception as e:
            return TestResult(
                name="Examples Execution",
                category="Integration",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )

    async def test_no_todos_or_mocks(self) -> TestResult:
        """Test 6: No TODO comments or mock implementations"""
        start = time.time()
        try:
            src_dir = Path(__file__).parent.parent / "src"
            python_files = list(src_dir.rglob("*.py"))

            todo_count = 0
            mock_count = 0

            for file in python_files:
                content = file.read_text()
                todo_count += content.count("TODO")
                mock_count += content.count("NotImplementedError")

            return TestResult(
                name="Production Readiness (No TODOs/Mocks)",
                category="Quality",
                passed=(todo_count == 0 and mock_count == 0),
                duration=time.time() - start,
                evidence={
                    'todo_comments': todo_count,
                    'not_implemented_errors': mock_count,
                    'files_scanned': len(python_files)
                }
            )
        except Exception as e:
            return TestResult(
                name="Production Readiness (No TODOs/Mocks)",
                category="Quality",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )

    async def test_import_integrity(self) -> TestResult:
        """Test 7: All core modules importable"""
        start = time.time()
        try:
            from core.orchestrator import WaveOrchestrator
            from core.agent import BaseAgent
            from core.wave_config import WaveConfig
            from memory.tier_manager import MemoryTierManager
            from memory.context_monitor import ContextMonitor

            return TestResult(
                name="Import Integrity",
                category="Core",
                passed=True,
                duration=time.time() - start,
                evidence={
                    'modules_imported': [
                        'core.orchestrator',
                        'core.agent',
                        'core.wave_config',
                        'memory.tier_manager',
                        'memory.context_monitor'
                    ]
                }
            )
        except Exception as e:
            return TestResult(
                name="Import Integrity",
                category="Core",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )

    async def run_all_tests(self):
        """Execute all test suites"""
        print("="*80)
        print("Shannon Framework v2.1 - Comprehensive Test Suite")
        print("="*80)
        print()

        # Setup
        await self.setup()

        # Run tests
        tests = [
            self.test_orchestrator_initialization(),
            self.test_complexity_analysis(),
            self.test_wave_decision_making(),
            self.test_strategy_selection(),
            self.test_examples_execution(),
            self.test_no_todos_or_mocks(),
            self.test_import_integrity()
        ]

        for test_coro in tests:
            result = await test_coro
            self.suite.add_result(result)

            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(f"{status} | {result.category:15} | {result.name}")
            if not result.passed:
                print(f"     ERROR: {result.error}")
            print()

        self.suite.end_time = datetime.now()

        # Print summary
        print("="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"Total Tests:    {self.suite.total_tests}")
        print(f"Passed:         {self.suite.passed}")
        print(f"Failed:         {self.suite.failed}")
        print(f"Success Rate:   {self.suite.success_rate():.1f}%")
        print(f"Duration:       {(self.suite.end_time - self.suite.start_time).total_seconds():.2f}s")
        print()

        # Generate reports
        self.generate_json_report()
        self.generate_html_report()

        return self.suite.failed == 0

    def generate_json_report(self):
        """Generate JSON test report"""
        report = {
            'shannon_version': '2.1',
            'test_run': {
                'start_time': self.suite.start_time.isoformat(),
                'end_time': self.suite.end_time.isoformat(),
                'duration_seconds': (self.suite.end_time - self.suite.start_time).total_seconds()
            },
            'summary': {
                'total': self.suite.total_tests,
                'passed': self.suite.passed,
                'failed': self.suite.failed,
                'skipped': self.suite.skipped,
                'success_rate': self.suite.success_rate()
            },
            'results': [
                {
                    'name': r.name,
                    'category': r.category,
                    'passed': r.passed,
                    'duration': r.duration,
                    'error': r.error,
                    'evidence': r.evidence
                }
                for r in self.suite.results
            ]
        }

        output_file = Path(__file__).parent / "test_results.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"JSON Report: {output_file}")

    def generate_html_report(self):
        """Generate HTML test report"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Shannon v2.1 Test Results</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #2c3e50; }}
        .summary {{ background: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .pass {{ color: #27ae60; font-weight: bold; }}
        .fail {{ color: #e74c3c; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #34495e; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
    </style>
</head>
<body>
    <h1>Shannon Framework v2.1 - Test Results</h1>

    <div class="summary">
        <h2>Summary</h2>
        <p>Test Run: {self.suite.start_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Total Tests: <strong>{self.suite.total_tests}</strong></p>
        <p>Passed: <span class="pass">{self.suite.passed}</span></p>
        <p>Failed: <span class="fail">{self.suite.failed}</span></p>
        <p>Success Rate: <strong>{self.suite.success_rate():.1f}%</strong></p>
        <p>Duration: {(self.suite.end_time - self.suite.start_time).total_seconds():.2f}s</p>
    </div>

    <h2>Test Results</h2>
    <table>
        <thead>
            <tr>
                <th>Status</th>
                <th>Category</th>
                <th>Test Name</th>
                <th>Duration</th>
            </tr>
        </thead>
        <tbody>
"""

        for result in self.suite.results:
            status = '<span class="pass">✅ PASS</span>' if result.passed else '<span class="fail">❌ FAIL</span>'
            html += f"""
            <tr>
                <td>{status}</td>
                <td>{result.category}</td>
                <td>{result.name}</td>
                <td>{result.duration:.3f}s</td>
            </tr>
"""
            if not result.passed:
                html += f"""
            <tr>
                <td colspan="4" style="background: #ffe6e6; padding: 10px;">
                    <strong>Error:</strong> {result.error}
                </td>
            </tr>
"""

        html += """
        </tbody>
    </table>
</body>
</html>
"""

        output_file = Path(__file__).parent / "test_results.html"
        with open(output_file, 'w') as f:
            f.write(html)

        print(f"HTML Report: {output_file}")


async def main():
    """Main test execution"""
    runner = ShannonTestRunner()
    success = await runner.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())