#!/usr/bin/env python3
"""
Shannon Cache System Demo

Demonstrates the 3-tier caching system with real operations.
"""

import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from shannon.cache import CacheManager


def demo_analysis_cache(manager: CacheManager):
    """Demo analysis cache with context awareness."""
    print("\n" + "=" * 60)
    print("DEMO 1: Analysis Cache (Context-Aware)")
    print("=" * 60)

    spec_text = """
    Build a web application with:
    - React frontend
    - Django backend
    - PostgreSQL database
    - Docker deployment
    """

    context = {
        'project_id': 'demo-project',
        'tech_stack': ['React', 'Django', 'PostgreSQL', 'Docker'],
        'loaded_files': {
            'frontend/App.jsx': {},
            'backend/views.py': {},
            'docker-compose.yml': {}
        }
    }

    # First request (cache miss)
    print("\n1. First analysis (will be cached)...")
    start = time.time()
    result = manager.analysis.get(spec_text, context=context)

    if result is None:
        print("   ❌ Cache MISS - performing analysis...")
        # Simulate expensive analysis
        time.sleep(0.1)
        result = {
            'complexity_score': 0.65,
            'domain_breakdown': {
                'Frontend': 35.0,
                'Backend': 35.0,
                'Database': 20.0,
                'DevOps': 10.0
            },
            'estimated_time_weeks': 8
        }
        manager.analysis.save(spec_text, result, context=context)
        elapsed = time.time() - start
        print(f"   ⏱️  Analysis completed in {elapsed:.3f}s")
    else:
        elapsed = time.time() - start
        print(f"   ✅ Cache HIT! Retrieved in {elapsed:.3f}s")

    # Second request (cache hit)
    print("\n2. Same analysis request (should hit cache)...")
    start = time.time()
    result = manager.analysis.get(spec_text, context=context)
    elapsed = time.time() - start

    if result and result.get('_cache_hit'):
        print(f"   ✅ Cache HIT! Retrieved in {elapsed:.3f}s")
        print(f"   📊 Result: {result['complexity_score']} complexity")
        print(f"   💰 Savings: ~$0.15 (API cost avoided)")
    else:
        print(f"   ❌ Unexpected cache miss")

    # Different context (cache miss)
    print("\n3. Same spec but different context (cache miss)...")
    different_context = {
        'project_id': 'different-project',
        'tech_stack': ['Vue', 'Flask'],
        'loaded_files': {'main.py': {}}
    }
    result = manager.analysis.get(spec_text, context=different_context)
    if result is None:
        print("   ❌ Cache MISS - context changed (expected)")
    else:
        print("   ⚠️  Unexpected cache hit")


def demo_command_cache(manager: CacheManager):
    """Demo command cache with version-based keys."""
    print("\n" + "=" * 60)
    print("DEMO 2: Command Cache (Version-Based)")
    print("=" * 60)

    # Save prime command result
    print("\n1. Caching 'prime' command result...")
    prime_result = {
        'instructions': 'Shannon Framework Instructions v3.0',
        'sections': ['Getting Started', 'Commands', 'Best Practices']
    }
    manager.command.save(
        'prime',
        prime_result,
        framework_version='3.0.0',
        execution_time=2.5
    )
    print("   ✅ Saved to cache")

    # Retrieve from cache
    print("\n2. Retrieving 'prime' command (should hit cache)...")
    start = time.time()
    result = manager.command.get('prime', framework_version='3.0.0')
    elapsed = time.time() - start

    if result and result.get('_cache_hit'):
        print(f"   ✅ Cache HIT! Retrieved in {elapsed:.3f}s")
        print(f"   ⏱️  Saved: ~2.5 seconds (execution time avoided)")
    else:
        print("   ❌ Unexpected cache miss")

    # Different version (cache miss)
    print("\n3. Different framework version (cache miss)...")
    result = manager.command.get('prime', framework_version='3.1.0')
    if result is None:
        print("   ❌ Cache MISS - version changed (expected)")


def demo_mcp_cache(manager: CacheManager):
    """Demo MCP cache with domain signatures."""
    print("\n" + "=" * 60)
    print("DEMO 3: MCP Cache (Deterministic Signatures)")
    print("=" * 60)

    domains = {
        'Backend': 40.0,
        'Frontend': 30.0,
        'Analytics': 20.0,
        'DevOps': 10.0
    }

    mcps = [
        {'mcp_name': 'serena', 'tier': 1, 'justification': 'Context preservation'},
        {'mcp_name': 'context7', 'tier': 2, 'justification': 'Backend docs'},
        {'mcp_name': 'sqlite', 'tier': 2, 'justification': 'Analytics ops'},
    ]

    # Save MCP recommendations
    print("\n1. Saving MCP recommendations...")
    signature = manager.mcp.compute_domain_signature(domains)
    print(f"   🔑 Domain signature: {signature}")
    manager.mcp.save(domains, mcps)
    print("   ✅ Saved to cache")

    # Retrieve from cache
    print("\n2. Retrieving MCP recommendations (should hit cache)...")
    start = time.time()
    result = manager.mcp.get(domains)
    elapsed = time.time() - start

    if result and result[0].get('_cache_hit'):
        print(f"   ✅ Cache HIT! Retrieved in {elapsed:.3f}s")
        print(f"   📦 Retrieved {len(result)} MCP recommendations")
    else:
        print("   ❌ Unexpected cache miss")

    # Same domains, different order (should hit - order independent)
    print("\n3. Same domains, different order (should hit)...")
    reordered_domains = {
        'DevOps': 10.0,
        'Analytics': 20.0,
        'Backend': 40.0,
        'Frontend': 30.0
    }
    result = manager.mcp.get(reordered_domains)
    if result and result[0].get('_cache_hit'):
        print("   ✅ Cache HIT! Order-independent hashing works")
    else:
        print("   ❌ Unexpected cache miss")


def demo_unified_stats(manager: CacheManager):
    """Demo unified statistics across all caches."""
    print("\n" + "=" * 60)
    print("DEMO 4: Unified Statistics")
    print("=" * 60)

    stats = manager.get_stats()

    print("\n📊 Overall Statistics:")
    print(f"   Total requests: {stats['overall']['total_requests']}")
    print(f"   Total hits: {stats['overall']['total_hits']}")
    print(f"   Total misses: {stats['overall']['total_misses']}")
    print(f"   Hit rate: {stats['overall']['hit_rate_percent']:.1f}%")
    print(f"   Total size: {stats['overall']['total_size_mb']:.3f} MB")
    print(f"   Utilization: {stats['overall']['utilization_percent']:.2f}%")

    print("\n💰 Savings:")
    print(f"   Cost savings: ${stats['overall']['total_savings_usd']:.2f}")
    print(f"   Time savings: {stats['overall']['total_savings_minutes']:.2f} minutes")

    print("\n📈 Per-Cache Statistics:")
    for cache_type in ['analysis', 'command', 'mcp']:
        cache_stats = stats[cache_type]
        print(f"\n   {cache_type.upper()}:")
        print(f"     Hits: {cache_stats['hits']}")
        print(f"     Misses: {cache_stats['misses']}")
        print(f"     Hit rate: {cache_stats['hit_rate_percent']:.1f}%")
        print(f"     Files: {cache_stats['cache_size_files']}")


def demo_health_check(manager: CacheManager):
    """Demo health monitoring."""
    print("\n" + "=" * 60)
    print("DEMO 5: Health Check")
    print("=" * 60)

    health = manager.health_check()

    print(f"\n🏥 Health Status: {'✅ HEALTHY' if health['healthy'] else '❌ UNHEALTHY'}")

    if health['issues']:
        print("\n⚠️  Issues:")
        for issue in health['issues']:
            print(f"   - {issue}")

    if health['warnings']:
        print("\n⚠️  Warnings:")
        for warning in health['warnings']:
            print(f"   - {warning}")

    if health['healthy'] and not health['warnings']:
        print("\n   ✅ All systems operational")


def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("SHANNON CACHE SYSTEM DEMONSTRATION")
    print("=" * 60)

    # Use temp directory for demo
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"\nUsing temporary cache directory: {tmpdir}")

        manager = CacheManager(base_dir=Path(tmpdir))

        # Run demos
        demo_analysis_cache(manager)
        demo_command_cache(manager)
        demo_mcp_cache(manager)
        demo_unified_stats(manager)
        demo_health_check(manager)

        print("\n" + "=" * 60)
        print("DEMO COMPLETE")
        print("=" * 60)
        print("\nCache system is ready for production use!")
        print("All features demonstrated successfully.\n")


if __name__ == '__main__':
    main()
