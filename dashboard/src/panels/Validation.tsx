/**
 * Validation Panel
 *
 * Streams validation results in real-time:
 * - Build validation
 * - Test execution
 * - Static analysis
 * - Quality metrics
 *
 * Part of: Wave 8 - Full Dashboard
 */

import React from 'react';

interface ValidationResult {
  id: string;
  type: 'build' | 'test' | 'lint' | 'quality';
  status: 'pending' | 'running' | 'passed' | 'failed';
  message: string;
  details?: string;
  duration?: number;
  timestamp: string;
}

interface ValidationPanelProps {
  results: ValidationResult[];
  isValidating: boolean;
}

const ValidationPanel: React.FC<ValidationPanelProps> = ({
  results,
  isValidating
}) => {
  const getStatusIcon = (status: string): string => {
    const icons = {
      pending: '⏳',
      running: '🔄',
      passed: '✅',
      failed: '❌'
    };
    return icons[status as keyof typeof icons] || '⚪';
  };

  const getStatusColor = (status: string): string => {
    const colors = {
      pending: '#94a3b8',
      running: '#3b82f6',
      passed: '#10b981',
      failed: '#ef4444'
    };
    return colors[status as keyof typeof icons] || '#94a3b8';
  };

  const getTypeLabel = (type: string): string => {
    const labels = {
      build: 'Build',
      test: 'Tests',
      lint: 'Lint',
      quality: 'Quality'
    };
    return labels[type as keyof typeof labels] || type;
  };

  // Calculate summary stats
  const summary = {
    total: results.length,
    passed: results.filter(r => r.status === 'passed').length,
    failed: results.filter(r => r.status === 'failed').length,
    running: results.filter(r => r.status === 'running').length
  };

  return (
    <div className="validation-panel">
      <div className="panel-header">
        <h2>Validation</h2>
        {isValidating && (
          <div className="validating-indicator">
            <span className="spinner">🔄</span>
            <span>Validating...</span>
          </div>
        )}
      </div>

      {/* Summary */}
      {results.length > 0 && (
        <div className="validation-summary">
          <div className="summary-item">
            <span className="summary-label">Total</span>
            <span className="summary-value">{summary.total}</span>
          </div>
          <div className="summary-item passed">
            <span className="summary-label">Passed</span>
            <span className="summary-value">{summary.passed}</span>
          </div>
          {summary.failed > 0 && (
            <div className="summary-item failed">
              <span className="summary-label">Failed</span>
              <span className="summary-value">{summary.failed}</span>
            </div>
          )}
          {summary.running > 0 && (
            <div className="summary-item running">
              <span className="summary-label">Running</span>
              <span className="summary-value">{summary.running}</span>
            </div>
          )}
        </div>
      )}

      {/* Validation results */}
      <div className="validation-results">
        {results.map(result => (
          <div
            key={result.id}
            className={`validation-result ${result.status}`}
          >
            <div className="result-header">
              <span
                className="result-icon"
                style={{ color: getStatusColor(result.status) }}
              >
                {getStatusIcon(result.status)}
              </span>
              <span className="result-type">{getTypeLabel(result.type)}</span>
              {result.duration && (
                <span className="result-duration">{result.duration}ms</span>
              )}
            </div>

            <div className="result-message">{result.message}</div>

            {result.details && (
              <div className="result-details">
                <pre>{result.details}</pre>
              </div>
            )}

            <div className="result-timestamp">
              {new Date(result.timestamp).toLocaleTimeString()}
            </div>
          </div>
        ))}
      </div>

      {results.length === 0 && !isValidating && (
        <div className="empty-state">
          <div className="empty-icon">📋</div>
          <div className="empty-message">No validation results yet</div>
        </div>
      )}

      <style jsx>{`
        .validation-panel {
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

        .validating-indicator {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          color: #3b82f6;
          font-size: 0.875rem;
        }

        .spinner {
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        .validation-summary {
          display: flex;
          gap: 1rem;
          padding: 1rem;
          background: #f8fafc;
          border-radius: 0.5rem;
          margin-bottom: 1.5rem;
        }

        .summary-item {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }

        .summary-label {
          font-size: 0.75rem;
          color: #64748b;
          text-transform: uppercase;
        }

        .summary-value {
          font-size: 1.5rem;
          font-weight: 600;
          color: #1e293b;
        }

        .summary-item.passed .summary-value {
          color: #10b981;
        }

        .summary-item.failed .summary-value {
          color: #ef4444;
        }

        .summary-item.running .summary-value {
          color: #3b82f6;
        }

        .validation-results {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .validation-result {
          background: white;
          border: 1px solid #e2e8f0;
          border-radius: 0.5rem;
          padding: 1rem;
          transition: all 0.2s;
        }

        .validation-result.passed {
          border-left: 4px solid #10b981;
          background: #f0fdf4;
        }

        .validation-result.failed {
          border-left: 4px solid #ef4444;
          background: #fef2f2;
        }

        .validation-result.running {
          border-left: 4px solid #3b82f6;
          background: #eff6ff;
        }

        .result-header {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 0.5rem;
        }

        .result-icon {
          font-size: 1.25rem;
        }

        .result-type {
          font-weight: 600;
          color: #1e293b;
          font-size: 0.875rem;
          text-transform: uppercase;
        }

        .result-duration {
          margin-left: auto;
          font-size: 0.75rem;
          color: #64748b;
        }

        .result-message {
          color: #475569;
          font-size: 0.875rem;
          line-height: 1.5;
          margin-bottom: 0.5rem;
        }

        .result-details {
          background: #f8fafc;
          border: 1px solid #e2e8f0;
          border-radius: 0.375rem;
          padding: 0.75rem;
          margin-top: 0.75rem;
        }

        .result-details pre {
          margin: 0;
          font-family: 'Monaco', 'Menlo', monospace;
          font-size: 0.75rem;
          color: #334155;
          white-space: pre-wrap;
          word-break: break-word;
        }

        .result-timestamp {
          font-size: 0.75rem;
          color: #94a3b8;
          margin-top: 0.5rem;
        }

        .empty-state {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 3rem 1rem;
          color: #94a3b8;
        }

        .empty-icon {
          font-size: 3rem;
          margin-bottom: 1rem;
          opacity: 0.5;
        }

        .empty-message {
          font-size: 0.875rem;
        }
      `}</style>
    </div>
  );
};

export default ValidationPanel;
