"""
Quantum-Inspired Superposition Engine

Implements quantum-inspired parallel universe exploration with probability amplitudes.
Solutions exist in superposition until observation collapses to best outcome.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic
from enum import Enum
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)

T = TypeVar('T')


class UniverseState(Enum):
    """State of a quantum universe"""
    SUPERPOSITION = "superposition"  # Exists but unobserved
    EVOLVING = "evolving"  # Being computed
    COLLAPSED = "collapsed"  # Observed outcome
    INTERFERED = "interfered"  # Destructively interfered


@dataclass
class QuantumState(Generic[T]):
    """
    Represents a quantum state in superposition.

    Each state has an amplitude (probability weight) and a solution value.
    The state exists in superposition until observed/collapsed.
    """
    universe_id: str
    amplitude: complex
    solution: Optional[T] = None
    state: UniverseState = UniverseState.SUPERPOSITION
    phase: float = 0.0  # Quantum phase
    entangled_with: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    collapsed_at: Optional[datetime] = None

    @property
    def probability(self) -> float:
        """Calculate probability from amplitude (Born rule)"""
        return abs(self.amplitude) ** 2

    def apply_phase_shift(self, phase: float) -> None:
        """Apply quantum phase shift to amplitude"""
        self.phase += phase
        magnitude = abs(self.amplitude)
        self.amplitude = magnitude * np.exp(1j * self.phase)

    def entangle(self, other_universe_id: str) -> None:
        """Create entanglement with another universe"""
        if other_universe_id not in self.entangled_with:
            self.entangled_with.append(other_universe_id)

    def collapse(self) -> T:
        """Collapse superposition to definite state"""
        if self.state == UniverseState.COLLAPSED:
            return self.solution

        self.state = UniverseState.COLLAPSED
        self.collapsed_at = datetime.now()
        return self.solution

    def __repr__(self) -> str:
        prob = self.probability
        return f"QuantumState(id={self.universe_id}, P={prob:.3f}, state={self.state.value})"


@dataclass
class SuperpositionResult(Generic[T]):
    """Result of quantum computation after collapse"""
    best_solution: T
    best_probability: float
    all_states: List[QuantumState[T]]
    interference_events: int
    total_amplitude: complex
    execution_time_ms: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def explored_universes(self) -> int:
        """Number of parallel universes explored"""
        return len(self.all_states)

    @property
    def coherence(self) -> float:
        """Measure of quantum coherence (phase alignment)"""
        if not self.all_states:
            return 0.0
        phases = [state.phase for state in self.all_states]
        coherence = abs(np.mean(np.exp(1j * np.array(phases))))
        return float(coherence)


class ProbabilityCalculator:
    """
    Calculates quantum probability amplitudes based on solution quality.

    Uses Born rule interpretation: probability = |amplitude|^2
    """

    def __init__(
        self,
        min_amplitude: float = 0.1,
        max_amplitude: float = 1.0,
        phase_variance: float = 0.5
    ):
        self.min_amplitude = min_amplitude
        self.max_amplitude = max_amplitude
        self.phase_variance = phase_variance

    def calculate_amplitude(
        self,
        score: float,
        context: Optional[Dict[str, Any]] = None
    ) -> complex:
        """
        Calculate complex amplitude from solution score.

        Args:
            score: Solution quality score (0-1)
            context: Additional context for amplitude calculation

        Returns:
            Complex amplitude with magnitude and phase
        """
        # Normalize score to amplitude range
        magnitude = self.min_amplitude + score * (self.max_amplitude - self.min_amplitude)

        # Calculate phase based on score and variance
        # Higher scores get lower phase variance (more coherent)
        phase_spread = self.phase_variance * (1.0 - score)
        phase = np.random.normal(0, phase_spread)

        # Apply context-based phase shifts if provided
        if context:
            if context.get('prefer_exploration', False):
                phase += np.pi / 4  # Phase shift for exploration
            if context.get('exploit_best', False):
                phase = 0.0  # Zero phase for exploitation

        amplitude = magnitude * np.exp(1j * phase)
        return complex(amplitude)

    def calculate_interference(
        self,
        state1: QuantumState,
        state2: QuantumState
    ) -> complex:
        """
        Calculate quantum interference between two states.

        Returns:
            Combined amplitude after interference
        """
        # Quantum interference: amplitudes add (not probabilities)
        combined = state1.amplitude + state2.amplitude

        # Check for destructive interference
        if abs(combined) < abs(state1.amplitude) * 0.5:
            logger.debug(
                f"Destructive interference between {state1.universe_id} "
                f"and {state2.universe_id}"
            )

        return combined

    def normalize_amplitudes(
        self,
        states: List[QuantumState]
    ) -> None:
        """
        Normalize amplitudes so total probability = 1.

        Modifies states in-place.
        """
        if not states:
            return

        # Calculate total probability
        total_prob = sum(state.probability for state in states)

        if total_prob == 0:
            logger.warning("Total probability is zero, cannot normalize")
            return

        # Normalize each amplitude
        normalization_factor = np.sqrt(1.0 / total_prob)
        for state in states:
            state.amplitude *= normalization_factor


class SuperpositionEngine(Generic[T]):
    """
    Quantum-inspired parallel universe exploration engine.

    Solutions exist in superposition across multiple parallel universes.
    Each universe is explored asynchronously until observation collapses
    the superposition to the best solution.

    Features:
    - Parallel universe execution with asyncio.gather()
    - Quantum probability amplitudes
    - Interference patterns
    - Entanglement between related solutions
    - Born rule collapse to best solution
    """

    def __init__(
        self,
        score_function: Callable[[T], float],
        max_universes: int = 10,
        interference_threshold: float = 0.3,
        enable_entanglement: bool = True
    ):
        """
        Initialize superposition engine.

        Args:
            score_function: Function to evaluate solution quality (returns 0-1)
            max_universes: Maximum parallel universes to explore
            interference_threshold: Threshold for destructive interference
            enable_entanglement: Whether to track entanglement between solutions
        """
        self.score_function = score_function
        self.max_universes = max_universes
        self.interference_threshold = interference_threshold
        self.enable_entanglement = enable_entanglement

        self.probability_calc = ProbabilityCalculator()
        self.states: List[QuantumState[T]] = []
        self.interference_events = 0

        logger.info(
            f"SuperpositionEngine initialized: max_universes={max_universes}, "
            f"interference_threshold={interference_threshold}"
        )

    async def create_universe(
        self,
        universe_id: str,
        solution_generator: Callable[[], Any]
    ) -> QuantumState[T]:
        """
        Create and evolve a parallel universe.

        Args:
            universe_id: Unique identifier for this universe
            solution_generator: Async function that generates solution

        Returns:
            Quantum state with evolved solution
        """
        state = QuantumState[T](
            universe_id=universe_id,
            amplitude=complex(1.0, 0.0),  # Initial uniform amplitude
            metadata={'generator': solution_generator.__name__ if hasattr(solution_generator, '__name__') else 'unknown'}
        )

        try:
            # Evolve universe by generating solution
            state.state = UniverseState.EVOLVING

            # Execute solution generator (may be sync or async)
            if asyncio.iscoroutinefunction(solution_generator):
                solution = await solution_generator()
            else:
                solution = solution_generator()

            state.solution = solution

            # Calculate score and amplitude
            score = self.score_function(solution)
            state.amplitude = self.probability_calc.calculate_amplitude(score)

            state.metadata['score'] = score
            state.metadata['probability'] = state.probability

            logger.debug(
                f"Universe {universe_id} evolved: score={score:.3f}, "
                f"probability={state.probability:.3f}"
            )

        except Exception as e:
            logger.error(f"Universe {universe_id} evolution failed: {e}")
            # Failed universe has zero amplitude
            state.amplitude = complex(0.0, 0.0)
            state.state = UniverseState.INTERFERED
            state.metadata['error'] = str(e)

        return state

    def apply_interference(self) -> None:
        """
        Apply quantum interference between similar solutions.

        Similar solutions can constructively or destructively interfere,
        affecting their probability amplitudes.
        """
        n_states = len(self.states)
        if n_states < 2:
            return

        # Check all pairs for interference
        for i in range(n_states):
            for j in range(i + 1, n_states):
                state1 = self.states[i]
                state2 = self.states[j]

                # Calculate similarity (simplified: based on probability)
                similarity = abs(state1.probability - state2.probability)

                if similarity < self.interference_threshold:
                    # States are similar enough to interfere
                    combined_amplitude = self.probability_calc.calculate_interference(
                        state1, state2
                    )

                    # Check if interference is destructive
                    if abs(combined_amplitude) < abs(state1.amplitude) * 0.7:
                        self.interference_events += 1

                        # Mark weaker state as interfered
                        if state1.probability < state2.probability:
                            state1.state = UniverseState.INTERFERED
                            state1.amplitude *= 0.5  # Reduce amplitude
                        else:
                            state2.state = UniverseState.INTERFERED
                            state2.amplitude *= 0.5

                        # Create entanglement if enabled
                        if self.enable_entanglement:
                            state1.entangle(state2.universe_id)
                            state2.entangle(state1.universe_id)

    async def explore_superposition(
        self,
        solution_generators: List[Callable[[], Any]]
    ) -> SuperpositionResult[T]:
        """
        Explore multiple parallel universes in superposition.

        Args:
            solution_generators: List of functions that generate solutions

        Returns:
            Result containing best solution after collapse
        """
        start_time = datetime.now()

        # Limit number of universes
        generators = solution_generators[:self.max_universes]
        n_universes = len(generators)

        logger.info(f"Exploring {n_universes} parallel universes")

        # Create universes in parallel using asyncio.gather()
        universe_tasks = [
            self.create_universe(f"universe_{i}", gen)
            for i, gen in enumerate(generators)
        ]

        # Execute all universes in parallel (TRUE PARALLELISM)
        self.states = await asyncio.gather(*universe_tasks)

        # Apply quantum interference
        self.apply_interference()

        # Normalize amplitudes
        self.probability_calc.normalize_amplitudes(self.states)

        # Collapse to best solution (observation)
        best_state = self._collapse_superposition()

        execution_time = (datetime.now() - start_time).total_seconds() * 1000

        result = SuperpositionResult(
            best_solution=best_state.solution,
            best_probability=best_state.probability,
            all_states=self.states,
            interference_events=self.interference_events,
            total_amplitude=sum(state.amplitude for state in self.states),
            execution_time_ms=execution_time,
            metadata={
                'n_universes': n_universes,
                'best_universe': best_state.universe_id,
                'coherence': 0.0  # Calculated by property
            }
        )

        logger.info(
            f"Superposition collapsed: best_probability={result.best_probability:.3f}, "
            f"coherence={result.coherence:.3f}, time={execution_time:.1f}ms"
        )

        return result

    def _collapse_superposition(self) -> QuantumState[T]:
        """
        Collapse superposition to single best state (Born rule).

        Returns:
            Best quantum state after measurement
        """
        # Filter out interfered states
        viable_states = [
            s for s in self.states
            if s.state != UniverseState.INTERFERED
        ]

        if not viable_states:
            logger.warning("No viable states, using all states")
            viable_states = self.states

        # Select best state by probability
        best_state = max(viable_states, key=lambda s: s.probability)
        best_state.collapse()

        return best_state

    def get_top_solutions(self, n: int = 5) -> List[QuantumState[T]]:
        """
        Get top N solutions by probability.

        Args:
            n: Number of top solutions to return

        Returns:
            List of top quantum states
        """
        viable_states = [
            s for s in self.states
            if s.state != UniverseState.INTERFERED and s.solution is not None
        ]

        sorted_states = sorted(viable_states, key=lambda s: s.probability, reverse=True)
        return sorted_states[:n]

    def reset(self) -> None:
        """Reset engine state for new computation"""
        self.states.clear()
        self.interference_events = 0