"""
Holographic State Encoding Module

Provides FFT-based holographic encoding for distributed state storage
with graceful degradation properties.
"""

from .state_encoder import (
    HolographicEncoder,
    HolographicFragment,
    EncodingMetadata,
    FragmentManager,
    InterferencePatternGenerator
)

__all__ = [
    'HolographicEncoder',
    'HolographicFragment',
    'EncodingMetadata',
    'FragmentManager',
    'InterferencePatternGenerator'
]