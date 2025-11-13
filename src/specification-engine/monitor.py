"""
Shannon Framework v4 - Specification Monitor

Real-time specification adherence monitoring during execution.
Detects deviations from requirements and generates alerts.
"""

from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
from .models import SpecificationObject, Requirement
from .validator import ValidationError


class SpecificationEvent:
    """Represents a specification-related event during execution."""

    def __init__(
        self,
        event_type: str,
        description: str,
        requirement_ids: List[str] = None,
        severity: str = "info",
        metadata: Dict[str, Any] = None
    ):
        self.event_type = event_type  # implementation, deviation, completion, validation
        self.description = description
        self.requirement_ids = requirement_ids or []
        self.severity = severity  # info, warning, error, critical
        self.timestamp = datetime.now()
        self.metadata = metadata or {}

    def __repr__(self):
        return f"SpecificationEvent({self.event_type}: {self.description} [{self.severity}])"


class DeviationAlert:
    """Represents a deviation from specification."""

    def __init__(
        self,
        deviation_type: str,
        message: str,
        original_requirement: Optional[Requirement] = None,
        actual_implementation: Optional[str] = None,
        severity: str = "warning"
    ):
        self.deviation_type = deviation_type
        self.message = message
        self.original_requirement = original_requirement
        self.actual_implementation = actual_implementation
        self.severity = severity
        self.timestamp = datetime.now()

    def __repr__(self):
        return f"DeviationAlert({self.deviation_type}: {self.message} [{self.severity}])"


class SpecificationMonitor:
    """Monitors real-time adherence to specifications."""

    def __init__(self, spec: SpecificationObject):
        self.spec = spec
        self.events: List[SpecificationEvent] = []
        self.deviations: List[DeviationAlert] = []
        self.completed_requirements: set = set()
        self.in_progress_requirements: set = set()
        self.callbacks: Dict[str, List[Callable]] = {
            'on_deviation': [],
            'on_requirement_complete': [],
            'on_spec_complete': [],
        }

    def track_implementation(
        self,
        requirement_id: str,
        description: str,
        metadata: Dict[str, Any] = None
    ):
        """
        Track implementation of a requirement.

        Args:
            requirement_id: ID of requirement being implemented
            description: Description of what was implemented
            metadata: Additional context
        """
        # Verify requirement exists
        if not self._requirement_exists(requirement_id):
            self.record_deviation(
                deviation_type="invalid_requirement",
                message=f"Attempted to implement non-existent requirement: {requirement_id}",
                severity="error"
            )
            return

        # Mark as in progress
        self.in_progress_requirements.add(requirement_id)

        # Record event
        event = SpecificationEvent(
            event_type="implementation",
            description=description,
            requirement_ids=[requirement_id],
            severity="info",
            metadata=metadata or {}
        )
        self.events.append(event)

    def complete_requirement(self, requirement_id: str, validation_notes: str = ""):
        """
        Mark a requirement as completed.

        Args:
            requirement_id: ID of completed requirement
            validation_notes: Notes about validation/testing
        """
        if not self._requirement_exists(requirement_id):
            self.record_deviation(
                deviation_type="invalid_requirement",
                message=f"Attempted to complete non-existent requirement: {requirement_id}",
                severity="error"
            )
            return

        # Move from in-progress to completed
        self.in_progress_requirements.discard(requirement_id)
        self.completed_requirements.add(requirement_id)

        # Record event
        event = SpecificationEvent(
            event_type="completion",
            description=f"Completed requirement: {requirement_id}",
            requirement_ids=[requirement_id],
            severity="info",
            metadata={"validation_notes": validation_notes}
        )
        self.events.append(event)

        # Trigger callbacks
        self._trigger_callbacks('on_requirement_complete', requirement_id)

        # Check if spec is complete
        if self.is_complete():
            self._trigger_callbacks('on_spec_complete', self.spec)

    def record_deviation(
        self,
        deviation_type: str,
        message: str,
        requirement_id: Optional[str] = None,
        actual_implementation: Optional[str] = None,
        severity: str = "warning"
    ):
        """
        Record a deviation from specification.

        Args:
            deviation_type: Type of deviation (scope_creep, missing_requirement, etc.)
            message: Detailed message about deviation
            requirement_id: Related requirement if applicable
            actual_implementation: What was actually implemented
            severity: Severity level (info, warning, error, critical)
        """
        req = None
        if requirement_id:
            req = self._get_requirement(requirement_id)

        deviation = DeviationAlert(
            deviation_type=deviation_type,
            message=message,
            original_requirement=req,
            actual_implementation=actual_implementation,
            severity=severity
        )
        self.deviations.append(deviation)

        # Record event
        event = SpecificationEvent(
            event_type="deviation",
            description=message,
            requirement_ids=[requirement_id] if requirement_id else [],
            severity=severity,
            metadata={
                "deviation_type": deviation_type,
                "actual_implementation": actual_implementation
            }
        )
        self.events.append(event)

        # Trigger callbacks
        self._trigger_callbacks('on_deviation', deviation)

    def check_adherence(self) -> Dict[str, Any]:
        """
        Check overall adherence to specification.

        Returns:
            Dictionary with adherence metrics
        """
        total_requirements = len(self.spec.requirements)
        completed = len(self.completed_requirements)
        in_progress = len(self.in_progress_requirements)
        not_started = total_requirements - completed - in_progress

        # Calculate adherence score
        completion_rate = completed / total_requirements if total_requirements > 0 else 0.0

        # Penalize for deviations
        critical_deviations = sum(1 for d in self.deviations if d.severity == "critical")
        error_deviations = sum(1 for d in self.deviations if d.severity == "error")
        warning_deviations = sum(1 for d in self.deviations if d.severity == "warning")

        deviation_penalty = (
            critical_deviations * 0.10 +
            error_deviations * 0.05 +
            warning_deviations * 0.02
        )

        adherence_score = max(0.0, completion_rate - deviation_penalty)

        return {
            "adherence_score": adherence_score,
            "total_requirements": total_requirements,
            "completed": completed,
            "in_progress": in_progress,
            "not_started": not_started,
            "completion_rate": completion_rate,
            "deviation_count": len(self.deviations),
            "critical_deviations": critical_deviations,
            "error_deviations": error_deviations,
            "warning_deviations": warning_deviations,
        }

    def get_audit_trail(self) -> List[Dict[str, Any]]:
        """
        Get complete audit trail of specification-related events.

        Returns:
            List of events in chronological order
        """
        return [
            {
                "timestamp": event.timestamp.isoformat(),
                "event_type": event.event_type,
                "description": event.description,
                "requirement_ids": event.requirement_ids,
                "severity": event.severity,
                "metadata": event.metadata,
            }
            for event in sorted(self.events, key=lambda e: e.timestamp)
        ]

    def get_deviations_report(self) -> Dict[str, Any]:
        """
        Generate report of all deviations.

        Returns:
            Dictionary with deviation analysis
        """
        deviations_by_type = {}
        deviations_by_severity = {}

        for deviation in self.deviations:
            # Group by type
            if deviation.deviation_type not in deviations_by_type:
                deviations_by_type[deviation.deviation_type] = []
            deviations_by_type[deviation.deviation_type].append(deviation)

            # Group by severity
            if deviation.severity not in deviations_by_severity:
                deviations_by_severity[deviation.severity] = []
            deviations_by_severity[deviation.severity].append(deviation)

        return {
            "total_deviations": len(self.deviations),
            "by_type": {
                dtype: len(devs) for dtype, devs in deviations_by_type.items()
            },
            "by_severity": {
                severity: len(devs) for severity, devs in deviations_by_severity.items()
            },
            "deviations": [
                {
                    "timestamp": d.timestamp.isoformat(),
                    "type": d.deviation_type,
                    "message": d.message,
                    "severity": d.severity,
                    "requirement_id": d.original_requirement.id if d.original_requirement else None,
                    "actual_implementation": d.actual_implementation,
                }
                for d in sorted(self.deviations, key=lambda d: d.timestamp)
            ]
        }

    def is_complete(self) -> bool:
        """Check if all requirements are completed."""
        return len(self.completed_requirements) == len(self.spec.requirements)

    def get_progress_summary(self) -> str:
        """
        Get human-readable progress summary.

        Returns:
            Formatted string with progress information
        """
        adherence = self.check_adherence()

        summary = f"""
Specification Adherence Report
==============================

Title: {self.spec.title}
Confidence: {self.spec.confidence:.2%}

Progress:
  Total Requirements: {adherence['total_requirements']}
  Completed: {adherence['completed']} ({adherence['completion_rate']:.1%})
  In Progress: {adherence['in_progress']}
  Not Started: {adherence['not_started']}

Adherence:
  Score: {adherence['adherence_score']:.2%}
  Deviations: {adherence['deviation_count']} total
    - Critical: {adherence['critical_deviations']}
    - Errors: {adherence['error_deviations']}
    - Warnings: {adherence['warning_deviations']}

Status: {'✅ COMPLETE' if self.is_complete() else '🔄 IN PROGRESS'}
"""
        return summary.strip()

    def register_callback(self, event_type: str, callback: Callable):
        """
        Register callback for specific events.

        Args:
            event_type: Event type (on_deviation, on_requirement_complete, on_spec_complete)
            callback: Callable to execute on event
        """
        if event_type in self.callbacks:
            self.callbacks[event_type].append(callback)

    def _requirement_exists(self, requirement_id: str) -> bool:
        """Check if requirement exists in specification."""
        return any(req.id == requirement_id for req in self.spec.requirements)

    def _get_requirement(self, requirement_id: str) -> Optional[Requirement]:
        """Get requirement by ID."""
        for req in self.spec.requirements:
            if req.id == requirement_id:
                return req
        return None

    def _trigger_callbacks(self, event_type: str, *args):
        """Trigger registered callbacks for event type."""
        for callback in self.callbacks.get(event_type, []):
            try:
                callback(*args)
            except Exception as e:
                # Log error but don't break execution
                print(f"Error in callback {callback.__name__}: {e}")


class MonitoringContext:
    """Context manager for monitoring specification adherence."""

    def __init__(self, monitor: SpecificationMonitor, requirement_id: str):
        self.monitor = monitor
        self.requirement_id = requirement_id

    def __enter__(self):
        self.monitor.track_implementation(
            self.requirement_id,
            f"Starting implementation of {self.requirement_id}"
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # No exception, mark as complete
            self.monitor.complete_requirement(
                self.requirement_id,
                "Implementation completed successfully"
            )
        else:
            # Exception occurred, record deviation
            self.monitor.record_deviation(
                deviation_type="implementation_failure",
                message=f"Failed to implement {self.requirement_id}: {exc_val}",
                requirement_id=self.requirement_id,
                severity="error"
            )
        return False  # Don't suppress exceptions
