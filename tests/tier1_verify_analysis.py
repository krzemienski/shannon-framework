#!/usr/bin/env python3
"""
Shannon v5.0 - Tier 1 Verification: Analysis Only

Tests /sh_spec on all 4 specifications without building.
Validates 8D complexity analysis, domain normalization, tech detection.

Usage: python tests/tier1_verify_analysis.py

Cost: ~$2-3
Duration: 5-10 minutes
Exit: 0 (all pass) or 1 (any fail)
"""

import os
import sys
import asyncio
import re
import time
from pathlib import Path
from typing import Dict, List, Tuple

# CRITICAL: Set API key BEFORE importing SDK
os.environ['ANTHROPIC_API_KEY'] = "REMOVED_SECRET"

# Import SDK types (AFTER setting API key)
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


# Test specifications with expected results
TEST_SPECS = [
    {
        'name': 'PRD Creator',
        'file': 'docs/ref/prd-creator-spec.md',
        'complexity_min': 0.40,
        'complexity_max': 0.50,
        'interpretation': 'MODERATE',
        'required_patterns': ['8D', 'Domain', 'Frontend', 'Backend', 'React', 'FastAPI'],
        'min_domains': 3,
    },
    {
        'name': 'Claude Code Expo',
        'file': 'docs/ref/claude-code-expo-spec.md',
        'complexity_min': 0.65,
        'complexity_max': 0.72,
        'interpretation': 'COMPLEX',
        'required_patterns': ['Mobile', 'React Native', 'WebSocket', 'Express'],
        'min_domains': 4,
    },
    {
        'name': 'Repo Nexus',
        'file': 'docs/ref/repo-nexus-spec.md',
        'complexity_min': 0.68,
        'complexity_max': 0.75,
        'interpretation': 'COMPLEX',
        'required_patterns': ['Mobile', 'FastAPI', 'PostgreSQL', 'Redis'],
        'min_domains': 4,
    },
    {
        'name': 'Shannon CLI',
        'file': 'docs/ref/shannon-cli-spec.md',
        'complexity_min': 0.72,
        'complexity_max': 0.78,
        'interpretation': 'HIGH',
        'required_patterns': ['Python', 'SDK', 'wave-based', 'CLI'],
        'min_domains': 3,
    }
]


def extract_complexity(output: str) -> float:
    """Extract complexity score from Shannon output"""
    patterns = [
        r'Complexity[:\s]+([0-9]\.[0-9]{2})',
        r'complexity[_\s]+score[:\s]+([0-9]\.[0-9]{2})',
        r'([0-9]\.[0-9]{2})\s*/\s*1\.00',
        r'Score[:\s]+([0-9]\.[0-9]{2})',
    ]

    for pattern in patterns:
        match = re.search(pattern, output, re.IGNORECASE)
        if match:
            return float(match.group(1))

    return None


def extract_domains(output: str) -> Dict[str, int]:
    """Extract domain percentages from Shannon output"""
    # Pattern: "Domain Name: 35%" or "Domain Name  35%"
    domain_pattern = r'([A-Z][a-zA-Z\s]+?):\s*(\d+)%'
    matches = re.findall(domain_pattern, output)

    domains = {}
    for domain_name, percentage in matches:
        domain_name = domain_name.strip()
        # Filter out obvious non-domains
        if len(domain_name) > 3 and 'Phase' not in domain_name:
            domains[domain_name] = int(percentage)

    return domains


def validate_complexity(output: str, min_val: float, max_val: float, name: str) -> Tuple[bool, str]:
    """Validate complexity score is in expected range"""
    complexity = extract_complexity(output)

    if complexity is None:
        return False, f"Could not extract complexity from output"

    if min_val <= complexity <= max_val:
        return True, f"{complexity:.2f} ✓"
    else:
        return False, f"{complexity:.2f} (expected {min_val:.2f}-{max_val:.2f})"


def validate_domains(output: str, min_count: int) -> Tuple[bool, str]:
    """Validate domains sum to 100% and minimum count exists"""
    domains = extract_domains(output)

    if not domains:
        return False, "No domains found in output"

    if len(domains) < min_count:
        return False, f"Only {len(domains)} domains (expected ≥{min_count})"

    total = sum(domains.values())

    if total == 100:
        domain_str = ", ".join(f"{k}:{v}%" for k, v in sorted(domains.items(), key=lambda x: -x[1]))
        return True, f"100% ({len(domains)} domains: {domain_str})"
    else:
        return False, f"Sum={total}% (expected 100%)"


def validate_patterns(output: str, patterns: List[str]) -> Tuple[bool, str]:
    """Validate required patterns appear in output"""
    missing = []
    for pattern in patterns:
        if pattern.lower() not in output.lower():
            missing.append(pattern)

    if not missing:
        return True, f"All {len(patterns)} patterns found"
    else:
        return False, f"Missing: {', '.join(missing)}"


async def test_spec_analysis(spec_config: dict) -> bool:
    """Test Shannon analysis on single specification"""

    print(f"\n{'='*80}")
    print(f"Testing: {spec_config['name']}")
    print(f"File:    {spec_config['file']}")
    print('='*80)

    # Check spec file exists
    spec_path = Path(spec_config['file'])
    if not spec_path.exists():
        print(f"❌ ERROR: Spec file not found: {spec_path}")
        return False

    # Read specification
    spec_text = spec_path.read_text()
    file_size_kb = len(spec_text) / 1024
    print(f"Size:    {file_size_kb:.1f} KB")

    # Load Shannon plugin
    plugin_path = Path("shannon-plugin")
    if not plugin_path.exists():
        print(f"❌ ERROR: Shannon plugin not found: {plugin_path.absolute()}")
        return False

    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": str(plugin_path)}],
        setting_sources=["user", "project"],  # REQUIRED for plugins to load!
        model="claude-sonnet-4-5",
        permission_mode="bypassPermissions",
        allowed_tools=[
            "Skill", "Read", "Grep", "Glob", "TodoWrite",
            # Allow ALL Serena tools (spec-analysis needs memory access)
            "mcp__serena__write_memory", "mcp__serena__read_memory",
            "mcp__serena__list_memories", "mcp__serena__get_current_config",
            # Allow sequential thinking
            "mcp__sequential-thinking__sequentialthinking"
        ]
    )

    # Execute /shannon-plugin:sh_spec (namespaced command)
    print(f"\nExecuting /shannon-plugin:sh_spec...")

    start_time = time.time()
    messages = []
    tool_count = 0
    session_id = None
    cost = 0.0

    try:
        async for message in query(prompt=f'/shannon-plugin:sh_spec "{spec_text}"', options=options):
            # AssistantMessage - Claude's responses with content blocks
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        messages.append(block.text)
                        print(".", end="", flush=True)
                    elif isinstance(block, ToolUseBlock):
                        tool_count += 1

            # SystemMessage - Session events (init, completion)
            elif isinstance(message, SystemMessage):
                if message.subtype == 'init':
                    print("\n✅ Session initialized", end="", flush=True)

            # ResultMessage - Final result with cost and duration
            elif isinstance(message, ResultMessage):
                session_id = message.session_id
                cost = message.total_cost_usd or 0.0

    except Exception as e:
        print(f"\n❌ ERROR during execution: {e}")
        import traceback
        traceback.print_exc()
        return False

    elapsed = time.time() - start_time
    print(f"\n✅ Completed: {tool_count} tools, {elapsed:.1f}s, ${cost:.4f}")

    if not messages:
        print("❌ ERROR: No output received from Shannon")
        return False

    output = ''.join(messages)

    # Validation checks
    print(f"\nValidation:")

    checks_passed = 0
    checks_total = 3

    # Check 1: Complexity in range
    check_name = "Complexity"
    passed, detail = validate_complexity(
        output,
        spec_config['complexity_min'],
        spec_config['complexity_max'],
        spec_config['name']
    )
    status = "✅" if passed else "❌"
    print(f"  {status} {check_name}: {detail}")
    if passed:
        checks_passed += 1

    # Check 2: Domains sum to 100%
    check_name = "Domains"
    passed, detail = validate_domains(output, spec_config['min_domains'])
    status = "✅" if passed else "❌"
    print(f"  {status} {check_name}: {detail}")
    if passed:
        checks_passed += 1

    # Check 3: Required patterns present
    check_name = "Patterns"
    passed, detail = validate_patterns(output, spec_config['required_patterns'])
    status = "✅" if passed else "❌"
    print(f"  {status} {check_name}: {detail}")
    if passed:
        checks_passed += 1

    # Result
    test_passed = checks_passed == checks_total
    result_status = "✅ PASSED" if test_passed else "❌ FAILED"

    print(f"\n{result_status}: {checks_passed}/{checks_total} checks passed")

    return test_passed


async def main():
    """Run Tier 1 verification on all 4 specifications"""

    print("="*80)
    print("SHANNON v5.0 - TIER 1 VERIFICATION")
    print("Specification Analysis (No Building)")
    print("="*80)

    print("\nTesting Shannon's /sh_spec command on 4 real specifications:")
    print("1. PRD Creator (18KB)")
    print("2. Claude Code Expo (81KB)")
    print("3. Repo Nexus (87KB)")
    print("4. Shannon CLI (153KB)")

    print(f"\nExpected cost: ~$2-3")
    print(f"Expected time: 5-10 minutes")

    # Run tests
    start_time = time.time()
    results = []

    for spec_config in TEST_SPECS:
        passed = await test_spec_analysis(spec_config)
        results.append((spec_config['name'], passed))

    total_elapsed = time.time() - start_time

    # Summary
    print(f"\n{'='*80}")
    print("TIER 1 SUMMARY")
    print('='*80)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for spec_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}  {spec_name}")

    print(f"\nResult: {passed_count}/{total_count} specifications passed")
    print(f"Duration: {total_elapsed:.1f}s ({total_elapsed/60:.1f} min)")

    # Exit code
    all_passed = passed_count == total_count

    if all_passed:
        print("\n✅ ALL TIER 1 TESTS PASSED")
        print("   Shannon analysis is working correctly.")
        print("   Ready to run Tier 2 (full builds) if needed.")
        return 0
    else:
        print(f"\n❌ {total_count - passed_count} TESTS FAILED")
        print("   Fix Shannon plugin before running Tier 2.")
        return 1


if __name__ == '__main__':
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
