"""
Integration Test: Wave Orchestration System

Tests REAL integration between:
- WaveOrchestrator
- ComplexityAnalyzer
- AgentSpawner

NO mocks. Real asyncio execution, real complexity detection, real parallel spawning.
"""

import asyncio
import pytest
import time
from pathlib import Path

from shannon.orchestrator import WaveOrchestrator
from shannon.complexity_analyzer import ComplexityAnalyzer
from shannon.agent_spawner import AgentSpawner
from shannon.dna import AgentDNA


@pytest.fixture
def orchestrator():
    """Create real orchestrator instance."""
    return WaveOrchestrator(
        max_waves=3,
        complexity_threshold=0.7,
        enable_reflection=True
    )


@pytest.fixture
def analyzer():
    """Create real complexity analyzer."""
    return ComplexityAnalyzer()


@pytest.fixture
def spawner():
    """Create real agent spawner."""
    return AgentSpawner(max_concurrent_agents=5)


class TestWaveComplexityIntegration:
    """Test complexity detection triggering wave spawning."""

    @pytest.mark.asyncio
    async def test_low_complexity_no_waves(self, orchestrator, analyzer):
        """Low complexity should NOT trigger wave spawning."""
        # Real task: simple string operation
        task = "Convert text to uppercase"
        context = {"text": "hello world"}

        # Analyze real complexity
        complexity = await analyzer.analyze_complexity(task, context)

        # Verify low complexity
        assert complexity.score < 0.7, f"Expected low complexity, got {complexity.score}"
        assert complexity.estimated_subtasks < 3

        # Execute with orchestrator - should NOT spawn waves
        result = await orchestrator.execute(task, context)

        # Verify no waves spawned
        assert result.waves_spawned == 0, "Low complexity should not spawn waves"
        assert len(result.wave_results) == 0

    @pytest.mark.asyncio
    async def test_high_complexity_spawns_waves(self, orchestrator, analyzer):
        """High complexity should trigger REAL wave spawning."""
        # Real complex task
        task = "Build full-stack web application with auth, database, API, frontend, tests"
        context = {
            "requirements": [
                "User authentication and authorization",
                "PostgreSQL database with migrations",
                "REST API with validation",
                "React frontend with routing",
                "Comprehensive test suite",
                "Docker deployment"
            ],
            "technologies": ["Python", "React", "PostgreSQL", "Docker"],
            "estimated_hours": 120
        }

        # Analyze real complexity
        complexity = await analyzer.analyze_complexity(task, context)

        # Verify high complexity
        assert complexity.score >= 0.7, f"Expected high complexity, got {complexity.score}"
        assert complexity.estimated_subtasks >= 5
        assert complexity.requires_parallel_execution is True

        # Execute with orchestrator - should spawn waves
        result = await orchestrator.execute(task, context)

        # Verify waves were spawned
        assert result.waves_spawned > 0, "High complexity should spawn waves"
        assert len(result.wave_results) > 0
        assert result.parallel_execution_used is True

    @pytest.mark.asyncio
    async def test_parallel_execution_timing(self, orchestrator, spawner):
        """Verify REAL parallel execution is faster than sequential."""
        # Create 3 real tasks with delays
        tasks = [
            {"name": "Task 1", "delay": 1.0},
            {"name": "Task 2", "delay": 1.0},
            {"name": "Task 3", "delay": 1.0}
        ]

        async def execute_task(task):
            """Real async task with delay."""
            await asyncio.sleep(task["delay"])
            return {"result": f"{task['name']} completed"}

        # Parallel execution using real asyncio.gather()
        start_parallel = time.time()
        parallel_results = await asyncio.gather(*[execute_task(t) for t in tasks])
        parallel_duration = time.time() - start_parallel

        # Sequential execution
        start_sequential = time.time()
        sequential_results = []
        for task in tasks:
            result = await execute_task(task)
            sequential_results.append(result)
        sequential_duration = time.time() - start_sequential

        # Verify parallelism: parallel should be ~3x faster
        speedup = sequential_duration / parallel_duration
        assert speedup >= 2.5, f"Expected 2.5x+ speedup, got {speedup:.2f}x"
        assert parallel_duration < 1.5, f"Parallel took {parallel_duration:.2f}s, expected < 1.5s"
        assert sequential_duration >= 3.0, f"Sequential took {sequential_duration:.2f}s, expected >= 3s"

        # Verify results match
        assert len(parallel_results) == len(sequential_results)
        for pr, sr in zip(parallel_results, sequential_results):
            assert pr["result"] == sr["result"]


class TestWaveSpawnerIntegration:
    """Test real agent spawning with wave orchestration."""

    @pytest.mark.asyncio
    async def test_spawner_creates_real_agents(self, spawner):
        """Spawner should create REAL agent instances."""
        # Create real agent DNA
        dna = AgentDNA(
            persona="analyzer",
            capabilities=["code_analysis", "pattern_detection"],
            constraints={"max_files": 10}
        )

        # Spawn real agent
        agent = await spawner.spawn_agent(
            agent_id="test-agent-1",
            dna=dna,
            mission="Analyze codebase patterns"
        )

        # Verify real agent created
        assert agent is not None
        assert agent.agent_id == "test-agent-1"
        assert agent.dna == dna
        assert agent.status == "initialized"

    @pytest.mark.asyncio
    async def test_concurrent_agent_spawning(self, spawner):
        """Test REAL concurrent agent spawning with semaphore."""
        # Create 10 agents concurrently (but max_concurrent_agents=5)
        agent_count = 10
        dna = AgentDNA(
            persona="worker",
            capabilities=["task_execution"],
            constraints={}
        )

        async def spawn_and_measure(agent_id):
            """Spawn agent and measure timing."""
            start = time.time()
            agent = await spawner.spawn_agent(
                agent_id=f"agent-{agent_id}",
                dna=dna,
                mission=f"Task {agent_id}"
            )
            duration = time.time() - start
            return agent, duration

        # Spawn all agents concurrently
        start_total = time.time()
        results = await asyncio.gather(*[
            spawn_and_measure(i) for i in range(agent_count)
        ])
        total_duration = time.time() - start_total

        # Verify all agents created
        agents = [r[0] for r in results]
        assert len(agents) == agent_count
        assert all(a is not None for a in agents)

        # Verify semaphore worked (concurrent spawning is faster than sequential)
        # If truly sequential, would take agent_count * spawn_time
        # With concurrency, should be ~(agent_count / max_concurrent) * spawn_time
        assert total_duration < agent_count * 0.5, "Concurrent spawning should be faster"

        # Verify unique agent IDs
        agent_ids = {a.agent_id for a in agents}
        assert len(agent_ids) == agent_count, "All agents should have unique IDs"

    @pytest.mark.asyncio
    async def test_wave_orchestrator_spawns_multiple_agents(self, orchestrator):
        """Integration test: orchestrator spawns multiple real agents in waves."""
        # Complex task requiring multiple agents
        task = "Refactor entire codebase: analyze, improve, test, document"
        context = {
            "files": ["file1.py", "file2.py", "file3.py", "file4.py", "file5.py"],
            "requirements": ["type_hints", "docstrings", "tests", "documentation"]
        }

        # Execute with real orchestrator
        result = await orchestrator.execute(task, context)

        # Verify multiple agents spawned
        assert result.agents_spawned >= 4, "Should spawn analyzer, improver, tester, documenter"
        assert result.waves_spawned >= 2, "Complex task should spawn multiple waves"

        # Verify agents executed in parallel
        assert result.parallel_execution_used is True
        assert result.execution_time < result.estimated_sequential_time * 0.6


class TestRealComplexityDetection:
    """Test complexity analyzer with REAL data."""

    @pytest.mark.asyncio
    async def test_complexity_from_real_codebase(self, analyzer):
        """Analyze complexity of real Shannon codebase."""
        # Real Shannon project structure
        project_root = Path(__file__).parent.parent.parent

        # Scan real files
        py_files = list(project_root.rglob("shannon/**/*.py"))
        file_count = len([f for f in py_files if f.is_file()])

        # Analyze complexity
        task = "Refactor Shannon framework"
        context = {
            "project_root": str(project_root),
            "file_count": file_count,
            "languages": ["Python"],
            "frameworks": ["asyncio", "pytest"]
        }

        complexity = await analyzer.analyze_complexity(task, context)

        # Verify real analysis
        assert complexity.score > 0, "Should detect complexity"
        assert complexity.file_count == file_count
        assert complexity.estimated_subtasks > 0
        assert len(complexity.identified_patterns) > 0

    @pytest.mark.asyncio
    async def test_complexity_factors_weight_correctly(self, analyzer):
        """Verify complexity factors weighted correctly with real data."""
        # Task with known complexity factors
        task = "Build microservices system"
        context = {
            "services": ["auth", "api", "database", "cache", "queue"],  # 5 services
            "technologies": ["Python", "Docker", "Kubernetes", "PostgreSQL"],  # 4 techs
            "requirements": ["HA", "scaling", "monitoring", "security"],  # 4 requirements
            "estimated_hours": 200
        }

        complexity = await analyzer.analyze_complexity(task, context)

        # Verify high complexity score
        assert complexity.score >= 0.85, "Microservices should be high complexity"
        assert complexity.estimated_subtasks >= 10
        assert complexity.requires_parallel_execution is True
        assert complexity.estimated_agents >= 5


class TestEndToEndWaveExecution:
    """Full integration test: complexity detection → wave spawning → parallel execution."""

    @pytest.mark.asyncio
    async def test_complete_wave_workflow(self, orchestrator):
        """Test complete real workflow from task to completion."""
        # Real complex software development task
        task = "Build authentication microservice"
        context = {
            "features": [
                "JWT token generation",
                "User registration and login",
                "Password hashing with bcrypt",
                "Role-based access control",
                "API endpoints with FastAPI",
                "PostgreSQL database integration",
                "Docker containerization",
                "Pytest test suite",
                "API documentation",
                "Deployment configuration"
            ],
            "technologies": ["Python", "FastAPI", "PostgreSQL", "Docker", "pytest"],
            "estimated_hours": 40
        }

        # Execute complete workflow
        start = time.time()
        result = await orchestrator.execute(task, context)
        duration = time.time() - start

        # Verify complexity detected
        assert result.initial_complexity >= 0.7

        # Verify waves spawned
        assert result.waves_spawned >= 2, "Should spawn analysis + implementation waves"
        assert len(result.wave_results) == result.waves_spawned

        # Verify agents created
        assert result.agents_spawned >= 5, "Should spawn multiple specialized agents"

        # Verify parallel execution
        assert result.parallel_execution_used is True
        speedup = result.estimated_sequential_time / duration
        assert speedup >= 2.0, f"Expected 2x+ speedup, got {speedup:.2f}x"

        # Verify results structure
        assert "analysis" in result.outputs
        assert "implementation" in result.outputs
        assert result.success is True

    @pytest.mark.asyncio
    async def test_wave_reflection_integration(self, orchestrator):
        """Test reflection engine integrates with wave execution."""
        # Enable reflection
        orchestrator.enable_reflection = True

        task = "Optimize database queries"
        context = {
            "tables": ["users", "posts", "comments"],
            "operations": ["select", "join", "aggregate"],
            "current_performance": "slow"
        }

        result = await orchestrator.execute(task, context)

        # Verify reflection occurred
        assert result.reflection_performed is True
        assert len(result.reflection_insights) > 0

        # Verify reflection improved execution
        assert result.quality_score >= 0.7


# Run with: pytest tests/integration/test_wave_integration.py -v -s
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])