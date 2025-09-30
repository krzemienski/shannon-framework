"""
Utility modules for Shannon Framework.
"""

from .async_executor import (
    ExecutionReport,
    ExceptionAggregator,
    ParallelExecutor,
    SemaphorePool,
    TaskMonitor,
    TaskResult,
    TaskStatus,
    get_parallel_executor,
)
from .error_recovery import (
    CircuitBreaker,
    CircuitState,
    CompensatingAction,
    CompensatingTransaction,
    ErrorRecoveryEngine,
    RecoveryResult,
    RecoveryStrategy,
    RetryPolicy,
    get_recovery_engine,
)

__all__ = [
    # Async execution
    "ExecutionReport",
    "ExceptionAggregator",
    "ParallelExecutor",
    "SemaphorePool",
    "TaskMonitor",
    "TaskResult",
    "TaskStatus",
    "get_parallel_executor",
    # Error recovery
    "CircuitBreaker",
    "CircuitState",
    "CompensatingAction",
    "CompensatingTransaction",
    "ErrorRecoveryEngine",
    "RecoveryResult",
    "RecoveryStrategy",
    "RetryPolicy",
    "get_recovery_engine",
]