/**
 * Agent Pool Panel
 *
 * Displays agent pool status with:
 * - Active agents and their tasks
 * - Agent roles and specializations
 * - Task queue status
 * - Performance metrics per agent
 *
 * Part of: Wave 6 - Agent Coordination
 */

import React from 'react';
import type { Agent, AgentPoolStats } from '../types';
import { AgentRole, AgentStatus } from '../types';

interface AgentPoolPanelProps {
  agents: Agent[];
  stats: AgentPoolStats;
}

const AgentPoolPanel: React.FC<AgentPoolPanelProps> = ({ agents, stats }) => {
  // Group agents by status
  const activeAgents = agents.filter(a => a.status === AgentStatus.ACTIVE);
  const idleAgents = agents.filter(a => a.status === AgentStatus.IDLE);
  const failedAgents = agents.filter(a => a.status === AgentStatus.FAILED);

  // Get role color
  const getRoleColor = (role: AgentRole): string => {
    const colors = {
      [AgentRole.RESEARCH]: '#4A90E2',
      [AgentRole.ANALYSIS]: '#7B68EE',
      [AgentRole.TESTING]: '#50C878',
      [AgentRole.VALIDATION]: '#FFB347',
      [AgentRole.GIT]: '#FF6B6B',
      [AgentRole.PLANNING]: '#A78BFA',
      [AgentRole.MONITORING]: '#60A5FA',
      [AgentRole.GENERIC]: '#9CA3AF'
    };
    return colors[role] || '#9CA3AF';
  };

  // Get status icon
  const getStatusIcon = (status: AgentStatus): string => {
    const icons = {
      [AgentStatus.IDLE]: '⚪',
      [AgentStatus.ACTIVE]: '🔵',
      [AgentStatus.BUSY]: '🟡',
      [AgentStatus.FAILED]: '🔴',
      [AgentStatus.COMPLETED]: '🟢'
    };
    return icons[status] || '⚫';
  };

  return (
    <div className="agent-pool-panel">
      {/* Header with pool stats */}
      <div className="panel-header">
        <h2>Agent Pool</h2>
        <div className="pool-stats">
          <div className="stat">
            <span className="stat-label">Active</span>
            <span className="stat-value">{stats.activeAgents}/{stats.maxActive}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Total</span>
            <span className="stat-value">{stats.totalAgents}/{stats.maxTotal}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Queued</span>
            <span className="stat-value">{stats.queuedTasks}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Completed</span>
            <span className="stat-value">{stats.completedTasks}</span>
          </div>
        </div>
      </div>

      {/* Active agents section */}
      {activeAgents.length > 0 && (
        <div className="agent-section">
          <h3>Active Agents ({activeAgents.length})</h3>
          <div className="agent-list">
            {activeAgents.map(agent => (
              <div key={agent.agentId} className="agent-card active">
                <div className="agent-header">
                  <span className="status-icon">{getStatusIcon(agent.status)}</span>
                  <span
                    className="agent-role"
                    style={{ color: getRoleColor(agent.role) }}
                  >
                    {agent.role}
                  </span>
                  <span className="agent-id">{agent.agentId}</span>
                </div>
                {agent.currentTask && (
                  <div className="agent-task">
                    <div className="task-description">{agent.currentTask}</div>
                    <div className="task-progress">
                      <div className="progress-bar">
                        <div className="progress-fill" style={{ width: '60%' }} />
                      </div>
                    </div>
                  </div>
                )}
                <div className="agent-stats">
                  <span>Completed: {agent.tasksCompleted}</span>
                  <span>Failed: {agent.tasksFailed}</span>
                  <span>Time: {agent.totalTime.toFixed(1)}s</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Idle agents section */}
      {idleAgents.length > 0 && (
        <div className="agent-section">
          <h3>Idle Agents ({idleAgents.length})</h3>
          <div className="agent-grid">
            {idleAgents.map(agent => (
              <div key={agent.agentId} className="agent-chip idle">
                <span className="status-icon">{getStatusIcon(agent.status)}</span>
                <span
                  className="agent-role"
                  style={{ color: getRoleColor(agent.role) }}
                >
                  {agent.role}
                </span>
                <span className="agent-count">
                  {agent.tasksCompleted} tasks
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Failed agents section */}
      {failedAgents.length > 0 && (
        <div className="agent-section">
          <h3>Failed Agents ({failedAgents.length})</h3>
          <div className="agent-list">
            {failedAgents.map(agent => (
              <div key={agent.agentId} className="agent-card failed">
                <div className="agent-header">
                  <span className="status-icon">{getStatusIcon(agent.status)}</span>
                  <span className="agent-role">{agent.role}</span>
                  <span className="agent-id">{agent.agentId}</span>
                </div>
                {agent.currentTask && (
                  <div className="error-message">
                    Task failed: {agent.currentTask}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      <style>{`
        .agent-pool-panel {
          padding: 1rem;
          height: 100%;
          overflow-y: auto;
        }

        .panel-header {
          margin-bottom: 1.5rem;
        }

        .panel-header h2 {
          margin: 0 0 1rem 0;
          color: #1e293b;
        }

        .pool-stats {
          display: flex;
          gap: 1.5rem;
          flex-wrap: wrap;
        }

        .stat {
          display: flex;
          flex-direction: column;
        }

        .stat-label {
          font-size: 0.75rem;
          color: #64748b;
          text-transform: uppercase;
        }

        .stat-value {
          font-size: 1.25rem;
          font-weight: 600;
          color: #1e293b;
        }

        .agent-section {
          margin-bottom: 2rem;
        }

        .agent-section h3 {
          margin: 0 0 1rem 0;
          color: #475569;
          font-size: 1rem;
        }

        .agent-list {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .agent-card {
          background: white;
          border: 1px solid #e2e8f0;
          border-radius: 0.5rem;
          padding: 1rem;
        }

        .agent-card.active {
          border-color: #3b82f6;
          background: #eff6ff;
        }

        .agent-card.failed {
          border-color: #ef4444;
          background: #fef2f2;
        }

        .agent-header {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-bottom: 0.5rem;
        }

        .status-icon {
          font-size: 0.875rem;
        }

        .agent-role {
          font-weight: 600;
          text-transform: uppercase;
          font-size: 0.75rem;
        }

        .agent-id {
          color: #64748b;
          font-size: 0.75rem;
        }

        .agent-task {
          margin: 0.75rem 0;
        }

        .task-description {
          font-size: 0.875rem;
          color: #475569;
          margin-bottom: 0.5rem;
        }

        .task-progress {
          margin-top: 0.5rem;
        }

        .progress-bar {
          height: 4px;
          background: #e2e8f0;
          border-radius: 2px;
          overflow: hidden;
        }

        .progress-fill {
          height: 100%;
          background: #3b82f6;
          transition: width 0.3s ease;
        }

        .agent-stats {
          display: flex;
          gap: 1rem;
          font-size: 0.75rem;
          color: #64748b;
          margin-top: 0.75rem;
        }

        .agent-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
          gap: 0.5rem;
        }

        .agent-chip {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.5rem 0.75rem;
          background: white;
          border: 1px solid #e2e8f0;
          border-radius: 0.375rem;
          font-size: 0.875rem;
        }

        .agent-chip.idle {
          border-color: #cbd5e1;
        }

        .agent-count {
          color: #64748b;
          font-size: 0.75rem;
        }

        .error-message {
          color: #dc2626;
          font-size: 0.875rem;
          margin-top: 0.5rem;
        }
      `}</style>
    </div>
  );
};

export default AgentPoolPanel;
