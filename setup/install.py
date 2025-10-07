#!/usr/bin/env python3
"""
Shannon Framework V3 Installer

Installs Shannon markdown-based framework into Claude Code by copying
markdown files to ~/.claude/ and registering the PreCompact hook.

Usage:
    python3 install.py install    # Install Shannon V3
    python3 install.py uninstall  # Remove Shannon V3
    python3 install.py verify     # Verify installation
    python3 install.py status     # Show installation status

Requirements:
    - Python 3.8+
    - Claude Code installed
    - Serena MCP server (recommended)
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# ============================================================================
# INSTALLATION CONFIGURATION
# ============================================================================

SHANNON_VERSION = "3.0.0"
CLAUDE_DIR = Path.home() / ".claude"
SHANNON_SOURCE = Path(__file__).parent.parent / "Shannon"
HOOKS_SOURCE = Path(__file__).parent.parent / "Hooks"

# File mappings: source → destination
FILE_MAPPINGS = {
    # Core system files
    "Core/TESTING_PHILOSOPHY.md": "core/TESTING_PHILOSOPHY.md",
    "Core/CONTEXT_MANAGEMENT.md": "core/CONTEXT_MANAGEMENT.md",
    "Core/SPEC_ANALYSIS.md": "core/SPEC_ANALYSIS.md",
    "Core/PROJECT_MEMORY.md": "core/PROJECT_MEMORY.md",
    "Core/HOOK_SYSTEM.md": "core/HOOK_SYSTEM.md",
    "Core/MCP_DISCOVERY.md": "core/MCP_DISCOVERY.md",
    "Core/PHASE_PLANNING.md": "core/PHASE_PLANNING.md",
    "Core/WAVE_ORCHESTRATION.md": "core/WAVE_ORCHESTRATION.md",

    # Agent definitions
    "Agents/SPEC_ANALYZER.md": "agents/SPEC_ANALYZER.md",
    "Agents/CONTEXT_GUARDIAN.md": "agents/CONTEXT_GUARDIAN.md",
    "Agents/WAVE_COORDINATOR.md": "agents/WAVE_COORDINATOR.md",
    "Agents/TEST_GUARDIAN.md": "agents/TEST_GUARDIAN.md",
    "Agents/PHASE_ARCHITECT.md": "agents/PHASE_ARCHITECT.md",
    "Agents/REFACTORER.md": "agents/REFACTORER.md",
    "Agents/IMPLEMENTATION_WORKER.md": "agents/IMPLEMENTATION_WORKER.md",
    "Agents/ANALYZER.md": "agents/ANALYZER.md",
    "Agents/SECURITY.md": "agents/SECURITY.md",
    "Agents/ARCHITECT.md": "agents/ARCHITECT.md",
    "Agents/BACKEND.md": "agents/BACKEND.md",
    "Agents/PERFORMANCE.md": "agents/PERFORMANCE.md",
    "Agents/QA.md": "agents/QA.md",
    "Agents/DEVOPS.md": "agents/DEVOPS.md",
    "Agents/FRONTEND.md": "agents/FRONTEND.md",
    "Agents/SCRIBE.md": "agents/SCRIBE.md",
    "Agents/MOBILE_DEVELOPER.md": "agents/MOBILE_DEVELOPER.md",
    "Agents/DATA_ENGINEER.md": "agents/DATA_ENGINEER.md",
    "Agents/MENTOR.md": "agents/MENTOR.md",

    # Commands - Shannon commands (sh:*)
    "Commands/sh_analyze.md": "commands/sh_analyze.md",
    "Commands/sh_checkpoint.md": "commands/sh_checkpoint.md",
    "Commands/sh_memory.md": "commands/sh_memory.md",
    "Commands/sh_north_star.md": "commands/sh_north_star.md",
    "Commands/sh_restore.md": "commands/sh_restore.md",
    "Commands/sh_spec.md": "commands/sh_spec.md",
    "Commands/sh_status.md": "commands/sh_status.md",
    "Commands/sh_wave.md": "commands/sh_wave.md",

    # Commands - SuperClaude commands (sc:*)
    "Commands/sc_build.md": "commands/sc_build.md",
    "Commands/sc_analyze.md": "commands/sc_analyze.md",
    "Commands/sc_implement.md": "commands/sc_implement.md",
    "Commands/sc_test.md": "commands/sc_test.md",
    "Commands/sc_document.md": "commands/sc_document.md",
    "Commands/sc_git.md": "commands/sc_git.md",
    "Commands/sc_improve.md": "commands/sc_improve.md",
    "Commands/sc_design.md": "commands/sc_design.md",
    "Commands/sc_cleanup.md": "commands/sc_cleanup.md",
    "Commands/sc_troubleshoot.md": "commands/sc_troubleshoot.md",
    "Commands/sc_explain.md": "commands/sc_explain.md",
    "Commands/sc_load.md": "commands/sc_load.md",
    "Commands/sc_estimate.md": "commands/sc_estimate.md",
    "Commands/sc_task.md": "commands/sc_task.md",
    "Commands/sc_save.md": "commands/sc_save.md",
    "Commands/sc_brainstorm.md": "commands/sc_brainstorm.md",
    "Commands/sc_spawn.md": "commands/sc_spawn.md",
    "Commands/sc_research.md": "commands/sc_research.md",
    "Commands/sc_index.md": "commands/sc_index.md",
    "Commands/sc_help.md": "commands/sc_help.md",
    "Commands/sc_reflect.md": "commands/sc_reflect.md",
    "Commands/sc_workflow.md": "commands/sc_workflow.md",
    "Commands/sc_select_tool.md": "commands/sc_select_tool.md",
    "Commands/sc_spec_panel.md": "commands/sc_spec_panel.md",
    "Commands/sc_business_panel.md": "commands/sc_business_panel.md",

    # Modes
    "Modes/SHANNON_INTEGRATION.md": "modes/SHANNON_INTEGRATION.md",
    "Modes/WAVE_EXECUTION.md": "modes/WAVE_EXECUTION.md",
}

HOOK_FILE = "precompact.py"
SETTINGS_FILE = "settings.json"


# ============================================================================
# COLOR OUTPUT
# ============================================================================

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(msg: str):
    """Print colored header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{msg}{Colors.ENDC}")


def print_success(msg: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {msg}{Colors.ENDC}")


def print_error(msg: str):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {msg}{Colors.ENDC}")


def print_warning(msg: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {msg}{Colors.ENDC}")


def print_info(msg: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {msg}{Colors.ENDC}")


# ============================================================================
# INSTALLATION FUNCTIONS
# ============================================================================

def check_prerequisites() -> Tuple[bool, List[str]]:
    """Check if prerequisites are met"""
    errors = []

    # Check Python version
    if sys.version_info < (3, 8):
        errors.append(f"Python 3.8+ required (found {sys.version_info.major}.{sys.version_info.minor})")

    # Check Claude directory exists
    if not CLAUDE_DIR.exists():
        errors.append(f"Claude Code directory not found: {CLAUDE_DIR}")

    # Check Shannon source exists
    if not SHANNON_SOURCE.exists():
        errors.append(f"Shannon source directory not found: {SHANNON_SOURCE}")

    # Check hooks source exists
    if not HOOKS_SOURCE.exists():
        errors.append(f"Hooks directory not found: {HOOKS_SOURCE}")

    return len(errors) == 0, errors


def copy_markdown_files() -> Tuple[int, int]:
    """
    Copy markdown files from Shannon/ to ~/.claude/
    Returns: (success_count, total_count)
    """
    success_count = 0
    total_count = len(FILE_MAPPINGS)

    for source_path, dest_path in FILE_MAPPINGS.items():
        source = SHANNON_SOURCE / source_path
        dest = CLAUDE_DIR / dest_path

        try:
            # Create destination directory if needed
            dest.parent.mkdir(parents=True, exist_ok=True)

            # Copy file
            shutil.copy2(source, dest)
            success_count += 1

        except Exception as e:
            print_error(f"Failed to copy {source_path}: {e}")

    return success_count, total_count


def install_precompact_hook() -> bool:
    """Install PreCompact hook and register in settings.json"""
    try:
        # Create hooks directory
        hooks_dir = CLAUDE_DIR / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)

        # Copy hook file
        source = HOOKS_SOURCE / HOOK_FILE
        dest = hooks_dir / HOOK_FILE
        shutil.copy2(source, dest)

        # Make executable
        os.chmod(dest, 0o755)

        # Register in settings.json
        settings_path = CLAUDE_DIR / SETTINGS_FILE

        if settings_path.exists():
            with open(settings_path, 'r') as f:
                settings = json.load(f)
        else:
            settings = {}

        # Add PreCompact hook
        if 'hooks' not in settings:
            settings['hooks'] = {}

        settings['hooks']['preCompact'] = {
            "enabled": True,
            "script": str(dest),
            "description": "Shannon V3 PreCompact Hook - Context preservation before context limits"
        }

        # Write settings
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=2)

        return True

    except Exception as e:
        print_error(f"Failed to install PreCompact hook: {e}")
        return False


def verify_serena_mcp() -> bool:
    """Check if Serena MCP is available (optional)"""
    try:
        settings_path = CLAUDE_DIR / SETTINGS_FILE

        if not settings_path.exists():
            return False

        with open(settings_path, 'r') as f:
            settings = json.load(f)

        mcp_servers = settings.get('mcpServers', {})

        # Check for Serena MCP
        return 'serena' in mcp_servers or 'Serena' in mcp_servers

    except Exception:
        return False


def verify_installation() -> Tuple[bool, Dict[str, bool]]:
    """
    Verify Shannon installation
    Returns: (all_ok, checks_dict)
    """
    checks = {
        'markdown_files': False,
        'hook_installed': False,
        'hook_registered': False,
        'serena_mcp': False,
    }

    # Check markdown files
    missing_files = []
    for _, dest_path in FILE_MAPPINGS.items():
        if not (CLAUDE_DIR / dest_path).exists():
            missing_files.append(dest_path)

    checks['markdown_files'] = len(missing_files) == 0

    # Check hook installed
    hook_path = CLAUDE_DIR / "hooks" / HOOK_FILE
    checks['hook_installed'] = hook_path.exists()

    # Check hook registered
    try:
        settings_path = CLAUDE_DIR / SETTINGS_FILE
        if settings_path.exists():
            with open(settings_path, 'r') as f:
                settings = json.load(f)
            checks['hook_registered'] = 'preCompact' in settings.get('hooks', {})
    except Exception:
        pass

    # Check Serena MCP (optional)
    checks['serena_mcp'] = verify_serena_mcp()

    all_ok = checks['markdown_files'] and checks['hook_installed'] and checks['hook_registered']

    return all_ok, checks


# ============================================================================
# UNINSTALL FUNCTIONS
# ============================================================================

def uninstall_shannon() -> Tuple[int, int]:
    """
    Remove Shannon files from ~/.claude/
    Returns: (removed_count, total_count)
    """
    removed_count = 0
    total_count = len(FILE_MAPPINGS)

    # Remove markdown files
    for _, dest_path in FILE_MAPPINGS.items():
        dest = CLAUDE_DIR / dest_path
        try:
            if dest.exists():
                dest.unlink()
                removed_count += 1
        except Exception as e:
            print_error(f"Failed to remove {dest_path}: {e}")

    # Remove hook
    hook_path = CLAUDE_DIR / "hooks" / HOOK_FILE
    if hook_path.exists():
        hook_path.unlink()

    # Remove hook registration
    try:
        settings_path = CLAUDE_DIR / SETTINGS_FILE
        if settings_path.exists():
            with open(settings_path, 'r') as f:
                settings = json.load(f)

            if 'hooks' in settings and 'preCompact' in settings['hooks']:
                del settings['hooks']['preCompact']

                with open(settings_path, 'w') as f:
                    json.dump(settings, f, indent=2)
    except Exception as e:
        print_error(f"Failed to remove hook registration: {e}")

    # Remove empty directories
    for dir_name in ['core', 'agents', 'commands', 'modes', 'hooks']:
        dir_path = CLAUDE_DIR / dir_name
        try:
            if dir_path.exists() and not list(dir_path.iterdir()):
                dir_path.rmdir()
        except Exception:
            pass

    return removed_count, total_count


# ============================================================================
# CLI COMMANDS
# ============================================================================

def cmd_install(args):
    """Install Shannon V3"""
    print_header(f"Shannon Framework V{SHANNON_VERSION} Installation")

    # Check prerequisites
    print_info("Checking prerequisites...")
    ok, errors = check_prerequisites()
    if not ok:
        print_error("Prerequisites not met:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print_success("Prerequisites OK")

    # Copy markdown files
    print_info("Copying markdown files...")
    success, total = copy_markdown_files()
    if success == total:
        print_success(f"Copied {success}/{total} markdown files")
    else:
        print_warning(f"Copied {success}/{total} markdown files (some failures)")

    # Install hook
    print_info("Installing PreCompact hook...")
    if install_precompact_hook():
        print_success("PreCompact hook installed and registered")
    else:
        print_error("Hook installation failed")
        return 1

    # Check Serena MCP
    print_info("Checking for Serena MCP...")
    if verify_serena_mcp():
        print_success("Serena MCP detected")
    else:
        print_warning("Serena MCP not found (optional but recommended)")

    # Verify installation
    print_info("Verifying installation...")
    all_ok, checks = verify_installation()

    if all_ok:
        print_success("Installation complete!")
        print_info("\nNext steps:")
        print("  1. Restart Claude Code")
        print("  2. Try: /sh:status to check Shannon status")
        print("  3. Try: /sc:help to see available commands")
        return 0
    else:
        print_error("Installation verification failed")
        return 1


def cmd_uninstall(args):
    """Uninstall Shannon V3"""
    print_header(f"Shannon Framework V{SHANNON_VERSION} Uninstallation")

    # Confirm
    if not args.force:
        response = input("Are you sure you want to uninstall Shannon V3? (y/N): ")
        if response.lower() != 'y':
            print_info("Uninstall cancelled")
            return 0

    print_info("Removing Shannon files...")
    removed, total = uninstall_shannon()
    print_success(f"Removed {removed}/{total} files")

    print_success("Uninstallation complete")
    print_info("Restart Claude Code to complete removal")
    return 0


def cmd_verify(args):
    """Verify Shannon installation"""
    print_header(f"Shannon Framework V{SHANNON_VERSION} Verification")

    all_ok, checks = verify_installation()

    print_info("Installation checks:")
    print(f"  Markdown files: {'✓' if checks['markdown_files'] else '✗'}")
    print(f"  Hook installed: {'✓' if checks['hook_installed'] else '✗'}")
    print(f"  Hook registered: {'✓' if checks['hook_registered'] else '✗'}")
    print(f"  Serena MCP: {'✓' if checks['serena_mcp'] else '⚠ (optional)'}")

    if all_ok:
        print_success("\nShannon V3 is properly installed")
        return 0
    else:
        print_error("\nShannon V3 installation has issues")
        print_info("Run 'python3 install.py install' to fix")
        return 1


def cmd_status(args):
    """Show installation status"""
    print_header(f"Shannon Framework V{SHANNON_VERSION} Status")

    all_ok, checks = verify_installation()

    if all_ok:
        print_success("Status: INSTALLED")
    else:
        print_warning("Status: INCOMPLETE or NOT INSTALLED")

    print(f"\nInstallation directory: {CLAUDE_DIR}")
    print(f"Markdown files: {sum(1 for _, p in FILE_MAPPINGS.items() if (CLAUDE_DIR / p).exists())}/{len(FILE_MAPPINGS)}")
    print(f"Hook status: {'Installed & Registered' if checks['hook_installed'] and checks['hook_registered'] else 'Not installed'}")
    print(f"Serena MCP: {'Available' if checks['serena_mcp'] else 'Not available (optional)'}")

    return 0


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Shannon Framework V3 Installer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 install.py install          Install Shannon V3
  python3 install.py uninstall        Remove Shannon V3
  python3 install.py verify           Verify installation
  python3 install.py status           Show status
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Install command
    parser_install = subparsers.add_parser('install', help='Install Shannon V3')
    parser_install.set_defaults(func=cmd_install)

    # Uninstall command
    parser_uninstall = subparsers.add_parser('uninstall', help='Uninstall Shannon V3')
    parser_uninstall.add_argument('--force', action='store_true', help='Skip confirmation')
    parser_uninstall.set_defaults(func=cmd_uninstall)

    # Verify command
    parser_verify = subparsers.add_parser('verify', help='Verify installation')
    parser_verify.set_defaults(func=cmd_verify)

    # Status command
    parser_status = subparsers.add_parser('status', help='Show installation status')
    parser_status.set_defaults(func=cmd_status)

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Execute command
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())