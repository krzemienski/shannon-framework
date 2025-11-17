"""
Tests for enhanced AgentPool with spawn/lifecycle management

Gate 2.1: Backend Unit Tests
Expected: 4/4 tests PASS before proceeding to Gate 2.2
"""
import pytest
from shannon.orchestration.agent_pool import (
    AgentPool,
    Agent,
    AgentRole,
    AgentStatus,
    AgentTask
)


class TestAgentSpawning:
    """Test spawn_agent() functionality"""

    @pytest.mark.asyncio
    async def test_spawn_single_agent(self):
        """Spawn one agent successfully"""
        pool = AgentPool(max_active=8, max_total=50)

        # Spawn a research agent
        task = AgentTask(
            task_id="task-123",
            description="Research knowledge on topic X",
            role=AgentRole.RESEARCH,
            priority=5
        )

        agent = await pool.create_agent(AgentRole.RESEARCH)
        assigned_agent = await pool.assign_task(task)

        # Verify agent created and assigned
        assert assigned_agent is not None
        assert assigned_agent.agent_id is not None
        assert assigned_agent.role == AgentRole.RESEARCH
        assert assigned_agent.status == AgentStatus.ACTIVE
        assert assigned_agent.current_task == task

    @pytest.mark.asyncio
    async def test_capacity_limit_enforced(self):
        """Cannot exceed max_total capacity"""
        pool = AgentPool(max_active=2, max_total=3)

        # Create 3 agents (at max_total capacity)
        await pool.create_agent(AgentRole.RESEARCH)
        await pool.create_agent(AgentRole.ANALYSIS)
        await pool.create_agent(AgentRole.TESTING)

        # Try creating 4th agent (should fail)
        with pytest.raises(RuntimeError) as exc_info:
            await pool.create_agent(AgentRole.VALIDATION)

        assert "maximum capacity" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_multiple_agents_parallel(self):
        """Multiple agents can be active simultaneously"""
        pool = AgentPool(max_active=8, max_total=50)

        # Create 3 agents
        agent1 = await pool.create_agent(AgentRole.RESEARCH)
        agent2 = await pool.create_agent(AgentRole.ANALYSIS)
        agent3 = await pool.create_agent(AgentRole.TESTING)

        # Create 3 tasks
        task1 = AgentTask(task_id="t1", description="Research", role=AgentRole.RESEARCH, priority=5)
        task2 = AgentTask(task_id="t2", description="Analyze", role=AgentRole.ANALYSIS, priority=5)
        task3 = AgentTask(task_id="t3", description="Test", role=AgentRole.TESTING, priority=5)

        # Assign tasks
        await pool.assign_task(task1)
        await pool.assign_task(task2)
        await pool.assign_task(task3)

        # Verify all active
        active_agents = pool.get_active_agents()
        assert len(active_agents) == 3
        assert all(a.status == AgentStatus.ACTIVE for a in active_agents)

    @pytest.mark.asyncio
    async def test_agent_completion_frees_slot(self):
        """Completing agent frees slot for new agent"""
        pool = AgentPool(max_active=2, max_total=10)

        # Create and assign 2 agents (at max_active)
        agent1 = await pool.create_agent(AgentRole.RESEARCH)
        agent2 = await pool.create_agent(AgentRole.ANALYSIS)

        task1 = AgentTask(task_id="t1", description="Research", role=AgentRole.RESEARCH, priority=5)
        task2 = AgentTask(task_id="t2", description="Analyze", role=AgentRole.ANALYSIS, priority=5)

        await pool.assign_task(task1)
        await pool.assign_task(task2)

        # Both should be active
        assert len(pool.get_active_agents()) == 2

        # Complete agent 1
        await pool.complete_task(agent1.agent_id, result={"status": "success"})

        # Should now have 1 active agent
        active = pool.get_active_agents()
        assert len(active) == 1
        assert active[0].agent_id == agent2.agent_id

        # Can create and assign new agent
        agent3 = await pool.create_agent(AgentRole.TESTING)
        task3 = AgentTask(task_id="t3", description="Test", role=AgentRole.TESTING, priority=5)
        await pool.assign_task(task3)

        # Should have 2 active again
        assert len(pool.get_active_agents()) == 2
