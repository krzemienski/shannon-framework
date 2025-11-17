// Event types from WebSocket server
export interface Event {
  type: string;
  data: any;
  timestamp: number;
}

export interface ExecutionState {
  taskName: string;
  status: 'idle' | 'running' | 'paused' | 'completed' | 'failed';
  progress: number;
  startTime: number | null;
  elapsedTime: number;
  estimatedTimeRemaining: number | null;
}

export interface Skill {
  id: string;
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  duration: number;
  startTime: number | null;
  endTime: number | null;
}

export interface FileChange {
  path: string;
  status: 'added' | 'modified' | 'deleted';
  diff: string;
  approved: boolean;
}

// Agent types - Using string union types instead of enums for erasableSyntaxOnly compatibility
export type AgentRole =
  | "research"
  | "analysis"
  | "testing"
  | "validation"
  | "git"
  | "planning"
  | "monitoring"
  | "generic";

export const AgentRole = {
  RESEARCH: "research" as AgentRole,
  ANALYSIS: "analysis" as AgentRole,
  TESTING: "testing" as AgentRole,
  VALIDATION: "validation" as AgentRole,
  GIT: "git" as AgentRole,
  PLANNING: "planning" as AgentRole,
  MONITORING: "monitoring" as AgentRole,
  GENERIC: "generic" as AgentRole
};

export type AgentStatus =
  | "idle"
  | "active"
  | "busy"
  | "failed"
  | "completed";

export const AgentStatus = {
  IDLE: "idle" as AgentStatus,
  ACTIVE: "active" as AgentStatus,
  BUSY: "busy" as AgentStatus,
  FAILED: "failed" as AgentStatus,
  COMPLETED: "completed" as AgentStatus
};

export interface Agent {
  agentId: string;
  role: AgentRole;
  status: AgentStatus;
  currentTask: string | null;
  tasksCompleted: number;
  tasksFailed: number;
  totalTime: number;
  lastActive: string;
}

export interface AgentPoolStats {
  totalAgents: number;
  activeAgents: number;
  idleAgents: number;
  maxActive: number;
  maxTotal: number;
  queuedTasks: number;
  completedTasks: number;
  failedTasks: number;
  totalProcessed: number;
  poolUptime: number;
}

// Decision types
export interface DecisionOption {
  optionId: string;
  label: string;
  description: string;
  action: string;
  consequences: string[];
  recommended: boolean;
}

export interface DecisionPoint {
  decisionId: string;
  title: string;
  description: string;
  options: DecisionOption[];
  priority: string;
  autoResolveSeconds?: number;
}

// Validation types
export interface ValidationResult {
  id: string;
  type: 'build' | 'test' | 'lint' | 'quality';
  status: 'pending' | 'running' | 'passed' | 'failed';
  message: string;
  details?: string;
  duration?: number;
  timestamp: string;
}

export interface ValidationLine {
  line: string;
  type: 'stdout' | 'stderr';
  checkName: string;
  timestamp: number;
}

export interface DashboardState {
  execution: ExecutionState;
  skills: Skill[];
  files: FileChange[];
  events: Event[];
  connected: boolean;
  agents: Agent[];
  agentStats: AgentPoolStats;
  pendingDecisions: DecisionPoint[];
  resolvedDecisions: DecisionPoint[];
  validationResults: ValidationResult[];
  isValidating: boolean;
  validationOutput: ValidationLine[];
}
