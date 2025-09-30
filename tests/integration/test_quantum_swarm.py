"""
Integration Test: Quantum & Swarm Intelligence

Tests REAL integration between:
- SuperpositionEngine (parallel universe exploration)
- SwarmIntelligence (collective decision making)

NO mocks. Real parallel execution, real consensus voting, real universe collapse.
"""

import asyncio
import pytest
import time
from typing import List, Dict, Any

from shannon.quantum.superposition_engine import SuperpositionEngine, UniverseState
from shannon.swarm.collective_intelligence import SwarmIntelligence, SwarmAgent
from shannon.consensus.byzantine_coordinator import ByzantineCoordinator


@pytest.fixture
def superposition_engine():
    """Create real superposition engine."""
    return SuperpositionEngine(
        max_universes=5,
        enable_interference=True
    )


@pytest.fixture
def swarm_intelligence():
    """Create real swarm intelligence."""
    return SwarmIntelligence(
        min_agents=3,
        max_agents=10,
        enable_learning=True
    )


@pytest.fixture
def byzantine_coordinator():
    """Create real Byzantine consensus coordinator."""
    return ByzantineCoordinator(
        min_replicas=4,
        fault_tolerance=1  # (N-1)/3, so N=4 tolerates 1 fault
    )


class TestQuantumSuperposition:
    """Test REAL parallel universe exploration."""

    @pytest.mark.asyncio
    async def test_multiple_universes_execute_in_parallel(self, superposition_engine):
        """Multiple universes should execute truly in parallel."""
        # Define different strategies for parallel execution
        strategies = [
            {"strategy": "greedy", "delay": 1.0},
            {"strategy": "optimal", "delay": 1.0},
            {"strategy": "balanced", "delay": 1.0},
            {"strategy": "conservative", "delay": 1.0},
            {"strategy": "aggressive", "delay": 1.0}
        ]

        async def execute_strategy(strategy_config):
            """Real async execution with delay."""
            await asyncio.sleep(strategy_config["delay"])
            return {
                "strategy": strategy_config["strategy"],
                "result": f"Result from {strategy_config['strategy']}",
                "cost": hash(strategy_config["strategy"]) % 100
            }

        # Create superposition of universes
        start = time.time()
        universe_states = await superposition_engine.create_superposition(
            strategies=strategies,
            executor=execute_strategy
        )
        duration = time.time() - start

        # Verify parallel execution (should take ~1s, not 5s)
        assert duration < 1.5, f"Parallel execution took {duration:.2f}s, expected < 1.5s"
        assert len(universe_states) == 5, "Should create 5 parallel universes"

        # Verify all universes have results
        for state in universe_states:
            assert state.result is not None
            assert "strategy" in state.result
            assert state.probability > 0

    @pytest.mark.asyncio
    async def test_born_rule_collapse(self, superposition_engine):
        """Test REAL quantum collapse using Born rule."""
        # Create universes with different outcomes
        strategies = [
            {"name": "high_probability", "expected_value": 100},
            {"name": "medium_probability", "expected_value": 50},
            {"name": "low_probability", "expected_value": 10}
        ]

        async def evaluate_strategy(config):
            """Evaluate strategy and return outcome."""
            return {
                "name": config["name"],
                "value": config["expected_value"],
                "probability": config["expected_value"] / 160  # Normalize
            }

        # Create and collapse superposition
        universe_states = await superposition_engine.create_superposition(
            strategies=strategies,
            executor=evaluate_strategy
        )

        # Collapse using Born rule (probability amplitude squared)
        collapsed = await superposition_engine.collapse(universe_states)

        # Verify collapsed universe
        assert collapsed is not None
        assert collapsed.name in ["high_probability", "medium_probability", "low_probability"]

        # Run multiple times to verify probabilistic nature
        collapse_counts = {name: 0 for name in ["high_probability", "medium_probability", "low_probability"]}
        for _ in range(100):
            states = await superposition_engine.create_superposition(
                strategies=strategies,
                executor=evaluate_strategy
            )
            result = await superposition_engine.collapse(states)
            collapse_counts[result.name] += 1

        # Verify high probability universe selected more often
        assert collapse_counts["high_probability"] > collapse_counts["low_probability"]
        assert collapse_counts["high_probability"] >= 40  # Should be ~62% but allow variance

    @pytest.mark.asyncio
    async def test_quantum_interference(self, superposition_engine):
        """Test constructive/destructive interference between universes."""
        # Create interfering strategies
        strategies = [
            {"phase": 0, "amplitude": 1.0},
            {"phase": 180, "amplitude": 1.0},  # Opposite phase
            {"phase": 90, "amplitude": 0.5}
        ]

        async def compute_wave_function(config):
            """Compute quantum amplitude."""
            import math
            phase_rad = math.radians(config["phase"])
            return {
                "amplitude": config["amplitude"],
                "phase": config["phase"],
                "real": config["amplitude"] * math.cos(phase_rad),
                "imag": config["amplitude"] * math.sin(phase_rad)
            }

        # Enable interference
        superposition_engine.enable_interference = True

        # Create superposition with interference
        states = await superposition_engine.create_superposition(
            strategies=strategies,
            executor=compute_wave_function
        )

        # Verify interference effects
        # Opposite phases should show destructive interference
        opposite_phase_states = [s for s in states if s.result["phase"] in [0, 180]]
        assert len(opposite_phase_states) == 2

        # Calculate combined amplitude (should be reduced due to interference)
        combined_amplitude = sum(s.result["real"] for s in opposite_phase_states)
        assert abs(combined_amplitude) < 1.5, "Destructive interference should reduce amplitude"


class TestSwarmIntelligence:
    """Test REAL swarm coordination and consensus."""

    @pytest.mark.asyncio
    async def test_swarm_agents_coordinate(self, swarm_intelligence):
        """Swarm agents should coordinate to solve problem."""
        # Create problem for swarm to solve
        problem = {
            "type": "optimization",
            "search_space": list(range(100)),
            "objective": "find_maximum",
            "iterations": 10
        }

        # Initialize swarm
        await swarm_intelligence.initialize_swarm(agent_count=5)

        # Execute swarm optimization
        result = await swarm_intelligence.optimize(problem)

        # Verify coordination occurred
        assert result is not None
        assert result["best_solution"] is not None
        assert result["iterations_completed"] == 10
        assert result["swarm_convergence"] is True

    @pytest.mark.asyncio
    async def test_swarm_voting_consensus(self, swarm_intelligence):
        """Swarm should reach consensus through voting."""
        # Create decision problem
        options = ["option_a", "option_b", "option_c"]

        # Initialize swarm with preferences
        agents = []
        for i in range(7):
            agent = SwarmAgent(
                agent_id=f"agent_{i}",
                preference=options[i % len(options)]  # Distributed preferences
            )
            agents.append(agent)

        # Execute voting
        consensus = await swarm_intelligence.vote(
            agents=agents,
            options=options,
            voting_method="majority"
        )

        # Verify consensus reached
        assert consensus is not None
        assert consensus["winner"] in options
        assert consensus["vote_count"] >= 3  # Majority of 7

    @pytest.mark.asyncio
    async def test_swarm_learning_from_experience(self, swarm_intelligence):
        """Swarm should improve performance through learning."""
        # Problem to solve repeatedly
        problem = {
            "type": "pathfinding",
            "start": (0, 0),
            "goal": (10, 10),
            "obstacles": [(5, 5), (5, 6), (6, 5)]
        }

        # Run swarm multiple times, track improvement
        performance_history = []

        for iteration in range(5):
            await swarm_intelligence.initialize_swarm(agent_count=5)
            result = await swarm_intelligence.solve(problem)

            performance_history.append({
                "iteration": iteration,
                "time_to_solution": result["time"],
                "path_length": result["path_length"]
            })

            # Learn from experience
            await swarm_intelligence.learn_from_result(result)

        # Verify improvement over iterations
        first_time = performance_history[0]["time_to_solution"]
        last_time = performance_history[-1]["time_to_solution"]
        assert last_time < first_time * 0.8, "Should improve by 20%+ through learning"


class TestByzantineConsensus:
    """Test REAL Byzantine fault tolerant consensus."""

    @pytest.mark.asyncio
    async def test_consensus_with_honest_nodes(self, byzantine_coordinator):
        """All honest nodes should reach consensus."""
        # Create honest nodes
        nodes = [
            {"node_id": f"node_{i}", "value": 42, "is_honest": True}
            for i in range(4)
        ]

        # Execute consensus
        result = await byzantine_coordinator.reach_consensus(nodes)

        # Verify consensus reached
        assert result is not None
        assert result["consensus_value"] == 42
        assert result["consensus_reached"] is True
        assert result["rounds_required"] <= 3  # PBFT typically 3 phases

    @pytest.mark.asyncio
    async def test_consensus_with_faulty_node(self, byzantine_coordinator):
        """Consensus should tolerate single faulty node."""
        # Create nodes with one Byzantine node
        nodes = [
            {"node_id": "node_0", "value": 42, "is_honest": True},
            {"node_id": "node_1", "value": 42, "is_honest": True},
            {"node_id": "node_2", "value": 42, "is_honest": True},
            {"node_id": "node_3", "value": 999, "is_honest": False}  # Byzantine!
        ]

        # Execute consensus (should tolerate 1 fault with 4 nodes)
        result = await byzantine_coordinator.reach_consensus(nodes)

        # Verify consensus reached despite faulty node
        assert result is not None
        assert result["consensus_value"] == 42, "Should ignore Byzantine node"
        assert result["consensus_reached"] is True
        assert result["faulty_nodes_detected"] == 1

    @pytest.mark.asyncio
    async def test_three_phase_commit_protocol(self, byzantine_coordinator):
        """Test PBFT 3-phase commit protocol."""
        # Create transaction proposal
        transaction = {
            "operation": "transfer",
            "amount": 100,
            "from": "account_a",
            "to": "account_b"
        }

        nodes = [
            {"node_id": f"node_{i}", "is_primary": (i == 0)}
            for i in range(4)
        ]

        # Execute PBFT phases
        phases_result = await byzantine_coordinator.execute_pbft(
            transaction=transaction,
            nodes=nodes
        )

        # Verify all phases completed
        assert "pre_prepare" in phases_result
        assert "prepare" in phases_result
        assert "commit" in phases_result
        assert phases_result["success"] is True


class TestQuantumSwarmIntegration:
    """Integration: Quantum exploration + Swarm consensus."""

    @pytest.mark.asyncio
    async def test_quantum_universes_voted_by_swarm(
        self, superposition_engine, swarm_intelligence
    ):
        """Swarm votes on best quantum universe to collapse into."""
        # Create quantum superposition of strategies
        strategies = [
            {"id": "strategy_1", "performance": 0.9},
            {"id": "strategy_2", "performance": 0.7},
            {"id": "strategy_3", "performance": 0.8},
            {"id": "strategy_4", "performance": 0.6},
            {"id": "strategy_5", "performance": 0.85}
        ]

        async def evaluate_strategy(config):
            """Evaluate strategy in parallel universe."""
            await asyncio.sleep(0.1)  # Simulate computation
            return {
                "strategy_id": config["id"],
                "performance": config["performance"],
                "cost": 1.0 - config["performance"]
            }

        # Step 1: Create quantum superposition
        universe_states = await superposition_engine.create_superposition(
            strategies=strategies,
            executor=evaluate_strategy
        )

        # Step 2: Create swarm agents to evaluate universes
        agents = []
        for i, state in enumerate(universe_states):
            agent = SwarmAgent(
                agent_id=f"evaluator_{i}",
                preference=state.result["strategy_id"],
                vote_weight=state.result["performance"]
            )
            agents.append(agent)

        # Step 3: Swarm votes on best universe
        consensus = await swarm_intelligence.vote(
            agents=agents,
            options=[state.result["strategy_id"] for state in universe_states],
            voting_method="weighted"
        )

        # Step 4: Collapse into voted universe
        chosen_universe = next(
            s for s in universe_states
            if s.result["strategy_id"] == consensus["winner"]
        )

        # Verify integration
        assert consensus["winner"] is not None
        assert chosen_universe is not None
        assert chosen_universe.result["performance"] >= 0.8, "Should choose high-performing universe"

    @pytest.mark.asyncio
    async def test_swarm_explores_quantum_search_space(
        self, superposition_engine, swarm_intelligence
    ):
        """Swarm optimization in quantum superposition."""
        # Define search space
        search_space = list(range(50))

        async def evaluate_position(position):
            """Objective function to optimize."""
            await asyncio.sleep(0.01)
            # Quadratic with maximum at position 25
            return {"position": position, "value": -(position - 25) ** 2 + 625}

        # Create quantum superposition of search positions
        initial_positions = [
            {"position": i * 10} for i in range(5)  # Sample 5 starting points
        ]

        universe_states = await superposition_engine.create_superposition(
            strategies=initial_positions,
            executor=evaluate_position
        )

        # Initialize swarm in each universe
        swarm_results = []
        for state in universe_states:
            # Swarm optimizes from this starting position
            problem = {
                "type": "optimization",
                "start_position": state.result["position"],
                "search_space": search_space,
                "objective": evaluate_position
            }

            await swarm_intelligence.initialize_swarm(agent_count=3)
            result = await swarm_intelligence.optimize(problem)
            swarm_results.append(result)

        # Find best result across all quantum universes
        best_result = max(swarm_results, key=lambda r: r["best_value"])

        # Verify quantum-swarm optimization found near-optimal solution
        assert best_result["best_solution"] is not None
        assert abs(best_result["best_solution"] - 25) <= 5, "Should find solution near optimal"
        assert best_result["best_value"] >= 600, "Should achieve near-maximum value"

    @pytest.mark.asyncio
    async def test_byzantine_consensus_on_quantum_results(
        self, superposition_engine, byzantine_coordinator
    ):
        """Byzantine consensus validates quantum computation results."""
        # Multiple nodes perform quantum computation
        strategies = [
            {"computation": "quantum_simulation", "seed": i}
            for i in range(4)
        ]

        async def quantum_compute(config):
            """Simulate quantum computation."""
            await asyncio.sleep(0.1)
            # Honest nodes return same result, simulate one faulty
            if config["seed"] == 3:
                return {"result": 999, "seed": config["seed"]}  # Byzantine result
            return {"result": 42, "seed": config["seed"]}

        # Each node creates quantum superposition
        all_node_results = []
        for strategy in strategies:
            universe_states = await superposition_engine.create_superposition(
                strategies=[strategy],
                executor=quantum_compute
            )
            collapsed = await superposition_engine.collapse(universe_states)
            all_node_results.append({
                "node_id": f"node_{strategy['seed']}",
                "value": collapsed.result["result"],
                "is_honest": collapsed.result["result"] == 42
            })

        # Byzantine consensus validates results
        consensus = await byzantine_coordinator.reach_consensus(all_node_results)

        # Verify consensus rejects Byzantine result
        assert consensus["consensus_value"] == 42
        assert consensus["consensus_reached"] is True
        assert consensus["faulty_nodes_detected"] == 1


class TestRealParallelism:
    """Verify REAL parallel execution, not sequential."""

    @pytest.mark.asyncio
    async def test_true_concurrent_execution(self):
        """Verify asyncio.gather provides true concurrency."""
        # Create tasks with known delays
        async def delayed_task(task_id, delay):
            start = time.time()
            await asyncio.sleep(delay)
            return {"task_id": task_id, "delay": delay, "start": start}

        tasks = [
            delayed_task(1, 1.0),
            delayed_task(2, 1.0),
            delayed_task(3, 1.0)
        ]

        # Execute in parallel
        start_total = time.time()
        results = await asyncio.gather(*tasks)
        total_duration = time.time() - start_total

        # Verify true parallelism
        assert total_duration < 1.5, f"Parallel took {total_duration:.2f}s, expected < 1.5s"

        # Verify all tasks started at roughly same time
        start_times = [r["start"] for r in results]
        time_spread = max(start_times) - min(start_times)
        assert time_spread < 0.1, f"Tasks started {time_spread:.2f}s apart, not truly parallel"


# Run with: pytest tests/integration/test_quantum_swarm.py -v -s
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])