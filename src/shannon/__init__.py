"""Shannon CLI Agent - Standalone Python CLI for Shannon Framework."""

__version__ = "2.0.0"
__author__ = "Shannon Framework Team"

# Export CLI entry point
from shannon.cli.commands import cli

__all__ = ['cli']
