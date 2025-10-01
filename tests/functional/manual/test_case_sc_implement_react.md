# Test Case: /sc:implement with React + shadcn Integration

**Test ID**: TC-003
**Priority**: High
**Category**: Integration/E2E/MCP
**Estimated Time**: 20 minutes

## Objective

Validate that /sc:implement command correctly creates a React UI component using shadcn MCP, follows Shannon behavioral patterns, and integrates with Serena MCP for project memory.

## Prerequisites

- [ ] Shannon project loaded in Claude Code
- [ ] Serena MCP configured and functional
- [ ] shadcn MCP configured and functional
- [ ] Node.js and npm installed
- [ ] React project structure available
- [ ] Test environment: /Users/nick/Documents/shannon

## Test Steps

### Step 1: Setup React Test Project

```bash
# Create minimal React project structure
cd /Users/nick/Documents/shannon
mkdir -p test-react-app/{src/components,src/lib,public}
mkdir -p test-results/TC-003/{artifacts,screenshots,logs}

# Create package.json
cat > test-react-app/package.json << 'EOF'
{
  "name": "test-react-app",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "typescript": "^5.0.0"
  }
}
EOF

# Create tsconfig.json
cat > test-react-app/tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "allowJs": true,
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"]
}
EOF

# Create basic index.tsx
cat > test-react-app/src/index.tsx << 'EOF'
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOF

# Create basic App.tsx
cat > test-react-app/src/App.tsx << 'EOF'
import React from 'react';

function App() {
  return (
    <div className="App">
      <h1>Test React App</h1>
    </div>
  );
}

export default App;
EOF
```

**Expected**: React project structure created successfully

### Step 2: Load Project in Shannon

**Command**:
```
/sh:load test-react-app/
```

**Expected Behavior**:
- Shannon project loaded
- Serena MCP indexes project files
- React project structure recognized
- Frontend domain detected

**Validation Checklist**:
- [ ] Load successful message
- [ ] React/TypeScript detected
- [ ] Project structure indexed
- [ ] No errors during load

### Step 3: Execute /sc:implement Command

**Command**:
```
/sc:implement "Create a login form component with email and password fields, a submit button, and basic validation"
```

**Expected Behavior**:
- IMPLEMENTER agent activates
- shadcn MCP detected as required (frontend task)
- Serena MCP used for project context
- Component implementation begins
- NO MOCKS or placeholders allowed

### Step 4: Validate Agent Activation

**Agent Behavior Checklist**:
- [ ] IMPLEMENTER agent explicitly mentioned or implied
- [ ] "Analyzing project structure..." shown
- [ ] "Using shadcn MCP for React components..." shown
- [ ] "Creating LoginForm component..." shown
- [ ] NO generic Claude Code responses
- [ ] Shannon-specific behavioral patterns visible

### Step 5: Validate MCP Integration

**shadcn MCP Usage Validation**:

**Expected**: shadcn MCP called with appropriate component request

```
# shadcn MCP should be used for:
- Form structure
- Input components
- Button component
- Validation patterns
```

**Validation Checklist**:
- [ ] shadcn MCP invoked (check logs)
- [ ] Component query: "form with inputs and button"
- [ ] Modern React patterns returned
- [ ] TypeScript types included
- [ ] Accessibility features present

**Serena MCP Usage Validation**:

```
# Serena MCP should be used for:
- Understanding existing project structure
- Finding appropriate component location
- Checking for naming conflicts
- Storing component context
```

**Validation Checklist**:
- [ ] Serena MCP queried for project structure
- [ ] Component placement determined correctly
- [ ] No naming conflicts
- [ ] Component context stored in memory

### Step 6: Validate Generated Component

**File Creation Validation**:

```bash
# Check component file created
ls -la test-react-app/src/components/LoginForm.tsx

# Check component exports
grep "export" test-react-app/src/components/LoginForm.tsx
```

**Expected Files**:
- [ ] `src/components/LoginForm.tsx` created
- [ ] File size >2KB (substantial implementation)
- [ ] TypeScript (.tsx extension)
- [ ] Proper React component structure

**Component Structure Checklist**:

```typescript
// Required elements in LoginForm.tsx

// 1. Imports
import React, { useState } from 'react';
// Should include shadcn components if available

// 2. Type Definitions
interface LoginFormProps {
  onSubmit?: (email: string, password: string) => void;
}

// 3. Component Definition
export function LoginForm({ onSubmit }: LoginFormProps) {
  // Implementation
}

// 4. State Management
const [email, setEmail] = useState('');
const [password, setPassword] = useState('');
const [errors, setErrors] = useState<{email?: string; password?: string}>({});

// 5. Validation Logic
const validateForm = () => {
  // Real validation, NOT a mock
};

// 6. Submit Handler
const handleSubmit = (e: React.FormEvent) => {
  // Real implementation, NOT a mock
};

// 7. JSX Return
return (
  <form onSubmit={handleSubmit}>
    {/* Actual form elements */}
  </form>
);
```

**Validation Checklist**:
- [ ] React import present
- [ ] useState hook used for state management
- [ ] TypeScript interface defined
- [ ] Props properly typed
- [ ] Email input field present
- [ ] Password input field present
- [ ] Submit button present
- [ ] Validation logic implemented (NOT mocked)
- [ ] Error handling present
- [ ] Accessibility attributes (aria-labels, etc.)
- [ ] Modern React patterns (hooks, not class components)

### Step 7: Validate NO MOCKS Rule

**Critical Anti-Pattern Detection**:

```bash
# Search for mock patterns
grep -i "todo\|mock\|placeholder\|implement.*later\|fix.*me" test-react-app/src/components/LoginForm.tsx
```

**NO MOCKS Validation Checklist**:
- [ ] NO `// TODO: implement validation`
- [ ] NO `// Mock implementation`
- [ ] NO `throw new Error("Not implemented")`
- [ ] NO `console.log("TODO: add validation")`
- [ ] NO empty function bodies
- [ ] NO placeholder comments
- [ ] NO incomplete implementations

**Validation Logic Must Be Real**:

```typescript
// ❌ UNACCEPTABLE (Mock)
const validateForm = () => {
  // TODO: implement validation
  return true;
};

// ✅ ACCEPTABLE (Real Implementation)
const validateForm = () => {
  const newErrors: {email?: string; password?: string} = {};

  if (!email) {
    newErrors.email = 'Email is required';
  } else if (!/\S+@\S+\.\S+/.test(email)) {
    newErrors.email = 'Email is invalid';
  }

  if (!password) {
    newErrors.password = 'Password is required';
  } else if (password.length < 8) {
    newErrors.password = 'Password must be at least 8 characters';
  }

  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
};
```

### Step 8: Validate Component Quality

**Code Quality Checklist**:

**TypeScript Types**:
- [ ] All props typed
- [ ] State variables typed
- [ ] Event handlers typed
- [ ] No `any` types (unless justified)

**React Best Practices**:
- [ ] Functional component (not class)
- [ ] Hooks used correctly
- [ ] State updates immutable
- [ ] Event handlers use arrow functions or useCallback
- [ ] No inline object/array creation in JSX
- [ ] Key props on lists (if applicable)

**Accessibility**:
- [ ] Form has proper labels
- [ ] Inputs have aria-labels or associated labels
- [ ] Error messages have aria-live regions
- [ ] Submit button has descriptive text
- [ ] Form is keyboard navigable

**Validation Logic**:
- [ ] Email validation (regex or similar)
- [ ] Password validation (length, complexity)
- [ ] Error messages clear and helpful
- [ ] Errors display properly
- [ ] Validation runs on submit
- [ ] Optional: real-time validation on blur

### Step 9: Validate Serena Memory Integration

**Memory Storage Validation**:

```
# Query Serena MCP to verify component stored
# Should return LoginForm component context
```

**Expected Memory Entries**:
- [ ] Component name: LoginForm
- [ ] Component location: src/components/LoginForm.tsx
- [ ] Component purpose: user authentication form
- [ ] Component props: onSubmit callback
- [ ] Component state: email, password, errors
- [ ] Validation logic documented

### Step 10: Test Component Integration

**Create Test Usage File**:

```typescript
// test-react-app/src/App.tsx
import React from 'react';
import { LoginForm } from './components/LoginForm';

function App() {
  const handleLogin = (email: string, password: string) => {
    console.log('Login attempt:', email);
  };

  return (
    <div className="App">
      <h1>Test React App</h1>
      <LoginForm onSubmit={handleLogin} />
    </div>
  );
}

export default App;
```

**Integration Validation**:

```bash
# Check TypeScript compilation
cd test-react-app
npx tsc --noEmit

# Should compile without errors
```

**Validation Checklist**:
- [ ] Component imports successfully
- [ ] No TypeScript errors
- [ ] Props properly typed
- [ ] Callback signature matches

### Step 11: Validate Documentation

**Component Documentation Checklist**:

```typescript
/**
 * LoginForm component for user authentication
 *
 * @param {LoginFormProps} props - Component props
 * @param {Function} props.onSubmit - Callback fired on successful validation
 *
 * @example
 * <LoginForm onSubmit={(email, password) => console.log(email)} />
 */
```

**Expected Documentation**:
- [ ] JSDoc comment present
- [ ] Component purpose described
- [ ] Props documented
- [ ] Usage example provided
- [ ] Return type documented (if needed)

### Step 12: Validate Behavioral Consistency

**Shannon-Specific Patterns Checklist**:
- [ ] NO generic "I'll create a component..." responses
- [ ] Implementation plan shown (not just execution)
- [ ] MCP usage explicitly mentioned
- [ ] Quality considerations discussed
- [ ] Real implementation provided (no mocks)
- [ ] Testing suggestions offered (optional)
- [ ] Integration guidance provided

**Anti-Patterns to Detect**:
- [ ] Generic component generation without context
- [ ] Copy-paste code without customization
- [ ] Missing error handling
- [ ] Incomplete implementations
- [ ] No consideration of existing project structure

## Expected Results

**Complete Implementation**:

```typescript
// src/components/LoginForm.tsx
import React, { useState, FormEvent } from 'react';

interface LoginFormProps {
  onSubmit?: (email: string, password: string) => void;
}

/**
 * LoginForm component for user authentication
 * Provides email/password inputs with validation
 */
export function LoginForm({ onSubmit }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{
    email?: string;
    password?: string;
  }>({});

  const validateForm = (): boolean => {
    const newErrors: typeof errors = {};

    // Email validation
    if (!email) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    // Password validation
    if (!password) {
      newErrors.password = 'Password is required';
    } else if (password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (validateForm()) {
      onSubmit?.(email, password);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="login-form">
      <div className="form-group">
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          aria-label="Email address"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? "email-error" : undefined}
        />
        {errors.email && (
          <span id="email-error" role="alert" className="error">
            {errors.email}
          </span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          aria-label="Password"
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? "password-error" : undefined}
        />
        {errors.password && (
          <span id="password-error" role="alert" className="error">
            {errors.password}
          </span>
        )}
      </div>

      <button type="submit">Log In</button>
    </form>
  );
}
```

## Validation Criteria

**Pass Criteria**:
- ✅ Component file created at correct location
- ✅ File size >2KB with substantial implementation
- ✅ TypeScript types complete and correct
- ✅ React hooks used properly
- ✅ Validation logic fully implemented (NO MOCKS)
- ✅ Accessibility attributes present
- ✅ shadcn MCP used for component patterns
- ✅ Serena MCP stores component context
- ✅ TypeScript compilation succeeds
- ✅ Component integrates with App.tsx
- ✅ Shannon behavioral patterns evident

**Fail Criteria**:
- ❌ Mock implementations or TODOs present
- ❌ Component file not created
- ❌ TypeScript errors
- ❌ Missing validation logic
- ❌ Class component instead of functional
- ❌ No MCP integration
- ❌ Generic Claude Code responses
- ❌ Incomplete implementation

## Debug Information

**Logs to Collect**:
- [ ] Copy implementation output: test-results/TC-003/implement_output.md
- [ ] Copy component file: test-results/TC-003/artifacts/LoginForm.tsx
- [ ] Copy App.tsx integration: test-results/TC-003/artifacts/App.tsx
- [ ] TypeScript errors (if any): test-results/TC-003/logs/tsc_errors.log
- [ ] Screenshots: test-results/TC-003/screenshots/

**Debug Commands**:
```bash
# Check component file
cat test-react-app/src/components/LoginForm.tsx

# Check for mocks
grep -n -i "todo\|mock\|placeholder" test-react-app/src/components/LoginForm.tsx

# TypeScript validation
cd test-react-app && npx tsc --noEmit

# Component line count
wc -l test-react-app/src/components/LoginForm.tsx

# Check imports
grep "^import" test-react-app/src/components/LoginForm.tsx
```

## Notes

**Record Observations**:
- Implementation time: _____ seconds
- Component file size: _____ lines
- shadcn MCP invoked: _____ (Y/N)
- Serena MCP invoked: _____ (Y/N)
- TypeScript errors: _____ (count)
- Mock patterns found: _____ (count)
- Quality score (1-10): _____

**Known Issues**:
- None at test creation time

**Variations to Test**:
1. Different component types (table, modal, nav)
2. Components with children props
3. Components with complex state
4. Components with external API calls
5. Components with animations/transitions
