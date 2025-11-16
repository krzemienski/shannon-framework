import { useEffect } from 'react';
import { useSocket } from './hooks/useSocket';
import { useDashboardStore } from './store/dashboardStore';
import { ExecutionOverview } from './panels/ExecutionOverview';
import { SkillsView } from './panels/SkillsView';
import { FileDiff } from './panels/FileDiff';
import { Wifi, WifiOff, Activity } from 'lucide-react';

const WEBSOCKET_URL = 'http://localhost:8000';

function App() {
  const {
    connected,
    error,
    events,
    haltExecution,
    resumeExecution,
    approveFileChange,
    revertFileChange,
    getExecutionState,
  } = useSocket({ url: WEBSOCKET_URL });

  const { setConnected, processEvent } = useDashboardStore();

  // Update connection status in store
  useEffect(() => {
    setConnected(connected);
  }, [connected, setConnected]);

  // Process incoming events
  useEffect(() => {
    if (events.length > 0) {
      const latestEvent = events[events.length - 1];
      processEvent(latestEvent);
    }
  }, [events, processEvent]);

  // Request initial state on connect
  useEffect(() => {
    if (connected) {
      console.log('Connected! Requesting initial state...');
      setTimeout(() => {
        getExecutionState();
      }, 500);
    }
  }, [connected, getExecutionState]);

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6">
      {/* Header */}
      <header className="mb-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Activity size={32} className="text-blue-500" />
            <div>
              <h1 className="text-3xl font-bold">Shannon Dashboard</h1>
              <p className="text-gray-400 text-sm">Real-time execution monitoring</p>
            </div>
          </div>

          {/* Connection Status */}
          <div className="flex items-center gap-2" data-testid="connection-status">
            {connected ? (
              <>
                <Wifi className="text-green-500" size={20} />
                <span className="text-green-500 font-medium" data-testid="connection-state">Connected</span>
              </>
            ) : (
              <>
                <WifiOff className="text-red-500" size={20} />
                <span className="text-red-500 font-medium" data-testid="connection-state">
                  {error ? `Error: ${error}` : 'Disconnected'}
                </span>
              </>
            )}
            <span className="text-gray-500 text-sm ml-2">{WEBSOCKET_URL}</span>
          </div>
        </div>
      </header>

      {/* Main Content - 3 Panel Layout */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {/* Panel 1: Execution Overview - Takes left column */}
        <div className="xl:col-span-1">
          <ExecutionOverview onHalt={haltExecution} onResume={resumeExecution} />
        </div>

        {/* Panel 2: Skills View - Takes right column, first row */}
        <div className="xl:col-span-1">
          <SkillsView />
        </div>

        {/* Panel 3: File Diff - Takes full width second row */}
        <div className="xl:col-span-2">
          <FileDiff onApprove={approveFileChange} onRevert={revertFileChange} />
        </div>
      </div>

      {/* Event Stream Debug Info - Collapsible */}
      {import.meta.env.DEV && events.length > 0 && (
        <details className="mt-8 bg-gray-900 rounded-lg p-4 border border-gray-800" data-testid="event-stream">
          <summary className="cursor-pointer text-gray-400 font-medium mb-2" data-testid="event-stream-summary">
            Event Stream (<span data-testid="event-count">{events.length}</span> events)
          </summary>
          <div className="space-y-2 max-h-64 overflow-y-auto" data-testid="event-list">
            {events.slice(-10).map((event, index) => (
              <div
                key={index}
                className="text-xs font-mono bg-gray-950 p-2 rounded text-gray-300"
                data-testid="event-item"
                data-event-type={event.type}
              >
                <span className="text-blue-400">{event.type}</span>
                <span className="text-gray-500 ml-2">
                  {new Date(event.timestamp).toLocaleTimeString()}
                </span>
                {event.data && Object.keys(event.data).length > 0 && (
                  <pre className="mt-1 text-gray-400">
                    {JSON.stringify(event.data, null, 2)}
                  </pre>
                )}
              </div>
            ))}
          </div>
        </details>
      )}

      {/* Footer */}
      <footer className="mt-8 pt-6 border-t border-gray-800 text-center text-gray-500 text-sm">
        <p>Shannon v4.0 Dashboard - Powered by WebSocket Live Updates</p>
      </footer>
    </div>
  );
}

export default App;
