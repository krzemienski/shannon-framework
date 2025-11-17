/**
 * Shannon Dashboard Store
 *
 * Global state management using Zustand
 */
import { create } from 'zustand';

// Types
export interface DecisionOption {
  id: string;
  label: string;
  description: string;
  confidence: number;
  pros?: string[];
  cons?: string[];
}

export interface Decision {
  id: string;
  question: string;
  options: DecisionOption[];
  status: 'pending' | 'approved' | 'rejected';
  selected_option_id?: string;
  auto_approved: boolean;
  context?: Record<string, any>;
  created_at: string;
  approved_at?: string;
}

export interface DashboardEvent {
  type: string;
  data: any;
  timestamp: number;
}

interface DashboardState {
  // Connection
  connected: boolean;
  connectionId?: string;

  // Decisions
  decisions: Decision[];
  pendingDecisions: Decision[];

  // Events
  events: DashboardEvent[];

  // Actions
  setConnected: (connected: boolean, connectionId?: string) => void;
  addDecision: (decision: Decision) => void;
  updateDecision: (decisionId: string, updates: Partial<Decision>) => void;
  approveDecision: (decisionId: string, selectedOptionId: string) => void;
  addEvent: (event: DashboardEvent) => void;
  handleSocketEvent: (eventType: string, data: any) => void;
}

export const useDashboardStore = create<DashboardState>((set, get) => ({
  // Initial state
  connected: false,
  decisions: [],
  pendingDecisions: [],
  events: [],

  // Connection actions
  setConnected: (connected, connectionId) => set({ connected, connectionId }),

  // Decision actions
  addDecision: (decision) => set((state) => ({
    decisions: [...state.decisions, decision],
    pendingDecisions: decision.status === 'pending'
      ? [...state.pendingDecisions, decision]
      : state.pendingDecisions
  })),

  updateDecision: (decisionId, updates) => set((state) => ({
    decisions: state.decisions.map(d =>
      d.id === decisionId ? { ...d, ...updates } : d
    ),
    pendingDecisions: state.pendingDecisions
      .map(d => d.id === decisionId ? { ...d, ...updates } : d)
      .filter(d => d.status === 'pending')
  })),

  approveDecision: (decisionId, selectedOptionId) => {
    const state = get();
    const decision = state.decisions.find(d => d.id === decisionId);

    if (decision) {
      set((state) => ({
        decisions: state.decisions.map(d =>
          d.id === decisionId
            ? { ...d, status: 'approved' as const, selected_option_id: selectedOptionId, approved_at: new Date().toISOString() }
            : d
        ),
        pendingDecisions: state.pendingDecisions.filter(d => d.id !== decisionId)
      }));
    }
  },

  // Event actions
  addEvent: (event) => set((state) => ({
    events: [...state.events, event]
  })),

  // Socket event handler
  handleSocketEvent: (eventType, data) => {
    const state = get();

    switch (eventType) {
      case 'connection_status':
        state.setConnected(data.status === 'connected', data.sid);
        break;

      case 'decision:requested':
        state.addDecision({
          id: data.id,
          question: data.question,
          options: data.options,
          status: data.status || 'pending',
          auto_approved: false,
          context: data.context,
          created_at: data.created_at
        });
        break;

      case 'decision:approved':
        state.updateDecision(data.decision_id, {
          status: 'approved',
          selected_option_id: data.selected_option,
          approved_at: data.timestamp
        });
        break;

      case 'decisions:pending':
        // Bulk update of pending decisions
        set({ pendingDecisions: data.decisions });
        break;

      default:
        // Add to event log
        state.addEvent({
          type: eventType,
          data,
          timestamp: Date.now()
        });
        break;
    }
  }
}));
