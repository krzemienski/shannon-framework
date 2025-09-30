"""
Real data execution validation tests.

Validates Shannon with actual execution:
- Real complex task execution
- Real file creation
- Real wave execution
- Actual performance metrics
"""

import asyncio
from pathlib import Path
from typing import Dict, Any

import pytest

from src.core.orchestrator import WaveOrchestrator, ComplexityAnalyzer
from src.core.agent import BaseAgent, AgentCapability, SimpleAgent
from src.core.wave_config import WaveConfig, WavePhase, ValidationLevel
from tests.validation.evidence_collector import EvidenceCollector


class TestRealDataExecution:
    """Real data execution validation suite"""

    @pytest.mark.asyncio
    async def test_complexity_analyzer_real_task(self, real_task_complex: Dict[str, Any]):
        """
        Test complexity analyzer with real complex task.

        Args:
            real_task_complex: Real complex task fixture
        """
        analyzer = ComplexityAnalyzer(threshold=0.7)

        # Analyze real task
        complexity = await analyzer.analyze(real_task_complex)

        # Validate complexity analysis
        assert complexity.total >= 0.0, "Complexity total should be non-negative"
        assert complexity.total <= 1.0, "Complexity total should not exceed 1.0"

        print(f"\nComplexity Analysis Results:")
        print(f"  Scope: {complexity.scope:.3f}")
        print(f"  Dependencies: {complexity.dependencies:.3f}")
        print(f"  Operations: {complexity.operations:.3f}")
        print(f"  Domains: {complexity.domains:.3f}")
        print(f"  Concurrency: {complexity.concurrency:.3f}")
        print(f"  Uncertainty: {complexity.uncertainty:.3f}")
        print(f"  Risk: {complexity.risk:.3f}")
        print(f"  Scale: {complexity.scale:.3f}")
        print(f"  Total: {complexity.total:.3f}")
        print(f"  Threshold Exceeded: {complexity.threshold_exceeded}")

        # Verify expected complexity for this task
        assert complexity.scope > 0.2, "Should detect significant scope"
        assert complexity.domains > 0.3, "Should detect multiple domains"
        assert complexity.operations > 0.2, "Should detect operations"

    @pytest.mark.asyncio
    async def test_orchestrator_decision_real_task(self, shannon_config: Dict[str, Any],
                                                   real_task_complex: Dict[str, Any]):
        """
        Test orchestrator decision making with real task.

        Args:
            shannon_config: Shannon configuration
            real_task_complex: Real complex task
        """
        orchestrator = WaveOrchestrator(shannon_config)

        # Make decision for real task
        decision = await orchestrator.analyze_and_decide(real_task_complex)

        print(f"\nOrchestration Decision:")
        print(f"  Should Orchestrate: {decision.should_orchestrate}")
        print(f"  Strategy: {decision.recommended_strategy.value}")
        print(f"  Agent Count: {decision.recommended_agent_count}")
        print(f"  Reasoning:")
        for reason in decision.reasoning:
            print(f"    - {reason}")
        if decision.warnings:
            print(f"  Warnings:")
            for warning in decision.warnings:
                print(f"    - {warning}")

        # Validate decision structure
        assert decision.complexity is not None, "Should have complexity analysis"
        assert decision.recommended_agent_count >= 3, "Should recommend multiple agents for complex task"
        assert len(decision.reasoning) > 0, "Should provide reasoning"

    @pytest.mark.asyncio
    async def test_real_wave_execution(self, shannon_config: Dict[str, Any], temp_workspace: Path):
        """
        Test real wave execution with file operations.

        Args:
            shannon_config: Shannon configuration
            temp_workspace: Temporary workspace directory
        """
        execution_id = "test_real_wave_001"
        collector = EvidenceCollector(execution_id)

        # Take initial file snapshot
        collector.snapshot_files(temp_workspace)

        # Create real agent factory
        async def analysis_task(task: Dict[str, Any]) -> Dict[str, Any]:
            """Real analysis operation"""
            # Create real analysis output file
            output_file = temp_workspace / 'analysis_results.txt'
            output_file.write_text("Analysis complete\nFiles analyzed: 10\nIssues found: 0\n")
            return {'status': 'success', 'output_file': str(output_file)}

        async def validation_task(task: Dict[str, Any]) -> Dict[str, Any]:
            """Real validation operation"""
            # Create real validation output file
            output_file = temp_workspace / 'validation_results.txt'
            output_file.write_text("Validation complete\nTests passed: 100%\n")
            return {'status': 'success', 'output_file': str(output_file)}

        agent_factory = {
            'AnalysisAgent': lambda agent_id, caps, cfg: SimpleAgent(
                agent_id, caps, {'callable': analysis_task, **cfg}
            ),
            'ValidationAgent': lambda agent_id, caps, cfg: SimpleAgent(
                agent_id, caps, {'callable': validation_task, **cfg}
            )
        }

        # Create wave configuration
        wave_config = WaveConfig(
            wave_id="test_wave_001",
            phases=[],
            strategy="progressive",
            validation_level=ValidationLevel.STANDARD
        )

        # Add phases with real operations
        from src.core.wave_config import AgentAllocation

        wave_config.phases.append(
            AgentAllocation(
                phase=WavePhase.ANALYSIS,
                agent_types=['AnalysisAgent'],
                agent_count=1,
                parallel_execution=True
            )
        )

        wave_config.phases.append(
            AgentAllocation(
                phase=WavePhase.VALIDATION,
                agent_types=['ValidationAgent'],
                agent_count=1,
                parallel_execution=True
            )
        )

        # Record operations
        collector.start_operation("wave_execution", "wave", None)

        # Execute wave
        orchestrator = WaveOrchestrator(shannon_config)
        result = await orchestrator.execute_wave(wave_config, agent_factory)

        collector.end_operation("wave_execution", result.success)

        # Take final file snapshot
        collector.snapshot_files(temp_workspace)

        # Finalize evidence
        evidence = collector.finalize(result.success)

        # Save evidence
        evidence_file = temp_workspace / 'execution_evidence.json'
        evidence.save_to_file(evidence_file)

        print(f"\nWave Execution Results:")
        print(f"  Success: {result.success}")
        print(f"  Duration: {result.total_duration_seconds:.3f}s")
        print(f"  Agents Executed: {result.agents_executed}")
        print(f"  Agents Succeeded: {result.agents_succeeded}")
        print(f"  Agents Failed: {result.agents_failed}")
        print(f"\nEvidence:")
        print(f"  Files Created: {len(evidence.files_created)}")
        print(f"  Operations: {len(evidence.operations)}")
        print(f"  Evidence File: {evidence_file}")

        # Validate execution
        assert result.success, "Wave execution should succeed"
        assert result.agents_executed > 0, "Should execute agents"
        assert result.agents_succeeded > 0, "Should have successful agents"
        assert result.agents_failed == 0, "Should have no failed agents"

        # Validate file creation
        assert len(evidence.files_created) > 0, "Should create files"
        assert evidence_file.exists(), "Should create evidence file"

        # Validate output files exist
        analysis_file = temp_workspace / 'analysis_results.txt'
        validation_file = temp_workspace / 'validation_results.txt'
        assert analysis_file.exists(), "Should create analysis results"
        assert validation_file.exists(), "Should create validation results"

    @pytest.mark.asyncio
    async def test_parallel_execution_detection(self, shannon_config: Dict[str, Any],
                                                temp_workspace: Path):
        """
        Test detection of parallel execution.

        Args:
            shannon_config: Shannon configuration
            temp_workspace: Temporary workspace
        """
        execution_id = "test_parallel_001"
        collector = EvidenceCollector(execution_id)

        # Create tasks that can run in parallel
        async def task_a(task: Dict[str, Any]) -> Dict[str, Any]:
            await asyncio.sleep(0.1)  # Simulate work
            return {'status': 'success', 'task': 'A'}

        async def task_b(task: Dict[str, Any]) -> Dict[str, Any]:
            await asyncio.sleep(0.1)  # Simulate work
            return {'status': 'success', 'task': 'B'}

        # Execute tasks in parallel
        collector.start_operation("task_a", "analysis", "agent_a")
        collector.start_operation("task_b", "analysis", "agent_b")

        results = await asyncio.gather(
            task_a({}),
            task_b({})
        )

        collector.end_operation("task_a", True)
        collector.end_operation("task_b", True)

        # Finalize and check parallelism
        evidence = collector.finalize(True)

        print(f"\nParallel Execution Detection:")
        if evidence.parallelism:
            print(f"  Parallelism Detected: {evidence.parallelism.parallelism_detected}")
            print(f"  Concurrent Operations: {len(evidence.parallelism.concurrent_operations)}")
            print(f"  Max Overlap: {evidence.parallelism.time_overlap_seconds:.3f}s")
            print(f"  Proof: {evidence.parallelism.proof}")
        else:
            print(f"  Parallelism Detected: False")

        # Validate parallelism detection
        assert evidence.parallelism is not None, "Should detect parallelism"
        assert evidence.parallelism.parallelism_detected, "Should confirm parallel execution"
        assert len(evidence.parallelism.concurrent_operations) > 0, "Should find concurrent pairs"
        assert evidence.parallelism.time_overlap_seconds > 0.0, "Should measure overlap"

    @pytest.mark.asyncio
    async def test_performance_metrics_collection(self, shannon_config: Dict[str, Any],
                                                  real_task_complex: Dict[str, Any]):
        """
        Test collection of real performance metrics.

        Args:
            shannon_config: Shannon configuration
            real_task_complex: Real complex task
        """
        orchestrator = WaveOrchestrator(shannon_config)

        # Execute analysis
        start_time = asyncio.get_event_loop().time()
        decision = await orchestrator.analyze_and_decide(real_task_complex)
        analysis_time = asyncio.get_event_loop().time() - start_time

        print(f"\nPerformance Metrics:")
        print(f"  Complexity Analysis Time: {analysis_time*1000:.2f}ms")
        print(f"  Decision Time: <1ms (synchronous)")

        # Validate performance
        assert analysis_time < 1.0, "Analysis should complete within 1 second"
        assert decision is not None, "Should produce decision"

    @pytest.mark.asyncio
    async def test_error_recovery_real_scenario(self, shannon_config: Dict[str, Any]):
        """
        Test error recovery with real failure scenario.

        Args:
            shannon_config: Shannon configuration
        """
        execution_id = "test_error_recovery_001"
        collector = EvidenceCollector(execution_id)

        # Create task that fails
        async def failing_task(task: Dict[str, Any]) -> Dict[str, Any]:
            raise RuntimeError("Simulated failure")

        agent_config = {
            'callable': failing_task,
            'wave_config': None,
            'phase': WavePhase.ANALYSIS
        }

        agent = SimpleAgent(
            agent_id="failing_agent_001",
            capabilities={AgentCapability.ANALYSIS},
            config=agent_config
        )

        # Initialize and run
        await agent.initialize()

        collector.start_operation("failing_task", "analysis", agent.agent_id)
        result = await agent.run({})
        collector.end_operation("failing_task", result.success, metadata={'error': result.error_message})

        evidence = collector.finalize(False, [result.error_message] if result.error_message else [])

        print(f"\nError Recovery Test:")
        print(f"  Task Success: {result.success}")
        print(f"  Error Message: {result.error_message}")
        print(f"  Evidence Collected: {len(evidence.operations)} operations")
        print(f"  Errors Recorded: {len(evidence.errors)}")

        # Validate error handling
        assert not result.success, "Failing task should report failure"
        assert result.error_message is not None, "Should capture error message"
        assert len(evidence.errors) > 0, "Evidence should record errors"
        assert evidence.operations[0].success is False, "Operation should be marked failed"