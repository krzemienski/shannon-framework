"""Shannon Orchestration Layer - Main user-facing orchestration system.

This package provides the complete orchestration layer that ties together
task parsing, execution planning, state management, and the shannon do command.

Components:
- TaskParser: Parse natural language tasks into structured intent
- ExecutionPlanner: Create execution plans with dependency resolution
- StateManager: Checkpoint and rollback management
- Orchestrator: Main execution coordinator

Created for: Wave 5 - Orchestration Layer
Purpose: Provide the main user-facing shannon do command
"""

from shannon.orchestration.task_parser import TaskParser, ParsedTask, TaskIntent
from shannon.orchestration.planner import ExecutionPlanner, ExecutionPlan
from shannon.orchestration.state_manager import StateManager, Checkpoint
from shannon.orchestration.orchestrator import Orchestrator

__all__ = [
    'TaskParser',
    'ParsedTask',
    'TaskIntent',
    'ExecutionPlanner',
    'ExecutionPlan',
    'StateManager',
    'Checkpoint',
    'Orchestrator',
]
