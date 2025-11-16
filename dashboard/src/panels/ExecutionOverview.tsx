import { useDashboardStore } from '../store/dashboardStore';
import { Play, Pause, StopCircle } from 'lucide-react';

interface ExecutionOverviewProps {
  onHalt: () => void;
  onResume: () => void;
}

export function ExecutionOverview({ onHalt, onResume }: ExecutionOverviewProps) {
  const execution = useDashboardStore((state) => state.execution);

  const formatTime = (ms: number): string => {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);

    if (hours > 0) {
      return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
    }
    if (minutes > 0) {
      return `${minutes}m ${seconds % 60}s`;
    }
    return `${seconds}s`;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'bg-green-500';
      case 'paused':
        return 'bg-yellow-500';
      case 'completed':
        return 'bg-blue-500';
      case 'failed':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStatusText = (status: string) => {
    return status.charAt(0).toUpperCase() + status.slice(1);
  };

  return (
    <div className="bg-gray-900 rounded-lg p-6 shadow-xl border border-gray-800">
      <h2 className="text-2xl font-bold mb-6 text-white">Execution Overview</h2>

      {/* Task Name */}
      <div className="mb-6">
        <div className="text-sm text-gray-400 mb-1">Task</div>
        <div className="text-xl font-semibold text-white">{execution.taskName}</div>
      </div>

      {/* Status Badge */}
      <div className="mb-6">
        <div className="text-sm text-gray-400 mb-2">Status</div>
        <div className="flex items-center gap-2">
          <span
            className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium text-white ${getStatusColor(
              execution.status
            )}`}
          >
            {getStatusText(execution.status)}
          </span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex justify-between text-sm text-gray-400 mb-2">
          <span>Progress</span>
          <span>{execution.progress.toFixed(1)}%</span>
        </div>
        <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
          <div
            className="bg-blue-500 h-full transition-all duration-300 rounded-full"
            style={{ width: `${execution.progress}%` }}
          />
        </div>
      </div>

      {/* Timing Information */}
      <div className="mb-6 grid grid-cols-2 gap-4">
        <div>
          <div className="text-sm text-gray-400 mb-1">Started</div>
          <div className="text-lg font-medium text-white">
            {execution.startTime
              ? new Date(execution.startTime).toLocaleTimeString()
              : 'N/A'}
          </div>
        </div>
        <div>
          <div className="text-sm text-gray-400 mb-1">Elapsed</div>
          <div className="text-lg font-medium text-white">
            {execution.elapsedTime > 0 ? formatTime(execution.elapsedTime) : '0s'}
          </div>
        </div>
      </div>

      {execution.estimatedTimeRemaining !== null && (
        <div className="mb-6">
          <div className="text-sm text-gray-400 mb-1">Estimated Time Remaining</div>
          <div className="text-lg font-medium text-white">
            {formatTime(execution.estimatedTimeRemaining)}
          </div>
        </div>
      )}

      {/* Control Buttons */}
      <div className="flex gap-3">
        {execution.status === 'running' ? (
          <button
            onClick={onHalt}
            className="flex-1 flex items-center justify-center gap-2 bg-yellow-600 hover:bg-yellow-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
          >
            <Pause size={20} />
            Halt
          </button>
        ) : execution.status === 'paused' ? (
          <>
            <button
              onClick={onResume}
              className="flex-1 flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
            >
              <Play size={20} />
              Resume
            </button>
            <button
              onClick={onHalt}
              className="flex-1 flex items-center justify-center gap-2 bg-red-600 hover:bg-red-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
            >
              <StopCircle size={20} />
              Stop
            </button>
          </>
        ) : (
          <button
            disabled
            className="flex-1 flex items-center justify-center gap-2 bg-gray-700 text-gray-400 font-semibold py-3 px-4 rounded-lg cursor-not-allowed"
          >
            No active execution
          </button>
        )}
      </div>

      {/* Quick Stats */}
      <div className="mt-6 pt-6 border-t border-gray-800">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-white">
              {useDashboardStore.getState().skills.length}
            </div>
            <div className="text-xs text-gray-400">Total Skills</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-400">
              {
                useDashboardStore
                  .getState()
                  .skills.filter((s) => s.status === 'completed').length
              }
            </div>
            <div className="text-xs text-gray-400">Completed</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-red-400">
              {
                useDashboardStore
                  .getState()
                  .skills.filter((s) => s.status === 'failed').length
              }
            </div>
            <div className="text-xs text-gray-400">Failed</div>
          </div>
        </div>
      </div>
    </div>
  );
}
