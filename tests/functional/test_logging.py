"""
Functional tests for logging system
NO MOCKS - Real file I/O
"""

import pytest
from pathlib import Path
import json
import shutil


@pytest.mark.functional
def test_logger_creates_log_file():
    """Logger should create log file in logs directory"""
    from shannon.logging_config import ShannonLogger

    session_id = "test_logging"
    logger = ShannonLogger(session_id, verbose=False)

    # Log something
    logger.log_event("test_event", {"key": "value"})

    # Verify log file exists
    log_dir = Path.home() / ".shannon" / "logs"
    log_file = log_dir / f"{session_id}.log"
    assert log_file.exists(), "Log file should be created"

    # Verify contains event
    log_content = log_file.read_text()
    assert "test_event" in log_content

    # Cleanup
    if log_file.exists():
        log_file.unlink()


@pytest.mark.functional
def test_logger_creates_event_log():
    """Logger should create JSONL event log"""
    from shannon.logging_config import ShannonLogger

    session_id = "test_events"
    logger = ShannonLogger(session_id, verbose=False)

    # Log multiple events
    logger.log_event("event1", {"data": 1})
    logger.log_event("event2", {"data": 2})

    # Verify event log file exists
    event_file = Path.home() / ".shannon" / "logs" / f"{session_id}.events.jsonl"
    assert event_file.exists(), "Event log should be created"

    # Verify JSONL format (one JSON object per line)
    lines = event_file.read_text().strip().split("\n")
    assert len(lines) == 2

    # Parse first event
    event1 = json.loads(lines[0])
    assert event1["event_type"] == "event1"
    assert event1["data"]["data"] == 1

    # Cleanup
    if event_file.exists():
        event_file.unlink()


@pytest.mark.functional
def test_logger_verbose_mode():
    """Verbose mode should print to console (stderr)"""
    from shannon.logging_config import ShannonLogger
    import io
    import sys

    session_id = "test_verbose"

    # Capture stderr (logging goes to stderr, not stdout)
    captured_output = io.StringIO()
    sys.stderr = captured_output

    logger = ShannonLogger(session_id, verbose=True)
    logger.log_event("verbose_test", {"message": "hello"})

    # Restore stderr
    sys.stderr = sys.__stderr__

    # Check output
    output = captured_output.getvalue()
    assert "verbose_test" in output or "hello" in output

    # Cleanup
    log_file = Path.home() / ".shannon" / "logs" / f"{session_id}.log"
    event_file = Path.home() / ".shannon" / "logs" / f"{session_id}.events.jsonl"
    if log_file.exists():
        log_file.unlink()
    if event_file.exists():
        event_file.unlink()


@pytest.mark.functional
def test_logger_info_warning_error():
    """Logger should support different log levels"""
    from shannon.logging_config import ShannonLogger

    session_id = "test_levels"
    logger = ShannonLogger(session_id, verbose=False)

    # Log at different levels
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")

    # Verify log file contains all levels
    log_file = Path.home() / ".shannon" / "logs" / f"{session_id}.log"
    log_content = log_file.read_text()

    assert "Info message" in log_content
    assert "Warning message" in log_content
    assert "Error message" in log_content

    # Cleanup
    if log_file.exists():
        log_file.unlink()
    event_file = Path.home() / ".shannon" / "logs" / f"{session_id}.events.jsonl"
    if event_file.exists():
        event_file.unlink()
