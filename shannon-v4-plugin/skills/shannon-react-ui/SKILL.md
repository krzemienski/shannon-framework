---
name: shannon-react-ui
display_name: "Shannon React UI"
description: "React 18 component generation with hooks, state management, TypeScript, and modern patterns"
category: frontend
version: "4.0.0"
priority: 1
auto_activate: true
activation_condition: "domain_analysis.frontend >= 20% AND 'React' in tech_stack"
mcp_servers:
  required: [serena]
  recommended: [shadcn-ui, context7, puppeteer]
allowed_tools: [Write, Read, Edit, Glob, Grep, puppeteer_navigate, puppeteer_click]
---

# Shannon React UI

> **React 18+ Component Generation**: Hooks, TypeScript, State Management

## Capabilities

- Component generation (functional with hooks)
- State management (useState, useReducer, Context API)
- Side effects (useEffect, useLayoutEffect, custom hooks)
- TypeScript integration
- Form handling with validation
- Error boundaries
- Code splitting & lazy loading
- Performance optimization (memo, useMemo, useCallback)

## Patterns

**Component Structure**:
```tsx
import { useState, useEffect } from 'react';

interface Props {
  // TypeScript props
}

export function Component({ }: Props) {
  // Hooks at top
  const [state, setState] = useState();

  useEffect(() => {
    // Side effects
  }, []);

  // Event handlers
  const handleClick = () => {};

  // Render
  return <div>...</div>;
}
```

**State Management**:
- Local: useState for component state
- Shared: Context API for cross-component state
- Complex: useReducer for state machines
- Global: External lib (Zustand/Redux) for app state

**Testing (NO MOCKS)**:
- Puppeteer for E2E testing
- Real user interactions
- Real browser rendering
- No enzyme, no testing-library mocks

## Integration

**shadcn-ui MCP**: Generate production-ready components
```bash
shadcn-ui add button
shadcn-ui add form
```

**Context7 MCP**: Load React 18 docs on-demand
```bash
context7 get "React useEffect"
context7 get "React Server Components"
```

📚 Full patterns: [resources/REACT_PATTERNS.md](./resources/REACT_PATTERNS.md)
