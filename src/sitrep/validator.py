"""
Shannon Framework v4 - SITREP Validator

Validates SITREP structure and content.
"""

from typing import List, Dict, Any
from .models import SITREP, Task, TaskStatus, SITREPStatus


class ValidationError:
    """SITREP validation error."""

    def __init__(self, field: str, message: str, severity: str = "error"):
        self.field = field
        self.message = message
        self.severity = severity

    def __repr__(self):
        return f"ValidationError({self.field}: {self.message} [{self.severity}])"


class SITREPValidator:
    """Validates SITREP structure and content."""

    def validate(self, sitrep: SITREP) -> List[ValidationError]:
        """
        Validate SITREP.

        Args:
            sitrep: SITREP to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Required fields
        errors.extend(self._validate_required_fields(sitrep))

        # Task validation
        errors.extend(self._validate_tasks(sitrep))

        # Status consistency
        errors.extend(self._validate_status(sitrep))

        # Completion percentage
        errors.extend(self._validate_completion(sitrep))

        # Critical items
        errors.extend(self._validate_critical_items(sitrep))

        return errors

    def _validate_required_fields(self, sitrep: SITREP) -> List[ValidationError]:
        """Validate required fields are present."""
        errors = []

        if not sitrep.agent_name:
            errors.append(ValidationError(
                "agent_name",
                "Agent name is required",
                "error"
            ))

        if not sitrep.mission:
            errors.append(ValidationError(
                "mission",
                "Mission description is required",
                "error"
            ))

        if not sitrep.timestamp:
            errors.append(ValidationError(
                "timestamp",
                "Timestamp is required",
                "error"
            ))

        return errors

    def _validate_tasks(self, sitrep: SITREP) -> List[ValidationError]:
        """Validate task structure and dependencies."""
        errors = []

        if not sitrep.tasks:
            errors.append(ValidationError(
                "tasks",
                "SITREP should contain at least one task",
                "warning"
            ))
            return errors

        # Check for duplicate task IDs
        task_ids = [task.id for task in sitrep.tasks]
        duplicates = [tid for tid in task_ids if task_ids.count(tid) > 1]
        if duplicates:
            errors.append(ValidationError(
                "tasks",
                f"Duplicate task IDs found: {', '.join(set(duplicates))}",
                "error"
            ))

        # Validate task dependencies
        task_id_set = set(task_ids)
        for task in sitrep.tasks:
            for dep_id in task.dependencies:
                if dep_id not in task_id_set:
                    errors.append(ValidationError(
                        f"tasks.{task.id}",
                        f"Invalid dependency '{dep_id}' (task does not exist)",
                        "error"
                    ))

            # Check completion percentage
            if not 0.0 <= task.completion <= 1.0:
                errors.append(ValidationError(
                    f"tasks.{task.id}",
                    f"Invalid completion percentage: {task.completion} (must be 0.0-1.0)",
                    "error"
                ))

            # Check status/completion consistency
            if task.status == TaskStatus.COMPLETED and task.completion < 1.0:
                errors.append(ValidationError(
                    f"tasks.{task.id}",
                    f"Task marked COMPLETED but completion is {task.completion:.1%}",
                    "warning"
                ))

            if task.status == TaskStatus.PENDING and task.completion > 0.0:
                errors.append(ValidationError(
                    f"tasks.{task.id}",
                    f"Task marked PENDING but has {task.completion:.1%} completion",
                    "warning"
                ))

        return errors

    def _validate_status(self, sitrep: SITREP) -> List[ValidationError]:
        """Validate status consistency."""
        errors = []

        # Check if status matches task states
        critical_items = sitrep.get_critical_items()

        if sitrep.overall_status == SITREPStatus.GREEN:
            if critical_items['blocked_tasks'] or critical_items['failed_tasks']:
                errors.append(ValidationError(
                    "overall_status",
                    "Status is GREEN but there are blocked or failed tasks",
                    "warning"
                ))

            if critical_items['critical_risks']:
                errors.append(ValidationError(
                    "overall_status",
                    "Status is GREEN but there are critical risks",
                    "warning"
                ))

        if sitrep.overall_status == SITREPStatus.COMPLETE:
            task_summary = sitrep.get_task_summary()
            if task_summary['completed'] < task_summary['total']:
                errors.append(ValidationError(
                    "overall_status",
                    f"Status is COMPLETE but only {task_summary['completed']}/{task_summary['total']} tasks done",
                    "error"
                ))

        return errors

    def _validate_completion(self, sitrep: SITREP) -> List[ValidationError]:
        """Validate completion percentage."""
        errors = []

        if not 0.0 <= sitrep.completion_percentage <= 1.0:
            errors.append(ValidationError(
                "completion_percentage",
                f"Invalid completion percentage: {sitrep.completion_percentage}",
                "error"
            ))

        # Check if completion matches tasks
        if sitrep.tasks:
            calculated = sitrep.calculate_completion()
            diff = abs(calculated - sitrep.completion_percentage)

            if diff > 0.05:  # 5% tolerance
                errors.append(ValidationError(
                    "completion_percentage",
                    f"Completion {sitrep.completion_percentage:.1%} doesn't match " +
                    f"calculated {calculated:.1%} from tasks",
                    "warning"
                ))

        return errors

    def _validate_critical_items(self, sitrep: SITREP) -> List[ValidationError]:
        """Validate critical items have mitigation."""
        errors = []

        critical_items = sitrep.get_critical_items()

        # Critical risks should have mitigation
        for risk in critical_items['critical_risks']:
            if not risk.get('mitigation'):
                errors.append(ValidationError(
                    "risks",
                    f"Critical risk '{risk['description'][:50]}...' has no mitigation plan",
                    "warning"
                ))

        # Blocked tasks should have notes
        for task in critical_items['blocked_tasks']:
            if not task.get('notes'):
                errors.append(ValidationError(
                    f"tasks.{task['id']}",
                    "Blocked task should have notes explaining blockage",
                    "info"
                ))

        # Failed tasks should have notes
        for task in critical_items['failed_tasks']:
            if not task.get('notes'):
                errors.append(ValidationError(
                    f"tasks.{task['id']}",
                    "Failed task should have notes explaining failure",
                    "warning"
                ))

        return errors

    def is_valid(self, sitrep: SITREP) -> bool:
        """
        Check if SITREP is valid (no errors).

        Args:
            sitrep: SITREP to validate

        Returns:
            True if valid (no errors, warnings OK)
        """
        errors = self.validate(sitrep)
        return not any(err.severity == "error" for err in errors)

    def get_error_summary(self, sitrep: SITREP) -> Dict[str, Any]:
        """
        Get validation error summary.

        Args:
            sitrep: SITREP to validate

        Returns:
            Summary dictionary
        """
        errors = self.validate(sitrep)

        error_count = sum(1 for e in errors if e.severity == "error")
        warning_count = sum(1 for e in errors if e.severity == "warning")
        info_count = sum(1 for e in errors if e.severity == "info")

        return {
            'is_valid': error_count == 0,
            'total_issues': len(errors),
            'error_count': error_count,
            'warning_count': warning_count,
            'info_count': info_count,
            'errors': [
                {
                    'field': e.field,
                    'message': e.message,
                    'severity': e.severity
                }
                for e in errors
            ]
        }
