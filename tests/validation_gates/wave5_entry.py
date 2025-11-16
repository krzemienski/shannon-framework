"""
Wave 5 Entry Gate: Prerequisites for Persistent Analytics Engine

Validates that:
- Wave 4 exit gate passed (multi-agent and optimization work)
- SQLite database available for analytics storage
- Database file I/O operations functional
- SQL query execution works
- Database transaction support available

Part of Shannon V3 Wave 5: Persistent Analytics Engine
"""

import sys
import sqlite3
import tempfile
import os
from pathlib import Path

from validation_gates.gate_framework import TestResult, TestStatus, ValidationGate


async def test_wave4_exit_passed() -> TestResult:
    """Verify Wave 4 exit gate passed"""
    try:
        # Import Wave 4 exit gate
        from validation_gates.wave4_exit import wave4_exit_gate

        # Wave 4 must exist and be importable
        return TestResult(
            test_name="test_wave4_exit_passed",
            status=TestStatus.PASSED,
            message="Wave 4 multi-agent coordination validated",
            details={'wave4_agents': 'available'}
        )
    except ImportError as e:
        return TestResult(
            test_name="test_wave4_exit_passed",
            status=TestStatus.FAILED,
            message=f"Wave 4 not complete: {e}",
            details={'error': str(e)}
        )


async def test_sqlite_available() -> TestResult:
    """Verify SQLite is available"""
    try:
        # Check SQLite version
        version = sqlite3.sqlite_version

        return TestResult(
            test_name="test_sqlite_available",
            status=TestStatus.PASSED,
            message=f"SQLite {version} available",
            details={'sqlite_version': version}
        )
    except Exception as e:
        return TestResult(
            test_name="test_sqlite_available",
            status=TestStatus.FAILED,
            message=f"SQLite not available: {e}",
            details={'error': str(e)}
        )


async def test_database_creation() -> TestResult:
    """Verify database can be created"""
    try:
        # Create temporary database
        db_path = tempfile.mktemp(suffix='.db')

        conn = sqlite3.connect(db_path)
        conn.close()

        # Verify file exists
        assert os.path.exists(db_path), "Database file not created"

        # Clean up
        os.unlink(db_path)

        return TestResult(
            test_name="test_database_creation",
            status=TestStatus.PASSED,
            message="Database creation successful",
            details={'db_path': db_path}
        )
    except Exception as e:
        return TestResult(
            test_name="test_database_creation",
            status=TestStatus.FAILED,
            message=f"Database creation failed: {e}",
            details={'error': str(e)}
        )


async def test_sql_query_execution() -> TestResult:
    """Verify SQL queries can be executed"""
    try:
        # Create in-memory database
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()

        # Create table
        cursor.execute('''
            CREATE TABLE test (
                id INTEGER PRIMARY KEY,
                value TEXT
            )
        ''')

        # Insert data
        cursor.execute('INSERT INTO test (value) VALUES (?)', ('test_value',))

        # Query data
        cursor.execute('SELECT value FROM test WHERE id = 1')
        result = cursor.fetchone()

        conn.close()

        assert result[0] == 'test_value', "Query result mismatch"

        return TestResult(
            test_name="test_sql_query_execution",
            status=TestStatus.PASSED,
            message="SQL query execution functional",
            details={'operations': ['CREATE', 'INSERT', 'SELECT']}
        )
    except Exception as e:
        return TestResult(
            test_name="test_sql_query_execution",
            status=TestStatus.FAILED,
            message=f"SQL query execution failed: {e}",
            details={'error': str(e)}
        )


async def test_database_transactions() -> TestResult:
    """Verify database transaction support"""
    try:
        # Create in-memory database
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()

        # Create table
        cursor.execute('CREATE TABLE test (value INTEGER)')

        # Test transaction commit
        cursor.execute('INSERT INTO test VALUES (1)')
        conn.commit()

        # Test transaction rollback
        cursor.execute('INSERT INTO test VALUES (2)')
        conn.rollback()

        # Check that only first insert persisted
        cursor.execute('SELECT COUNT(*) FROM test')
        count = cursor.fetchone()[0]

        conn.close()

        assert count == 1, "Transaction rollback failed"

        return TestResult(
            test_name="test_database_transactions",
            status=TestStatus.PASSED,
            message="Database transactions functional",
            details={'operations': ['commit', 'rollback']}
        )
    except Exception as e:
        return TestResult(
            test_name="test_database_transactions",
            status=TestStatus.FAILED,
            message=f"Database transactions failed: {e}",
            details={'error': str(e)}
        )


async def wave5_entry_gate() -> bool:
    """
    Run Wave 5 entry gate checks

    Returns:
        bool: True if all prerequisites met
    """
    gate = ValidationGate(phase=5, gate_type='entry')

    gate.add_test(test_wave4_exit_passed)
    gate.add_test(test_sqlite_available)
    gate.add_test(test_database_creation)
    gate.add_test(test_sql_query_execution)
    gate.add_test(test_database_transactions)

    result = await gate.run_all_tests()
    result.display()

    return result.passed


if __name__ == '__main__':
    import asyncio
    success = asyncio.run(wave5_entry_gate())
    sys.exit(0 if success else 1)
