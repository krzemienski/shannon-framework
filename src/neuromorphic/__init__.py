"""
Neuromorphic Computing Module

Implements biologically-inspired spiking neural networks with spike-timing-dependent
plasticity (STDP) for event-driven computation and adaptive routing.
"""

from .spiking_network import (
    SpikingNeuralNetwork,
    Neuron,
    NeuronState,
    Synapse,
    Spike,
    SynapticPlasticity
)

__all__ = [
    'SpikingNeuralNetwork',
    'Neuron',
    'NeuronState',
    'Synapse',
    'Spike',
    'SynapticPlasticity'
]