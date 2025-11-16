#!/usr/bin/env python3
"""
Test script for LibraryDiscoverer with real API integration

Tests:
1. npm search for 'React UI components'
2. PyPI search for 'Python web framework'
3. Caching behavior (second call should be faster)
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from shannon.executor.library_discoverer import LibraryDiscoverer


async def test_npm_search():
    """Test npm registry search"""
    print("\n" + "="*70)
    print("TEST 1: npm search for 'React UI components'")
    print("="*70)

    discoverer = LibraryDiscoverer(project_root=Path.cwd())

    # First call (should hit API)
    print("\n📡 First call (should search npm registry)...")
    start_time = datetime.now()

    results = await discoverer.discover_for_feature(
        feature_description="UI components",
        category="ui"
    )

    elapsed = (datetime.now() - start_time).total_seconds()

    print(f"\n✅ Results: {len(results)} libraries found in {elapsed:.2f}s")
    for i, lib in enumerate(results, 1):
        print(f"\n{i}. {lib.name}")
        print(f"   Description: {lib.description}")
        print(f"   Stars: {lib.stars}")
        print(f"   Weekly Downloads: {lib.weekly_downloads}")
        print(f"   Updated: {lib.last_updated}")
        print(f"   Quality Score: {lib.score:.1f}")
        print(f"   Recommendation: {lib.why_recommended}")

    # Second call (should hit cache)
    print("\n\n📦 Second call (should use Serena cache)...")
    start_time = datetime.now()

    cached_results = await discoverer.discover_for_feature(
        feature_description="UI components",
        category="ui"
    )

    cache_elapsed = (datetime.now() - start_time).total_seconds()

    print(f"\n✅ Cached Results: {len(cached_results)} libraries in {cache_elapsed:.2f}s")
    print(f"⚡ Speedup: {elapsed/cache_elapsed:.1f}x faster")

    return results


async def test_pypi_search():
    """Test PyPI search"""
    print("\n" + "="*70)
    print("TEST 2: PyPI search for 'Python web framework'")
    print("="*70)

    discoverer = LibraryDiscoverer(project_root=Path.cwd())

    # First call
    print("\n📡 First call (should search PyPI)...")
    start_time = datetime.now()

    results = await discoverer.discover_for_feature(
        feature_description="web framework",
        category="http"
    )

    elapsed = (datetime.now() - start_time).total_seconds()

    print(f"\n✅ Results: {len(results)} libraries found in {elapsed:.2f}s")
    for i, lib in enumerate(results, 1):
        print(f"\n{i}. {lib.name}")
        print(f"   Description: {lib.description}")
        print(f"   Quality Score: {lib.score:.1f}")

    # Verify expected libraries
    expected = ['fastapi', 'flask', 'django']
    found_names = [lib.name.lower() for lib in results]

    print("\n\n📋 Validation:")
    for exp in expected:
        if any(exp in name for name in found_names):
            print(f"   ✅ Found {exp}")
        else:
            print(f"   ❌ Missing {exp}")

    return results


async def main():
    """Run all tests"""
    print("🚀 Shannon V3.5 Library Discovery Tests")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    try:
        # Test 1: npm
        npm_results = await test_npm_search()

        # Test 2: PyPI
        pypi_results = await test_pypi_search()

        # Summary
        print("\n" + "="*70)
        print("📊 SUMMARY")
        print("="*70)
        print(f"npm libraries: {len(npm_results)}")
        print(f"PyPI libraries: {len(pypi_results)}")
        print("\n✅ All tests completed successfully!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
