"""Shannon CLI configuration management.

This module provides centralized configuration management for Shannon CLI,
supporting both environment variables and configuration files.
"""

from pathlib import Path
from typing import Optional
import json
import os


class ShannonConfig:
    """Shannon CLI configuration management.

    Manages all configuration settings for Shannon CLI, including:
    - Log levels and output paths
    - Session storage directories
    - Token budgets for Claude SDK
    - Runtime configuration options

    Configuration priority (highest to lowest):
    1. Environment variables (SHANNON_*)
    2. Configuration file (~/.shannon/config.json)
    3. Default values

    Attributes:
        config_dir: Path to Shannon configuration directory (~/.shannon)
        config_file: Path to configuration JSON file
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        session_dir: Directory for session storage
        token_budget: Maximum tokens per Claude SDK call

    Environment Variables:
        SHANNON_LOG_LEVEL: Override log level (default: DEBUG)
        SHANNON_SESSION_DIR: Override session directory
        SHANNON_TOKEN_BUDGET: Override token budget (default: 150000)

    Example:
        >>> config = ShannonConfig()
        >>> config.log_level
        'DEBUG'
        >>> config.token_budget
        150000
        >>> config.save()  # Persist current settings
    """

    def __init__(self) -> None:
        """Initialize Shannon configuration.

        Loads configuration from:
        1. Environment variables (if set)
        2. Configuration file (if exists)
        3. Default values

        Creates configuration directory if it doesn't exist.
        """
        self.config_dir: Path = Path.home() / '.shannon'
        self.config_file: Path = self.config_dir / 'config.json'

        # Default values (can be overridden by env vars or config file)
        self.log_level: str = 'DEBUG'
        self.token_budget: int = 150000
        self.session_dir: Path = self.config_dir / 'sessions'
        self.framework_path: Optional[str] = None  # Path to Shannon Framework
        self.cost_budget: float = 100.00  # Cost budget in USD for V3 cost optimization

        # Load from file first (if exists)
        self.load()

        # Environment variables override everything
        self._apply_env_overrides()

    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides to configuration.

        Environment variables take precedence over both file-based
        configuration and defaults.

        Supported environment variables:
        - SHANNON_LOG_LEVEL: Log level (DEBUG, INFO, WARNING, ERROR)
        - SHANNON_SESSION_DIR: Session storage directory path
        - SHANNON_TOKEN_BUDGET: Token budget (integer)
        - SHANNON_FRAMEWORK_PATH: Path to Shannon Framework installation
        """
        if 'SHANNON_LOG_LEVEL' in os.environ:
            self.log_level = os.environ['SHANNON_LOG_LEVEL']

        if 'SHANNON_SESSION_DIR' in os.environ:
            self.session_dir = Path(os.environ['SHANNON_SESSION_DIR'])

        if 'SHANNON_TOKEN_BUDGET' in os.environ:
            try:
                self.token_budget = int(os.environ['SHANNON_TOKEN_BUDGET'])
            except ValueError:
                # Keep existing value if conversion fails
                pass

        if 'SHANNON_FRAMEWORK_PATH' in os.environ:
            self.framework_path = os.environ['SHANNON_FRAMEWORK_PATH']

        if 'SHANNON_COST_BUDGET' in os.environ:
            try:
                self.cost_budget = float(os.environ['SHANNON_COST_BUDGET'])
            except ValueError:
                # Keep existing value if conversion fails
                pass

    def load(self) -> None:
        """Load configuration from JSON file if it exists.

        Loads settings from ~/.shannon/config.json and updates
        instance attributes. If file doesn't exist, uses defaults.

        File format:
            {
                "log_level": "DEBUG",
                "session_dir": "/path/to/sessions",
                "token_budget": 150000
            }

        Raises:
            json.JSONDecodeError: If config file is malformed
            OSError: If config file cannot be read
        """
        if not self.config_file.exists():
            return

        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)

                if 'log_level' in data:
                    self.log_level = data['log_level']

                if 'session_dir' in data:
                    self.session_dir = Path(data['session_dir'])

                if 'token_budget' in data:
                    self.token_budget = data['token_budget']

                if 'framework_path' in data:
                    self.framework_path = data['framework_path']

                if 'cost_budget' in data:
                    self.cost_budget = data['cost_budget']
        except (json.JSONDecodeError, OSError):
            # If config is malformed or unreadable, use defaults
            # Don't raise - degrade gracefully
            pass

    def save(self) -> None:
        """Save current configuration to JSON file.

        Persists current configuration values to ~/.shannon/config.json.
        Creates configuration directory if it doesn't exist.

        File format:
            {
                "log_level": "DEBUG",
                "session_dir": "/path/to/sessions",
                "token_budget": 150000
            }

        Raises:
            OSError: If config directory cannot be created or file cannot be written
        """
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Write configuration as JSON
        config_data = {
            'log_level': self.log_level,
            'session_dir': str(self.session_dir),
            'token_budget': self.token_budget,
            'framework_path': self.framework_path,
            'cost_budget': self.cost_budget
        }

        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=2)

    def ensure_directories(self) -> None:
        """Ensure all required directories exist.

        Creates:
        - Configuration directory (~/.shannon)
        - Session directory (~/.shannon/sessions)
        - Log directory (~/.shannon/logs)

        Called automatically by logger initialization.

        Raises:
            OSError: If directories cannot be created
        """
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        (self.config_dir / 'logs').mkdir(parents=True, exist_ok=True)

    def get_log_dir(self) -> Path:
        """Get log directory path.

        Returns:
            Path to log directory (~/.shannon/logs)
        """
        return self.config_dir / 'logs'

    def __repr__(self) -> str:
        """String representation of configuration.

        Returns:
            String representation showing key configuration values
        """
        return (
            f"ShannonConfig(log_level={self.log_level!r}, "
            f"token_budget={self.token_budget}, "
            f"session_dir={self.session_dir!r})"
        )
