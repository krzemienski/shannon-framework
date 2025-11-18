#!/usr/bin/env python3
"""Test runner for Shannon orchestration tests"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

if __name__ == "__main__":
    # Run tests with proper path
    sys.exit(pytest.main([
        "tests/orchestration/test_halt_resume.py",
        "-v",
        "--tb=short"
    ]))
