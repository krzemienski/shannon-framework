#!/usr/bin/env python3
"""
Shannon v5.0 - Tier 2: Build Claude Code Expo Mobile App

Builds complete Claude Code Expo mobile application and verifies.

Specification: docs/ref/claude-code-expo-spec.md (81KB)
Expected: React Native + Express + WebSocket

Cost: ~$35-40
Duration: 60-75 minutes
Exit: 0 (success) or 1 (failure)
"""

import sys
import asyncio
import time
from pathlib import Path

try:
    from claude_agent_sdk import query, ClaudeAgentOptions
except ImportError:
    print("❌ ERROR: claude-agent-sdk not installed")
    print("   Run: pip install -r tests/requirements.txt")
    sys.exit(1)


BUILD_CONFIG = {
    'name': 'Claude Code Expo',
    'spec_file': 'docs/ref/claude-code-expo-spec.md',
    'output_dir': 'test-builds/claude-code-expo',
    'expected_files': [
        'package.json',
        'app.json',
        'README.md',
        'App.tsx',
        'src/screens/HomeScreen.tsx',
        'src/components/ChatInterface.tsx',
        'server/index.js',
        'server/package.json',
    ],
    'verification_skill': '.claude/skills/shannon-execution-verifier',
}


async def build_application(spec_text: str, output_dir: Path) -> tuple[bool, str]:
    """Execute Shannon /shannon:wave to build complete application"""
    print(f"Building mobile application with Shannon...")
    print(f"Output directory: {output_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    plugin_path = Path(".")
    if not plugin_path.exists():
        return False, f"Shannon plugin not found: {plugin_path.absolute()}"

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": str(plugin_path)}],
        model="claude-sonnet-4-5"
    )

    prompt = f'''Build the complete mobile application from this specification.

Work in: {output_dir.absolute()}

Specification:
{spec_text}

Execute /shannon:wave to build everything including mobile app and backend.
'''

    print(f"\nExecuting /shannon:wave (this will take 60-75 minutes)...")
    print("Progress:")

    start_time = time.time()
    messages = []
    tool_count = 0
    last_update = start_time

    try:
        async for msg in query(prompt=prompt, options=options):
            if msg.type == 'assistant':
                messages.append(msg.content)
                now = time.time()
                if now - last_update >= 30:
                    elapsed_min = (now - start_time) / 60
                    print(f"  [{elapsed_min:.1f} min] Building... ({tool_count} tools)")
                    last_update = now
            elif msg.type == 'tool_call':
                tool_count += 1
    except Exception as e:
        return False, f"Build execution failed: {e}"

    elapsed = time.time() - start_time
    print(f"\n✅ Build completed in {elapsed:.1f}s ({elapsed/60:.1f} min)")
    print(f"   Tools used: {tool_count}")

    return True, ''.join(messages)


def verify_file_structure(output_dir: Path, expected_files: list) -> tuple[bool, list]:
    """Verify expected files exist"""
    print(f"\nVerifying file structure...")

    missing = []
    for file_path in expected_files:
        full_path = output_dir / file_path
        if not full_path.exists():
            missing.append(file_path)

    if not missing:
        print(f"  ✅ All {len(expected_files)} expected files exist")
        return True, []
    else:
        print(f"  ❌ Missing {len(missing)} files:")
        for f in missing:
            print(f"     - {f}")
        return False, missing


async def run_verification_skill(output_dir: Path, spec_text: str, skill_path: Path) -> tuple[bool, str]:
    """Execute shannon-execution-verifier skill"""
    print(f"\nRunning shannon-execution-verifier skill...")

    if not skill_path.exists():
        return False, f"Verification skill not found: {skill_path}"

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, f"Skill SKILL.md not found: {skill_md}"

    skill_content = skill_md.read_text()

    prompt = f'''Verify this built mobile application meets the specification requirements.

Application directory: {output_dir.absolute()}

Original specification:
{spec_text}

{skill_content}

Focus on:
- React Native mobile app structure
- Backend server setup
- WebSocket functionality
- Component architecture

Run complete verification and report results.
'''

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "."}],
        model="claude-sonnet-4-5"
    )

    messages = []
    try:
        async for msg in query(prompt=prompt, options=options):
            if msg.type == 'assistant':
                messages.append(msg.content)
                print(".", end="", flush=True)
    except Exception as e:
        return False, f"Verification failed: {e}"

    print()

    report = ''.join(messages)
    passed = any(indicator in report for indicator in ["✅", "PASSED", "All checks passed", "Verification successful"])

    return passed, report


async def main():
    """Run complete Tier 2 build and verification"""

    print("="*80)
    print("SHANNON v5.0 - TIER 2 BUILD VERIFICATION")
    print(f"Application: {BUILD_CONFIG['name']}")
    print("="*80)

    print(f"\nSpecification: {BUILD_CONFIG['spec_file']}")
    print(f"Output: {BUILD_CONFIG['output_dir']}")
    print(f"\nExpected cost: ~$35-40")
    print(f"Expected time: 60-75 minutes")
    print("\nStarting build...")

    overall_start = time.time()

    # Load specification
    spec_path = Path(BUILD_CONFIG['spec_file'])
    if not spec_path.exists():
        print(f"❌ ERROR: Spec file not found: {spec_path}")
        return 1

    spec_text = spec_path.read_text()
    print(f"\nLoaded specification: {len(spec_text)/1024:.1f} KB")

    # Build application
    output_dir = Path(BUILD_CONFIG['output_dir'])
    success, build_output = await build_application(spec_text, output_dir)

    if not success:
        print(f"\n❌ BUILD FAILED: {build_output}")
        return 1

    # Verify file structure
    success, missing_files = verify_file_structure(output_dir, BUILD_CONFIG['expected_files'])

    if not success:
        print(f"\n❌ FILE STRUCTURE VERIFICATION FAILED")
        return 1

    # Run comprehensive verification
    skill_path = Path(BUILD_CONFIG['verification_skill'])
    success, verification_report = await run_verification_skill(output_dir, spec_text, skill_path)

    # Save report
    report_path = output_dir / "verification_report.txt"
    report_path.write_text(verification_report)
    print(f"\nVerification report saved: {report_path}")

    # Final result
    total_elapsed = time.time() - overall_start

    print(f"\n{'='*80}")
    print("TIER 2 BUILD SUMMARY")
    print('='*80)
    print(f"Application: {BUILD_CONFIG['name']}")
    print(f"Duration: {total_elapsed:.1f}s ({total_elapsed/60:.1f} min)")
    print(f"Output: {output_dir.absolute()}")

    if success:
        print(f"\n✅ BUILD VERIFICATION PASSED")
        return 0
    else:
        print(f"\n❌ BUILD VERIFICATION FAILED")
        print(f"   See report: {report_path}")
        return 1


if __name__ == '__main__':
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Build interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
