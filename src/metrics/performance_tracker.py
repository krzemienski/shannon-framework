"""
Performance tracking and anomaly detection for Shannon Framework.

Provides real-time metrics collection, performance monitoring, and anomaly detection
for wave execution, parallel operations, and resource utilization.
"""

import asyncio
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from statistics import mean, stdev
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


class MetricType(Enum):
    """Types of metrics tracked by the system."""
    WAVE_EXECUTION_TIME = "wave_execution_time"
    PARALLEL_EFFICIENCY = "parallel_efficiency"
    TOKEN_USAGE = "token_usage"
    SUCCESS_RATE = "success_rate"
    ERROR_RATE = "error_rate"
    RESOURCE_UTILIZATION = "resource_utilization"
    LATENCY = "latency"
    THROUGHPUT = "throughput"


class AnomalyType(Enum):
    """Types of anomalies detected in metrics."""
    PERFORMANCE_DEGRADATION = "performance_degradation"
    RESOURCE_SPIKE = "resource_spike"
    ERROR_SPIKE = "error_spike"
    LATENCY_INCREASE = "latency_increase"
    EFFICIENCY_DROP = "efficiency_drop"


@dataclass
class Metric:
    """Individual metric data point."""
    metric_type: MetricType
    value: float
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)


@dataclass
class AnomalyDetection:
    """Detected anomaly with context."""
    anomaly_type: AnomalyType
    metric_type: MetricType
    current_value: float
    expected_range: Tuple[float, float]
    severity: float  # 0.0-1.0
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceReport:
    """Comprehensive performance report."""
    start_time: datetime
    end_time: datetime
    duration: float
    metrics_summary: Dict[MetricType, Dict[str, float]]
    anomalies: List[AnomalyDetection]
    recommendations: List[str]


class MetricCollector:
    """Collects and aggregates individual metrics."""

    def __init__(self, window_size: int = 100):
        """
        Initialize metric collector.

        Args:
            window_size: Number of recent metrics to keep for statistics
        """
        self.window_size = window_size
        self._metrics: Dict[MetricType, deque] = defaultdict(
            lambda: deque(maxlen=window_size)
        )
        self._lock = asyncio.Lock()

    async def record(
        self,
        metric_type: MetricType,
        value: float,
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[Set[str]] = None,
    ) -> None:
        """
        Record a metric value.

        Args:
            metric_type: Type of metric
            value: Metric value
            context: Additional context
            tags: Metric tags
        """
        metric = Metric(
            metric_type=metric_type,
            value=value,
            timestamp=datetime.now(),
            context=context or {},
            tags=tags or set(),
        )

        async with self._lock:
            self._metrics[metric_type].append(metric)

    async def get_statistics(
        self, metric_type: MetricType
    ) -> Optional[Dict[str, float]]:
        """
        Get statistics for a metric type.

        Args:
            metric_type: Type of metric

        Returns:
            Statistics dict with mean, min, max, stdev, or None if insufficient data
        """
        async with self._lock:
            metrics = self._metrics.get(metric_type)
            if not metrics or len(metrics) < 2:
                return None

            values = [m.value for m in metrics]
            return {
                "mean": mean(values),
                "min": min(values),
                "max": max(values),
                "stdev": stdev(values) if len(values) > 1 else 0.0,
                "count": len(values),
                "latest": values[-1],
            }

    async def get_recent_metrics(
        self, metric_type: MetricType, count: int = 10
    ) -> List[Metric]:
        """
        Get recent metrics of a type.

        Args:
            metric_type: Type of metric
            count: Number of recent metrics to return

        Returns:
            List of recent metrics
        """
        async with self._lock:
            metrics = self._metrics.get(metric_type, deque())
            return list(metrics)[-count:]


class AnomalyDetector:
    """Detects anomalies in performance metrics."""

    def __init__(
        self,
        std_threshold: float = 2.5,
        min_samples: int = 10,
    ):
        """
        Initialize anomaly detector.

        Args:
            std_threshold: Number of standard deviations for anomaly detection
            min_samples: Minimum samples required for detection
        """
        self.std_threshold = std_threshold
        self.min_samples = min_samples

    async def detect_anomalies(
        self,
        metric_type: MetricType,
        current_value: float,
        statistics: Dict[str, float],
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[AnomalyDetection]:
        """
        Detect anomalies in a metric value.

        Args:
            metric_type: Type of metric
            current_value: Current metric value
            statistics: Historical statistics
            context: Additional context

        Returns:
            AnomalyDetection if anomaly detected, None otherwise
        """
        if statistics["count"] < self.min_samples:
            return None

        mean_val = statistics["mean"]
        std_val = statistics["stdev"]

        # Calculate expected range
        lower_bound = mean_val - (self.std_threshold * std_val)
        upper_bound = mean_val + (self.std_threshold * std_val)

        # Check if current value is outside expected range
        if lower_bound <= current_value <= upper_bound:
            return None

        # Determine anomaly type based on metric and direction
        anomaly_type = self._classify_anomaly(
            metric_type, current_value, mean_val
        )

        # Calculate severity (0.0-1.0)
        deviation = abs(current_value - mean_val)
        severity = min(1.0, deviation / (self.std_threshold * std_val + 1e-6))

        return AnomalyDetection(
            anomaly_type=anomaly_type,
            metric_type=metric_type,
            current_value=current_value,
            expected_range=(lower_bound, upper_bound),
            severity=severity,
            timestamp=datetime.now(),
            context=context or {},
        )

    def _classify_anomaly(
        self, metric_type: MetricType, current: float, mean: float
    ) -> AnomalyType:
        """Classify the type of anomaly based on metric type and direction."""
        is_increase = current > mean

        if metric_type == MetricType.WAVE_EXECUTION_TIME:
            return (
                AnomalyType.PERFORMANCE_DEGRADATION
                if is_increase
                else AnomalyType.EFFICIENCY_DROP
            )
        elif metric_type == MetricType.ERROR_RATE:
            return AnomalyType.ERROR_SPIKE if is_increase else None
        elif metric_type == MetricType.LATENCY:
            return AnomalyType.LATENCY_INCREASE if is_increase else None
        elif metric_type == MetricType.RESOURCE_UTILIZATION:
            return AnomalyType.RESOURCE_SPIKE if is_increase else None
        elif metric_type == MetricType.PARALLEL_EFFICIENCY:
            return (
                AnomalyType.EFFICIENCY_DROP
                if not is_increase
                else None
            )
        else:
            return AnomalyType.PERFORMANCE_DEGRADATION


class PerformanceTracker:
    """
    Tracks performance metrics and detects anomalies.

    Provides comprehensive performance monitoring for wave execution,
    parallel operations, token usage, and system health.
    """

    def __init__(
        self,
        window_size: int = 100,
        anomaly_threshold: float = 2.5,
        min_samples: int = 10,
    ):
        """
        Initialize performance tracker.

        Args:
            window_size: Number of metrics to keep in memory
            anomaly_threshold: Standard deviations for anomaly detection
            min_samples: Minimum samples for statistical analysis
        """
        self.collector = MetricCollector(window_size=window_size)
        self.detector = AnomalyDetector(
            std_threshold=anomaly_threshold,
            min_samples=min_samples,
        )
        self.anomalies: List[AnomalyDetection] = []
        self._lock = asyncio.Lock()
        self._callbacks: List[Callable[[AnomalyDetection], None]] = []

    async def record_wave_execution(
        self,
        wave_id: str,
        duration: float,
        success: bool,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Record wave execution metrics.

        Args:
            wave_id: Wave identifier
            duration: Execution duration in seconds
            success: Whether execution succeeded
            context: Additional context
        """
        ctx = context or {}
        ctx["wave_id"] = wave_id
        ctx["success"] = success

        # Record execution time
        await self.collector.record(
            MetricType.WAVE_EXECUTION_TIME,
            duration,
            context=ctx,
            tags={"wave", wave_id},
        )

        # Record success/failure
        success_rate = 1.0 if success else 0.0
        await self.collector.record(
            MetricType.SUCCESS_RATE,
            success_rate,
            context=ctx,
            tags={"wave", wave_id},
        )

        # Check for anomalies
        await self._check_anomalies(
            MetricType.WAVE_EXECUTION_TIME, duration, ctx
        )

    async def record_parallel_efficiency(
        self,
        tasks_count: int,
        parallel_time: float,
        sequential_time: float,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Record parallel execution efficiency.

        Args:
            tasks_count: Number of parallel tasks
            parallel_time: Actual parallel execution time
            sequential_time: Estimated sequential execution time
            context: Additional context
        """
        # Calculate efficiency as speedup ratio
        efficiency = (
            sequential_time / parallel_time if parallel_time > 0 else 0.0
        )

        ctx = context or {}
        ctx.update(
            {
                "tasks_count": tasks_count,
                "parallel_time": parallel_time,
                "sequential_time": sequential_time,
                "speedup": efficiency,
            }
        )

        await self.collector.record(
            MetricType.PARALLEL_EFFICIENCY,
            efficiency,
            context=ctx,
            tags={"parallel"},
        )

        await self._check_anomalies(
            MetricType.PARALLEL_EFFICIENCY, efficiency, ctx
        )

    async def record_token_usage(
        self,
        tokens: int,
        operation: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Record token usage.

        Args:
            tokens: Number of tokens used
            operation: Operation name
            context: Additional context
        """
        ctx = context or {}
        ctx["operation"] = operation

        await self.collector.record(
            MetricType.TOKEN_USAGE,
            float(tokens),
            context=ctx,
            tags={"tokens", operation},
        )

        await self._check_anomalies(MetricType.TOKEN_USAGE, float(tokens), ctx)

    async def record_error(
        self, error_type: str, context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Record an error occurrence.

        Args:
            error_type: Type of error
            context: Additional context
        """
        ctx = context or {}
        ctx["error_type"] = error_type

        await self.collector.record(
            MetricType.ERROR_RATE, 1.0, context=ctx, tags={"error", error_type}
        )

    async def get_performance_report(
        self, duration_minutes: Optional[int] = None
    ) -> PerformanceReport:
        """
        Generate comprehensive performance report.

        Args:
            duration_minutes: Report time window (None for all data)

        Returns:
            Performance report with metrics and recommendations
        """
        end_time = datetime.now()
        start_time = end_time

        # Collect statistics for all metric types
        metrics_summary = {}
        for metric_type in MetricType:
            stats = await self.collector.get_statistics(metric_type)
            if stats:
                metrics_summary[metric_type] = stats

        # Generate recommendations based on metrics
        recommendations = await self._generate_recommendations(metrics_summary)

        return PerformanceReport(
            start_time=start_time,
            end_time=end_time,
            duration=(end_time - start_time).total_seconds(),
            metrics_summary=metrics_summary,
            anomalies=self.anomalies.copy(),
            recommendations=recommendations,
        )

    async def _check_anomalies(
        self,
        metric_type: MetricType,
        value: float,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Check for anomalies and trigger callbacks."""
        stats = await self.collector.get_statistics(metric_type)
        if not stats:
            return

        anomaly = await self.detector.detect_anomalies(
            metric_type, value, stats, context
        )

        if anomaly:
            async with self._lock:
                self.anomalies.append(anomaly)

            # Trigger callbacks
            for callback in self._callbacks:
                try:
                    callback(anomaly)
                except Exception:
                    pass  # Don't let callback errors break tracking

    async def _generate_recommendations(
        self, metrics_summary: Dict[MetricType, Dict[str, float]]
    ) -> List[str]:
        """Generate performance recommendations based on metrics."""
        recommendations = []

        # Check parallel efficiency
        if MetricType.PARALLEL_EFFICIENCY in metrics_summary:
            efficiency = metrics_summary[MetricType.PARALLEL_EFFICIENCY]
            if efficiency["mean"] < 1.5:
                recommendations.append(
                    "Parallel efficiency is low. Consider increasing task granularity or reducing coordination overhead."
                )

        # Check token usage
        if MetricType.TOKEN_USAGE in metrics_summary:
            tokens = metrics_summary[MetricType.TOKEN_USAGE]
            if tokens["mean"] > 10000:
                recommendations.append(
                    "High token usage detected. Consider optimizing prompts or using streaming."
                )

        # Check error rate
        if MetricType.ERROR_RATE in metrics_summary:
            error_rate = metrics_summary[MetricType.ERROR_RATE]
            if error_rate["mean"] > 0.1:
                recommendations.append(
                    "Elevated error rate detected. Review error recovery strategies."
                )

        # Check execution time variance
        if MetricType.WAVE_EXECUTION_TIME in metrics_summary:
            exec_time = metrics_summary[MetricType.WAVE_EXECUTION_TIME]
            if exec_time["stdev"] > exec_time["mean"] * 0.5:
                recommendations.append(
                    "High execution time variance. Consider load balancing or resource optimization."
                )

        return recommendations

    def register_anomaly_callback(
        self, callback: Callable[[AnomalyDetection], None]
    ) -> None:
        """
        Register callback for anomaly notifications.

        Args:
            callback: Function to call when anomaly detected
        """
        self._callbacks.append(callback)


# Global performance tracker instance
_global_tracker: Optional[PerformanceTracker] = None


def get_performance_tracker() -> PerformanceTracker:
    """Get or create global performance tracker."""
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = PerformanceTracker()
    return _global_tracker