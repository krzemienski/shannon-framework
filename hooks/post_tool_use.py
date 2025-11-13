#!/usr/bin/env -S python3
"""
Shannon PostToolUse Hook - NO MOCKS Testing Philosophy Enforcement

Purpose: Automatically detects and blocks mock usage in test files, enforcing
         Shannon's NO MOCKS philosophy in real-time.

How It Works:
1. Hook fires after any Write/Edit/MultiEdit tool use
2. Checks if file is a test file
3. Scans content for mock patterns (jest.mock, unittest.mock, etc.)
4. If mocks detected, blocks with clear guidance
5. Provides functional test alternatives

Benefits: Real-time enforcement of NO MOCKS philosophy, catches violations immediately

Author: Shannon Framework
Version: 3.0.1
License: MIT
Copyright (c) 2024 Shannon Framework Team
"""

import json
import sys
import re


# Mock patterns to detect and block
MOCK_PATTERNS = [
    (r'jest\.mock\(', 'jest.mock()'),
    (r'jest\.spyOn', 'jest.spyOn()'),
    (r'unittest\.mock', 'unittest.mock'),
    (r'from\s+unittest\.mock\s+import', 'unittest.mock imports'),
    (r'@[Mm]ock\b', '@Mock annotation'),
    (r'@[Pp]atch\b', '@patch decorator'),
    (r'sinon\.(stub|mock|fake|spy)', 'sinon mocking'),
    (r'mockImplementation', 'mockImplementation'),
    (r'mockReturnValue', 'mockReturnValue'),
    (r'createMock[^a-z]', 'createMock'),
    (r'MockedFunction', 'MockedFunction type'),
    (r'vi\.mock\(', 'vitest mock'),
    (r'TestDouble', 'TestDouble'),
]


def detect_mocks(content: str) -> list:
    """
    Detect mock usage patterns in content

    Args:
        content: File content to scan

    Returns:
        List of detected mock pattern names
    """
    violations = []
    for pattern, name in MOCK_PATTERNS:
        if re.search(pattern, content, re.MULTILINE):
            violations.append(name)
    return violations


def is_test_file(file_path: str) -> bool:
    """
    Check if file is a test file

    Args:
        file_path: Path to check

    Returns:
        True if file is a test file
    """
    test_indicators = [
        '/test/', '/__tests__/', '/tests/',
        '.test.', '.spec.',
        '_test.', '_spec.',
        'test_', 'spec_'
    ]

    return any(indicator in file_path for indicator in test_indicators)


def main():
    """
    Main execution for PostToolUse hook

    Detects and blocks mock usage in test files.
    """
    try:
        # Read hook input
        input_data = json.loads(sys.stdin.read())

        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})

        # Only check Write/Edit operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)

        # Get file path
        file_path = tool_input.get('file_path', '')
        if not file_path:
            sys.exit(0)

        # Only check test files
        if not is_test_file(file_path):
            sys.exit(0)

        # Get file content
        content = tool_input.get('content', '') or tool_input.get('new_string', '')
        if not content:
            sys.exit(0)

        # Check for mock patterns
        violations = detect_mocks(content)

        if violations:
            # Block with clear explanation
            output = {
                "decision": "block",
                "reason": f"""🚨 **Shannon NO MOCKS Violation Detected**

**File**: {file_path}
**Violations**: {', '.join(violations)}

**Shannon Testing Philosophy**: Tests must validate REAL system behavior with real components, not mocked responses.

**Why NO MOCKS**:
- Mock-based tests create false confidence
- Production bugs aren't caught by mocked tests
- Integration issues missed
- Refactoring breaks hidden by mocks

**Required Actions**:
1. Remove all mock usage from {file_path}
2. Implement functional test using:
   - **Web/Frontend**: Puppeteer MCP for real browser testing
   - **Backend/API**: Real HTTP requests to actual server
   - **Database**: Real database instance (Docker test DB)
   - **Mobile**: iOS Simulator or Android Emulator

**Quick Start**:
- Run `/shannon:check_mcps` to ensure Puppeteer MCP is configured
- See TEST_GUARDIAN agent for functional test patterns
- Reference: shannon-plugin/core/TESTING_PHILOSOPHY.md

**Need Help**: Ask CONTEXT_GUARDIAN or TEST_GUARDIAN agent for functional test examples."""
            }

            print(json.dumps(output))
            sys.exit(0)

    except Exception as e:
        # Don't block on errors
        print(f"[Shannon PostToolUse] Warning: {e}", file=sys.stderr)
        pass

    # Allow if no violations or error
    sys.exit(0)


if __name__ == "__main__":
    main()
