"""
Wave 3 Exit Gate: Intelligent State Caching Validation

Runs all 7 Wave 3 functional tests to validate:
- Context fingerprinting and cache key generation
- Cache hit/miss detection
- Cache invalidation strategies
- Cache persistence across sessions
- Cache size management
- Cache performance improvements
- Cache consistency guarantees

Requires 100% pass rate to proceed to Wave 4.

Part of Shannon V3 Wave 3: Intelligent State Caching
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from validation_gates.gate_framework import ValidationGate
from cli_functional.test_wave3_cache import TestWave3Cache


async def wave3_exit_gate() -> bool:
    """
    Run Wave 3 exit gate - all 7 functional tests

    Returns:
        bool: True if all tests pass
    """
    gate = ValidationGate(phase=3, gate_type='exit')

    # Instantiate test class
    cache_tests = TestWave3Cache()

    # Add all 7 Wave 3 tests
    gate.add_test(cache_tests.test_context_fingerprinting)
    gate.add_test(cache_tests.test_cache_hit_miss_detection)
    gate.add_test(cache_tests.test_cache_invalidation)
    gate.add_test(cache_tests.test_cache_persistence)
    gate.add_test(cache_tests.test_cache_size_management)
    gate.add_test(cache_tests.test_cache_performance)
    gate.add_test(cache_tests.test_cache_consistency)

    result = await gate.run_all_tests()
    result.display()

    return result.passed


if __name__ == '__main__':
    import asyncio
    success = asyncio.run(wave3_exit_gate())
    sys.exit(0 if success else 1)
