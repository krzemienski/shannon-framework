"""
Tests for Shannon Skills Framework - Dependency Resolution

Comprehensive test suite for the DependencyResolver covering:
- Simple dependency chains
- Parallel execution opportunities
- Circular dependency detection
- Missing dependency detection
- Complex dependency graphs
- Edge cases and error handling
"""

import pytest
import asyncio
from pathlib import Path
from typing import List

from shannon.skills.models import Skill, Execution, ExecutionType, SkillMetadata, Hooks
from shannon.skills.registry import SkillRegistry
from shannon.skills.dependencies import (
    DependencyResolver,
    ResolvedDependencies,
    CircularDependencyError,
    MissingDependencyError,
    DependencyError
)


# Test Fixtures

def create_test_skill(name: str, dependencies: List[str] = None) -> Skill:
    """Helper to create a test skill"""
    return Skill(
        name=name,
        version="1.0.0",
        description=f"Test skill {name}",
        category="testing",
        dependencies=dependencies or [],
        execution=Execution(
            type=ExecutionType.NATIVE,
            module="test",
            class_name="TestClass",
            method="test_method"
        ),
        hooks=Hooks(),
        metadata=SkillMetadata()
    )


def setup_registry(tmp_path):
    """Helper to create a registry for testing"""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["name", "version", "description", "execution"],
        "properties": {
            "name": {"type": "string"},
            "version": {"type": "string"},
            "description": {"type": "string"},
            "category": {"type": "string"},
            "dependencies": {"type": "array"},
            "execution": {"type": "object"},
            "hooks": {"type": "object"},
            "parameters": {"type": "array"},
            "metadata": {"type": "object"}
        }
    }

    import json
    schema_path = tmp_path / "skill.schema.json"
    with open(schema_path, 'w') as f:
        json.dump(schema, f)

    SkillRegistry.reset_instance()
    return SkillRegistry(schema_path=schema_path)


async def register_skills(registry, skills):
    """Helper to register multiple skills"""
    for skill in skills:
        await registry.register(skill)


# Test Cases

class TestSimpleDependencyChain:
    """Test simple linear dependency chains: A -> B -> C"""

    @pytest.mark.asyncio
    async def test_three_skill_chain(self, tmp_path):
        """Test A -> B -> C dependency chain"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=[])
        skill_b = create_test_skill("B", dependencies=["A"])
        skill_c = create_test_skill("C", dependencies=["B"])

        await register_skills(registry, [skill_a, skill_b, skill_c])

        resolved = resolver.resolve_dependencies([skill_a, skill_b, skill_c])

        # Check execution order - A must come before B, B before C
        assert resolved.execution_order == ["A", "B", "C"]

        # Check parallel groups - no parallelism in a chain
        assert resolved.parallel_groups == [["A"], ["B"], ["C"]]

        # Check dependency levels
        assert resolved.dependency_levels == 3

        # Check graph info
        assert resolved.graph_info['total_skills'] == 3
        assert resolved.graph_info['total_dependencies'] == 2
        assert resolved.graph_info['is_dag'] is True
        assert resolved.graph_info['entry_points'] == ["A"]
        assert resolved.graph_info['exit_points'] == ["C"]

    @pytest.mark.asyncio
    async def test_two_skill_chain(self, tmp_path):
        """Test A -> B dependency chain"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=[])
        skill_b = create_test_skill("B", dependencies=["A"])

        await register_skills(registry, [skill_a, skill_b])

        resolved = resolver.resolve_dependencies([skill_a, skill_b])

        assert resolved.execution_order == ["A", "B"]
        assert resolved.parallel_groups == [["A"], ["B"]]
        assert resolved.dependency_levels == 2

    @pytest.mark.asyncio
    async def test_single_skill_no_dependencies(self, tmp_path):
        """Test single skill with no dependencies"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=[])

        await register_skills(registry, [skill_a])

        resolved = resolver.resolve_dependencies([skill_a])

        assert resolved.execution_order == ["A"]
        assert resolved.parallel_groups == [["A"]]
        assert resolved.dependency_levels == 1
        assert resolved.graph_info['entry_points'] == ["A"]
        assert resolved.graph_info['exit_points'] == ["A"]


class TestParallelSkills:
    """Test parallel execution opportunities"""

    @pytest.mark.asyncio
    async def test_independent_skills(self, tmp_path):
        """Test A, B independent, both needed by C"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=[])
        skill_b = create_test_skill("B", dependencies=[])
        skill_c = create_test_skill("C", dependencies=["A", "B"])

        await register_skills(registry, [skill_a, skill_b, skill_c])

        resolved = resolver.resolve_dependencies([skill_a, skill_b, skill_c])

        # A and B can run in parallel
        assert set(resolved.parallel_groups[0]) == {"A", "B"}
        assert resolved.parallel_groups[1] == ["C"]

        # Check dependency levels
        assert resolved.dependency_levels == 2

        # Check that A and B are both entry points
        assert set(resolved.graph_info['entry_points']) == {"A", "B"}
        assert resolved.graph_info['exit_points'] == ["C"]

        # Verify execution order has A and B before C
        c_index = resolved.execution_order.index("C")
        a_index = resolved.execution_order.index("A")
        b_index = resolved.execution_order.index("B")
        assert a_index < c_index
        assert b_index < c_index

    @pytest.mark.asyncio
    async def test_diamond_dependency(self, tmp_path):
        """Test diamond pattern: A -> B,C -> D"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=[])
        skill_b = create_test_skill("B", dependencies=["A"])
        skill_c = create_test_skill("C", dependencies=["A"])
        skill_d = create_test_skill("D", dependencies=["B", "C"])

        await register_skills(registry, [skill_a, skill_b, skill_c, skill_d])

        resolved = resolver.resolve_dependencies([skill_a, skill_b, skill_c, skill_d])

        # Check parallel groups
        assert resolved.parallel_groups[0] == ["A"]
        assert set(resolved.parallel_groups[1]) == {"B", "C"}
        assert resolved.parallel_groups[2] == ["D"]

        # Check dependency levels
        assert resolved.dependency_levels == 3

    @pytest.mark.asyncio
    async def test_multiple_independent_chains(self, tmp_path):
        """Test multiple independent chains: A->B and C->D"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=[])
        skill_b = create_test_skill("B", dependencies=["A"])
        skill_c = create_test_skill("C", dependencies=[])
        skill_d = create_test_skill("D", dependencies=["C"])

        await register_skills(registry, [skill_a, skill_b, skill_c, skill_d])

        resolved = resolver.resolve_dependencies([skill_a, skill_b, skill_c, skill_d])

        # Level 0: A and C (no dependencies)
        assert set(resolved.parallel_groups[0]) == {"A", "C"}
        # Level 1: B and D (depend on level 0)
        assert set(resolved.parallel_groups[1]) == {"B", "D"}

        # Check dependency levels
        assert resolved.dependency_levels == 2


class TestCircularDependencies:
    """Test circular dependency detection"""

    @pytest.mark.asyncio
    async def test_simple_cycle_two_skills(self, tmp_path):
        """Test A -> B -> A cycle"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=["B"])
        skill_b = create_test_skill("B", dependencies=["A"])

        await register_skills(registry, [skill_a, skill_b])

        with pytest.raises(CircularDependencyError) as exc_info:
            resolver.resolve_dependencies([skill_a, skill_b])

        error_msg = str(exc_info.value)
        assert "Circular dependencies detected" in error_msg
        assert "A" in error_msg and "B" in error_msg

    @pytest.mark.asyncio
    async def test_simple_cycle_three_skills(self, tmp_path):
        """Test A -> B -> C -> A cycle"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=["C"])
        skill_b = create_test_skill("B", dependencies=["A"])
        skill_c = create_test_skill("C", dependencies=["B"])

        await register_skills(registry, [skill_a, skill_b, skill_c])

        with pytest.raises(CircularDependencyError) as exc_info:
            resolver.resolve_dependencies([skill_a, skill_b, skill_c])

        error_msg = str(exc_info.value)
        assert "Circular dependencies detected" in error_msg

    @pytest.mark.asyncio
    async def test_self_dependency(self, tmp_path):
        """Test skill depending on itself"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=["A"])

        await registry.register(skill_a)

        with pytest.raises(CircularDependencyError):
            resolver.resolve_dependencies([skill_a])


class TestMissingDependencies:
    """Test missing dependency detection"""

    @pytest.mark.asyncio
    async def test_single_missing_dependency(self, tmp_path):
        """Test skill with one missing dependency"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_b = create_test_skill("B", dependencies=["A"])

        await registry.register(skill_b)

        with pytest.raises(MissingDependencyError) as exc_info:
            resolver.resolve_dependencies([skill_b])

        error_msg = str(exc_info.value)
        assert "Missing dependencies" in error_msg
        assert "A" in error_msg

    @pytest.mark.asyncio
    async def test_multiple_missing_dependencies(self, tmp_path):
        """Test skill with multiple missing dependencies"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_d = create_test_skill("D", dependencies=["A", "B", "C"])

        await registry.register(skill_d)

        with pytest.raises(MissingDependencyError) as exc_info:
            resolver.resolve_dependencies([skill_d])

        error_msg = str(exc_info.value)
        assert "Missing dependencies" in error_msg
        assert "A" in error_msg
        assert "B" in error_msg
        assert "C" in error_msg

    @pytest.mark.asyncio
    async def test_find_missing_dependencies_helper(self, tmp_path):
        """Test find_missing_dependencies helper method"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=[])
        skill_b = create_test_skill("B", dependencies=["A", "C"])

        await register_skills(registry, [skill_a, skill_b])

        missing = resolver.find_missing_dependencies([skill_a, skill_b])

        assert missing == ["C"]


class TestComplexGraphs:
    """Test complex dependency scenarios"""

    @pytest.mark.asyncio
    async def test_large_graph(self, tmp_path):
        """Test graph with 10 skills and various dependencies"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        # Create skills with complex dependencies
        skills_data = {
            "A": [],
            "B": [],
            "C": ["A"],
            "D": ["A", "B"],
            "E": ["C"],
            "F": ["D"],
            "G": ["E", "F"],
            "H": ["B"],
            "I": ["G", "H"],
            "J": ["I"],
        }

        skills = {name: create_test_skill(name, deps) for name, deps in skills_data.items()}

        await register_skills(registry, skills.values())

        resolved = resolver.resolve_dependencies(list(skills.values()))

        # Verify it's a valid execution order
        assert len(resolved.execution_order) == 10

        # Verify dependencies are satisfied
        for i, skill_name in enumerate(resolved.execution_order):
            skill = skills[skill_name]
            for dep in skill.dependencies:
                dep_index = resolved.execution_order.index(dep)
                assert dep_index < i, f"{dep} should come before {skill_name}"

        # Check that we have multiple levels
        assert resolved.dependency_levels > 3

    @pytest.mark.asyncio
    async def test_wide_graph(self, tmp_path):
        """Test graph with many parallel skills"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        # Create 5 independent skills all feeding into one final skill
        skills = []
        for i in range(5):
            skill = create_test_skill(f"parallel_{i}", dependencies=[])
            skills.append(skill)

        final = create_test_skill("final", dependencies=[f"parallel_{i}" for i in range(5)])
        skills.append(final)

        await register_skills(registry, skills)

        resolved = resolver.resolve_dependencies(skills)

        # First level should have all parallel skills
        assert len(resolved.parallel_groups[0]) == 5
        # Second level should have only the final skill
        assert resolved.parallel_groups[1] == ["final"]

        # Should be only 2 levels deep
        assert resolved.dependency_levels == 2


class TestConvenienceMethods:
    """Test convenience methods for common operations"""

    @pytest.mark.asyncio
    async def test_get_execution_order(self, tmp_path):
        """Test get_execution_order convenience method"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=[])
        skill_b = create_test_skill("B", dependencies=["A"])
        skill_c = create_test_skill("C", dependencies=["B"])

        await register_skills(registry, [skill_a, skill_b, skill_c])

        order = resolver.get_execution_order(["A", "B", "C"])
        assert order == ["A", "B", "C"]

    @pytest.mark.asyncio
    async def test_get_parallel_groups(self, tmp_path):
        """Test get_parallel_groups convenience method"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=[])
        skill_b = create_test_skill("B", dependencies=[])
        skill_c = create_test_skill("C", dependencies=["A", "B"])

        await register_skills(registry, [skill_a, skill_b, skill_c])

        groups = resolver.get_parallel_groups(["A", "B", "C"])
        assert set(groups[0]) == {"A", "B"}
        assert groups[1] == ["C"]

    @pytest.mark.asyncio
    async def test_analyze_skill_dependencies(self, tmp_path):
        """Test analyze_skill_dependencies method"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=[])
        skill_b = create_test_skill("B", dependencies=["A"])
        skill_c = create_test_skill("C", dependencies=["B"])
        skill_d = create_test_skill("D", dependencies=["B"])

        await register_skills(registry, [skill_a, skill_b, skill_c, skill_d])

        # Analyze skill B
        analysis = resolver.analyze_skill_dependencies("B")

        assert analysis['skill_name'] == "B"
        assert analysis['direct_dependencies'] == ["A"]
        assert analysis['all_dependencies'] == ["A"]
        assert set(analysis['dependents']) == {"C", "D"}
        assert analysis['is_entry_point'] is False
        assert analysis['is_exit_point'] is False

        # Analyze skill A (entry point)
        analysis_a = resolver.analyze_skill_dependencies("A")
        assert analysis_a['is_entry_point'] is True
        assert analysis_a['all_dependencies'] == []
        assert set(analysis_a['dependents']) == {"B", "C", "D"}


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_skill_list(self, tmp_path):
        """Test resolution with empty skill list"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        resolved = resolver.resolve_dependencies([])

        assert resolved.execution_order == []
        assert resolved.parallel_groups == []
        assert resolved.dependency_levels == 0
        assert resolved.graph_info['total_skills'] == 0

    @pytest.mark.asyncio
    async def test_skill_with_empty_dependencies_list(self, tmp_path):
        """Test skill with explicitly empty dependencies list"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill = create_test_skill("A", dependencies=[])
        await registry.register(skill)

        resolved = resolver.resolve_dependencies([skill])

        assert resolved.execution_order == ["A"]
        assert resolved.parallel_groups == [["A"]]

    @pytest.mark.asyncio
    async def test_duplicate_skills_in_list(self, tmp_path):
        """Test behavior with duplicate skills in input list"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=[])
        await registry.register(skill_a)

        # Pass same skill twice
        resolved = resolver.resolve_dependencies([skill_a, skill_a])

        # Should handle gracefully (graph deduplicates)
        assert resolved.execution_order == ["A"]

    @pytest.mark.asyncio
    async def test_unregistered_skill_lookup(self, tmp_path):
        """Test get_execution_order with unregistered skill"""
        from shannon.skills.registry import SkillNotFoundError

        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        with pytest.raises(SkillNotFoundError):
            resolver.get_execution_order(["nonexistent"])


class TestGraphMetadata:
    """Test graph metadata and statistics"""

    @pytest.mark.asyncio
    async def test_graph_info_metadata(self, tmp_path):
        """Test graph_info contains correct metadata"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=[])
        skill_b = create_test_skill("B", dependencies=["A"])
        skill_c = create_test_skill("C", dependencies=["A"])

        await register_skills(registry, [skill_a, skill_b, skill_c])

        resolved = resolver.resolve_dependencies([skill_a, skill_b, skill_c])

        info = resolved.graph_info
        assert info['total_skills'] == 3
        assert info['total_dependencies'] == 2
        assert info['is_dag'] is True
        assert info['entry_point_count'] == 1
        assert info['exit_point_count'] == 2
        assert info['max_depth'] == 1  # A is depth 0, B and C are depth 1

    @pytest.mark.asyncio
    async def test_skill_dependencies_map(self, tmp_path):
        """Test skill_dependencies map is populated correctly"""
        registry = setup_registry(tmp_path)
        resolver = DependencyResolver(registry)

        skill_a = create_test_skill("A", dependencies=[])
        skill_b = create_test_skill("B", dependencies=["A"])

        await register_skills(registry, [skill_a, skill_b])

        resolved = resolver.resolve_dependencies([skill_a, skill_b])

        assert resolved.skill_dependencies == {
            "A": [],
            "B": ["A"]
        }


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
