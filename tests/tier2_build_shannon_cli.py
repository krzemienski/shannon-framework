#!/usr/bin/env python3
"""
Shannon v5.0 - Tier 2: Build Shannon CLI (Meta-Circular)

Builds Shannon CLI tool - meta-circular test where Shannon builds itself.

Specification: docs/ref/shannon-cli-spec.md (153KB)
Expected: Python CLI tool (Python + Claude SDK + Click + Rich)

Cost: ~$50-60
Duration: 90-120 minutes
Exit: 0 (success) or 1 (failure)

Note: This is philosophically interesting - Shannon analyzing and building Shannon.
"""

import sys
import asyncio
import time
from pathlib import Path

try:
    from claude_agent_sdk import (
        query,
        ClaudeAgentOptions,
        AssistantMessage,
        SystemMessage,
        ResultMessage,
        TextBlock,
        ToolUseBlock
    )
except ImportError:
    print("❌ ERROR: claude-agent-sdk not installed")
    print("   Run: pip install -r tests/requirements.txt")
    sys.exit(1)


BUILD_CONFIG = {
    'name': 'Shannon CLI (Meta-Circular)',
    'spec_file': 'docs/ref/shannon-cli-spec.md',
    'output_dir': 'test-builds/shannon-cli',
    'expected_files': [
        'pyproject.toml',
        'README.md',
        'src/shannon_cli/__init__.py',
        'src/shannon_cli/main.py',
        'src/shannon_cli/commands/__init__.py',
        'src/shannon_cli/commands/spec.py',
        'src/shannon_cli/commands/wave.py',
        'src/shannon_cli/core/analyzer.py',
        'tests/test_analyzer.py',
    ],
    'verification_skill': '.claude/skills/shannon-execution-verifier',
}


async def build_application(spec_text: str, output_dir: Path) -> tuple[bool, str]:
    """Execute Shannon /shannon:wave to build Shannon CLI"""
    print(f"Building Shannon CLI with Shannon (meta-circular)...")
    print(f"Output directory: {output_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    plugin_path = Path(".")
    if not plugin_path.exists():
        return False, f"Shannon plugin not found: {plugin_path.absolute()}"

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": str(plugin_path)}],
        model="claude-sonnet-4-5"
    )

    prompt = f'''Build the complete Shannon CLI tool from this specification.

Work in: {output_dir.absolute()}

Specification:
{spec_text}

Execute /shannon:wave to build everything.

Note: This is meta-circular - you're building a Shannon CLI tool that implements
the same 8D complexity analysis algorithm you're using right now.
'''

    print(f"\nExecuting /shannon:wave (this will take 90-120 minutes)...")
    print("Progress:")

    start_time = time.time()
    messages = []
    tool_count = 0
    last_update = start_time

    try:
        async for msg in query(prompt=prompt, options=options):
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        messages.append(block.text)
                    elif isinstance(block, ToolUseBlock):
                        tool_count += 1

                now = time.time()
                if now - last_update >= 30:
                    elapsed_min = (now - start_time) / 60
                    print(f"  [{elapsed_min:.1f} min] Building... ({tool_count} tools)")
                    last_update = now

            elif isinstance(msg, SystemMessage):
                if msg.subtype == 'init':
                    print("  ✓ Session initialized", flush=True)

            elif isinstance(msg, ResultMessage):
                cost = msg.total_cost_usd or 0.0
                print(f"  ✓ Cost: ${cost:.4f}", flush=True)

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

    prompt = f'''Verify this built Shannon CLI tool meets the specification requirements.

Application directory: {output_dir.absolute()}

Original specification:
{spec_text}

{skill_content}

Focus on:
- Python package structure (pyproject.toml)
- CLI commands (spec, wave, checkpoint, etc.)
- Core 8D complexity analyzer implementation
- Testing infrastructure
- Documentation completeness
- Installability (pip install -e .)

Meta-circular verification: This CLI should implement the same 8D algorithm
that was used to build it. Check for algorithm correctness.

Run complete verification and report results.
'''

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "."}],
        model="claude-sonnet-4-5"
    )

    messages = []
    try:
        async for msg in query(prompt=prompt, options=options):
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        messages.append(block.text)
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
    print(f"\nExpected cost: ~$50-60")
    print(f"Expected time: 90-120 minutes")
    print("\nMeta-circular note: Shannon building Shannon CLI")
    print("This tests Shannon's ability to handle self-referential specifications.")
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
    print("TIER 2 BUILD SUMMARY (Meta-Circular)")
    print('='*80)
    print(f"Application: {BUILD_CONFIG['name']}")
    print(f"Duration: {total_elapsed:.1f}s ({total_elapsed/60:.1f} min)")
    print(f"Output: {output_dir.absolute()}")

    if success:
        print(f"\n✅ BUILD VERIFICATION PASSED")
        print(f"   Shannon successfully built Shannon CLI")
        print(f"   Meta-circular test successful")
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
