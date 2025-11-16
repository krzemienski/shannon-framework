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

// Agent types
export enum AgentRole {
  RESEARCH = "research",
  ANALYSIS = "analysis",
  TESTING = "testing",
  VALIDATION = "validation",
  GIT = "git",
  PLANNING = "planning",
  MONITORING = "monitoring",
  GENERIC = "generic"
}

export enum AgentStatus {
  IDLE = "idle",
  ACTIVE = "active",
  BUSY = "busy",
  FAILED = "failed",
  COMPLETED = "completed"
}

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
}
