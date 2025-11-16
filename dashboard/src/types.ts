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

export interface DashboardState {
  execution: ExecutionState;
  skills: Skill[];
  files: FileChange[];
  events: Event[];
  connected: boolean;
}
