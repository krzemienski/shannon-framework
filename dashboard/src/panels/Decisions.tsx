/**
 * Decisions Panel
 *
 * Displays decision points with options:
 * - REDIRECT, INJECT, APPROVE, OVERRIDE
 * - Auto-resolve timeout
 * - Decision history
 *
 * Part of: Wave 8 - Full Dashboard
 */

import React, { useState } from 'react';

interface DecisionOption {
  optionId: string;
  label: string;
  description: string;
  action: string;
  consequences: string[];
  recommended: boolean;
}

interface DecisionPoint {
  decisionId: string;
  title: string;
  description: string;
  options: DecisionOption[];
  priority: string;
  autoResolveSeconds?: number;
}

interface DecisionsPanelProps {
  pendingDecisions: DecisionPoint[];
  resolvedDecisions: DecisionPoint[];
  onResolve: (decisionId: string, optionId: string) => void;
}

const DecisionsPanel: React.FC<DecisionsPanelProps> = ({
  pendingDecisions,
  resolvedDecisions,
  onResolve
}) => {
  const [selectedDecision, setSelectedDecision] = useState<string | null>(null);

  const getPriorityColor = (priority: string): string => {
    const colors = {
      critical: '#dc2626',
      high: '#ea580c',
      medium: '#f59e0b',
      low: '#84cc16'
    };
    return colors[priority as keyof typeof colors] || '#84cc16';
  };

  const getActionIcon = (action: string): string => {
    const icons = {
      redirect: '🔀',
      inject: '💉',
      approve: '✅',
      override: '⚠️',
      skip: '⏭️'
    };
    return icons[action as keyof typeof icons] || '📌';
  };

  return (
    <div className="decisions-panel">
      <div className="panel-header">
        <h2>Decision Points</h2>
        <div className="decision-stats">
          <span className="stat pending">{pendingDecisions.length} pending</span>
          <span className="stat resolved">{resolvedDecisions.length} resolved</span>
        </div>
      </div>

      {/* Pending decisions */}
      {pendingDecisions.length > 0 && (
        <div className="decision-section">
          <h3>Pending Decisions</h3>
          {pendingDecisions.map(decision => (
            <div
              key={decision.decisionId}
              className="decision-card pending"
              style={{
                borderLeftColor: getPriorityColor(decision.priority)
              }}
            >
              <div className="decision-header">
                <h4>{decision.title}</h4>
                <span
                  className="priority-badge"
                  style={{ background: getPriorityColor(decision.priority) }}
                >
                  {decision.priority}
                </span>
              </div>

              <p className="decision-description">{decision.description}</p>

              {decision.autoResolveSeconds && (
                <div className="auto-resolve-notice">
                  Auto-resolves in {decision.autoResolveSeconds}s
                </div>
              )}

              <div className="decision-options">
                {decision.options.map(option => (
                  <button
                    key={option.optionId}
                    className={`option-button ${option.recommended ? 'recommended' : ''}`}
                    onClick={() => onResolve(decision.decisionId, option.optionId)}
                  >
                    <span className="option-icon">{getActionIcon(option.action)}</span>
                    <div className="option-content">
                      <div className="option-label">{option.label}</div>
                      <div className="option-description">{option.description}</div>
                      {option.consequences.length > 0 && (
                        <div className="option-consequences">
                          {option.consequences.map((c, i) => (
                            <span key={i} className="consequence">{c}</span>
                          ))}
                        </div>
                      )}
                    </div>
                    {option.recommended && (
                      <span className="recommended-badge">Recommended</span>
                    )}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Resolved decisions history */}
      {resolvedDecisions.length > 0 && (
        <div className="decision-section">
          <h3>Recent Decisions</h3>
          <div className="decision-history">
            {resolvedDecisions.slice(-5).map(decision => (
              <div key={decision.decisionId} className="decision-history-item">
                <div className="history-title">{decision.title}</div>
                <div className="history-resolution">
                  <span className="resolution-icon">✓</span>
                  Resolved
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <style jsx>{`
        .decisions-panel {
          padding: 1rem;
          height: 100%;
          overflow-y: auto;
        }

        .panel-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1.5rem;
        }

        .panel-header h2 {
          margin: 0;
          color: #1e293b;
        }

        .decision-stats {
          display: flex;
          gap: 1rem;
        }

        .stat {
          font-size: 0.875rem;
          padding: 0.25rem 0.75rem;
          border-radius: 0.375rem;
        }

        .stat.pending {
          background: #fef3c7;
          color: #92400e;
        }

        .stat.resolved {
          background: #d1fae5;
          color: #065f46;
        }

        .decision-section {
          margin-bottom: 2rem;
        }

        .decision-section h3 {
          margin: 0 0 1rem 0;
          font-size: 1rem;
          color: #475569;
        }

        .decision-card {
          background: white;
          border: 1px solid #e2e8f0;
          border-left-width: 4px;
          border-radius: 0.5rem;
          padding: 1.25rem;
          margin-bottom: 1rem;
        }

        .decision-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 0.75rem;
        }

        .decision-header h4 {
          margin: 0;
          font-size: 1rem;
          color: #1e293b;
        }

        .priority-badge {
          font-size: 0.75rem;
          color: white;
          padding: 0.25rem 0.625rem;
          border-radius: 0.375rem;
          text-transform: uppercase;
          font-weight: 600;
        }

        .decision-description {
          color: #475569;
          font-size: 0.875rem;
          margin: 0 0 1rem 0;
          line-height: 1.5;
        }

        .auto-resolve-notice {
          background: #eff6ff;
          color: #1e40af;
          padding: 0.5rem 0.75rem;
          border-radius: 0.375rem;
          font-size: 0.875rem;
          margin-bottom: 1rem;
          border: 1px solid #bfdbfe;
        }

        .decision-options {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .option-button {
          display: flex;
          align-items: flex-start;
          gap: 0.75rem;
          padding: 1rem;
          background: #f8fafc;
          border: 2px solid #e2e8f0;
          border-radius: 0.5rem;
          cursor: pointer;
          text-align: left;
          transition: all 0.2s;
        }

        .option-button:hover {
          background: #f1f5f9;
          border-color: #cbd5e1;
        }

        .option-button.recommended {
          border-color: #3b82f6;
          background: #eff6ff;
        }

        .option-icon {
          font-size: 1.5rem;
          flex-shrink: 0;
        }

        .option-content {
          flex: 1;
        }

        .option-label {
          font-weight: 600;
          color: #1e293b;
          margin-bottom: 0.25rem;
        }

        .option-description {
          font-size: 0.875rem;
          color: #64748b;
          line-height: 1.4;
        }

        .option-consequences {
          display: flex;
          flex-wrap: wrap;
          gap: 0.375rem;
          margin-top: 0.5rem;
        }

        .consequence {
          font-size: 0.75rem;
          background: #fef3c7;
          color: #92400e;
          padding: 0.125rem 0.5rem;
          border-radius: 0.25rem;
        }

        .recommended-badge {
          flex-shrink: 0;
          background: #3b82f6;
          color: white;
          font-size: 0.75rem;
          padding: 0.375rem 0.75rem;
          border-radius: 0.375rem;
          font-weight: 600;
          align-self: center;
        }

        .decision-history {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .decision-history-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.75rem 1rem;
          background: #f8fafc;
          border-radius: 0.375rem;
          border: 1px solid #e2e8f0;
        }

        .history-title {
          font-size: 0.875rem;
          color: #475569;
        }

        .history-resolution {
          display: flex;
          align-items: center;
          gap: 0.375rem;
          font-size: 0.75rem;
          color: #059669;
        }

        .resolution-icon {
          font-size: 0.875rem;
        }
      `}</style>
    </div>
  );
};

export default DecisionsPanel;
