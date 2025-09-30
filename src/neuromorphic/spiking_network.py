"""
Neuromorphic Spiking Neural Network

Implements event-driven spiking neural networks with spike-timing-dependent
plasticity (STDP) for adaptive routing and decision-making.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Callable
from enum import Enum
from collections import defaultdict, deque
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)


class NeuronState(Enum):
    """State of a spiking neuron"""
    RESTING = "resting"
    EXCITED = "excited"
    FIRING = "firing"
    REFRACTORY = "refractory"


@dataclass
class Spike:
    """Represents a spike event"""
    neuron_id: str
    timestamp: float  # Simulation time
    amplitude: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"Spike(neuron={self.neuron_id}, t={self.timestamp:.3f}, amp={self.amplitude:.2f})"


@dataclass
class Synapse:
    """
    Synapse connecting two neurons with adaptive weight.

    Weight changes based on spike-timing-dependent plasticity (STDP).
    """
    source_id: str
    target_id: str
    weight: float
    delay: float  # Synaptic delay in ms
    plasticity_enabled: bool = True
    last_update: float = 0.0
    spike_history: deque = field(default_factory=lambda: deque(maxlen=100))

    # STDP parameters
    a_plus: float = 0.1  # LTP amplitude
    a_minus: float = 0.12  # LTD amplitude
    tau_plus: float = 20.0  # LTP time constant (ms)
    tau_minus: float = 20.0  # LTD time constant (ms)

    # Weight bounds
    w_min: float = 0.0
    w_max: float = 1.0

    def apply_stdp(
        self,
        pre_spike_time: float,
        post_spike_time: float,
        current_time: float
    ) -> None:
        """
        Apply spike-timing-dependent plasticity.

        Args:
            pre_spike_time: Presynaptic spike time
            post_spike_time: Postsynaptic spike time
            current_time: Current simulation time
        """
        if not self.plasticity_enabled:
            return

        # Calculate time difference
        delta_t = post_spike_time - pre_spike_time

        # STDP rule: potentiation if pre before post, depression otherwise
        if delta_t > 0:
            # Long-term potentiation (LTP)
            delta_w = self.a_plus * np.exp(-delta_t / self.tau_plus)
        else:
            # Long-term depression (LTD)
            delta_w = -self.a_minus * np.exp(delta_t / self.tau_minus)

        # Update weight with bounds
        old_weight = self.weight
        self.weight = np.clip(self.weight + delta_w, self.w_min, self.w_max)
        self.last_update = current_time

        # Record in history
        self.spike_history.append({
            'time': current_time,
            'delta_t': delta_t,
            'delta_w': delta_w,
            'old_weight': old_weight,
            'new_weight': self.weight
        })

    def transmit_spike(self, spike: Spike) -> Spike:
        """
        Transmit spike through synapse with weight modulation and delay.

        Args:
            spike: Input spike

        Returns:
            Modulated spike for target neuron
        """
        return Spike(
            neuron_id=self.target_id,
            timestamp=spike.timestamp + self.delay,
            amplitude=spike.amplitude * self.weight,
            metadata={
                'source': self.source_id,
                'synapse_weight': self.weight,
                'synapse_delay': self.delay
            }
        )

    def __repr__(self) -> str:
        return f"Synapse({self.source_id}→{self.target_id}, w={self.weight:.3f}, d={self.delay:.1f}ms)"


@dataclass
class Neuron:
    """
    Spiking neuron with leaky integrate-and-fire dynamics.

    Features:
    - Membrane potential with leak
    - Firing threshold
    - Refractory period
    - Spike generation
    """
    neuron_id: str
    neuron_type: str = "excitatory"  # excitatory or inhibitory

    # Membrane dynamics
    membrane_potential: float = 0.0
    resting_potential: float = 0.0
    threshold: float = 1.0
    reset_potential: float = 0.0

    # Time constants
    tau_membrane: float = 10.0  # ms
    refractory_period: float = 2.0  # ms

    # State
    state: NeuronState = NeuronState.RESTING
    last_spike_time: float = -1000.0
    refractory_until: float = 0.0

    # Spike history
    spike_times: List[float] = field(default_factory=list)

    # Input accumulation
    input_current: float = 0.0

    def update(self, current_time: float, dt: float) -> Optional[Spike]:
        """
        Update neuron state for time step.

        Args:
            current_time: Current simulation time
            dt: Time step

        Returns:
            Spike if neuron fires, None otherwise
        """
        # Check refractory period
        if current_time < self.refractory_until:
            self.state = NeuronState.REFRACTORY
            return None

        # Leaky integration
        decay = np.exp(-dt / self.tau_membrane)
        self.membrane_potential = (
            self.membrane_potential * decay +
            self.input_current * (1 - decay)
        )

        # Reset input current
        self.input_current = 0.0

        # Check for firing
        if self.membrane_potential >= self.threshold:
            return self._fire(current_time)

        # Update state based on potential
        if self.membrane_potential > self.threshold * 0.7:
            self.state = NeuronState.EXCITED
        else:
            self.state = NeuronState.RESTING

        return None

    def _fire(self, current_time: float) -> Spike:
        """
        Generate spike and reset neuron.

        Args:
            current_time: Current simulation time

        Returns:
            Generated spike
        """
        self.state = NeuronState.FIRING
        self.last_spike_time = current_time
        self.spike_times.append(current_time)
        self.refractory_until = current_time + self.refractory_period

        # Reset membrane potential
        self.membrane_potential = self.reset_potential

        # Create spike
        spike = Spike(
            neuron_id=self.neuron_id,
            timestamp=current_time,
            amplitude=1.0 if self.neuron_type == "excitatory" else -1.0,
            metadata={'neuron_type': self.neuron_type}
        )

        logger.debug(f"Neuron {self.neuron_id} fired at t={current_time:.3f}")

        return spike

    def receive_input(self, current: float) -> None:
        """
        Receive input current from synapse.

        Args:
            current: Input current magnitude
        """
        self.input_current += current

    @property
    def firing_rate(self) -> float:
        """Calculate average firing rate (Hz)"""
        if len(self.spike_times) < 2:
            return 0.0

        time_span = self.spike_times[-1] - self.spike_times[0]
        if time_span == 0:
            return 0.0

        return len(self.spike_times) / (time_span / 1000.0)  # Convert ms to s

    def __repr__(self) -> str:
        return (
            f"Neuron(id={self.neuron_id}, type={self.neuron_type}, "
            f"V={self.membrane_potential:.3f}, state={self.state.value})"
        )


class SynapticPlasticity:
    """
    Manages synaptic plasticity rules and learning.

    Implements STDP (Spike-Timing-Dependent Plasticity) for adaptive
    weight updates based on spike timing correlations.
    """

    def __init__(
        self,
        learning_rate: float = 0.01,
        enable_homeostasis: bool = True,
        target_rate: float = 10.0  # Target firing rate (Hz)
    ):
        self.learning_rate = learning_rate
        self.enable_homeostasis = enable_homeostasis
        self.target_rate = target_rate

        # Track neuron activity for homeostatic plasticity
        self.neuron_rates: Dict[str, float] = {}

    def update_synapse(
        self,
        synapse: Synapse,
        pre_neuron: Neuron,
        post_neuron: Neuron,
        current_time: float
    ) -> None:
        """
        Update synapse weight based on neuron activity.

        Args:
            synapse: Synapse to update
            pre_neuron: Presynaptic neuron
            post_neuron: Postsynaptic neuron
            current_time: Current simulation time
        """
        # Apply STDP if both neurons have spiked
        if pre_neuron.spike_times and post_neuron.spike_times:
            pre_spike = pre_neuron.spike_times[-1]
            post_spike = post_neuron.spike_times[-1]

            # Only apply if spikes are recent and correlated
            if abs(post_spike - pre_spike) < 50.0:  # Within 50ms window
                synapse.apply_stdp(pre_spike, post_spike, current_time)

        # Apply homeostatic plasticity if enabled
        if self.enable_homeostasis:
            self._apply_homeostatic_scaling(synapse, post_neuron)

    def _apply_homeostatic_scaling(
        self,
        synapse: Synapse,
        post_neuron: Neuron
    ) -> None:
        """
        Apply homeostatic scaling to maintain target firing rate.

        Args:
            synapse: Synapse to scale
            post_neuron: Postsynaptic neuron
        """
        # Calculate current firing rate
        current_rate = post_neuron.firing_rate

        # Scale weights to push toward target rate
        if current_rate > self.target_rate * 1.2:
            # Too active, reduce weights
            scale_factor = 1.0 - self.learning_rate * 0.1
        elif current_rate < self.target_rate * 0.8:
            # Too quiet, increase weights
            scale_factor = 1.0 + self.learning_rate * 0.1
        else:
            # In target range, no scaling
            return

        synapse.weight = np.clip(
            synapse.weight * scale_factor,
            synapse.w_min,
            synapse.w_max
        )


class SpikingNeuralNetwork:
    """
    Event-driven spiking neural network for adaptive routing and decision-making.

    Features:
    - Asynchronous spike propagation
    - STDP learning
    - Homeostatic plasticity
    - Event-driven computation
    - Efficient spike queue processing
    """

    def __init__(
        self,
        dt: float = 0.1,  # Time step (ms)
        enable_plasticity: bool = True,
        max_spike_queue_size: int = 10000
    ):
        """
        Initialize spiking neural network.

        Args:
            dt: Simulation time step (ms)
            enable_plasticity: Enable synaptic plasticity
            max_spike_queue_size: Maximum spikes in queue
        """
        self.dt = dt
        self.enable_plasticity = enable_plasticity
        self.max_spike_queue_size = max_spike_queue_size

        # Network components
        self.neurons: Dict[str, Neuron] = {}
        self.synapses: Dict[str, List[Synapse]] = defaultdict(list)  # source_id -> List[Synapse]

        # Plasticity manager
        self.plasticity = SynapticPlasticity()

        # Event-driven simulation
        self.spike_queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=max_spike_queue_size)
        self.current_time: float = 0.0
        self.simulation_active: bool = False

        # Statistics
        self.total_spikes: int = 0
        self.steps_simulated: int = 0

        logger.info(f"SpikingNeuralNetwork initialized: dt={dt}ms, plasticity={enable_plasticity}")

    def add_neuron(
        self,
        neuron_id: str,
        neuron_type: str = "excitatory",
        threshold: float = 1.0
    ) -> Neuron:
        """
        Add neuron to network.

        Args:
            neuron_id: Unique neuron identifier
            neuron_type: "excitatory" or "inhibitory"
            threshold: Firing threshold

        Returns:
            Created neuron
        """
        neuron = Neuron(
            neuron_id=neuron_id,
            neuron_type=neuron_type,
            threshold=threshold
        )
        self.neurons[neuron_id] = neuron
        logger.debug(f"Added {neuron_type} neuron: {neuron_id}")
        return neuron

    def add_synapse(
        self,
        source_id: str,
        target_id: str,
        weight: float = 0.5,
        delay: float = 1.0
    ) -> Synapse:
        """
        Add synapse between neurons.

        Args:
            source_id: Source neuron ID
            target_id: Target neuron ID
            weight: Initial synaptic weight
            delay: Synaptic delay (ms)

        Returns:
            Created synapse
        """
        if source_id not in self.neurons:
            raise ValueError(f"Source neuron {source_id} not found")
        if target_id not in self.neurons:
            raise ValueError(f"Target neuron {target_id} not found")

        synapse = Synapse(
            source_id=source_id,
            target_id=target_id,
            weight=weight,
            delay=delay,
            plasticity_enabled=self.enable_plasticity
        )

        self.synapses[source_id].append(synapse)
        logger.debug(f"Added synapse: {source_id} → {target_id} (w={weight:.3f}, d={delay:.1f}ms)")

        return synapse

    async def inject_spike(self, neuron_id: str, amplitude: float = 1.0) -> None:
        """
        Inject external spike into network.

        Args:
            neuron_id: Target neuron ID
            amplitude: Spike amplitude
        """
        spike = Spike(
            neuron_id=neuron_id,
            timestamp=self.current_time,
            amplitude=amplitude,
            metadata={'source': 'external'}
        )

        await self.spike_queue.put((spike.timestamp, spike))
        self.total_spikes += 1

    async def _propagate_spike(self, spike: Spike) -> None:
        """
        Propagate spike through network.

        Args:
            spike: Spike to propagate
        """
        # Get target neuron
        if spike.neuron_id not in self.neurons:
            logger.warning(f"Spike for unknown neuron: {spike.neuron_id}")
            return

        # Send spike through all outgoing synapses
        if spike.neuron_id in self.synapses:
            for synapse in self.synapses[spike.neuron_id]:
                # Transmit through synapse
                output_spike = synapse.transmit_spike(spike)

                # Queue output spike
                await self.spike_queue.put((output_spike.timestamp, output_spike))

                # Apply plasticity if enabled
                if self.enable_plasticity:
                    source_neuron = self.neurons[synapse.source_id]
                    target_neuron = self.neurons[synapse.target_id]
                    self.plasticity.update_synapse(
                        synapse,
                        source_neuron,
                        target_neuron,
                        self.current_time
                    )

    async def simulate_step(self) -> int:
        """
        Simulate single time step.

        Returns:
            Number of spikes processed
        """
        spikes_processed = 0

        # Update all neurons
        for neuron in self.neurons.values():
            spike = neuron.update(self.current_time, self.dt)
            if spike:
                await self.spike_queue.put((spike.timestamp, spike))
                self.total_spikes += 1

        # Process spike queue for current time
        while not self.spike_queue.empty():
            timestamp, spike = await self.spike_queue.get()

            # Only process spikes for current time
            if timestamp > self.current_time + self.dt:
                # Put back for next step
                await self.spike_queue.put((timestamp, spike))
                break

            # Deliver spike to target neuron
            if spike.neuron_id in self.neurons:
                target_neuron = self.neurons[spike.neuron_id]
                target_neuron.receive_input(spike.amplitude)

            # Propagate spike
            await self._propagate_spike(spike)

            spikes_processed += 1

        # Advance time
        self.current_time += self.dt
        self.steps_simulated += 1

        return spikes_processed

    async def run_simulation(
        self,
        duration_ms: float,
        callback: Optional[Callable[[float], None]] = None
    ) -> Dict[str, Any]:
        """
        Run network simulation for specified duration.

        Args:
            duration_ms: Simulation duration (ms)
            callback: Optional callback called each step with current time

        Returns:
            Simulation statistics
        """
        self.simulation_active = True
        start_time = self.current_time
        end_time = start_time + duration_ms

        logger.info(f"Starting simulation: {duration_ms}ms ({int(duration_ms/self.dt)} steps)")

        total_spikes_processed = 0

        try:
            while self.current_time < end_time and self.simulation_active:
                spikes = await self.simulate_step()
                total_spikes_processed += spikes

                if callback:
                    callback(self.current_time)

        except asyncio.CancelledError:
            logger.warning("Simulation cancelled")

        finally:
            self.simulation_active = False

        # Gather statistics
        stats = {
            'duration_ms': self.current_time - start_time,
            'steps_simulated': self.steps_simulated,
            'total_spikes': self.total_spikes,
            'spikes_processed': total_spikes_processed,
            'neurons': len(self.neurons),
            'synapses': sum(len(syns) for syns in self.synapses.values()),
            'average_firing_rates': {
                nid: neuron.firing_rate
                for nid, neuron in self.neurons.items()
            }
        }

        logger.info(
            f"Simulation complete: {stats['duration_ms']:.1f}ms, "
            f"{stats['total_spikes']} spikes"
        )

        return stats

    def stop_simulation(self) -> None:
        """Stop running simulation"""
        self.simulation_active = False

    def reset(self) -> None:
        """Reset network state"""
        for neuron in self.neurons.values():
            neuron.membrane_potential = neuron.resting_potential
            neuron.state = NeuronState.RESTING
            neuron.spike_times.clear()

        # Clear spike queue
        while not self.spike_queue.empty():
            try:
                self.spike_queue.get_nowait()
            except asyncio.QueueEmpty:
                break

        self.current_time = 0.0
        self.total_spikes = 0
        self.steps_simulated = 0

        logger.info("Network reset")

    def get_network_state(self) -> Dict[str, Any]:
        """
        Get current network state snapshot.

        Returns:
            Dictionary with network state information
        """
        return {
            'current_time': self.current_time,
            'neurons': {
                nid: {
                    'membrane_potential': n.membrane_potential,
                    'state': n.state.value,
                    'firing_rate': n.firing_rate,
                    'spike_count': len(n.spike_times)
                }
                for nid, n in self.neurons.items()
            },
            'synapses': {
                f"{src}->{syn.target_id}": {
                    'weight': syn.weight,
                    'delay': syn.delay,
                    'last_update': syn.last_update
                }
                for src, syns in self.synapses.items()
                for syn in syns
            },
            'statistics': {
                'total_spikes': self.total_spikes,
                'steps_simulated': self.steps_simulated,
                'queue_size': self.spike_queue.qsize()
            }
        }