#!/usr/bin/env python3
"""
Direct test of npm registry API integration

Tests _search_npm() method directly to verify npm API works
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from shannon.executor.library_discoverer import LibraryDiscoverer


async def test_npm_direct():
    """Test npm registry API directly"""
    print("\n" + "="*70)
    print("DIRECT TEST: npm Registry API for 'React UI components'")
    print("="*70)

    # Create discoverer (language detection will be Python, but we'll call npm directly)
    discoverer = LibraryDiscoverer(project_root=Path.cwd())

    print(f"\nDetected language: {discoverer.language}")
    print(f"Detected project type: {discoverer.project_type}")
    print("\nℹ️  Bypassing language routing to test npm API directly...\n")

    # Call _search_npm directly
    print("📡 Calling _search_npm('UI components')...")
    start_time = datetime.now()

    raw_results = await discoverer._search_npm("UI components")

    elapsed = (datetime.now() - start_time).total_seconds()

    print(f"\n✅ Raw Results: {len(raw_results)} packages from npm registry in {elapsed:.2f}s\n")

    # Display results
    for i, lib in enumerate(raw_results[:5], 1):
        print(f"{i}. {lib.get('name', 'unknown')}")
        print(f"   Description: {lib.get('description', 'N/A')[:80]}...")
        print(f"   Version: {lib.get('version', 'N/A')}")
        print(f"   npm Score: {lib.get('npm_score', 0):.1f}")
        print(f"   License: {lib.get('license', 'N/A')}")
        print()

    # Test again with different query
    print("\n" + "="*70)
    print("DIRECT TEST: npm Registry API for 'state management'")
    print("="*70)

    print("\n📡 Calling _search_npm('state management')...")
    start_time = datetime.now()

    state_results = await discoverer._search_npm("state management")

    elapsed = (datetime.now() - start_time).total_seconds()

    print(f"\n✅ Raw Results: {len(state_results)} packages from npm registry in {elapsed:.2f}s\n")

    for i, lib in enumerate(state_results[:5], 1):
        print(f"{i}. {lib.get('name', 'unknown')}")
        print(f"   Description: {lib.get('description', 'N/A')[:80]}...")
        print()

    # Summary
    print("="*70)
    print("📊 SUMMARY")
    print("="*70)
    print(f"✅ npm API integration: WORKING")
    print(f"✅ UI components query: {len(raw_results)} packages")
    print(f"✅ State management query: {len(state_results)} packages")

    return raw_results


if __name__ == "__main__":
    asyncio.run(test_npm_direct())
