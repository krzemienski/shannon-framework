"""
Shannon Skills Framework - Core Data Models

Defines the fundamental data structures for the skills framework:
- Skill definitions and metadata
- Execution results and states
- Parameters and validation
- Hooks and dependencies
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime


class ExecutionType(Enum):
    """Types of skill execution"""
    NATIVE = "native"      # Python module.class.method
    SCRIPT = "script"      # Shell script/executable
    MCP = "mcp"           # MCP server tool
    COMPOSITE = "composite"  # Multiple skills orchestrated


class SkillStatus(Enum):
    """Skill execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class HookTrigger(Enum):
    """When hooks should execute"""
    PRE = "pre"      # Before main execution
    POST = "post"    # After successful execution
    ERROR = "error"  # On execution failure


@dataclass
class Parameter:
    """Skill parameter definition"""
    name: str
    type: str  # string, integer, float, boolean, array, object
    required: bool = False
    default: Any = None
    description: str = ""
    validation: Optional[str] = None  # Regex pattern for strings

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Parameter':
        """Create from dictionary"""
        return cls(
            name=data['name'],
            type=data['type'],
            required=data.get('required', False),
            default=data.get('default'),
            description=data.get('description', ''),
            validation=data.get('validation')
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'name': self.name,
            'type': self.type,
            'required': self.required,
            'default': self.default,
            'description': self.description,
            'validation': self.validation
        }


@dataclass
class Hooks:
    """Skill lifecycle hooks"""
    pre: List[str] = field(default_factory=list)    # Run before execution
    post: List[str] = field(default_factory=list)   # Run after success
    error: List[str] = field(default_factory=list)  # Run on failure

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Hooks':
        """Create from dictionary"""
        return cls(
            pre=data.get('pre', []),
            post=data.get('post', []),
            error=data.get('error', [])
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'pre': self.pre,
            'post': self.post,
            'error': self.error
        }


@dataclass
class Execution:
    """Skill execution configuration"""
    type: ExecutionType

    # For native (Python) execution
    module: Optional[str] = None
    class_name: Optional[str] = None
    method: Optional[str] = None

    # For script execution
    script: Optional[str] = None

    # For MCP execution
    mcp_server: Optional[str] = None
    mcp_tool: Optional[str] = None

    # For composite execution
    skills: Optional[List[Any]] = None  # List of skill names or configs

    # General execution config
    timeout: int = 300  # seconds
    retry: int = 0      # retry attempts

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Execution':
        """Create from dictionary"""
        exec_type = ExecutionType(data['type'])

        return cls(
            type=exec_type,
            module=data.get('module'),
            class_name=data.get('class'),
            method=data.get('method'),
            script=data.get('script'),
            mcp_server=data.get('mcp_server'),
            mcp_tool=data.get('mcp_tool'),
            skills=data.get('skills'),
            timeout=data.get('timeout', 300),
            retry=data.get('retry', 0)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        result = {
            'type': self.type.value,
            'timeout': self.timeout,
            'retry': self.retry
        }

        if self.module:
            result['module'] = self.module
        if self.class_name:
            result['class'] = self.class_name
        if self.method:
            result['method'] = self.method
        if self.script:
            result['script'] = self.script
        if self.mcp_server:
            result['mcp_server'] = self.mcp_server
        if self.mcp_tool:
            result['mcp_tool'] = self.mcp_tool
        if self.skills:
            result['skills'] = self.skills

        return result


@dataclass
class SkillMetadata:
    """Skill metadata for tracking and analytics"""
    author: str = "Shannon Framework"
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    auto_generated: bool = False
    usage_count: int = 0
    success_rate: float = 1.0
    avg_duration: float = 0.0
    tags: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillMetadata':
        """Create from dictionary"""
        created = data.get('created')
        updated = data.get('updated')

        return cls(
            author=data.get('author', 'Shannon Framework'),
            created=datetime.fromisoformat(created) if created else None,
            updated=datetime.fromisoformat(updated) if updated else None,
            auto_generated=data.get('auto_generated', False),
            usage_count=data.get('usage_count', 0),
            success_rate=data.get('success_rate', 1.0),
            avg_duration=data.get('avg_duration', 0.0),
            tags=data.get('tags', [])
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'author': self.author,
            'created': self.created.isoformat() if self.created else None,
            'updated': self.updated.isoformat() if self.updated else None,
            'auto_generated': self.auto_generated,
            'usage_count': self.usage_count,
            'success_rate': self.success_rate,
            'avg_duration': self.avg_duration,
            'tags': self.tags
        }


@dataclass
class Skill:
    """Complete skill definition"""
    name: str
    version: str
    description: str
    execution: Execution

    category: str = "other"
    parameters: List[Parameter] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    hooks: Hooks = field(default_factory=Hooks)
    validation: Optional[Dict[str, Any]] = None
    metadata: SkillMetadata = field(default_factory=SkillMetadata)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Skill':
        """Create skill from dictionary (loaded from YAML/JSON)"""
        return cls(
            name=data['name'],
            version=data['version'],
            description=data['description'],
            category=data.get('category', 'other'),
            parameters=[Parameter.from_dict(p) for p in data.get('parameters', [])],
            dependencies=data.get('dependencies', []),
            hooks=Hooks.from_dict(data.get('hooks', {})),
            execution=Execution.from_dict(data['execution']),
            validation=data.get('validation'),
            metadata=SkillMetadata.from_dict(data.get('metadata', {}))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'category': self.category,
            'parameters': [p.to_dict() for p in self.parameters],
            'dependencies': self.dependencies,
            'hooks': self.hooks.to_dict(),
            'execution': self.execution.to_dict(),
            'validation': self.validation,
            'metadata': self.metadata.to_dict()
        }

    def get_parameter(self, name: str) -> Optional[Parameter]:
        """Get parameter by name"""
        for param in self.parameters:
            if param.name == name:
                return param
        return None


@dataclass
class SkillResult:
    """Result of skill execution"""
    skill_name: str
    success: bool
    data: Any = None
    error: Optional[str] = None
    duration: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    checkpoint_id: Optional[str] = None
    hooks_executed: Dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'skill_name': self.skill_name,
            'success': self.success,
            'data': self.data,
            'error': self.error,
            'duration': self.duration,
            'timestamp': self.timestamp.isoformat(),
            'checkpoint_id': self.checkpoint_id,
            'hooks_executed': self.hooks_executed
        }


@dataclass
class ExecutionContext:
    """Context for skill execution"""
    task: str
    variables: Dict[str, Any] = field(default_factory=dict)
    skill_results: List[SkillResult] = field(default_factory=list)
    checkpoints: List[Any] = field(default_factory=list)
    decision_history: List[Dict] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)

    def add_result(self, result: SkillResult):
        """Add skill result to context"""
        self.skill_results.append(result)

    def get_result(self, skill_name: str) -> Optional[SkillResult]:
        """Get result of previous skill"""
        for result in reversed(self.skill_results):
            if result.skill_name == skill_name:
                return result
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'task': self.task,
            'variables': self.variables,
            'skill_results': [r.to_dict() for r in self.skill_results],
            'checkpoints': [c.id for c in self.checkpoints],
            'decision_history': self.decision_history,
            'constraints': self.constraints
        }


@dataclass
class AgentState:
    """State of an execution agent"""
    agent_id: str
    role: str  # research, analysis, testing, validation, git_ops, planning, monitoring
    task: str
    status: SkillStatus
    progress: float = 0.0  # 0.0 to 1.0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'agent_id': self.agent_id,
            'role': self.role,
            'task': self.task,
            'status': self.status.value,
            'progress': self.progress,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'result': self.result,
            'error': self.error
        }


# Re-export from executor.models for backward compatibility
from shannon.executor.models import LibraryRecommendation

__all__ = [
    'ExecutionType',
    'SkillStatus',
    'HookTrigger',
    'Parameter',
    'Hooks',
    'Execution',
    'SkillMetadata',
    'Skill',
    'SkillResult',
    'ExecutionContext',
    'AgentState',
    'LibraryRecommendation',
]
