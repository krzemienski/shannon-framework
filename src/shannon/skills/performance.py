"""Performance Monitoring for Skills.

Tracks and optimizes skill performance:
- Execution time tracking
- Resource usage monitoring
- Bottleneck detection
- Optimization recommendations

Part of: Wave 10 - Dynamic Skills & Polish
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import time
from collections import defaultdict


@dataclass
class PerformanceMetric:
    """Performance metric for a skill."""
    skill_name: str
    execution_time: float
    memory_usage: float
    success: bool
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceReport:
    """Performance report for skill."""
    skill_name: str
    total_executions: int
    avg_execution_time: float
    min_execution_time: float
    max_execution_time: float
    success_rate: float
    bottlenecks: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class PerformanceMonitor:
    """Monitors skill performance and provides optimization recommendations.

    Features:
    - Execution time tracking
    - Success rate monitoring
    - Bottleneck detection
    - Optimization suggestions
    """

    def __init__(self):
        """Initialize performance monitor."""
        self.metrics: Dict[str, List[PerformanceMetric]] = defaultdict(list)
        self.active_timers: Dict[str, float] = {}

    def start_tracking(self, skill_name: str):
        """Start tracking skill execution.

        Args:
            skill_name: Name of skill
        """
        self.active_timers[skill_name] = time.time()

    def stop_tracking(
        self,
        skill_name: str,
        success: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Stop tracking and record metric.

        Args:
            skill_name: Name of skill
            success: Whether execution succeeded
            metadata: Additional metadata
        """
        if skill_name not in self.active_timers:
            return

        start_time = self.active_timers[skill_name]
        execution_time = time.time() - start_time
        del self.active_timers[skill_name]

        metric = PerformanceMetric(
            skill_name=skill_name,
            execution_time=execution_time,
            memory_usage=0.0,  # TODO: Track actual memory
            success=success,
            metadata=metadata or {}
        )

        self.metrics[skill_name].append(metric)

    def generate_report(self, skill_name: str) -> Optional[PerformanceReport]:
        """Generate performance report for skill.

        Args:
            skill_name: Name of skill

        Returns:
            Performance report or None
        """
        if skill_name not in self.metrics:
            return None

        metrics = self.metrics[skill_name]

        if not metrics:
            return None

        execution_times = [m.execution_time for m in metrics]
        successes = sum(1 for m in metrics if m.success)

        report = PerformanceReport(
            skill_name=skill_name,
            total_executions=len(metrics),
            avg_execution_time=sum(execution_times) / len(execution_times),
            min_execution_time=min(execution_times),
            max_execution_time=max(execution_times),
            success_rate=successes / len(metrics) if metrics else 0.0
        )

        # Detect bottlenecks
        if report.max_execution_time > report.avg_execution_time * 3:
            report.bottlenecks.append(
                f"High variance in execution time (max: {report.max_execution_time:.2f}s)"
            )

        if report.success_rate < 0.9:
            report.bottlenecks.append(
                f"Low success rate: {report.success_rate*100:.1f}%"
            )

        # Generate recommendations
        if report.avg_execution_time > 5.0:
            report.recommendations.append(
                "Consider caching intermediate results"
            )

        if report.bottlenecks:
            report.recommendations.append(
                "Review bottlenecks and optimize critical paths"
            )

        return report

    def get_top_slow_skills(self, n: int = 5) -> List[PerformanceReport]:
        """Get slowest skills by average execution time.

        Args:
            n: Number of skills to return

        Returns:
            List of performance reports
        """
        reports = []

        for skill_name in self.metrics.keys():
            report = self.generate_report(skill_name)
            if report:
                reports.append(report)

        # Sort by average execution time
        reports.sort(key=lambda r: r.avg_execution_time, reverse=True)

        return reports[:n]

    def clear_metrics(self, skill_name: Optional[str] = None):
        """Clear metrics for skill or all skills.

        Args:
            skill_name: Skill to clear, or None for all
        """
        if skill_name:
            if skill_name in self.metrics:
                self.metrics[skill_name] = []
        else:
            self.metrics.clear()

    def export_metrics(self) -> Dict[str, Any]:
        """Export all metrics as dictionary.

        Returns:
            Metrics dictionary
        """
        return {
            skill_name: [
                {
                    'execution_time': m.execution_time,
                    'success': m.success,
                    'timestamp': m.timestamp.isoformat()
                }
                for m in metrics
            ]
            for skill_name, metrics in self.metrics.items()
        }
