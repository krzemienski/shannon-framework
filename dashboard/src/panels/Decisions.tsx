/**
 * Decisions Panel
 *
 * Display pending decisions and allow human approval.
 */
import { useState } from 'react';
import { useDashboardStore } from '../store/dashboardStore';
import type { Decision, DecisionOption } from '../store/dashboardStore';

interface DecisionCardProps {
  decision: Decision;
  onApprove: (decisionId: string, optionId: string) => void;
}

function DecisionCard({ decision, onApprove }: DecisionCardProps) {
  const [selectedOption, setSelectedOption] = useState<string | null>(null);

  const handleApprove = () => {
    if (selectedOption) {
      onApprove(decision.id, selectedOption);
    }
  };

  return (
    <div
      className="decision-card border border-gray-300 rounded-lg p-4 mb-4 bg-white shadow-sm"
      data-testid="decision-card"
      data-decision-id={decision.id}
    >
      {/* Question */}
      <div className="decision-question mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{decision.question}</h3>
        <p className="text-sm text-gray-500 mt-1">
          Asked {new Date(decision.created_at).toLocaleTimeString()}
        </p>
      </div>

      {/* Options */}
      <div className="decision-options space-y-3">
        {decision.options.map((option) => (
          <OptionCard
            key={option.id}
            option={option}
            selected={selectedOption === option.id}
            onSelect={() => setSelectedOption(option.id)}
          />
        ))}
      </div>

      {/* Context (if provided) */}
      {decision.context && Object.keys(decision.context).length > 0 && (
        <div className="decision-context mt-4 p-3 bg-gray-50 rounded text-sm">
          <strong className="text-gray-700">Context:</strong>
          <pre className="mt-1 text-gray-600 whitespace-pre-wrap">
            {JSON.stringify(decision.context, null, 2)}
          </pre>
        </div>
      )}

      {/* Approve Button */}
      <div className="decision-actions mt-4">
        <button
          className={`px-4 py-2 rounded font-medium transition-colors ${
            selectedOption
              ? 'bg-blue-600 text-white hover:bg-blue-700'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
          onClick={handleApprove}
          disabled={!selectedOption}
          data-testid="approve-button"
        >
          Approve Decision
        </button>
      </div>
    </div>
  );
}

interface OptionCardProps {
  option: DecisionOption;
  selected: boolean;
  onSelect: () => void;
}

function OptionCard({ option, selected, onSelect }: OptionCardProps) {
  const confidenceColor = option.confidence >= 0.95
    ? 'text-green-600'
    : option.confidence >= 0.7
    ? 'text-yellow-600'
    : 'text-red-600';

  return (
    <div
      className={`option-card border-2 rounded-lg p-3 cursor-pointer transition-all ${
        selected
          ? 'border-blue-600 bg-blue-50'
          : 'border-gray-200 hover:border-gray-300 bg-white'
      }`}
      onClick={onSelect}
      data-testid="option-card"
      data-option-id={option.id}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2">
            {/* Selection Radio */}
            <div
              className={`w-4 h-4 rounded-full border-2 flex items-center justify-center ${
                selected ? 'border-blue-600' : 'border-gray-300'
              }`}
            >
              {selected && <div className="w-2 h-2 rounded-full bg-blue-600" />}
            </div>

            {/* Label */}
            <h4 className="font-semibold text-gray-900">{option.label}</h4>
          </div>

          {/* Description */}
          <p className="text-sm text-gray-600 mt-1 ml-6">{option.description}</p>

          {/* Pros/Cons */}
          {(option.pros && option.pros.length > 0) || (option.cons && option.cons.length > 0) ? (
            <div className="ml-6 mt-2 space-y-1">
              {option.pros && option.pros.length > 0 && (
                <div className="pros">
                  <span className="text-xs font-medium text-green-700">Pros:</span>
                  <ul className="list-disc list-inside text-xs text-gray-600 ml-2">
                    {option.pros.map((pro, i) => (
                      <li key={i}>{pro}</li>
                    ))}
                  </ul>
                </div>
              )}
              {option.cons && option.cons.length > 0 && (
                <div className="cons">
                  <span className="text-xs font-medium text-red-700">Cons:</span>
                  <ul className="list-disc list-inside text-xs text-gray-600 ml-2">
                    {option.cons.map((con, i) => (
                      <li key={i}>{con}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : null}
        </div>

        {/* Confidence Badge */}
        <div className="ml-4 text-right">
          <div className={`text-xs font-bold ${confidenceColor}`}>
            {(option.confidence * 100).toFixed(0)}%
          </div>
          <div className="text-xs text-gray-500">confidence</div>
        </div>
      </div>
    </div>
  );
}

export function Decisions() {
  const { pendingDecisions, approveDecision } = useDashboardStore();

  const handleApproveDecision = (decisionId: string, optionId: string) => {
    // Update local state
    approveDecision(decisionId, optionId);

    // Send to backend via WebSocket
    // In real implementation, this would use socket.emit('approve_decision', {...})
    // For now, we're just updating local state
    console.log(`[Decisions] Approving decision ${decisionId} with option ${optionId}`);
  };

  return (
    <div className="decisions-panel h-full overflow-y-auto p-4 bg-gray-50">
      <div className="max-w-4xl mx-auto">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Decisions
          {pendingDecisions.length > 0 && (
            <span className="ml-2 text-sm font-normal text-gray-600">
              ({pendingDecisions.length} pending)
            </span>
          )}
        </h2>

        {pendingDecisions.length === 0 ? (
          <div className="empty-state text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">✓</div>
            <h3 className="text-lg font-medium text-gray-600">No pending decisions</h3>
            <p className="text-sm text-gray-500 mt-2">
              Shannon is running autonomously. Decisions will appear here when human input is needed.
            </p>
          </div>
        ) : (
          <div className="decisions-list">
            {pendingDecisions.map((decision) => (
              <DecisionCard
                key={decision.id}
                decision={decision}
                onApprove={handleApproveDecision}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
