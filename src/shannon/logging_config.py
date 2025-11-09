"""Shannon CLI logging configuration"""

from pathlib import Path
from datetime import datetime
import json
import logging


class ShannonLogger:
    """
    Structured logging for Shannon CLI

    Features:
    - Text log file: ~/.shannon/logs/{session_id}.log
    - Event log (JSONL): ~/.shannon/logs/{session_id}.events.jsonl
    - Optional verbose output to console
    """

    def __init__(self, session_id: str, verbose: bool = False):
        """
        Initialize logger

        Args:
            session_id: Session identifier
            verbose: Print to console in addition to file
        """
        self.session_id = session_id
        self.verbose = verbose

        # Create logs directory
        self.log_dir = Path.home() / ".shannon" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Log files
        self.log_file = self.log_dir / f"{session_id}.log"
        self.event_file = self.log_dir / f"{session_id}.events.jsonl"

        # Setup Python logger
        self.logger = logging.getLogger(f"shannon.{session_id}")
        self.logger.setLevel(logging.DEBUG)

        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console handler (if verbose)
        if verbose:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def log_event(self, event_type: str, data: dict):
        """
        Log structured event to JSONL file

        Args:
            event_type: Event type identifier
            data: Event data (must be JSON-serializable)
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data,
        }

        # Write to JSONL file (one JSON object per line)
        with open(self.event_file, "a") as f:
            f.write(json.dumps(event) + "\n")

        # Also log to text log
        self.logger.info(f"Event: {event_type} - {data}")

    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)

    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)

    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)

    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
