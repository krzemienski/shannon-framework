#!/usr/bin/env python3
"""
Shannon Framework SDK Test Script

Tests Shannon plugin via Claude Agents SDK (Python).
Loads plugin, executes /sh_spec command, validates output.

Requirements:
- Claude Agents SDK: pip install claude-agent-sdk
- ANTHROPIC_API_KEY environment variable set
- Shannon plugin at: ./shannon-plugin/

Usage:
    python test_shannon_sdk.py
"""

import sys
import time
import asyncio
import re
from pathlib import Path
from datetime import datetime

try:
    from claude_agent_sdk import query, ClaudeAgentOptions
except ImportError:
    print("❌ Claude Agents SDK not installed")
    print("   Install: pip install claude-agent-sdk")
    sys.exit(1)


# Test configuration
PLUGIN_PATH = "./shannon-plugin"
SPEC_FILE = "docs/ref/prd-creator-spec.md"


class ProgressMonitor:
    """Monitor and report progress from SDK messages"""

    def __init__(self):
        self.start_time = time.time()
        self.tool_count = 0
        self.message_count = 0
        self.current_activity = "Initializing..."
        self.tools_used = []

    def update(self, message):
        """Update from SDK message"""
        self.message_count += 1
        elapsed = time.time() - self.start_time

        if message.type == 'tool_call':
            self.tool_count += 1
            self.tools_used.append(message.tool_name)
            self.current_activity = f"Tool: {message.tool_name}"
            self.report_progress(elapsed)

        elif message.type == 'assistant' and message.content:
            # Update from assistant message
            preview = message.content[:60]
            if preview and preview != self.current_activity:
                self.current_activity = preview
                self.report_progress(elapsed)

    def report_progress(self, elapsed: float):
        """Print progress update"""
        print(f"[{elapsed:6.1f}s] {self.current_activity}")

    def summary(self):
        """Print final summary"""
        total_time = time.time() - self.start_time
        print("\n" + "=" * 80)
        print("EXECUTION SUMMARY")
        print("=" * 80)
        print(f"Duration: {total_time:.1f}s")
        print(f"Messages: {self.message_count}")
        print(f"Tools: {self.tool_count}")
        if self.tools_used:
            from collections import Counter
            tool_counts = Counter(self.tools_used)
            print("\nTool usage:")
            for tool, count in tool_counts.most_common():
                print(f"  {tool}: {count}x")


def extract_value(text: str, pattern: str) -> str:
    """Extract value using regex pattern"""
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def validate_shannon_output(output: str) -> dict:
    """
    Validate Shannon /sh_spec output structure and content

    Returns:
        dict with validation results
    """
    print("\n" + "=" * 80)
    print("VALIDATION")
    print("=" * 80)

    result = {
        'checks_passed': 0,
        'checks_total': 0,
        'success': False,
        'details': []
    }

    # Check 1: Contains "Shannon Specification Analysis" header
    result['checks_total'] += 1
    if "Shannon Specification Analysis" in output or "Specification Analysis" in output:
        print("✅ Check 1: Contains analysis header")
        result['checks_passed'] += 1
        result['details'].append("Header: PASS")
    else:
        print("❌ Check 1: Missing analysis header")
        result['details'].append("Header: FAIL")

    # Check 2: Contains complexity score
    result['checks_total'] += 1
    complexity = extract_value(output, r'Complexity[:\s]+([0-9.]+)')
    if complexity:
        complexity_val = float(complexity)
        if 0 <= complexity_val <= 100:
            print(f"✅ Check 2: Valid complexity score: {complexity_val}")
            result['checks_passed'] += 1
            result['details'].append(f"Complexity: {complexity_val} (PASS)")
        else:
            print(f"❌ Check 2: Complexity out of range: {complexity_val}")
            result['details'].append(f"Complexity: {complexity_val} (OUT OF RANGE)")
    else:
        print("❌ Check 2: No complexity score found")
        result['details'].append("Complexity: NOT FOUND")

    # Check 3: Contains 8D breakdown (at least 5 dimensions)
    result['checks_total'] += 1
    dimensions = [
        'Structural', 'Cognitive', 'Coordination', 'Temporal',
        'Technical', 'Scale', 'Uncertainty', 'Dependencies'
    ]
    found_dimensions = [d for d in dimensions if d in output]
    if len(found_dimensions) >= 5:
        print(f"✅ Check 3: Found {len(found_dimensions)}/8 dimensions")
        result['checks_passed'] += 1
        result['details'].append(f"Dimensions: {len(found_dimensions)}/8 (PASS)")
    else:
        print(f"❌ Check 3: Only found {len(found_dimensions)}/8 dimensions")
        result['details'].append(f"Dimensions: {len(found_dimensions)}/8 (FAIL)")

    # Check 4: Contains domain breakdown
    result['checks_total'] += 1
    if "Domain" in output and "%" in output:
        print("✅ Check 4: Contains domain breakdown")
        result['checks_passed'] += 1
        result['details'].append("Domains: PASS")
    else:
        print("❌ Check 4: Missing domain breakdown")
        result['details'].append("Domains: FAIL")

    # Check 5: Contains risk or timeline information
    result['checks_total'] += 1
    has_risk_info = any(term in output for term in [
        'Risk', 'Timeline', 'Team Size', 'Estimate'
    ])
    if has_risk_info:
        print("✅ Check 5: Contains risk/timeline information")
        result['checks_passed'] += 1
        result['details'].append("Risk/Timeline: PASS")
    else:
        print("❌ Check 5: Missing risk/timeline information")
        result['details'].append("Risk/Timeline: FAIL")

    # Check 6: Contains MCP recommendations (optional but preferred)
    result['checks_total'] += 1
    has_mcps = "MCP" in output and ("Required" in output or "Recommended" in output)
    if has_mcps:
        print("✅ Check 6: Contains MCP recommendations")
        result['checks_passed'] += 1
        result['details'].append("MCPs: PASS")
    else:
        print("⚠️  Check 6: No MCP recommendations (may be expected)")
        # Don't count as fail - this is optional
        result['checks_passed'] += 1
        result['details'].append("MCPs: SKIPPED (optional)")

    # Calculate success
    result['success'] = result['checks_passed'] >= (result['checks_total'] - 1)  # Allow 1 failure

    print("\n" + "-" * 80)
    print(f"Validation: {result['checks_passed']}/{result['checks_total']} checks passed")
    print(f"Result: {'✅ PASS' if result['success'] else '❌ FAIL'}")
    print("=" * 80)

    return result


async def test_shannon_plugin():
    """
    Main test function: Load Shannon plugin and execute /sh_spec command
    """
    print("=" * 80)
    print("SHANNON FRAMEWORK SDK TEST")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Plugin path: {PLUGIN_PATH}")
    print(f"Spec file: {SPEC_FILE}")
    print("=" * 80)

    # Verify plugin exists
    plugin_path = Path(PLUGIN_PATH)
    plugin_json = plugin_path / ".claude-plugin" / "plugin.json"

    if not plugin_json.exists():
        print(f"\n❌ Plugin not found at: {plugin_json}")
        print(f"   Current directory: {Path.cwd()}")
        return 1

    print(f"✅ Plugin found: {plugin_json}")

    # Load spec file
    spec_path = Path(SPEC_FILE)
    if not spec_path.exists():
        print(f"\n❌ Spec file not found: {spec_path}")
        return 1

    with open(spec_path, 'r') as f:
        spec_content = f.read()

    print(f"✅ Spec loaded: {len(spec_content)} characters")

    # Configure SDK options
    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": str(plugin_path.absolute())}],
        permission_mode="acceptEdits",  # Auto-approve file operations
        model="claude-sonnet-4-5",
    )

    print("\n" + "=" * 80)
    print("EXECUTING: /sh_spec")
    print("=" * 80)

    # Prepare command - use shortened spec for testing
    spec_excerpt = spec_content[:2000]  # First 2000 chars
    command = f'/sh_spec "{spec_excerpt}"'

    print(f"Command: {command[:100]}...")

    # Execute and monitor
    monitor = ProgressMonitor()
    messages = []

    try:
        async with asyncio.timeout(300):  # 5 minute timeout
            async for msg in query(prompt=command, options=options):
                monitor.update(msg)

                # Capture system init
                if msg.type == 'system' and msg.subtype == 'init':
                    print(f"\n📍 Session ID: {msg.session_id}")
                    print(f"📍 Model: {msg.model}")
                    if hasattr(msg, 'plugins') and msg.plugins:
                        print(f"📍 Plugins loaded: {len(msg.plugins)}")

                # Capture assistant responses
                if msg.type == 'assistant':
                    messages.append(msg.content)

                # Show errors
                if msg.type == 'error':
                    print(f"\n⚠️  Error: {msg.error.message}")

    except asyncio.TimeoutError:
        print("\n❌ Operation timed out after 5 minutes")
        monitor.summary()
        return 1

    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        monitor.summary()
        return 1

    # Show summary
    monitor.summary()

    # Combine output
    output = ''.join(messages)

    print("\n" + "=" * 80)
    print("OUTPUT PREVIEW (first 500 chars)")
    print("=" * 80)
    print(output[:500])
    print("...")
    print("=" * 80)

    # Validate output
    validation_result = validate_shannon_output(output)

    # Save full output
    output_file = Path("test_output_shannon_sdk.txt")
    with open(output_file, 'w') as f:
        f.write(f"Shannon Framework SDK Test Output\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"{'=' * 80}\n\n")
        f.write(output)

    print(f"\n📄 Full output saved to: {output_file.absolute()}")

    # Final result
    print("\n" + "=" * 80)
    print("FINAL RESULT")
    print("=" * 80)

    if validation_result['success']:
        print("✅ TEST PASSED")
        print("\nShannon plugin successfully:")
        print("  • Loaded via SDK")
        print("  • Executed /sh_spec command")
        print("  • Produced valid analysis output")
        return 0
    else:
        print("❌ TEST FAILED")
        print(f"\nValidation: {validation_result['checks_passed']}/{validation_result['checks_total']} checks passed")
        print("\nDetails:")
        for detail in validation_result['details']:
            print(f"  • {detail}")
        return 1


def main():
    """Entry point"""
    try:
        exit_code = asyncio.run(test_shannon_plugin())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
