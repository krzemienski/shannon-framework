import { useState, useEffect, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';
import type { Event } from '../types';

interface UseSocketOptions {
  url: string;
  autoConnect?: boolean;
}

export function useSocket({ url, autoConnect = true }: UseSocketOptions) {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [events, setEvents] = useState<Event[]>([]);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!autoConnect) return;

    console.log('Connecting to WebSocket:', url);
    const s = io(url, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });

    s.on('connect', () => {
      console.log('WebSocket connected');
      setConnected(true);
      setError(null);
    });

    s.on('disconnect', () => {
      console.log('WebSocket disconnected');
      setConnected(false);
    });

    s.on('connect_error', (err) => {
      console.error('Connection error:', err);
      setError(err.message);
      setConnected(false);
    });

    // Listen to all events
    s.onAny((eventName: string, data: any) => {
      console.log('Received event:', eventName, data);
      const event: Event = {
        type: eventName,
        data,
        timestamp: Date.now(),
      };
      setEvents((prev) => [...prev, event]);
    });

    setSocket(s);

    return () => {
      console.log('Disconnecting WebSocket');
      s.disconnect();
    };
  }, [url, autoConnect]);

  const sendCommand = useCallback(
    (type: string, params?: any) => {
      if (!socket || !connected) {
        console.warn('Cannot send command: not connected');
        return;
      }

      console.log('Sending command:', type, params);
      socket.emit('command', { type, ...params });
    },
    [socket, connected]
  );

  const clearEvents = useCallback(() => {
    setEvents([]);
  }, []);

  // Specific command helpers
  const haltExecution = useCallback(() => {
    sendCommand('halt');
  }, [sendCommand]);

  const resumeExecution = useCallback(() => {
    sendCommand('resume');
  }, [sendCommand]);

  const getExecutionState = useCallback(() => {
    sendCommand('get_execution_state');
  }, [sendCommand]);

  const getSkillStatus = useCallback((skillId?: string) => {
    sendCommand('get_skill_status', skillId ? { skill_id: skillId } : undefined);
  }, [sendCommand]);

  const approveFileChange = useCallback((filePath: string) => {
    sendCommand('approve_file_change', { file_path: filePath });
  }, [sendCommand]);

  const revertFileChange = useCallback((filePath: string) => {
    sendCommand('revert_file_change', { file_path: filePath });
  }, [sendCommand]);

  const setBreakpoint = useCallback((location: string) => {
    sendCommand('set_breakpoint', { location });
  }, [sendCommand]);

  const removeBreakpoint = useCallback((location: string) => {
    sendCommand('remove_breakpoint', { location });
  }, [sendCommand]);

  const stepOver = useCallback(() => {
    sendCommand('step_over');
  }, [sendCommand]);

  return {
    socket,
    events,
    connected,
    error,
    sendCommand,
    clearEvents,
    // Command helpers
    haltExecution,
    resumeExecution,
    getExecutionState,
    getSkillStatus,
    approveFileChange,
    revertFileChange,
    setBreakpoint,
    removeBreakpoint,
    stepOver,
  };
}
