"""
Functional tests for SessionManager
NO MOCKS - Real file I/O
"""

import pytest
from pathlib import Path
import json
import shutil


@pytest.mark.functional
def test_session_manager_save_and_load():
    """
    FUNCTIONAL TEST: SessionManager persists data correctly
    NO MOCKS - Real file I/O
    """
    from shannon.core.session_manager import SessionManager

    # Setup
    session_id = "test_session_123"
    session = SessionManager(session_id)

    # Save data
    test_data = {
        "complexity_score": 0.68,
        "domains": {"Frontend": 40, "Backend": 60},
    }
    session.write_memory("spec_analysis", test_data)

    # Verify file created
    expected_file = (
        Path.home() / ".shannon" / "sessions" / session_id / "spec_analysis.json"
    )
    assert expected_file.exists(), "JSON file should be created"

    # Verify file content
    with open(expected_file) as f:
        saved_data = json.load(f)
    assert saved_data == test_data

    # Load data in new session instance (simulates resume)
    session2 = SessionManager(session_id)
    loaded_data = session2.read_memory("spec_analysis")

    # Verify exact match
    assert loaded_data == test_data, "Data must round-trip perfectly"

    # Cleanup
    session_dir = Path.home() / ".shannon" / "sessions" / session_id
    if session_dir.exists():
        shutil.rmtree(session_dir)


@pytest.mark.functional
def test_session_manager_list_memories():
    """Verify list_memories returns all saved keys"""
    from shannon.core.session_manager import SessionManager

    session_id = "test_list_123"
    session = SessionManager(session_id)

    # Save multiple items
    session.write_memory("key1", {"data": 1})
    session.write_memory("key2", {"data": 2})
    session.write_memory("key3", {"data": 3})

    # List should return all keys
    keys = session.list_memories()
    assert "key1" in keys
    assert "key2" in keys
    assert "key3" in keys
    assert len(keys) == 3

    # Cleanup
    session_dir = Path.home() / ".shannon" / "sessions" / session_id
    if session_dir.exists():
        shutil.rmtree(session_dir)


@pytest.mark.functional
def test_session_manager_has_memory():
    """Verify has_memory correctly checks existence"""
    from shannon.core.session_manager import SessionManager

    session_id = "test_has_123"
    session = SessionManager(session_id)

    # Initially no memories
    assert not session.has_memory("nonexistent")

    # Save a memory
    session.write_memory("exists", {"test": "data"})

    # Now it exists
    assert session.has_memory("exists")
    assert not session.has_memory("still_nonexistent")

    # Cleanup
    session_dir = Path.home() / ".shannon" / "sessions" / session_id
    if session_dir.exists():
        shutil.rmtree(session_dir)


@pytest.mark.functional
def test_session_manager_read_nonexistent():
    """Reading nonexistent memory returns None"""
    from shannon.core.session_manager import SessionManager

    session_id = "test_nonexist_123"
    session = SessionManager(session_id)

    result = session.read_memory("does_not_exist")
    assert result is None

    # Cleanup
    session_dir = Path.home() / ".shannon" / "sessions" / session_id
    if session_dir.exists():
        shutil.rmtree(session_dir)


@pytest.mark.functional
def test_session_manager_list_all_sessions():
    """Verify list_all_sessions returns all session IDs"""
    from shannon.core.session_manager import SessionManager

    # Create multiple sessions
    session1 = SessionManager("session_a")
    session2 = SessionManager("session_b")
    session1.write_memory("test", {"data": 1})
    session2.write_memory("test", {"data": 2})

    # List all sessions
    sessions = SessionManager.list_all_sessions()
    assert "session_a" in sessions
    assert "session_b" in sessions

    # Cleanup
    for sid in ["session_a", "session_b"]:
        session_dir = Path.home() / ".shannon" / "sessions" / sid
        if session_dir.exists():
            shutil.rmtree(session_dir)
