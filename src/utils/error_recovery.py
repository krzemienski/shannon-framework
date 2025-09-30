"""
Error recovery engine for Shannon Framework.

Provides comprehensive error recovery strategies including retry policies,
circuit breakers, compensating transactions, and async recovery execution.
"""

import asyncio
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Coroutine, Dict, List, Optional, Set, Tuple


logger = logging.getLogger(__name__)


class RecoveryStrategy(Enum):
    """Error recovery strategies."""
    RETRY = "retry"
    CIRCUIT_BREAKER = "circuit_breaker"
    COMPENSATING_TRANSACTION = "compensating_transaction"
    GRACEFUL_DEGRADATION = "graceful_degradation"
    FALLBACK = "fallback"


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery


@dataclass
class RetryPolicy:
    """Retry policy configuration."""
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True
    retry_on: Set[type] = field(default_factory=lambda: {Exception})


@dataclass
class RecoveryResult:
    """Result of recovery attempt."""
    success: bool
    strategy: RecoveryStrategy
    attempts: int
    error: Optional[Exception]
    recovery_time: float
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CompensatingAction:
    """Action to compensate for a failed operation."""
    action: Callable[..., Coroutine[Any, Any, Any]]
    args: Tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    description: str = ""


class CircuitBreaker:
    """
    Circuit breaker to prevent cascading failures.

    Tracks failure rates and opens circuit when threshold exceeded,
    preventing requests during cooldown period.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout: float = 60.0,
        half_open_timeout: float = 10.0,
    ):
        """
        Initialize circuit breaker.

        Args:
            failure_threshold: Failures before opening circuit
            success_threshold: Successes needed to close circuit
            timeout: Time to wait before attempting recovery (seconds)
            half_open_timeout: Time to wait in half-open state
        """
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout = timeout
        self.half_open_timeout = half_open_timeout

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self._lock = asyncio.Lock()

    async def call(
        self, func: Callable[..., Coroutine[Any, Any, Any]], *args: Any, **kwargs: Any
    ) -> Any:
        """
        Execute function with circuit breaker protection.

        Args:
            func: Async function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result

        Raises:
            Exception: If circuit is open or function fails
        """
        async with self._lock:
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                else:
                    raise Exception(
                        f"Circuit breaker is OPEN. Last failure: {self.last_failure_time}"
                    )

        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except Exception as e:
            await self._on_failure()
            raise e

    async def _on_success(self) -> None:
        """Handle successful execution."""
        async with self._lock:
            self.failure_count = 0

            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.success_threshold:
                    self.state = CircuitState.CLOSED
                    logger.info("Circuit breaker closed after recovery")

    async def _on_failure(self) -> None:
        """Handle failed execution."""
        async with self._lock:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                logger.warning(
                    f"Circuit breaker opened after {self.failure_count} failures"
                )
            elif self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
                logger.warning("Circuit breaker reopened during half-open state")

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return True

        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.timeout

    async def reset(self) -> None:
        """Manually reset circuit breaker."""
        async with self._lock:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            self.success_count = 0
            self.last_failure_time = None
            logger.info("Circuit breaker manually reset")


class CompensatingTransaction:
    """
    Manages compensating transactions for rollback.

    Tracks actions and provides rollback capability for failed operations.
    """

    def __init__(self):
        """Initialize compensating transaction manager."""
        self.actions: List[CompensatingAction] = []
        self._lock = asyncio.Lock()

    async def add_compensation(
        self,
        action: Callable[..., Coroutine[Any, Any, Any]],
        *args: Any,
        description: str = "",
        **kwargs: Any,
    ) -> None:
        """
        Add compensating action.

        Args:
            action: Async function to execute for compensation
            *args: Positional arguments
            description: Action description
            **kwargs: Keyword arguments
        """
        async with self._lock:
            self.actions.append(
                CompensatingAction(
                    action=action,
                    args=args,
                    kwargs=kwargs,
                    description=description or action.__name__,
                )
            )

    async def rollback(self) -> List[Tuple[str, bool, Optional[Exception]]]:
        """
        Execute all compensating actions in reverse order.

        Returns:
            List of (description, success, error) tuples
        """
        results = []

        async with self._lock:
            # Execute in reverse order (undo last actions first)
            for action in reversed(self.actions):
                try:
                    await action.action(*action.args, **action.kwargs)
                    results.append((action.description, True, None))
                    logger.info(f"Compensation succeeded: {action.description}")
                except Exception as e:
                    results.append((action.description, False, e))
                    logger.error(
                        f"Compensation failed: {action.description} - {str(e)}"
                    )

            # Clear actions after rollback
            self.actions.clear()

        return results

    async def clear(self) -> None:
        """Clear all compensating actions."""
        async with self._lock:
            self.actions.clear()


class ErrorRecoveryEngine:
    """
    Comprehensive error recovery engine.

    Provides multiple recovery strategies including retry with exponential backoff,
    circuit breakers, compensating transactions, and async recovery execution.
    """

    def __init__(self):
        """Initialize error recovery engine."""
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.compensating_transactions: Dict[str, CompensatingTransaction] = {}
        self.recovery_stats: Dict[str, Dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        self._lock = asyncio.Lock()

    async def retry_with_backoff(
        self,
        func: Callable[..., Coroutine[Any, Any, Any]],
        policy: RetryPolicy,
        *args: Any,
        context: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> RecoveryResult:
        """
        Execute function with retry and exponential backoff.

        Args:
            func: Async function to execute
            policy: Retry policy configuration
            *args: Positional arguments
            context: Recovery context
            **kwargs: Keyword arguments

        Returns:
            Recovery result
        """
        start_time = datetime.now()
        last_error: Optional[Exception] = None

        for attempt in range(1, policy.max_attempts + 1):
            try:
                result = await func(*args, **kwargs)
                recovery_time = (datetime.now() - start_time).total_seconds()

                await self._record_recovery(
                    RecoveryStrategy.RETRY, True, attempt, context
                )

                return RecoveryResult(
                    success=True,
                    strategy=RecoveryStrategy.RETRY,
                    attempts=attempt,
                    error=None,
                    recovery_time=recovery_time,
                    context=context or {},
                )

            except Exception as e:
                last_error = e
                logger.warning(
                    f"Retry attempt {attempt}/{policy.max_attempts} failed: {str(e)}"
                )

                # Check if we should retry this error
                if not any(isinstance(e, exc_type) for exc_type in policy.retry_on):
                    break

                # Don't sleep after last attempt
                if attempt < policy.max_attempts:
                    delay = self._calculate_backoff(
                        attempt, policy.initial_delay, policy.exponential_base, policy.max_delay, policy.jitter
                    )
                    await asyncio.sleep(delay)

        recovery_time = (datetime.now() - start_time).total_seconds()
        await self._record_recovery(
            RecoveryStrategy.RETRY, False, policy.max_attempts, context
        )

        return RecoveryResult(
            success=False,
            strategy=RecoveryStrategy.RETRY,
            attempts=policy.max_attempts,
            error=last_error,
            recovery_time=recovery_time,
            context=context or {},
        )

    def _calculate_backoff(
        self,
        attempt: int,
        initial_delay: float,
        base: float,
        max_delay: float,
        jitter: bool,
    ) -> float:
        """Calculate backoff delay with exponential increase and optional jitter."""
        import random

        delay = min(initial_delay * (base ** (attempt - 1)), max_delay)

        if jitter:
            # Add random jitter (±25%)
            jitter_amount = delay * 0.25
            delay += random.uniform(-jitter_amount, jitter_amount)

        return max(0, delay)

    async def with_circuit_breaker(
        self,
        func: Callable[..., Coroutine[Any, Any, Any]],
        breaker_id: str,
        *args: Any,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        context: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> RecoveryResult:
        """
        Execute function with circuit breaker protection.

        Args:
            func: Async function to execute
            breaker_id: Circuit breaker identifier
            *args: Positional arguments
            failure_threshold: Failures before opening circuit
            timeout: Cooldown period
            context: Recovery context
            **kwargs: Keyword arguments

        Returns:
            Recovery result
        """
        start_time = datetime.now()

        # Get or create circuit breaker
        if breaker_id not in self.circuit_breakers:
            async with self._lock:
                if breaker_id not in self.circuit_breakers:
                    self.circuit_breakers[breaker_id] = CircuitBreaker(
                        failure_threshold=failure_threshold, timeout=timeout
                    )

        breaker = self.circuit_breakers[breaker_id]

        try:
            result = await breaker.call(func, *args, **kwargs)
            recovery_time = (datetime.now() - start_time).total_seconds()

            await self._record_recovery(
                RecoveryStrategy.CIRCUIT_BREAKER, True, 1, context
            )

            return RecoveryResult(
                success=True,
                strategy=RecoveryStrategy.CIRCUIT_BREAKER,
                attempts=1,
                error=None,
                recovery_time=recovery_time,
                context=context or {},
            )

        except Exception as e:
            recovery_time = (datetime.now() - start_time).total_seconds()

            await self._record_recovery(
                RecoveryStrategy.CIRCUIT_BREAKER, False, 1, context
            )

            return RecoveryResult(
                success=False,
                strategy=RecoveryStrategy.CIRCUIT_BREAKER,
                attempts=1,
                error=e,
                recovery_time=recovery_time,
                context=context or {},
            )

    async def with_compensation(
        self,
        func: Callable[..., Coroutine[Any, Any, Any]],
        transaction_id: str,
        *args: Any,
        context: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> RecoveryResult:
        """
        Execute function with compensating transaction support.

        Args:
            func: Async function to execute
            transaction_id: Transaction identifier
            *args: Positional arguments
            context: Recovery context
            **kwargs: Keyword arguments

        Returns:
            Recovery result
        """
        start_time = datetime.now()

        # Get or create transaction
        if transaction_id not in self.compensating_transactions:
            async with self._lock:
                if transaction_id not in self.compensating_transactions:
                    self.compensating_transactions[
                        transaction_id
                    ] = CompensatingTransaction()

        transaction = self.compensating_transactions[transaction_id]

        try:
            result = await func(*args, **kwargs)
            recovery_time = (datetime.now() - start_time).total_seconds()

            # Clear compensation actions on success
            await transaction.clear()

            await self._record_recovery(
                RecoveryStrategy.COMPENSATING_TRANSACTION, True, 1, context
            )

            return RecoveryResult(
                success=True,
                strategy=RecoveryStrategy.COMPENSATING_TRANSACTION,
                attempts=1,
                error=None,
                recovery_time=recovery_time,
                context=context or {},
            )

        except Exception as e:
            logger.error(
                f"Transaction {transaction_id} failed, rolling back: {str(e)}"
            )

            # Execute rollback
            rollback_results = await transaction.rollback()
            recovery_time = (datetime.now() - start_time).total_seconds()

            ctx = context or {}
            ctx["rollback_results"] = rollback_results

            await self._record_recovery(
                RecoveryStrategy.COMPENSATING_TRANSACTION, False, 1, context
            )

            return RecoveryResult(
                success=False,
                strategy=RecoveryStrategy.COMPENSATING_TRANSACTION,
                attempts=1,
                error=e,
                recovery_time=recovery_time,
                context=ctx,
            )

    async def with_fallback(
        self,
        primary_func: Callable[..., Coroutine[Any, Any, Any]],
        fallback_func: Callable[..., Coroutine[Any, Any, Any]],
        *args: Any,
        context: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> RecoveryResult:
        """
        Execute function with fallback on failure.

        Args:
            primary_func: Primary async function
            fallback_func: Fallback async function
            *args: Positional arguments
            context: Recovery context
            **kwargs: Keyword arguments

        Returns:
            Recovery result
        """
        start_time = datetime.now()

        try:
            result = await primary_func(*args, **kwargs)
            recovery_time = (datetime.now() - start_time).total_seconds()

            await self._record_recovery(RecoveryStrategy.FALLBACK, True, 1, context)

            return RecoveryResult(
                success=True,
                strategy=RecoveryStrategy.FALLBACK,
                attempts=1,
                error=None,
                recovery_time=recovery_time,
                context=context or {},
            )

        except Exception as primary_error:
            logger.warning(
                f"Primary function failed, using fallback: {str(primary_error)}"
            )

            try:
                result = await fallback_func(*args, **kwargs)
                recovery_time = (datetime.now() - start_time).total_seconds()

                ctx = context or {}
                ctx["primary_error"] = str(primary_error)
                ctx["used_fallback"] = True

                await self._record_recovery(
                    RecoveryStrategy.FALLBACK, True, 2, context
                )

                return RecoveryResult(
                    success=True,
                    strategy=RecoveryStrategy.FALLBACK,
                    attempts=2,
                    error=None,
                    recovery_time=recovery_time,
                    context=ctx,
                )

            except Exception as fallback_error:
                recovery_time = (datetime.now() - start_time).total_seconds()

                ctx = context or {}
                ctx["primary_error"] = str(primary_error)
                ctx["fallback_error"] = str(fallback_error)

                await self._record_recovery(
                    RecoveryStrategy.FALLBACK, False, 2, context
                )

                return RecoveryResult(
                    success=False,
                    strategy=RecoveryStrategy.FALLBACK,
                    attempts=2,
                    error=fallback_error,
                    recovery_time=recovery_time,
                    context=ctx,
                )

    async def _record_recovery(
        self,
        strategy: RecoveryStrategy,
        success: bool,
        attempts: int,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record recovery statistics."""
        async with self._lock:
            key = "success" if success else "failure"
            self.recovery_stats[strategy.value][key] += 1
            self.recovery_stats[strategy.value]["total_attempts"] += attempts

    async def get_recovery_stats(self) -> Dict[str, Dict[str, int]]:
        """Get recovery statistics."""
        async with self._lock:
            return dict(self.recovery_stats)

    def get_circuit_breaker(self, breaker_id: str) -> Optional[CircuitBreaker]:
        """Get circuit breaker by ID."""
        return self.circuit_breakers.get(breaker_id)

    def get_transaction(self, transaction_id: str) -> Optional[CompensatingTransaction]:
        """Get compensating transaction by ID."""
        return self.compensating_transactions.get(transaction_id)


# Global error recovery engine instance
_global_recovery_engine: Optional[ErrorRecoveryEngine] = None


def get_recovery_engine() -> ErrorRecoveryEngine:
    """Get or create global error recovery engine."""
    global _global_recovery_engine
    if _global_recovery_engine is None:
        _global_recovery_engine = ErrorRecoveryEngine()
    return _global_recovery_engine