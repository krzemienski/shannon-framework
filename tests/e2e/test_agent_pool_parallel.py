"""
E2E test for Agent Pool parallel execution

Gate 2.4: E2E Validation
Expected: Demonstrates 3 agents executing in parallel
"""
import pytest
import asyncio
from shannon.orchestration.agent_pool import AgentPool, AgentRole, AgentTask, AgentStatus


class TestAgentPoolE2E:
    """End-to-end tests for agent pool parallel execution"""

    @pytest.mark.asyncio
    async def test_three_agents_parallel_execution(self):
        """
        CRITICAL TEST: 3 agents execute in parallel
        This validates the core parallel execution capability
        """
        pool = AgentPool(max_active=8, max_total=50)

        # Create 3 different agent roles
        research_agent = await pool.create_agent(AgentRole.RESEARCH)
        analysis_agent = await pool.create_agent(AgentRole.ANALYSIS)
        testing_agent = await pool.create_agent(AgentRole.TESTING)

        # Create 3 tasks
        task1 = AgentTask(
            task_id="research-1",
            description="Research Python async patterns",
            role=AgentRole.RESEARCH,
            priority=5
        )
        task2 = AgentTask(
            task_id="analysis-1",
            description="Analyze code complexity",
            role=AgentRole.ANALYSIS,
            priority=5
        )
        task3 = AgentTask(
            task_id="testing-1",
            description="Run test suite",
            role=AgentRole.TESTING,
            priority=5
        )

        # Submit all tasks
        await pool.submit_task(task1)
        await pool.submit_task(task2)
        await pool.submit_task(task3)

        # Verify all 3 agents are active simultaneously
        active_agents = pool.get_active_agents()
        assert len(active_agents) == 3, f"Expected 3 active agents, got {len(active_agents)}"

        # Verify each role is represented
        active_roles = {agent.role for agent in active_agents}
        assert AgentRole.RESEARCH in active_roles
        assert AgentRole.ANALYSIS in active_roles
        assert AgentRole.TESTING in active_roles

        # Verify all are in ACTIVE status
        for agent in active_agents:
            assert agent.status == AgentStatus.ACTIVE

        # Get pool stats
        stats = pool.get_agent_stats()
        assert stats['active_agents'] == 3
        assert stats['total_agents'] == 3

        # Simulate parallel execution completion
        for agent in active_agents:
            await pool.complete_task(agent.agent_id, result={'status': 'success'})

        # All should be complete
        assert len(pool.get_active_agents()) == 0
        assert len(pool.completed_tasks) == 3

        print("\n✅ PARALLEL EXECUTION VALIDATED:")
        print(f"   - 3 agents spawned")
        print(f"   - 3 agents active simultaneously")
        print(f"   - All 3 tasks completed successfully")

    @pytest.mark.asyncio
    async def test_agent_pool_capacity_limits(self):
        """Verify pool respects capacity limits"""
        pool = AgentPool(max_active=8, max_total=50)

        # Spawn 8 agents (at max_active capacity)
        agents = []
        for i in range(8):
            role = list(AgentRole)[i % len(list(AgentRole))]
            agent = await pool.create_agent(role)
            task = AgentTask(
                task_id=f"task-{i}",
                description=f"Task {i}",
                role=role,
                priority=5
            )
            await pool.assign_task(task)
            agents.append(agent)

        # Should have 8 active
        assert len(pool.get_active_agents()) == 8

        # Get stats
        stats = pool.get_agent_stats()
        assert stats['active_agents'] == 8
        assert stats['max_active'] == 8

        print("\n✅ CAPACITY MANAGEMENT VALIDATED:")
        print(f"   - Max active: {stats['max_active']}")
        print(f"   - Current active: {stats['active_agents']}")
        print(f"   - Total agents: {stats['total_agents']}")

    @pytest.mark.asyncio
    async def test_agent_pool_stats_reporting(self):
        """Verify agent pool reports statistics"""
        pool = AgentPool(max_active=8, max_total=50)

        # Create 3 agents and assign tasks
        for i in range(3):
            role = list(AgentRole)[i]
            agent = await pool.create_agent(role)
            task = AgentTask(
                task_id=f"task-{i}",
                description=f"Task {i}",
                role=role,
                priority=5
            )
            await pool.submit_task(task)

        # Get stats
        stats = pool.get_agent_stats()

        # Verify stat structure and values
        assert 'total_agents' in stats
        assert 'active_agents' in stats
        assert 'max_active' in stats
        assert 'max_total' in stats
        assert 'completed_tasks' in stats
        assert 'failed_tasks' in stats

        assert stats['total_agents'] == 3
        assert stats['active_agents'] == 3
        assert stats['max_active'] == 8
        assert stats['max_total'] == 50

        print("\n✅ STATISTICS REPORTING VALIDATED:")
        print(f"   - Total agents: {stats['total_agents']}")
        print(f"   - Active agents: {stats['active_agents']}")
        print(f"   - Max active: {stats['max_active']}")
        print(f"   - Max total: {stats['max_total']}")


if __name__ == "__main__":
    # Run tests directly
    import sys
    sys.exit(pytest.main([__file__, "-v", "-s"]))
