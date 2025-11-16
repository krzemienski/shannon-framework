import { useDashboardStore } from '../store/dashboardStore';
import { FileText, FilePlus, FileX, Check, X } from 'lucide-react';
import type { FileChange } from '../types';

interface FileDiffProps {
  onApprove: (filePath: string) => void;
  onRevert: (filePath: string) => void;
}

export function FileDiff({ onApprove, onRevert }: FileDiffProps) {
  const files = useDashboardStore((state) => state.files);

  const getFileIcon = (status: FileChange['status']) => {
    switch (status) {
      case 'added':
        return <FilePlus className="text-green-500" size={20} />;
      case 'deleted':
        return <FileX className="text-red-500" size={20} />;
      case 'modified':
        return <FileText className="text-blue-500" size={20} />;
      default:
        return <FileText className="text-gray-400" size={20} />;
    }
  };

  const getStatusColor = (status: FileChange['status']) => {
    switch (status) {
      case 'added':
        return 'text-green-500 bg-green-500/10 border-green-500/30';
      case 'deleted':
        return 'text-red-500 bg-red-500/10 border-red-500/30';
      case 'modified':
        return 'text-blue-500 bg-blue-500/10 border-blue-500/30';
      default:
        return 'text-gray-500 bg-gray-500/10 border-gray-500/30';
    }
  };

  const getStatusText = (status: FileChange['status']) => {
    return status.charAt(0).toUpperCase() + status.slice(1);
  };

  const renderDiff = (diff: string) => {
    if (!diff) {
      return <div className="text-gray-500 text-sm italic">No diff available</div>;
    }

    const lines = diff.split('\n');
    return (
      <div className="font-mono text-xs bg-gray-950 rounded p-3 overflow-x-auto">
        {lines.map((line, index) => {
          let className = 'text-gray-300';
          if (line.startsWith('+')) {
            className = 'text-green-400 bg-green-500/10';
          } else if (line.startsWith('-')) {
            className = 'text-red-400 bg-red-500/10';
          } else if (line.startsWith('@@')) {
            className = 'text-blue-400';
          }

          return (
            <div key={index} className={`${className} px-2 py-0.5`}>
              {line || ' '}
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="bg-gray-900 rounded-lg p-6 shadow-xl border border-gray-800">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-white">File Changes</h2>
        <div className="text-sm text-gray-400">
          {files.length} {files.length === 1 ? 'file' : 'files'} modified
        </div>
      </div>

      {files.length === 0 ? (
        <div className="text-center py-12 text-gray-400">
          <FileText size={48} className="mx-auto mb-4 opacity-50" />
          <p className="text-lg">No file changes</p>
          <p className="text-sm mt-2">Modified files will appear here</p>
        </div>
      ) : (
        <div className="space-y-4">
          {files.map((file) => (
            <div
              key={file.path}
              className={`border rounded-lg overflow-hidden transition-all ${
                file.approved
                  ? 'border-green-500/50 bg-green-500/5'
                  : 'border-gray-700 bg-gray-800/50'
              }`}
            >
              {/* File Header */}
              <div className="p-4 border-b border-gray-700 bg-gray-800/50">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-center gap-3 flex-1 min-w-0">
                    {getFileIcon(file.status)}
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-white truncate" title={file.path}>
                        {file.path}
                      </div>
                      <div className="flex items-center gap-2 mt-1">
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border ${getStatusColor(
                            file.status
                          )}`}
                        >
                          {getStatusText(file.status)}
                        </span>
                        {file.approved && (
                          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium text-green-500 bg-green-500/10 border border-green-500/30">
                            <Check size={12} className="mr-1" />
                            Approved
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex gap-2">
                    {!file.approved && (
                      <>
                        <button
                          onClick={() => onApprove(file.path)}
                          className="flex items-center gap-1 px-3 py-1.5 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded transition-colors"
                          title="Approve changes"
                        >
                          <Check size={16} />
                          Approve
                        </button>
                        <button
                          onClick={() => onRevert(file.path)}
                          className="flex items-center gap-1 px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white text-sm font-medium rounded transition-colors"
                          title="Revert changes"
                        >
                          <X size={16} />
                          Revert
                        </button>
                      </>
                    )}
                  </div>
                </div>
              </div>

              {/* Diff Content */}
              <div className="p-4 max-h-96 overflow-y-auto">{renderDiff(file.diff)}</div>
            </div>
          ))}
        </div>
      )}

      {/* Summary */}
      {files.length > 0 && (
        <div className="mt-6 pt-6 border-t border-gray-800">
          <div className="grid grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-sm text-gray-400 mb-1">Total</div>
              <div className="text-2xl font-bold text-white">{files.length}</div>
            </div>
            <div className="text-center">
              <div className="text-sm text-gray-400 mb-1">Added</div>
              <div className="text-2xl font-bold text-green-400">
                {files.filter((f) => f.status === 'added').length}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-gray-400 mb-1">Modified</div>
              <div className="text-2xl font-bold text-blue-400">
                {files.filter((f) => f.status === 'modified').length}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-gray-400 mb-1">Deleted</div>
              <div className="text-2xl font-bold text-red-400">
                {files.filter((f) => f.status === 'deleted').length}
              </div>
            </div>
          </div>

          {/* Approval Status */}
          <div className="mt-4 text-center">
            <div className="text-sm text-gray-400">Approved Changes</div>
            <div className="text-lg font-semibold text-white mt-1">
              {files.filter((f) => f.approved).length} / {files.length}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
