/**
 * Validation Panel
 *
 * Streams validation output in real-time line-by-line:
 * - Test execution output
 * - Build output
 * - Lint results
 * - Syntax highlighting for PASS/FAIL lines
 *
 * Part of: Batch 1 - Validation Streaming
 */

import React, { useEffect, useRef } from 'react';
import { useDashboardStore } from '../store/dashboardStore';

const Validation: React.FC = () => {
  const validationOutput = useDashboardStore((state) => state.validationOutput);
  const isValidating = useDashboardStore((state) => state.isValidating);
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new output arrives
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [validationOutput]);

  const getLineColor = (line: string): string => {
    if (line.includes('PASSED') || line.includes('PASS') || line.includes('✓') || line.includes('OK')) {
      return 'text-green-500';
    }
    if (line.includes('FAILED') || line.includes('FAIL') || line.includes('ERROR') || line.includes('✗')) {
      return 'text-red-500';
    }
    if (line.includes('WARNING') || line.includes('WARN')) {
      return 'text-yellow-500';
    }
    return 'text-gray-300';
  };

  return (
    <div className="h-full flex flex-col">
      <div className="flex justify-between items-center p-4 border-b">
        <h2 className="text-xl font-bold">Validation Output</h2>
        {isValidating && (
          <div className="flex items-center gap-2 text-blue-500">
            <div className="animate-spin">🔄</div>
            <span className="text-sm">Validating...</span>
          </div>
        )}
      </div>

      <div
        ref={containerRef}
        className="flex-1 overflow-y-auto bg-gray-900 p-4 font-mono text-sm"
      >
        {validationOutput.length === 0 && !isValidating && (
          <div className="flex flex-col items-center justify-center h-full text-gray-500">
            <div className="text-4xl mb-4">📋</div>
            <div>No validation output yet</div>
            <div className="text-xs mt-2">Output will stream here during test execution</div>
          </div>
        )}

        {validationOutput.map((item, index) => (
          <div
            key={index}
            className={`${getLineColor(item.line)} leading-relaxed`}
            data-testid="validation-line"
          >
            {item.line}
          </div>
        ))}

        {validationOutput.length > 0 && isValidating && (
          <div className="text-blue-400 mt-2 animate-pulse">
            ▊ Streaming...
          </div>
        )}
      </div>

      {validationOutput.length > 0 && (
        <div className="p-2 border-t bg-gray-800 text-gray-400 text-xs font-mono">
          {validationOutput.length} lines • Auto-scroll enabled
        </div>
      )}
    </div>
  );
};

export default Validation;
