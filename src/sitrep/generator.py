"""
Shannon Framework v4 - SITREP Generator

Helpers for creating SITREPs from various sources.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from .models import (
    SITREP, Task, Finding, Risk, Metric,
    SITREPStatus, SITREPPriority, TaskStatus
)


class SITREPGenerator:
    """Generate SITREPs from various data sources."""

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> SITREP:
        """
        Create SITREP from dictionary.

        Args:
            data: Dictionary with SITREP data

        Returns:
            SITREP instance
        """
        header = data.get('header', {})
        status = data.get('status', {})
        situation = data.get('situation', {})
        analysis = data.get('analysis', {})
        actions = data.get('actions', {})
        resources = data.get('resources', {})

        # Parse timestamp
        timestamp = header.get('timestamp')
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        elif not timestamp:
            timestamp = datetime.now()

        # Parse tasks
        tasks = []
        for task_data in situation.get('tasks', []):
            tasks.append(Task(
                id=task_data['id'],
                description=task_data['description'],
                status=TaskStatus[task_data['status']],
                assignee=task_data.get('assignee'),
                completion=task_data.get('completion', 0.0),
                notes=task_data.get('notes'),
                dependencies=task_data.get('dependencies', [])
            ))

        # Parse findings
        findings = []
        for finding_data in analysis.get('findings', []):
            findings.append(Finding(
                category=finding_data['category'],
                description=finding_data['description'],
                impact=finding_data['impact'],
                recommendation=finding_data.get('recommendation')
            ))

        # Parse risks
        risks = []
        for risk_data in analysis.get('risks', []):
            risks.append(Risk(
                description=risk_data['description'],
                severity=risk_data['severity'],
                mitigation=risk_data.get('mitigation'),
                owner=risk_data.get('owner')
            ))

        # Parse metrics
        metrics = []
        for metric_data in analysis.get('metrics', []):
            metrics.append(Metric(
                name=metric_data['name'],
                value=metric_data['value'],
                unit=metric_data.get('unit'),
                target=metric_data.get('target'),
                status=metric_data.get('status')
            ))

        return SITREP(
            agent_name=header['agent_name'],
            mission=header['mission'],
            timestamp=timestamp,
            report_number=header.get('report_number', 1),
            priority=SITREPPriority[header.get('priority', 'ROUTINE')],
            overall_status=SITREPStatus[status.get('overall_status', 'GREEN')],
            completion_percentage=status.get('completion_percentage', 0.0),
            situation_summary=situation.get('summary', ''),
            tasks=tasks,
            findings=findings,
            risks=risks,
            metrics=metrics,
            completed_actions=actions.get('completed', []),
            next_actions=actions.get('next', []),
            resources_used=resources.get('used', []),
            resources_needed=resources.get('needed', []),
            notes=data.get('notes'),
            attachments=data.get('attachments', []),
            metadata=data.get('metadata', {})
        )

    @staticmethod
    def create_simple(
        agent_name: str,
        mission: str,
        status: str = "GREEN",
        summary: str = "",
        completed: List[str] = None,
        next_steps: List[str] = None
    ) -> SITREP:
        """
        Create simple SITREP with minimal information.

        Args:
            agent_name: Name of reporting agent
            mission: Mission description
            status: Status (GREEN/YELLOW/RED/COMPLETE)
            summary: Situation summary
            completed: Completed actions
            next_steps: Next actions

        Returns:
            SITREP instance
        """
        return SITREP(
            agent_name=agent_name,
            mission=mission,
            overall_status=SITREPStatus[status],
            situation_summary=summary,
            completed_actions=completed or [],
            next_actions=next_steps or []
        )

    @staticmethod
    def create_from_tasks(
        agent_name: str,
        mission: str,
        tasks: List[Dict[str, Any]]
    ) -> SITREP:
        """
        Create SITREP from task list.

        Args:
            agent_name: Name of reporting agent
            mission: Mission description
            tasks: List of task dictionaries

        Returns:
            SITREP instance with tasks
        """
        sitrep = SITREP(
            agent_name=agent_name,
            mission=mission
        )

        for task_data in tasks:
            task = Task(
                id=task_data['id'],
                description=task_data['description'],
                status=TaskStatus[task_data.get('status', 'PENDING')],
                assignee=task_data.get('assignee'),
                completion=task_data.get('completion', 0.0),
                notes=task_data.get('notes'),
                dependencies=task_data.get('dependencies', [])
            )
            sitrep.add_task(task)

        sitrep.update_status()
        return sitrep

    @staticmethod
    def create_research_sitrep(
        agent_name: str,
        research_topic: str,
        findings: List[Dict[str, Any]],
        confidence: float = 0.0,
        recommendations: List[str] = None
    ) -> SITREP:
        """
        Create SITREP for research agents.

        Args:
            agent_name: Name of research agent
            research_topic: Topic being researched
            findings: List of finding dictionaries
            confidence: Overall confidence score
            recommendations: List of recommendations

        Returns:
            Research SITREP
        """
        sitrep = SITREP(
            agent_name=agent_name,
            mission=f"Research: {research_topic}",
            situation_summary=f"Research investigation into {research_topic}"
        )

        # Add findings
        for finding_data in findings:
            finding = Finding(
                category=finding_data.get('category', 'research'),
                description=finding_data['description'],
                impact=finding_data.get('impact', 'medium'),
                recommendation=finding_data.get('recommendation')
            )
            sitrep.add_finding(finding)

        # Add confidence metric
        sitrep.add_metric(Metric(
            name='Research Confidence',
            value=confidence,
            unit='%',
            target=0.90,
            status='on_track' if confidence >= 0.90 else 'at_risk'
        ))

        # Add recommendations as next actions
        if recommendations:
            sitrep.next_actions = recommendations

        sitrep.update_status()
        return sitrep

    @staticmethod
    def merge_sitreps(sitreps: List[SITREP], merged_agent_name: str, merged_mission: str) -> SITREP:
        """
        Merge multiple SITREPs into one consolidated report.

        Args:
            sitreps: List of SITREPs to merge
            merged_agent_name: Name for merged SITREP
            merged_mission: Mission for merged SITREP

        Returns:
            Consolidated SITREP
        """
        if not sitreps:
            return SITREP(
                agent_name=merged_agent_name,
                mission=merged_mission
            )

        merged = SITREP(
            agent_name=merged_agent_name,
            mission=merged_mission,
            timestamp=datetime.now(),
            report_number=1
        )

        # Collect all data from source SITREPs
        for sitrep in sitreps:
            # Merge tasks (prefix with agent name to avoid ID conflicts)
            for task in sitrep.tasks:
                merged_task = Task(
                    id=f"{sitrep.agent_name}:{task.id}",
                    description=task.description,
                    status=task.status,
                    assignee=task.assignee or sitrep.agent_name,
                    completion=task.completion,
                    notes=task.notes,
                    dependencies=task.dependencies
                )
                merged.add_task(merged_task)

            # Merge findings
            for finding in sitrep.findings:
                merged.add_finding(finding)

            # Merge risks
            for risk in sitrep.risks:
                merged.add_risk(risk)

            # Merge metrics (prefix with agent name)
            for metric in sitrep.metrics:
                merged_metric = Metric(
                    name=f"{sitrep.agent_name}: {metric.name}",
                    value=metric.value,
                    unit=metric.unit,
                    target=metric.target,
                    status=metric.status
                )
                merged.add_metric(merged_metric)

            # Merge actions
            for action in sitrep.completed_actions:
                merged.completed_actions.append(f"[{sitrep.agent_name}] {action}")

            for action in sitrep.next_actions:
                merged.next_actions.append(f"[{sitrep.agent_name}] {action}")

            # Merge resources
            merged.resources_used.extend(sitrep.resources_used)
            merged.resources_needed.extend(sitrep.resources_needed)

        # Deduplicate resources
        merged.resources_used = list(set(merged.resources_used))
        merged.resources_needed = list(set(merged.resources_needed))

        # Build summary
        merged.situation_summary = f"Consolidated report from {len(sitreps)} agents: " + \
                                  ", ".join(s.agent_name for s in sitreps)

        # Update status
        merged.update_status()

        return merged

    @staticmethod
    def create_wave_sitrep(
        wave_number: int,
        wave_name: str,
        tasks: List[Dict[str, Any]],
        metrics: Dict[str, Any] = None
    ) -> SITREP:
        """
        Create SITREP for wave execution.

        Args:
            wave_number: Wave number
            wave_name: Wave name
            tasks: List of task dictionaries
            metrics: Optional metrics dictionary

        Returns:
            Wave execution SITREP
        """
        sitrep = SITREPGenerator.create_from_tasks(
            agent_name=f"Wave {wave_number}",
            mission=f"Wave {wave_number}: {wave_name}",
            tasks=tasks
        )

        # Add wave-specific metrics
        if metrics:
            for name, value in metrics.items():
                sitrep.add_metric(Metric(
                    name=name,
                    value=value
                ))

        return sitrep
