#!/usr/bin/env python3
"""Bundle Shannon Framework with Shannon CLI for offline/airgapped installations.

This script copies the Shannon Framework into the CLI package, allowing
Shannon CLI to work without external dependencies on the framework.

Usage:
    python scripts/bundle_framework.py [--source PATH] [--verify]

Options:
    --source PATH   Path to Shannon Framework (default: ~/Desktop/shannon-framework)
    --verify        Verify bundled framework after copying
    --clean         Clean existing bundled framework before copying

Example:
    # Bundle from default location
    python scripts/bundle_framework.py

    # Bundle from custom location
    python scripts/bundle_framework.py --source /path/to/shannon-framework

    # Bundle and verify
    python scripts/bundle_framework.py --verify

Notes:
    - Bundled framework will be ~5-10 MB
    - Only bundles essential files (skills, commands, core)
    - Excludes: .git, __pycache__, .DS_Store, test files
"""

import shutil
import argparse
from pathlib import Path
from typing import List, Set

# Files and directories to exclude from bundling
EXCLUDE_PATTERNS: Set[str] = {
    '.git',
    '__pycache__',
    '.DS_Store',
    '*.pyc',
    '.pytest_cache',
    'node_modules',
    '.venv',
    'venv',
    'tests',
    '*.test.py',
    '.github',
}


def get_dir_size(path: Path) -> float:
    """Calculate directory size in MB.

    Args:
        path: Directory path

    Returns:
        Size in megabytes
    """
    total_size = 0
    for item in path.rglob('*'):
        if item.is_file():
            total_size += item.stat().st_size
    return total_size / (1024 * 1024)


def should_exclude(path: Path) -> bool:
    """Check if path should be excluded from bundling.

    Args:
        path: Path to check

    Returns:
        True if path should be excluded, False otherwise
    """
    # Check if any parent or the path itself matches exclude patterns
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith('*'):
            # Wildcard pattern
            if path.name.endswith(pattern[1:]):
                return True
        elif path.name == pattern:
            return True
    return False


def copy_tree_filtered(src: Path, dst: Path) -> int:
    """Copy directory tree with filtering.

    Args:
        src: Source directory
        dst: Destination directory

    Returns:
        Number of files copied
    """
    copied_count = 0

    for item in src.rglob('*'):
        if should_exclude(item):
            continue

        # Calculate relative path
        rel_path = item.relative_to(src)
        dest_path = dst / rel_path

        if item.is_dir():
            dest_path.mkdir(parents=True, exist_ok=True)
        else:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest_path)
            copied_count += 1

    return copied_count


def verify_bundle(bundle_path: Path) -> bool:
    """Verify bundled framework is complete.

    Args:
        bundle_path: Path to bundled framework

    Returns:
        True if verification passes, False otherwise
    """
    from shannon.setup.framework_detector import FrameworkDetector

    is_valid, message = FrameworkDetector.verify_framework(bundle_path)

    if is_valid:
        print(f"✅ Verification passed: {message}")
        return True
    else:
        print(f"❌ Verification failed: {message}")
        return False


def bundle_framework(
    source: Path,
    clean: bool = False,
    verify: bool = False
) -> bool:
    """Bundle Shannon Framework into CLI package.

    Args:
        source: Path to Shannon Framework source
        clean: Whether to clean existing bundle first
        verify: Whether to verify bundle after copying

    Returns:
        True if bundling succeeded, False otherwise
    """
    # Determine destination
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    dest = project_root / 'src' / 'shannon' / 'bundled' / 'shannon-framework'

    print("Shannon Framework Bundling")
    print("=" * 60)
    print()

    # Check source exists
    if not source.exists():
        print(f"❌ Source not found: {source}")
        print()
        print("Options:")
        print(f"  1. Clone Shannon Framework to {source}")
        print(f"  2. Specify --source with custom path")
        return False

    print(f"Source:      {source}")
    print(f"Destination: {dest}")
    print()

    # Clean existing bundle if requested
    if clean and dest.exists():
        print("Cleaning existing bundle...")
        shutil.rmtree(dest)
        print("✓ Cleaned")
        print()

    # Copy framework
    print("Copying framework files...")
    try:
        copied = copy_tree_filtered(source, dest)
        print(f"✓ Copied {copied} files")
    except Exception as e:
        print(f"❌ Copy failed: {e}")
        return False

    # Calculate size
    size_mb = get_dir_size(dest)
    print(f"✓ Bundle size: {size_mb:.2f} MB")
    print()

    # Verify if requested
    if verify:
        print("Verifying bundle...")
        if not verify_bundle(dest):
            return False
        print()

    # Success
    print("=" * 60)
    print("✅ Framework bundled successfully")
    print()
    print("The bundled framework will be used as a fallback when:")
    print("  - Shannon Framework is not installed via plugin system")
    print("  - SHANNON_FRAMEWORK_PATH is not set")
    print("  - Framework is not found in other standard locations")
    print()
    print("Note: Bundled framework won't receive automatic updates.")
    print("      Users should prefer plugin system installation.")
    print()

    return True


def main():
    """Main entry point for bundling script."""
    parser = argparse.ArgumentParser(
        description='Bundle Shannon Framework with Shannon CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--source',
        type=Path,
        default=Path.home() / 'Desktop' / 'shannon-framework',
        help='Path to Shannon Framework (default: ~/Desktop/shannon-framework)'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify bundled framework after copying'
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Clean existing bundled framework before copying'
    )

    args = parser.parse_args()

    success = bundle_framework(
        source=args.source,
        clean=args.clean,
        verify=args.verify
    )

    exit(0 if success else 1)


if __name__ == '__main__':
    main()
