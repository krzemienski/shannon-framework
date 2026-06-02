"""
Shannon Framework v4 - SITREP Template Engine

Generates formatted SITREP reports from data structures.
"""

from typing import Optional
from datetime import datetime
from .models import SITREP, Task, Finding, Risk, Metric, TaskStatus, SITREPStatus


class SITREPTemplate:
    """Template engine for generating formatted SITREPs."""

    @staticmethod
    def render_markdown(sitrep: SITREP) -> str:
        """
        Render SITREP as markdown.

        Args:
            sitrep: SITREP object

        Returns:
            Formatted markdown string
        """
        lines = []

        # Header
        lines.append("# SITREP")
        lines.append("")
        lines.append(f"**Agent:** {sitrep.agent_name}")
        lines.append(f"**Mission:** {sitrep.mission}")
        lines.append(f"**Timestamp:** {sitrep.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        lines.append(f"**Report #:** {sitrep.report_number}")
        lines.append(f"**Priority:** {sitrep.priority.value}")
        lines.append("")

        # Status
        status_emoji = SITREPTemplate._get_status_emoji(sitrep.overall_status)
        lines.append(f"## Status: {status_emoji} {sitrep.overall_status.value}")
        lines.append("")
        lines.append(f"**Completion:** {sitrep.completion_percentage:.1%}")
        lines.append("")

        # Situation
        lines.append("## Situation")
        lines.append("")
        if sitrep.situation_summary:
            lines.append(sitrep.situation_summary)
            lines.append("")

        # Tasks
        if sitrep.tasks:
            task_summary = sitrep.get_task_summary()
            lines.append("### Tasks")
            lines.append("")
            lines.append(f"- Total: {task_summary['total']}")
            lines.append(f"- ✅ Completed: {task_summary['completed']}")
            lines.append(f"- 🔄 In Progress: {task_summary['in_progress']}")
            lines.append(f"- ⏸️  Pending: {task_summary['pending']}")
            lines.append(f"- 🚫 Blocked: {task_summary['blocked']}")
            lines.append(f"- ❌ Failed: {task_summary['failed']}")
            lines.append("")

            # Task details
            for task in sitrep.tasks:
                task_emoji = SITREPTemplate._get_task_emoji(task.status)
                lines.append(f"**{task_emoji} {task.id}:** {task.description}")
                if task.completion > 0:
                    lines.append(f"  - Progress: {task.completion:.1%}")
                if task.assignee:
                    lines.append(f"  - Assignee: {task.assignee}")
                if task.notes:
                    lines.append(f"  - Notes: {task.notes}")
                if task.dependencies:
                    lines.append(f"  - Dependencies: {', '.join(task.dependencies)}")
                lines.append("")

        # Analysis
        lines.append("## Analysis")
        lines.append("")

        # Findings
        if sitrep.findings:
            lines.append("### Findings")
            lines.append("")
            for finding in sitrep.findings:
                impact_emoji = SITREPTemplate._get_impact_emoji(finding.impact)
                lines.append(f"**{impact_emoji} [{finding.category}]** {finding.description}")
                if finding.recommendation:
                    lines.append(f"  - Recommendation: {finding.recommendation}")
                lines.append("")

        # Risks
        if sitrep.risks:
            lines.append("### Risks & Blockers")
            lines.append("")
            for risk in sitrep.risks:
                severity_emoji = SITREPTemplate._get_severity_emoji(risk.severity)
                lines.append(f"**{severity_emoji} {risk.severity.upper()}:** {risk.description}")
                if risk.mitigation:
                    lines.append(f"  - Mitigation: {risk.mitigation}")
                if risk.owner:
                    lines.append(f"  - Owner: {risk.owner}")
                lines.append("")

        # Metrics
        if sitrep.metrics:
            lines.append("### Metrics")
            lines.append("")
            for metric in sitrep.metrics:
                value_str = f"{metric.value}"
                if metric.unit:
                    value_str += f" {metric.unit}"

                line = f"- **{metric.name}:** {value_str}"

                if metric.target:
                    line += f" (target: {metric.target}"
                    if metric.unit:
                        line += f" {metric.unit}"
                    line += ")"

                if metric.status:
                    status_emoji = SITREPTemplate._get_metric_status_emoji(metric.status)
                    line += f" {status_emoji}"

                lines.append(line)
            lines.append("")

        # Actions
        lines.append("## Actions")
        lines.append("")

        if sitrep.completed_actions:
            lines.append("### Completed")
            lines.append("")
            for action in sitrep.completed_actions:
                lines.append(f"- ✅ {action}")
            lines.append("")

        if sitrep.next_actions:
            lines.append("### Next Steps")
            lines.append("")
            for action in sitrep.next_actions:
                lines.append(f"- ⏭️  {action}")
            lines.append("")

        # Resources
        if sitrep.resources_used or sitrep.resources_needed:
            lines.append("## Resources")
            lines.append("")

            if sitrep.resources_used:
                lines.append("### Used")
                for resource in sitrep.resources_used:
                    lines.append(f"- {resource}")
                lines.append("")

            if sitrep.resources_needed:
                lines.append("### Needed")
                for resource in sitrep.resources_needed:
                    lines.append(f"- {resource}")
                lines.append("")

        # Notes
        if sitrep.notes:
            lines.append("## Additional Notes")
            lines.append("")
            lines.append(sitrep.notes)
            lines.append("")

        # Attachments
        if sitrep.attachments:
            lines.append("## Attachments")
            lines.append("")
            for attachment in sitrep.attachments:
                lines.append(f"- {attachment}")
            lines.append("")

        return '\n'.join(lines)

    @staticmethod
    def render_compact(sitrep: SITREP) -> str:
        """
        Render compact SITREP (single paragraph).

        Args:
            sitrep: SITREP object

        Returns:
            Compact string representation
        """
        status_emoji = SITREPTemplate._get_status_emoji(sitrep.overall_status)
        task_summary = sitrep.get_task_summary()

        parts = [
            f"SITREP [{sitrep.agent_name}]:",
            f"{status_emoji} {sitrep.overall_status.value}",
            f"({sitrep.completion_percentage:.0%} complete).",
        ]

        if sitrep.tasks:
            parts.append(
                f"Tasks: {task_summary['completed']}/{task_summary['total']} done, "
                f"{task_summary['in_progress']} in progress."
            )

        critical = sitrep.get_critical_items()
        if critical['critical_risks']:
            parts.append(f"⚠️ {len(critical['critical_risks'])} critical risks.")
        if critical['blocked_tasks']:
            parts.append(f"🚫 {len(critical['blocked_tasks'])} blocked tasks.")

        if sitrep.next_actions:
            parts.append(f"Next: {sitrep.next_actions[0]}")

        return ' '.join(parts)

    @staticmethod
    def render_text(sitrep: SITREP) -> str:
        """
        Render SITREP as plain text (military format).

        Args:
            sitrep: SITREP object

        Returns:
            Plain text SITREP
        """
        lines = []

        # Header
        lines.append("=" * 60)
        lines.append("SITUATION REPORT")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"FROM:     {sitrep.agent_name}")
        lines.append(f"MISSION:  {sitrep.mission}")
        lines.append(f"DTG:      {sitrep.timestamp.strftime('%d%H%M%SZ %b %Y')}")
        lines.append(f"REPORT:   #{sitrep.report_number}")
        lines.append(f"PRIORITY: {sitrep.priority.value}")
        lines.append("")

        # Status
        lines.append(f"STATUS:   {sitrep.overall_status.value}")
        lines.append(f"PROGRESS: {sitrep.completion_percentage:.1%}")
        lines.append("")

        # Situation
        lines.append("1. SITUATION:")
        lines.append("")
        if sitrep.situation_summary:
            for line in sitrep.situation_summary.split('\n'):
                lines.append(f"   {line}")
        lines.append("")

        # Tasks
        if sitrep.tasks:
            task_summary = sitrep.get_task_summary()
            lines.append("2. TASK STATUS:")
            lines.append("")
            lines.append(f"   Total Tasks:     {task_summary['total']}")
            lines.append(f"   Completed:       {task_summary['completed']}")
            lines.append(f"   In Progress:     {task_summary['in_progress']}")
            lines.append(f"   Pending:         {task_summary['pending']}")
            lines.append(f"   Blocked:         {task_summary['blocked']}")
            lines.append(f"   Failed:          {task_summary['failed']}")
            lines.append("")

        # Analysis
        if sitrep.findings or sitrep.risks:
            lines.append("3. ANALYSIS:")
            lines.append("")

            if sitrep.findings:
                lines.append("   Key Findings:")
                for finding in sitrep.findings:
                    lines.append(f"   - [{finding.impact.upper()}] {finding.description}")
                lines.append("")

            if sitrep.risks:
                lines.append("   Risks:")
                for risk in sitrep.risks:
                    lines.append(f"   - [{risk.severity.upper()}] {risk.description}")
                lines.append("")

        # Actions
        if sitrep.completed_actions or sitrep.next_actions:
            lines.append("4. ACTIONS:")
            lines.append("")

            if sitrep.completed_actions:
                lines.append("   Completed:")
                for action in sitrep.completed_actions:
                    lines.append(f"   - {action}")
                lines.append("")

            if sitrep.next_actions:
                lines.append("   Next Steps:")
                for action in sitrep.next_actions:
                    lines.append(f"   - {action}")
                lines.append("")

        # Resources
        if sitrep.resources_needed:
            lines.append("5. RESOURCES NEEDED:")
            lines.append("")
            for resource in sitrep.resources_needed:
                lines.append(f"   - {resource}")
            lines.append("")

        lines.append("=" * 60)
        lines.append("END SITREP")
        lines.append("=" * 60)

        return '\n'.join(lines)

    @staticmethod
    def _get_status_emoji(status: SITREPStatus) -> str:
        """Get emoji for SITREP status."""
        return {
            SITREPStatus.GREEN: '🟢',
            SITREPStatus.YELLOW: '🟡',
            SITREPStatus.RED: '🔴',
            SITREPStatus.COMPLETE: '✅',
        }.get(status, '⚪')

    @staticmethod
    def _get_task_emoji(status: TaskStatus) -> str:
        """Get emoji for task status."""
        return {
            TaskStatus.COMPLETED: '✅',
            TaskStatus.IN_PROGRESS: '🔄',
            TaskStatus.PENDING: '⏸️',
            TaskStatus.BLOCKED: '🚫',
            TaskStatus.FAILED: '❌',
        }.get(status, '⚪')

    @staticmethod
    def _get_impact_emoji(impact: str) -> str:
        """Get emoji for impact level."""
        return {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢',
        }.get(impact.lower(), '⚪')

    @staticmethod
    def _get_severity_emoji(severity: str) -> str:
        """Get emoji for severity level."""
        return {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢',
        }.get(severity.lower(), '⚪')

    @staticmethod
    def _get_metric_status_emoji(status: str) -> str:
        """Get emoji for metric status."""
        return {
            'on_track': '🟢',
            'at_risk': '🟡',
            'off_track': '🔴',
        }.get(status.lower(), '⚪')
