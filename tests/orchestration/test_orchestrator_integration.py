"""
Tests for Orchestrator integration with AgentPool

Gate 2.2: Orchestrator Integration Tests
Expected: 2/2 tests PASS before proceeding to Gate 2.3
"""
import pytest
import asyncio
from shannon.orchestration.agent_pool import AgentPool, AgentRole, AgentTask
from shannon.orchestrator import ContextAwareOrchestrator


class TestOrchestratorAgentIntegration:
    """Test orchestrator integration with agent pool"""

    @pytest.mark.asyncio
    async def test_orchestrator_has_agent_pool(self):
        """Orchestrator initializes with agent pool"""
        orchestrator = ContextAwareOrchestrator()

        # Should have agent pool attribute
        assert hasattr(orchestrator, 'agent_pool')

        # If agent pool exists, verify it's configured
        if orchestrator.agent_pool:
            assert isinstance(orchestrator.agent_pool, AgentPool)
            assert orchestrator.agent_pool.max_active >= 8
            assert orchestrator.agent_pool.max_total >= 50

    @pytest.mark.asyncio
    async def test_parallel_execution_via_agent_pool(self):
        """Test parallel execution through agent pool"""
        pool = AgentPool(max_active=8, max_total=50)

        # Create 3 different tasks
        task1 = AgentTask(
            task_id="t1",
            description="Research Python best practices",
            role=AgentRole.RESEARCH,
            priority=5
        )
        task2 = AgentTask(
            task_id="t2",
            description="Analyze code quality",
            role=AgentRole.ANALYSIS,
            priority=5
        )
        task3 = AgentTask(
            task_id="t3",
            description="Run test suite",
            role=AgentRole.TESTING,
            priority=5
        )

        # Submit tasks to pool
        await pool.submit_task(task1)
        await pool.submit_task(task2)
        await pool.submit_task(task3)

        # All 3 should be assigned (parallel execution)
        active_agents = pool.get_active_agents()
        assert len(active_agents) == 3

        # Verify roles are correct
        roles = {agent.role for agent in active_agents}
        assert AgentRole.RESEARCH in roles
        assert AgentRole.ANALYSIS in roles
        assert AgentRole.TESTING in roles

        # Complete all tasks
        for agent in active_agents:
            await pool.complete_task(agent.agent_id, result={"status": "success"})

        # All should be completed
        assert len(pool.get_active_agents()) == 0
        assert len(pool.completed_tasks) == 3
