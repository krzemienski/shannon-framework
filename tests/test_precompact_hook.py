#!/usr/bin/env python3
"""
Test Shannon PreCompact Hook

Comprehensive test suite for validating PreCompact hook functionality:
1. Hook file exists and is executable
2. Hook returns valid JSON
3. Hook executes within timeout
4. Hook output has required fields
5. Hook handles errors gracefully
6. Hook properly formats checkpoint instructions

Author: Shannon Framework
Version: 1.0.0
License: MIT
"""

import json
import subprocess
import sys
import unittest
import time
from pathlib import Path


class TestPreCompactHook(unittest.TestCase):
    """Comprehensive PreCompact Hook Test Suite"""

    @classmethod
    def setUpClass(cls):
        """Setup test environment once for all tests"""
        cls.hook_path = Path.home() / ".claude" / "hooks" / "precompact.py"
        cls.timeout = 5  # 5 second timeout as per spec

    def test_01_hook_exists(self):
        """Test 1: Hook file should exist at expected location"""
        self.assertTrue(
            self.hook_path.exists(),
            f"Hook file not found at {self.hook_path}"
        )
        print(f"✓ Hook exists at: {self.hook_path}")

    def test_02_hook_executable(self):
        """Test 2: Hook file should be executable"""
        self.assertTrue(self.hook_path.is_file(), "Hook is not a file")

        import os
        self.assertTrue(
            os.access(self.hook_path, os.X_OK),
            f"Hook file is not executable. Run: chmod +x {self.hook_path}"
        )
        print("✓ Hook is executable")

    def test_03_hook_returns_valid_json(self):
        """Test 3: Hook should return valid JSON on stdout"""
        result = subprocess.run(
            [str(self.hook_path)],
            input='{}',
            capture_output=True,
            text=True,
            timeout=self.timeout
        )

        self.assertEqual(result.returncode, 0, f"Hook failed with: {result.stderr}")

        # Parse JSON output
        try:
            output = json.loads(result.stdout)
            self.assertIsInstance(output, dict, "Output should be JSON object")
            print("✓ Hook returns valid JSON")
        except json.JSONDecodeError as e:
            self.fail(f"Hook output is not valid JSON: {e}\nOutput: {result.stdout}")

    def test_04_hook_has_required_fields(self):
        """Test 4: Hook output should have hookSpecificOutput with correct structure"""
        result = subprocess.run(
            [str(self.hook_path)],
            input=json.dumps({"test": True}),
            capture_output=True,
            text=True,
            timeout=self.timeout
        )

        output = json.loads(result.stdout)

        # Check hookSpecificOutput exists
        self.assertIn('hookSpecificOutput', output, "Missing hookSpecificOutput field")

        hook_output = output['hookSpecificOutput']

        # Check required fields
        self.assertIn('hookEventName', hook_output, "Missing hookEventName")
        self.assertEqual(
            hook_output['hookEventName'],
            'PreCompact',
            f"Wrong hook event name: {hook_output.get('hookEventName')}"
        )

        # Check for checkpoint key
        self.assertIn('checkpointKey', hook_output, "Missing checkpointKey")

        # Check for additionalContext (checkpoint instructions)
        self.assertIn('additionalContext', hook_output, "Missing additionalContext")
        self.assertTrue(
            len(hook_output['additionalContext']) > 0,
            "additionalContext should not be empty"
        )

        print(f"✓ Hook output has all required fields")
        print(f"  - Event: {hook_output['hookEventName']}")
        print(f"  - Checkpoint: {hook_output['checkpointKey']}")

    def test_05_hook_timeout_compliance(self):
        """Test 5: Hook should complete within configured timeout (5 seconds)"""
        start = time.time()

        result = subprocess.run(
            [str(self.hook_path)],
            input='{}',
            capture_output=True,
            text=True,
            timeout=self.timeout
        )

        elapsed = time.time() - start

        self.assertEqual(result.returncode, 0, "Hook should succeed")
        self.assertLess(
            elapsed,
            self.timeout,
            f"Hook took {elapsed:.2f}s (should be <{self.timeout}s)"
        )

        print(f"✓ Hook completed in {elapsed:.3f}s (within {self.timeout}s limit)")

    def test_06_hook_error_handling(self):
        """Test 6: Hook should handle invalid input gracefully"""
        # Test with invalid JSON
        result = subprocess.run(
            [str(self.hook_path)],
            input='invalid json data',
            capture_output=True,
            text=True,
            timeout=self.timeout
        )

        # Should still exit 0 (graceful degradation)
        self.assertEqual(result.returncode, 0, "Hook should not crash on invalid input")

        # Should return valid JSON even on error
        try:
            output = json.loads(result.stdout)
            self.assertIn('hookSpecificOutput', output)

            # Should indicate error
            self.assertTrue(
                output['hookSpecificOutput'].get('error', False),
                "Hook should set error: true for invalid input"
            )

            print("✓ Hook handles errors gracefully")
            print(f"  - Error message: {output['hookSpecificOutput'].get('errorMessage', 'N/A')}")
        except json.JSONDecodeError:
            self.fail("Hook should return valid JSON even on error")

    def test_07_checkpoint_instructions_format(self):
        """Test 7: Checkpoint instructions should follow Shannon format"""
        result = subprocess.run(
            [str(self.hook_path)],
            input=json.dumps({"transcript": "test session data"}),
            capture_output=True,
            text=True,
            timeout=self.timeout
        )

        output = json.loads(result.stdout)
        instructions = output['hookSpecificOutput']['additionalContext']

        # Verify instructions contain key elements
        self.assertIn('CONTEXT_GUARDIAN', instructions, "Should mention CONTEXT_GUARDIAN")
        self.assertIn('write_memory', instructions, "Should include write_memory instructions")
        self.assertIn('checkpoint', instructions.lower(), "Should mention checkpoint")

        # Verify checkpoint key is included in instructions
        checkpoint_key = output['hookSpecificOutput']['checkpointKey']
        self.assertIn(checkpoint_key, instructions, "Checkpoint key should be in instructions")

        print("✓ Checkpoint instructions are properly formatted")

    def test_08_hook_version_info(self):
        """Test 8: Hook should include version information"""
        result = subprocess.run(
            [str(self.hook_path)],
            input='{}',
            capture_output=True,
            text=True,
            timeout=self.timeout
        )

        output = json.loads(result.stdout)
        hook_output = output['hookSpecificOutput']

        self.assertIn('version', hook_output, "Hook should include version")
        print(f"✓ Hook version: {hook_output['version']}")

    def test_09_hook_timestamp_generation(self):
        """Test 9: Hook should generate unique timestamps for checkpoints"""
        # Run hook twice
        result1 = subprocess.run(
            [str(self.hook_path)],
            input='{}',
            capture_output=True,
            text=True,
            timeout=self.timeout
        )

        time.sleep(1)  # Wait 1 second

        result2 = subprocess.run(
            [str(self.hook_path)],
            input='{}',
            capture_output=True,
            text=True,
            timeout=self.timeout
        )

        output1 = json.loads(result1.stdout)
        output2 = json.loads(result2.stdout)

        key1 = output1['hookSpecificOutput']['checkpointKey']
        key2 = output2['hookSpecificOutput']['checkpointKey']

        self.assertNotEqual(key1, key2, "Checkpoint keys should be unique")
        print(f"✓ Generates unique checkpoint keys")
        print(f"  - First: {key1}")
        print(f"  - Second: {key2}")


class TestHookIntegration(unittest.TestCase):
    """Integration tests for hook with Claude Code settings"""

    def test_settings_json_format(self):
        """Test: settings.json should have correct hook format"""
        settings_path = Path.home() / ".claude" / "settings.json"

        if not settings_path.exists():
            self.skipTest("settings.json not found (run install first)")

        with open(settings_path, 'r') as f:
            settings = json.load(f)

        # Check hooks structure
        self.assertIn('hooks', settings, "settings.json should have hooks section")

        # Check PreCompact hook
        if 'PreCompact' in settings['hooks']:
            precompact = settings['hooks']['PreCompact']
            self.assertIsInstance(precompact, list, "PreCompact should be array")

            if len(precompact) > 0:
                # Find Shannon hook
                shannon_hooks = [
                    h for h in precompact
                    if isinstance(h, dict) and 'precompact.py' in h.get('command', '')
                ]

                if shannon_hooks:
                    hook = shannon_hooks[0]
                    self.assertEqual(hook.get('type'), 'command', "Hook type should be 'command'")
                    self.assertIn('command', hook, "Hook should have command field")
                    self.assertIn('timeout', hook, "Hook should have timeout field")

                    print("✓ Hook is properly registered in settings.json")
                    print(f"  - Type: {hook.get('type')}")
                    print(f"  - Command: {hook.get('command')}")
                    print(f"  - Timeout: {hook.get('timeout')}ms")
                else:
                    print("⚠ Shannon PreCompact hook not found in settings.json")
        else:
            print("⚠ PreCompact hooks not configured in settings.json")


def run_tests():
    """Run all tests with detailed output"""
    print("="*70)
    print("Shannon PreCompact Hook Test Suite")
    print("="*70)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPreCompactHook))
    suite.addTests(loader.loadTestsFromTestCase(TestHookIntegration))

    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("="*70)
    if result.wasSuccessful():
        print("✓ All tests passed!")
        print(f"  - Tests run: {result.testsRun}")
        print(f"  - Failures: 0")
        print(f"  - Errors: 0")
        return 0
    else:
        print("✗ Some tests failed")
        print(f"  - Tests run: {result.testsRun}")
        print(f"  - Failures: {len(result.failures)}")
        print(f"  - Errors: {len(result.errors)}")
        return 1


if __name__ == '__main__':
    sys.exit(run_tests())
