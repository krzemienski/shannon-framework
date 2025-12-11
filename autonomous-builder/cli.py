#!/usr/bin/env python3
"""
CLI for Autonomous Claude Code Builder.

Usage:
    autonomous-builder build <spec> [--dir DIR] [--max-iterations N] [--model MODEL]
    autonomous-builder analyze <dir>
    autonomous-builder resume <dir>
    autonomous-builder status <dir>

Examples:
    autonomous-builder build "Create a todo app with React and FastAPI"
    autonomous-builder build spec.md --dir ./my-project
    autonomous-builder resume ./my-project
"""

import argparse
import asyncio
import sys
import json
import logging
from pathlib import Path
from typing import Optional

from .builder import AutonomousBuilder
from .config import BuilderConfig
from .scenario_handler import ScenarioHandler
from .serena_context import SerenaContextManager


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Autonomous Claude Code Builder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Build command
    build_parser = subparsers.add_parser("build", help="Build from specification")
    build_parser.add_argument(
        "spec",
        help="Specification text or path to spec file"
    )
    build_parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=Path("./autonomous_build"),
        help="Target directory (default: ./autonomous_build)"
    )
    build_parser.add_argument(
        "--max-iterations", "-n",
        type=int,
        default=None,
        help="Maximum coding sessions (default: unlimited)"
    )
    build_parser.add_argument(
        "--model", "-m",
        default="claude-sonnet-4-5-20250929",
        help="Claude model to use"
    )
    build_parser.add_argument(
        "--no-puppeteer",
        action="store_true",
        help="Disable Puppeteer MCP"
    )
    build_parser.add_argument(
        "--max-cost",
        type=float,
        default=None,
        help="Maximum cost in USD"
    )

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze existing directory")
    analyze_parser.add_argument(
        "dir",
        type=Path,
        help="Directory to analyze"
    )

    # Resume command
    resume_parser = subparsers.add_parser("resume", help="Resume interrupted build")
    resume_parser.add_argument(
        "dir",
        type=Path,
        help="Project directory with feature_list.json"
    )
    resume_parser.add_argument(
        "--max-iterations", "-n",
        type=int,
        default=None,
        help="Maximum additional coding sessions"
    )

    # Status command
    status_parser = subparsers.add_parser("status", help="Show build status")
    status_parser.add_argument(
        "dir",
        type=Path,
        help="Project directory"
    )

    # Global options
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to config file (YAML or JSON)"
    )

    return parser.parse_args()


async def cmd_build(args: argparse.Namespace) -> int:
    """Execute build command."""
    print(f"\n{'='*60}")
    print("  AUTONOMOUS CLAUDE CODE BUILDER")
    print(f"{'='*60}\n")

    # Get specification
    spec_path = Path(args.spec)
    if spec_path.exists():
        spec = spec_path.read_text()
        print(f"Loaded specification from: {spec_path}")
    else:
        spec = args.spec
        print(f"Using inline specification: {spec[:100]}...")

    # Create config
    config = BuilderConfig(
        target_dir=args.dir.resolve(),
        puppeteer_enabled=not args.no_puppeteer,
        verbose=args.verbose
    )
    config.execution.max_iterations = args.max_iterations
    config.execution.model = args.model
    config.execution.max_cost_usd = args.max_cost

    print(f"\nTarget directory: {config.target_dir}")
    print(f"Model: {config.execution.model}")
    if config.execution.max_iterations:
        print(f"Max iterations: {config.execution.max_iterations}")

    # Create and run builder
    builder = AutonomousBuilder(config)

    print(f"\n{'='*60}")
    print("  STARTING BUILD")
    print(f"{'='*60}\n")

    try:
        result = await builder.build(spec)
    except KeyboardInterrupt:
        print("\n\nBuild interrupted. Run 'resume' to continue.")
        return 1

    # Print result
    print(f"\n{'='*60}")
    print("  BUILD COMPLETE" if result.success else "  BUILD FAILED")
    print(f"{'='*60}\n")

    print(f"Success: {result.success}")
    print(f"Features: {result.features_completed}/{result.features_total}")
    print(f"Sessions: {result.sessions_executed}")
    print(f"Duration: {result.total_duration_seconds:.1f}s")

    if result.total_cost_usd:
        print(f"Cost: ${result.total_cost_usd:.4f}")

    if result.errors:
        print(f"\nErrors:")
        for error in result.errors:
            print(f"  - {error}")

    if result.warnings:
        print(f"\nWarnings:")
        for warning in result.warnings:
            print(f"  - {warning}")

    print(f"\nProject directory: {result.target_dir}")

    return 0 if result.success else 1


async def cmd_analyze(args: argparse.Namespace) -> int:
    """Execute analyze command."""
    print(f"\nAnalyzing: {args.dir}")

    if not args.dir.exists():
        print(f"Error: Directory does not exist: {args.dir}")
        return 1

    serena = SerenaContextManager(args.dir)
    context = await serena.analyze_existing_directory()

    print(f"\n{'='*60}")
    print("  ANALYSIS RESULT")
    print(f"{'='*60}\n")

    if not context.exists:
        print("No project detected (empty directory)")
        return 0

    print(f"Project Type: {context.project_type}")
    print(f"Languages: {', '.join(context.languages)}")

    if context.frameworks:
        print(f"Frameworks: {', '.join(context.frameworks)}")

    if context.dependencies:
        print(f"\nDependencies ({len(context.dependencies)}):")
        for name, version in list(context.dependencies.items())[:10]:
            print(f"  - {name}: {version}")
        if len(context.dependencies) > 10:
            print(f"  ... and {len(context.dependencies) - 10} more")

    if context.patterns:
        print(f"\nPatterns detected:")
        for pattern in context.patterns:
            print(f"  - {pattern}")

    if context.structure:
        print(f"\nStructure:")
        dirs = context.structure.get("directories", [])
        if dirs:
            print(f"  Directories: {', '.join(dirs[:10])}")

    return 0


async def cmd_resume(args: argparse.Namespace) -> int:
    """Execute resume command."""
    print(f"\nResuming build in: {args.dir}")

    if not args.dir.exists():
        print(f"Error: Directory does not exist: {args.dir}")
        return 1

    feature_list = args.dir / "feature_list.json"
    if not feature_list.exists():
        print(f"Error: No feature_list.json found in {args.dir}")
        print("This doesn't appear to be an autonomous build directory.")
        return 1

    # Load feature list and show progress
    features = json.loads(feature_list.read_text())
    total = len(features.get("features", []))
    completed = sum(1 for f in features.get("features", []) if f.get("passes"))

    print(f"\nProgress: {completed}/{total} features ({completed/total*100:.1f}%)")

    if completed >= total:
        print("All features complete!")
        return 0

    # Create config
    config = BuilderConfig(
        target_dir=args.dir.resolve(),
        verbose=args.verbose if hasattr(args, 'verbose') else False
    )
    config.execution.max_iterations = args.max_iterations

    # Resume build
    builder = AutonomousBuilder(config)

    print(f"\n{'='*60}")
    print("  RESUMING BUILD")
    print(f"{'='*60}\n")

    try:
        result = await builder.build("Resume from feature list")
    except KeyboardInterrupt:
        print("\n\nBuild interrupted. Run 'resume' to continue.")
        return 1

    print(f"\nResumed build {'completed' if result.success else 'failed'}")
    print(f"Features: {result.features_completed}/{result.features_total}")

    return 0 if result.success else 1


async def cmd_status(args: argparse.Namespace) -> int:
    """Execute status command."""
    if not args.dir.exists():
        print(f"Error: Directory does not exist: {args.dir}")
        return 1

    print(f"\n{'='*60}")
    print(f"  BUILD STATUS: {args.dir.name}")
    print(f"{'='*60}\n")

    # Check for feature list
    feature_list = args.dir / "feature_list.json"
    if feature_list.exists():
        features = json.loads(feature_list.read_text())
        total = len(features.get("features", []))
        completed = sum(1 for f in features.get("features", []) if f.get("passes"))
        pending = total - completed

        print(f"Feature Progress:")
        print(f"  Total:     {total}")
        print(f"  Completed: {completed}")
        print(f"  Pending:   {pending}")
        print(f"  Progress:  {completed/total*100:.1f}%")

        # Show incomplete features
        if pending > 0:
            print(f"\nNext features to implement:")
            incomplete = [f for f in features.get("features", []) if not f.get("passes")]
            for f in incomplete[:5]:
                print(f"  [{f['id']}] {f['description'][:50]}")
            if len(incomplete) > 5:
                print(f"  ... and {len(incomplete) - 5} more")
    else:
        print("No feature_list.json found - build not started")

    # Check for progress file
    progress_file = args.dir / "claude-progress.txt"
    if progress_file.exists():
        print(f"\nLatest progress from claude-progress.txt:")
        lines = progress_file.read_text().strip().split('\n')[-15:]
        for line in lines:
            print(f"  {line}")

    # Check for init.sh
    init_script = args.dir / "init.sh"
    if init_script.exists():
        print(f"\nInit script: {init_script} (exists)")

    return 0


async def main() -> int:
    """Main entry point."""
    args = parse_args()
    setup_logging(args.verbose if hasattr(args, 'verbose') else False)

    if args.command == "build":
        return await cmd_build(args)
    elif args.command == "analyze":
        return await cmd_analyze(args)
    elif args.command == "resume":
        return await cmd_resume(args)
    elif args.command == "status":
        return await cmd_status(args)
    else:
        print("No command specified. Use --help for usage.")
        return 1


def cli_entry():
    """Entry point for CLI."""
    sys.exit(asyncio.run(main()))


if __name__ == "__main__":
    cli_entry()
