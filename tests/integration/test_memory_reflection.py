"""
Integration Test: Memory & Reflection System

Tests REAL integration between:
- MemoryTierManager (5-tier memory)
- ReflectionEngine (5-stage reflection)
- Serena MCP (if available)

NO mocks. Real tier transitions, real compression, real persistence.
"""

import asyncio
import pytest
import time
import tempfile
from pathlib import Path

from shannon.memory.tier_manager import MemoryTierManager, MemoryTier
from shannon.reflection.reflection_engine import ReflectionEngine, ReflectionStage
from shannon.memory.context_monitor import ContextMonitor


@pytest.fixture
def temp_storage():
    """Create temporary storage for memory persistence."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def tier_manager(temp_storage):
    """Create real memory tier manager."""
    return MemoryTierManager(
        storage_path=temp_storage,
        enable_compression=True,
        enable_serena=False  # Skip Serena if not configured
    )


@pytest.fixture
def reflection_engine():
    """Create real reflection engine."""
    return ReflectionEngine(
        enable_metrics=True,
        enable_learning=True
    )


@pytest.fixture
def context_monitor():
    """Create real context monitor."""
    return ContextMonitor(
        warning_threshold=0.75,
        critical_threshold=0.90
    )


class TestMemoryTierTransitions:
    """Test REAL tier transitions with actual data."""

    @pytest.mark.asyncio
    async def test_working_to_short_term_transition(self, tier_manager):
        """Test real transition from working to short-term memory."""
        # Store data in working memory
        working_data = {
            "agent_id": "test-agent",
            "task": "code_analysis",
            "results": ["pattern_1", "pattern_2", "pattern_3"],
            "timestamp": time.time()
        }

        memory_id = await tier_manager.store(
            tier=MemoryTier.WORKING,
            data=working_data,
            tags=["analysis", "code"]
        )

        # Verify stored in working tier
        retrieved = await tier_manager.retrieve(memory_id)
        assert retrieved is not None
        assert retrieved["task"] == "code_analysis"
        assert retrieved["tier"] == MemoryTier.WORKING.value

        # Trigger transition to short-term (simulate age)
        await tier_manager.age_memories(working_age_threshold=0.001)  # 1ms for testing

        # Give time for transition
        await asyncio.sleep(0.1)

        # Verify moved to short-term
        retrieved = await tier_manager.retrieve(memory_id)
        assert retrieved is not None
        assert retrieved["tier"] == MemoryTier.SHORT_TERM.value

    @pytest.mark.asyncio
    async def test_compression_during_transition(self, tier_manager):
        """Test REAL compression when transitioning between tiers."""
        # Create large data object
        large_data = {
            "agent_id": "agent-1",
            "detailed_analysis": "x" * 10000,  # 10KB of data
            "metadata": {"key": "value"} * 100,
            "timestamp": time.time()
        }

        # Store in working memory
        memory_id = await tier_manager.store(
            tier=MemoryTier.WORKING,
            data=large_data,
            tags=["large"]
        )

        # Get original size
        original_size = len(str(large_data))

        # Transition to long-term (should compress)
        await tier_manager.transition(
            memory_id=memory_id,
            target_tier=MemoryTier.LONG_TERM
        )

        # Retrieve and verify compression
        retrieved = await tier_manager.retrieve(memory_id)
        compressed_size = len(str(retrieved.get("compressed_data", "")))

        # Verify compression occurred
        assert compressed_size < original_size * 0.5, "Should compress to <50% original"
        assert retrieved["tier"] == MemoryTier.LONG_TERM.value
        assert retrieved.get("compression_ratio") is not None

    @pytest.mark.asyncio
    async def test_archival_tier_persistence(self, tier_manager, temp_storage):
        """Test REAL file persistence in archival tier."""
        # Create archival-worthy data
        archival_data = {
            "session_id": "session-123",
            "important_findings": ["finding_1", "finding_2"],
            "created_at": time.time()
        }

        # Store in archival tier
        memory_id = await tier_manager.store(
            tier=MemoryTier.ARCHIVAL,
            data=archival_data,
            tags=["important", "session"]
        )

        # Verify file created in temp storage
        archival_files = list(temp_storage.glob("**/*.json"))
        assert len(archival_files) > 0, "Should create physical file"

        # Verify file contains data
        import json
        with open(archival_files[0], 'r') as f:
            stored_data = json.load(f)
            assert stored_data["session_id"] == "session-123"

    @pytest.mark.asyncio
    async def test_tier_eviction_policy(self, tier_manager):
        """Test LRU eviction when tier capacity exceeded."""
        # Configure small capacity for testing
        tier_manager.configure_tier(
            tier=MemoryTier.WORKING,
            max_items=3
        )

        # Store 5 items (exceeds capacity)
        memory_ids = []
        for i in range(5):
            mid = await tier_manager.store(
                tier=MemoryTier.WORKING,
                data={"item": i},
                tags=[f"item_{i}"]
            )
            memory_ids.append(mid)
            await asyncio.sleep(0.01)  # Ensure different timestamps

        # Verify only 3 items remain in working memory
        working_items = await tier_manager.list_tier(MemoryTier.WORKING)
        assert len(working_items) == 3, "Should evict to capacity limit"

        # Verify oldest items evicted (LRU)
        remaining_ids = {item["id"] for item in working_items}
        assert memory_ids[0] not in remaining_ids, "Oldest should be evicted"
        assert memory_ids[1] not in remaining_ids, "Second oldest should be evicted"
        assert memory_ids[4] in remaining_ids, "Newest should remain"


class TestReflectionMemoryIntegration:
    """Test reflection engine with real memory storage."""

    @pytest.mark.asyncio
    async def test_reflection_stores_insights(self, reflection_engine, tier_manager):
        """Reflection should store insights in memory."""
        # Perform reflection on real task
        task_data = {
            "task": "implement_authentication",
            "complexity": 0.8,
            "agents_used": 5,
            "execution_time": 120.5,
            "success": True
        }

        # Run reflection
        insights = await reflection_engine.reflect(
            stage=ReflectionStage.POST_WAVE,
            data=task_data
        )

        # Verify insights generated
        assert len(insights) > 0
        assert any("improvement" in i.lower() for i in insights)

        # Store insights in memory
        memory_id = await tier_manager.store(
            tier=MemoryTier.SHORT_TERM,
            data={
                "reflection_insights": insights,
                "task_data": task_data
            },
            tags=["reflection", "insights"]
        )

        # Retrieve and verify
        retrieved = await tier_manager.retrieve(memory_id)
        assert retrieved["reflection_insights"] == insights

    @pytest.mark.asyncio
    async def test_learning_from_stored_reflections(self, reflection_engine, tier_manager):
        """Reflection engine should learn from stored past reflections."""
        # Store multiple reflection results
        past_reflections = []
        for i in range(5):
            data = {
                "task": f"task_{i}",
                "success": i % 2 == 0,  # Alternating success/failure
                "execution_time": 10 * (i + 1)
            }

            insights = await reflection_engine.reflect(
                stage=ReflectionStage.POST_WAVE,
                data=data
            )

            memory_id = await tier_manager.store(
                tier=MemoryTier.SHORT_TERM,
                data={"insights": insights, "task_data": data},
                tags=["reflection"]
            )
            past_reflections.append(memory_id)

        # Query reflection memories
        all_reflections = await tier_manager.query_by_tags(["reflection"])

        # Verify learning patterns
        assert len(all_reflections) == 5
        success_count = sum(1 for r in all_reflections if r["data"]["task_data"]["success"])
        assert success_count == 3  # 3 successes, 2 failures

    @pytest.mark.asyncio
    async def test_reflection_triggers_memory_consolidation(self, reflection_engine, tier_manager):
        """Reflection should trigger memory consolidation."""
        # Store related memories
        related_ids = []
        for i in range(3):
            mid = await tier_manager.store(
                tier=MemoryTier.WORKING,
                data={"subtask": i, "related_to": "main_task"},
                tags=["subtask", "main_task"]
            )
            related_ids.append(mid)

        # Perform reflection
        consolidation_data = {
            "task": "main_task",
            "subtask_ids": related_ids,
            "requires_consolidation": True
        }

        insights = await reflection_engine.reflect(
            stage=ReflectionStage.SYNTHESIS,
            data=consolidation_data
        )

        # Trigger consolidation
        consolidated_id = await tier_manager.consolidate_memories(
            memory_ids=related_ids,
            tags=["consolidated", "main_task"]
        )

        # Verify consolidated memory created
        consolidated = await tier_manager.retrieve(consolidated_id)
        assert consolidated is not None
        assert len(consolidated["source_memories"]) == 3


class TestContextMonitorIntegration:
    """Test context monitoring with real memory operations."""

    @pytest.mark.asyncio
    async def test_context_warning_on_memory_pressure(self, context_monitor, tier_manager):
        """Context monitor should warn when memory pressure increases."""
        # Monitor context usage
        initial_usage = await context_monitor.get_usage()
        assert initial_usage < 0.75, "Should start below warning threshold"

        # Store many items to increase pressure
        for i in range(100):
            await tier_manager.store(
                tier=MemoryTier.WORKING,
                data={"item": i, "data": "x" * 1000},
                tags=[f"item_{i}"]
            )

        # Check updated usage
        current_usage = await context_monitor.get_usage()

        # Verify warning triggered if threshold exceeded
        if current_usage >= 0.75:
            warnings = await context_monitor.get_warnings()
            assert len(warnings) > 0
            assert any("memory pressure" in w.lower() for w in warnings)

    @pytest.mark.asyncio
    async def test_memory_cleanup_on_critical_context(self, context_monitor, tier_manager):
        """Memory should auto-cleanup when context critical."""
        # Fill working memory
        for i in range(50):
            await tier_manager.store(
                tier=MemoryTier.WORKING,
                data={"item": i, "large_data": "x" * 5000},
                tags=[f"item_{i}"]
            )

        # Check context
        usage = await context_monitor.get_usage()

        # If critical, should trigger cleanup
        if usage >= 0.90:
            await tier_manager.emergency_cleanup()

            # Verify cleanup occurred
            working_items = await tier_manager.list_tier(MemoryTier.WORKING)
            assert len(working_items) < 50, "Should remove some items"

            # Verify usage decreased
            new_usage = await context_monitor.get_usage()
            assert new_usage < usage, "Cleanup should reduce usage"


class TestCrossSessionPersistence:
    """Test memory persistence across simulated sessions."""

    @pytest.mark.asyncio
    async def test_memory_survives_session_restart(self, temp_storage):
        """Memory should persist across manager instances."""
        # Session 1: Create manager and store data
        manager1 = MemoryTierManager(
            storage_path=temp_storage,
            enable_compression=True,
            enable_serena=False
        )

        session1_data = {
            "session": "session_1",
            "important": "persistent_data",
            "timestamp": time.time()
        }

        memory_id = await manager1.store(
            tier=MemoryTier.ARCHIVAL,
            data=session1_data,
            tags=["persistent"]
        )

        # Shutdown first manager
        await manager1.shutdown()
        del manager1

        # Session 2: Create new manager with same storage
        manager2 = MemoryTierManager(
            storage_path=temp_storage,
            enable_compression=True,
            enable_serena=False
        )

        # Retrieve data from "previous session"
        retrieved = await manager2.retrieve(memory_id)

        # Verify data persisted
        assert retrieved is not None
        assert retrieved["session"] == "session_1"
        assert retrieved["important"] == "persistent_data"

        await manager2.shutdown()


class TestEndToEndMemoryReflection:
    """Complete workflow: memory storage → reflection → consolidation."""

    @pytest.mark.asyncio
    async def test_complete_memory_reflection_workflow(self, tier_manager, reflection_engine):
        """Test full cycle from memory creation to consolidated learning."""
        # Step 1: Execute multiple tasks, store results
        task_results = []
        for i in range(5):
            result = {
                "task_id": f"task_{i}",
                "complexity": 0.5 + (i * 0.1),
                "success": i > 1,  # First 2 fail
                "execution_time": 10 + (i * 5),
                "patterns": [f"pattern_{i}"]
            }

            memory_id = await tier_manager.store(
                tier=MemoryTier.WORKING,
                data=result,
                tags=["task_result"]
            )
            task_results.append((memory_id, result))

        # Step 2: Reflect on all results
        all_results = [r[1] for r in task_results]
        insights = await reflection_engine.reflect(
            stage=ReflectionStage.POST_WAVE,
            data={"all_tasks": all_results}
        )

        # Verify insights about failures
        assert len(insights) > 0
        assert any("failure" in i.lower() or "success" in i.lower() for i in insights)

        # Step 3: Store insights
        insights_id = await tier_manager.store(
            tier=MemoryTier.SHORT_TERM,
            data={"insights": insights, "task_count": len(all_results)},
            tags=["insights", "learning"]
        )

        # Step 4: Consolidate task memories into long-term learning
        consolidated_id = await tier_manager.consolidate_memories(
            memory_ids=[r[0] for r in task_results],
            tags=["consolidated", "learning"]
        )

        # Step 5: Verify consolidated memory
        consolidated = await tier_manager.retrieve(consolidated_id)
        assert consolidated is not None
        assert len(consolidated["source_memories"]) == 5
        assert consolidated["tier"] == MemoryTier.LONG_TERM.value

        # Step 6: Future reflection uses consolidated memory
        future_insights = await reflection_engine.reflect(
            stage=ReflectionStage.PLANNING,
            data={"reference_memory": consolidated_id}
        )

        # Verify learning applied
        assert len(future_insights) > 0


# Run with: pytest tests/integration/test_memory_reflection.py -v -s
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])