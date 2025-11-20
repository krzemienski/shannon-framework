"""
Shannon Framework v4 - SITREP Models

Data structures for military-style Situation Reports.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class SITREPStatus(Enum):
    """SITREP status types."""
    GREEN = "GREEN"      # All systems nominal
    YELLOW = "YELLOW"    # Minor issues, continuing
    RED = "RED"          # Critical issues, blocked
    COMPLETE = "COMPLETE"  # Mission complete


class SITREPPriority(Enum):
    """SITREP priority levels."""
    ROUTINE = "ROUTINE"
    PRIORITY = "PRIORITY"
    IMMEDIATE = "IMMEDIATE"
    FLASH = "FLASH"


class TaskStatus(Enum):
    """Individual task status."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"


@dataclass
class Task:
    """Individual task within a SITREP."""
    id: str
    description: str
    status: TaskStatus
    assignee: Optional[str] = None
    completion: float = 0.0  # 0.0 to 1.0
    notes: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status.value,
            'assignee': self.assignee,
            'completion': self.completion,
            'notes': self.notes,
            'dependencies': self.dependencies,
        }


@dataclass
class Finding:
    """Key finding or discovery."""
    category: str  # e.g., "technical", "architectural", "risk"
    description: str
    impact: str  # "high", "medium", "low"
    recommendation: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'category': self.category,
            'description': self.description,
            'impact': self.impact,
            'recommendation': self.recommendation,
        }


@dataclass
class Risk:
    """Identified risk or blocker."""
    description: str
    severity: str  # "critical", "high", "medium", "low"
    mitigation: Optional[str] = None
    owner: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'description': self.description,
            'severity': self.severity,
            'mitigation': self.mitigation,
            'owner': self.owner,
        }


@dataclass
class Metric:
    """Quantitative metric."""
    name: str
    value: Any
    unit: Optional[str] = None
    target: Optional[Any] = None
    status: Optional[str] = None  # "on_track", "at_risk", "off_track"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'value': self.value,
            'unit': self.unit,
            'target': self.target,
            'status': self.status,
        }


@dataclass
class SITREP:
    """
    Military-style Situation Report.

    Standard format for agent communication and status reporting.
    """
    # Header
    agent_name: str
    mission: str
    timestamp: datetime = field(default_factory=datetime.now)
    report_number: int = 1
    priority: SITREPPriority = SITREPPriority.ROUTINE

    # Status
    overall_status: SITREPStatus = SITREPStatus.GREEN
    completion_percentage: float = 0.0

    # Situation
    situation_summary: str = ""
    tasks: List[Task] = field(default_factory=list)

    # Analysis
    findings: List[Finding] = field(default_factory=list)
    risks: List[Risk] = field(default_factory=list)
    metrics: List[Metric] = field(default_factory=list)

    # Actions
    completed_actions: List[str] = field(default_factory=list)
    next_actions: List[str] = field(default_factory=list)

    # Resources
    resources_used: List[str] = field(default_factory=list)
    resources_needed: List[str] = field(default_factory=list)

    # Additional context
    notes: Optional[str] = None
    attachments: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert SITREP to dictionary."""
        return {
            'header': {
                'agent_name': self.agent_name,
                'mission': self.mission,
                'timestamp': self.timestamp.isoformat(),
                'report_number': self.report_number,
                'priority': self.priority.value,
            },
            'status': {
                'overall_status': self.overall_status.value,
                'completion_percentage': self.completion_percentage,
            },
            'situation': {
                'summary': self.situation_summary,
                'tasks': [task.to_dict() for task in self.tasks],
            },
            'analysis': {
                'findings': [f.to_dict() for f in self.findings],
                'risks': [r.to_dict() for r in self.risks],
                'metrics': [m.to_dict() for m in self.metrics],
            },
            'actions': {
                'completed': self.completed_actions,
                'next': self.next_actions,
            },
            'resources': {
                'used': self.resources_used,
                'needed': self.resources_needed,
            },
            'notes': self.notes,
            'attachments': self.attachments,
            'metadata': self.metadata,
        }

    def get_task_summary(self) -> Dict[str, int]:
        """Get task status summary."""
        summary = {
            'total': len(self.tasks),
            'completed': 0,
            'in_progress': 0,
            'blocked': 0,
            'failed': 0,
            'pending': 0,
        }

        for task in self.tasks:
            if task.status == TaskStatus.COMPLETED:
                summary['completed'] += 1
            elif task.status == TaskStatus.IN_PROGRESS:
                summary['in_progress'] += 1
            elif task.status == TaskStatus.BLOCKED:
                summary['blocked'] += 1
            elif task.status == TaskStatus.FAILED:
                summary['failed'] += 1
            elif task.status == TaskStatus.PENDING:
                summary['pending'] += 1

        return summary

    def get_critical_items(self) -> Dict[str, List]:
        """Get critical risks and blockers."""
        critical_risks = [
            r for r in self.risks
            if r.severity in ['critical', 'high']
        ]

        blocked_tasks = [
            t for t in self.tasks
            if t.status == TaskStatus.BLOCKED
        ]

        failed_tasks = [
            t for t in self.tasks
            if t.status == TaskStatus.FAILED
        ]

        return {
            'critical_risks': [r.to_dict() for r in critical_risks],
            'blocked_tasks': [t.to_dict() for t in blocked_tasks],
            'failed_tasks': [t.to_dict() for t in failed_tasks],
        }

    def calculate_completion(self) -> float:
        """
        Calculate overall completion percentage from tasks.

        Returns:
            Completion percentage (0.0 to 1.0)
        """
        if not self.tasks:
            return self.completion_percentage

        total_completion = sum(task.completion for task in self.tasks)
        return total_completion / len(self.tasks)

    def update_status(self):
        """Update overall status based on tasks and risks."""
        # Check for critical issues
        critical_items = self.get_critical_items()

        if critical_items['blocked_tasks'] or critical_items['failed_tasks']:
            self.overall_status = SITREPStatus.RED
        elif critical_items['critical_risks']:
            self.overall_status = SITREPStatus.YELLOW
        elif self.completion_percentage >= 1.0:
            self.overall_status = SITREPStatus.COMPLETE
        else:
            self.overall_status = SITREPStatus.GREEN

        # Update completion percentage
        self.completion_percentage = self.calculate_completion()

    def add_task(self, task: Task):
        """Add a task to the SITREP."""
        self.tasks.append(task)
        self.update_status()

    def add_finding(self, finding: Finding):
        """Add a finding to the SITREP."""
        self.findings.append(finding)

    def add_risk(self, risk: Risk):
        """Add a risk to the SITREP."""
        self.risks.append(risk)
        self.update_status()

    def add_metric(self, metric: Metric):
        """Add a metric to the SITREP."""
        self.metrics.append(metric)
