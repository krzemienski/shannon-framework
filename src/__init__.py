"""Shannon Framework - Advanced information processing system.

A production-ready framework for parallel information processing with
resource management, error recovery, and comprehensive monitoring.
"""

__version__ = "0.1.0"
__author__ = "Shannon Framework Contributors"
__license__ = "MIT"

# Core components
from shannon.processor import InformationProcessor
from shannon.executor import ParallelExecutor
from shannon.channel import DataChannel
from shannon.monitor import ResourceMonitor
from shannon.recovery import ErrorRecoverySystem

__all__ = [
    "InformationProcessor",
    "ParallelExecutor",
    "DataChannel",
    "ResourceMonitor",
    "ErrorRecoverySystem",
]