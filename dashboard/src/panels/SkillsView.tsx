import { useDashboardStore } from '../store/dashboardStore';
import { CheckCircle2, XCircle, Clock, Loader2 } from 'lucide-react';
import type { Skill } from '../types';

export function SkillsView() {
  const skills = useDashboardStore((state) => state.skills);

  const formatDuration = (ms: number): string => {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);

    if (minutes > 0) {
      return `${minutes}m ${seconds % 60}s`;
    }
    return `${seconds}s`;
  };

  const getStatusIcon = (status: Skill['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="text-green-500" size={20} />;
      case 'failed':
        return <XCircle className="text-red-500" size={20} />;
      case 'running':
        return <Loader2 className="text-blue-500 animate-spin" size={20} />;
      case 'pending':
        return <Clock className="text-gray-400" size={20} />;
      default:
        return <Clock className="text-gray-400" size={20} />;
    }
  };

  const getStatusColor = (status: Skill['status']) => {
    switch (status) {
      case 'completed':
        return 'text-green-500';
      case 'failed':
        return 'text-red-500';
      case 'running':
        return 'text-blue-500';
      case 'pending':
        return 'text-gray-400';
      default:
        return 'text-gray-400';
    }
  };

  const getStatusText = (status: Skill['status']) => {
    return status.charAt(0).toUpperCase() + status.slice(1);
  };

  const getRowBackground = (status: Skill['status']) => {
    switch (status) {
      case 'running':
        return 'bg-blue-900/20';
      case 'completed':
        return 'bg-green-900/10';
      case 'failed':
        return 'bg-red-900/20';
      default:
        return 'bg-gray-800/50';
    }
  };

  return (
    <div className="bg-gray-900 rounded-lg p-6 shadow-xl border border-gray-800">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-white">Skills</h2>
        <div className="text-sm text-gray-400">
          {skills.length} {skills.length === 1 ? 'skill' : 'skills'}
        </div>
      </div>

      {skills.length === 0 ? (
        <div className="text-center py-12 text-gray-400">
          <Clock size={48} className="mx-auto mb-4 opacity-50" />
          <p className="text-lg">No skills executing</p>
          <p className="text-sm mt-2">Skills will appear here when execution starts</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-300">
                  Status
                </th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-300">
                  Skill Name
                </th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-300">
                  Progress
                </th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-300">
                  Duration
                </th>
              </tr>
            </thead>
            <tbody>
              {skills.map((skill) => (
                <tr
                  key={skill.id}
                  className={`border-b border-gray-800 transition-colors ${getRowBackground(
                    skill.status
                  )}`}
                >
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-2">
                      {getStatusIcon(skill.status)}
                      <span className={`text-sm font-medium ${getStatusColor(skill.status)}`}>
                        {getStatusText(skill.status)}
                      </span>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <div className="font-medium text-white">{skill.name}</div>
                    <div className="text-xs text-gray-400 mt-1">ID: {skill.id}</div>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-3">
                      <div className="flex-1 bg-gray-700 rounded-full h-2 overflow-hidden min-w-[100px]">
                        <div
                          className={`h-full transition-all duration-300 rounded-full ${
                            skill.status === 'completed'
                              ? 'bg-green-500'
                              : skill.status === 'failed'
                              ? 'bg-red-500'
                              : skill.status === 'running'
                              ? 'bg-blue-500'
                              : 'bg-gray-500'
                          }`}
                          style={{ width: `${skill.progress}%` }}
                        />
                      </div>
                      <span className="text-sm text-gray-300 min-w-[45px] text-right">
                        {skill.progress.toFixed(0)}%
                      </span>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <div className="text-sm text-gray-300">
                      {skill.duration > 0 ? formatDuration(skill.duration) : '-'}
                    </div>
                    {skill.startTime && !skill.endTime && (
                      <div className="text-xs text-gray-500 mt-1">
                        Started {new Date(skill.startTime).toLocaleTimeString()}
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Summary Statistics */}
      {skills.length > 0 && (
        <div className="mt-6 pt-6 border-t border-gray-800">
          <div className="grid grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-sm text-gray-400 mb-1">Pending</div>
              <div className="text-2xl font-bold text-gray-300">
                {skills.filter((s) => s.status === 'pending').length}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-gray-400 mb-1">Running</div>
              <div className="text-2xl font-bold text-blue-400">
                {skills.filter((s) => s.status === 'running').length}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-gray-400 mb-1">Completed</div>
              <div className="text-2xl font-bold text-green-400">
                {skills.filter((s) => s.status === 'completed').length}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-gray-400 mb-1">Failed</div>
              <div className="text-2xl font-bold text-red-400">
                {skills.filter((s) => s.status === 'failed').length}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Average Duration for Completed Skills */}
      {skills.filter((s) => s.status === 'completed' && s.duration > 0).length > 0 && (
        <div className="mt-4 text-center">
          <div className="text-sm text-gray-400">Average Completion Time</div>
          <div className="text-lg font-semibold text-white mt-1">
            {formatDuration(
              skills
                .filter((s) => s.status === 'completed' && s.duration > 0)
                .reduce((sum, s) => sum + s.duration, 0) /
                skills.filter((s) => s.status === 'completed' && s.duration > 0).length
            )}
          </div>
        </div>
      )}
    </div>
  );
}
