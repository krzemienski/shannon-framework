# Shannon v4.0 Dashboard

Real-time React dashboard for monitoring Shannon autonomous execution.

## Features

- **Execution Overview Panel**: Task status, progress, timing, and execution controls
- **Skills View Panel**: Real-time skill tracking with progress and duration
- **File Diff Panel**: File change monitoring with approve/revert controls
- **WebSocket Live Updates**: Real-time event streaming from execution server

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

Dashboard will be available at `http://localhost:5173`

### 3. Build for Production

```bash
npm run build
```

### 4. Preview Production Build

```bash
npm run preview
```

## WebSocket Connection

The dashboard connects to Shannon WebSocket server at `http://localhost:8000`.

To change the connection URL, edit `WEBSOCKET_URL` in `src/App.tsx`:

```typescript
const WEBSOCKET_URL = 'http://localhost:8000';
```

## Architecture

### Core Components

1. **`src/App.tsx`** - Main application with 3-panel layout
2. **`src/hooks/useSocket.ts`** - WebSocket connection and event handling
3. **`src/store/dashboardStore.ts`** - Zustand state management
4. **`src/panels/ExecutionOverview.tsx`** - Execution status and controls
5. **`src/panels/SkillsView.tsx`** - Skills tracking table
6. **`src/panels/FileDiff.tsx`** - File change viewer

### Event Processing

The dashboard processes 25+ WebSocket event types:

- Execution events: `execution_started`, `execution_paused`, `execution_completed`, etc.
- Skill events: `skill_started`, `skill_progress`, `skill_completed`, etc.
- File events: `file_changed`, `file_approved`, `file_reverted`
- And more...

### Command Sending

The dashboard can send 9 command types:

- `halt` - Halt execution
- `resume` - Resume paused execution
- `get_execution_state` - Request current state
- `get_skill_status` - Request skill status
- `approve_file_change` - Approve file modification
- `revert_file_change` - Revert file modification
- And more...

## Testing

### Connection Test

Open `test-connection.html` in a browser to test WebSocket connectivity:

```bash
open test-connection.html
```

This simple test page:
- Shows connection status
- Sends test commands
- Displays received events
- No build required

### Development Mode

In development mode, the dashboard shows an event stream debug panel at the bottom of the page with the last 10 events.

## Technology Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Socket.IO Client** - WebSocket connection
- **Zustand** - State management
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

## Project Structure

```
dashboard/
├── src/
│   ├── App.tsx                 # Main application
│   ├── index.css               # Global styles
│   ├── types.ts                # TypeScript types
│   ├── hooks/
│   │   └── useSocket.ts        # WebSocket hook
│   ├── store/
│   │   └── dashboardStore.ts   # Zustand store
│   └── panels/
│       ├── ExecutionOverview.tsx
│       ├── SkillsView.tsx
│       └── FileDiff.tsx
├── test-connection.html         # Simple connection test
└── README.md                    # This file
```

## Development

### Running the Dashboard

1. Ensure Shannon WebSocket server is running on port 8000
2. Start the dashboard: `npm run dev`
3. Open browser to `http://localhost:5173`
4. Dashboard will automatically connect and display real-time updates

### Adding New Features

1. **New Event Type**: Add handler to `processEvent` in `dashboardStore.ts`
2. **New Command**: Add method to `useSocket.ts` hook
3. **New Panel**: Create component in `src/panels/` and add to `App.tsx`

## Troubleshooting

### Connection Issues

- Verify WebSocket server is running on `http://localhost:8000`
- Check browser console for connection errors
- Use `test-connection.html` to verify basic connectivity

### Build Errors

- Ensure all dependencies are installed: `npm install`
- Clear build cache: `rm -rf node_modules/.vite`
- Rebuild: `npm run build`

## License

MIT
