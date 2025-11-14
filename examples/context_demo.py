#!/usr/bin/env python3
"""
Shannon Context Management Demo

Demonstrates onboarding the shannon-cli codebase itself.

Usage:
    python examples/context_demo.py
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from shannon.context import ContextManager


async def main():
    """Demo: Onboard shannon-cli codebase"""

    # Initialize manager
    manager = ContextManager()

    # Get shannon-cli path
    shannon_path = Path(__file__).parent.parent

    print("=" * 60)
    print("Shannon Context Management Demo")
    print("=" * 60)
    print(f"\nOnboarding: {shannon_path}")
    print("\nThis will:")
    print("  1. Scan the shannon-cli directory tree")
    print("  2. Detect languages and tech stack")
    print("  3. Analyze patterns and modules")
    print("  4. Create knowledge graph in Serena")
    print("  5. Save local index files")
    print("\nExpected duration: 2-5 minutes (shannon-cli is ~6,500 lines)")
    print("=" * 60)

    input("\nPress Enter to start onboarding...")

    # Onboard
    try:
        result = await manager.onboard_project(
            project_path=str(shannon_path),
            project_id="shannon_cli_v3"
        )

        print("\n" + "=" * 60)
        print("Onboarding Complete!")
        print("=" * 60)
        print(f"\nProject ID: {result['project_id']}")
        print(f"Files: {result['discovery']['file_count']}")
        print(f"Lines: {result['discovery']['total_lines']:,}")
        print(f"Languages: {', '.join(result['discovery']['languages'].keys())}")
        print(f"Tech stack: {', '.join(result['discovery']['tech_stack'])}")

        # Show patterns
        patterns = result['analysis']['patterns']
        if patterns:
            print(f"\nPatterns detected ({len(patterns)}):")
            for pattern in patterns:
                print(f"  • {pattern['name']}: {pattern['description']}")

        # Show modules
        modules = result['analysis']['modules']
        if modules:
            print(f"\nModules detected ({len(modules)}):")
            for module in modules[:5]:
                print(f"  • {module['name']} ({len(module['files'])} files)")

        print("\n" + "=" * 60)
        print("Demo: Prime Project")
        print("=" * 60)
        print("\nNow demonstrating quick context reload...")

        # Prime
        context = await manager.prime_project(
            project_id="shannon_cli_v3",
            load_files=True,
            check_mcps=False
        )

        print(f"\nPrimed in seconds!")
        print(f"Files loaded: {len(context.critical_files)}")
        print(f"Modules: {len(context.modules)}")
        print(f"Patterns: {len(context.patterns)}")

        print("\n" + "=" * 60)
        print("Demo: Smart Loading")
        print("=" * 60)
        print("\nLoading context for task: 'Add metrics dashboard'")

        # Load for task
        loaded = await manager.load_for_task(
            task_description="Add metrics dashboard to Shannon CLI",
            project_id="shannon_cli_v3"
        )

        print(f"\nLoaded {len(loaded.relevant_files)} relevant files:")
        for file_path, score in loaded.relevance_scores[:5]:
            print(f"  • {file_path} (score: {score:.1f})")

        print(f"\nTotal lines loaded: {loaded.total_lines}")
        print(f"Relevance: {len(loaded.relevant_files)} files of {result['discovery']['file_count']} total")
        print(f"           ({len(loaded.relevant_files) / result['discovery']['file_count'] * 100:.1f}% of codebase)")

        print("\n" + "=" * 60)
        print("Demo Complete!")
        print("=" * 60)
        print("\nLocal index saved to:")
        print(f"  ~/.shannon/projects/shannon_cli_v3/")
        print("\nSerena knowledge graph created with:")
        print(f"  • Project node")
        print(f"  • {len(modules)} module nodes")
        print(f"  • {len(patterns)} pattern nodes")

        print("\nNext steps:")
        print("  1. Run: shannon prime --project shannon_cli_v3")
        print("  2. Run: shannon context update")
        print("  3. Explore local index files")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
