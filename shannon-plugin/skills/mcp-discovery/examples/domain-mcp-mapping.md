# Domain-to-MCP Mapping Examples

This document provides concrete examples of how Shannon V4's MCP Discovery skill maps specification domains to optimal MCP server recommendations.

## Example 1: React E-commerce Frontend (High Complexity)

### Specification Domain Breakdown
```yaml
domains:
  Frontend: 0.75  # Complex product catalog, checkout flows
  Backend: 0.20   # API integration only
  Database: 0.05  # Client-side data management
total_complexity: 0.68
frameworks:
  - React
  - Next.js
  - Tailwind CSS
```

### MCP Recommendations

**MANDATORY**:
- **shadcn-ui**: React framework detected → MANDATORY for all UI components
  - Use for: Product cards, checkout forms, navigation, modals
  - Components: Button, Card, Form, Input, Select, Dialog, Sheet
  - Blocks: Dashboard layout, authentication flows
  - Why: Production-ready accessible components with Radix UI primitives

**RECOMMENDED**:
- **puppeteer**: E2E testing and accessibility validation
  - Use for: Checkout flow testing, form validation, visual regression
  - Why: Real browser validation (NO MOCKS), accessibility testing
- **context7**: React/Next.js patterns and documentation
  - Use for: Next.js App Router patterns, React hooks best practices
  - Why: Framework-specific official documentation

**CONDITIONAL**:
- **playwright**: If cross-browser testing required
  - Use for: Safari/Firefox compatibility validation
  - Why: Multi-browser E2E testing beyond Chrome

**FORBIDDEN**:
- **magic**: DEPRECATED for React projects (use shadcn-ui instead)

### Integration Pattern
```
Pattern: shadcn + Puppeteer Integration (Pattern 6)
Flow:
  1. shadcn query available components (Button, Card, Form)
  2. shadcn generate component source code
  3. Install: npx shadcn@latest add button card form
  4. Customize with Tailwind classes
  5. Puppeteer test accessibility (WCAG 2.1 AA)
  6. Puppeteer test user interactions (click, fill, submit)
  7. Puppeteer visual regression testing
```

---

## Example 2: Node.js REST API Backend (Moderate Complexity)

### Specification Domain Breakdown
```yaml
domains:
  Backend: 0.80    # Express routes, middleware, authentication
  Database: 0.15   # PostgreSQL via Prisma ORM
  Testing: 0.05    # API endpoint testing
total_complexity: 0.52
frameworks:
  - Node.js
  - Express
  - Prisma
```

### MCP Recommendations

**RECOMMENDED**:
- **context7**: Express and Prisma documentation
  - Use for: Express middleware patterns, Prisma schema design, authentication strategies
  - Why: Official framework documentation and best practices
- **serena**: Code navigation and refactoring
  - Use for: API route organization, dependency analysis, symbol renaming
  - Why: Semantic code understanding across large codebases

**CONDITIONAL**:
- **sequential**: If complex business logic analysis required
  - Use for: Authentication flow analysis, performance optimization decisions
  - Why: Multi-step systematic reasoning for complex backend logic
- **puppeteer**: If API has web interface for testing
  - Use for: Admin panel testing, API documentation UI validation
  - Why: Real browser validation if web UI exists

### Integration Pattern
```
Pattern: Sequential Server Coordination (Pattern 2)
Flow:
  1. context7: Lookup Express middleware best practices
  2. serena: Understand current route organization
  3. sequential: Analyze authentication security implications
  4. serena: Apply refactoring to organize routes
```

---

## Example 3: iOS Mobile Application (Very High Complexity)

### Specification Domain Breakdown
```yaml
domains:
  Mobile: 0.85     # Swift UI, native iOS features
  Backend: 0.10    # API integration
  Testing: 0.05    # UI automation testing
total_complexity: 0.78
frameworks:
  - Swift
  - SwiftUI
  - Xcode
platforms:
  - iOS
```

### MCP Recommendations

**MANDATORY**:
- **xc-mcp**: iOS framework detected → MANDATORY for all iOS development
  - Use for: Xcode builds, simulator management, UI testing, performance profiling
  - Why: Comprehensive iOS tooling (xcodebuild, simctl, idb)

**RECOMMENDED**:
- **context7**: Swift and SwiftUI documentation
  - Use for: SwiftUI patterns, Combine framework, iOS SDK best practices
  - Why: Official Apple framework documentation
- **serena**: Swift code navigation and refactoring
  - Use for: Symbol navigation, protocol conformance, dependency tracking
  - Why: LSP-based semantic understanding for Swift

**CONDITIONAL**:
- **sequential**: If complex architectural decisions required
  - Use for: State management architecture, navigation patterns
  - Why: Systematic analysis for architectural trade-offs

### Integration Pattern
```
Pattern: xc-mcp + Context7 + Serena Coordination
Flow:
  1. context7: Lookup SwiftUI view composition patterns
  2. serena: Navigate existing view hierarchy
  3. serena: Refactor view components
  4. xc-mcp: Build project (xcodebuild-build)
  5. xc-mcp: Boot simulator (simctl-boot)
  6. xc-mcp: Install app (simctl-install)
  7. xc-mcp: Test UI interactions (idb-ui-tap, idb-ui-input)
  8. xc-mcp: Capture screenshots (screenshot)
```

---

## Example 4: React Native Cross-Platform App (High Complexity)

### Specification Domain Breakdown
```yaml
domains:
  Mobile: 0.70     # React Native components
  Frontend: 0.20   # Shared React patterns
  Backend: 0.10    # API integration
total_complexity: 0.65
frameworks:
  - React Native
  - Expo
platforms:
  - iOS
  - Android
```

### MCP Recommendations

**RECOMMENDED**:
- **expo-mcp**: React Native framework detected
  - Use for: Expo library installation, documentation, cross-platform development
  - Why: Specialized Expo development tooling
- **context7**: React Native and Expo documentation
  - Use for: React Native patterns, Expo SDK, cross-platform APIs
  - Why: Framework-specific documentation
- **shadcn-ui**: For React Native Web compatibility (if applicable)
  - Use for: Shared components between web and mobile
  - Why: React component library works with React Native Web

**CONDITIONAL**:
- **xc-mcp**: If iOS-specific testing or features required
  - Use for: iOS simulator testing, native module development
  - Why: iOS-specific development and testing capabilities
- **puppeteer**: If React Native Web UI testing required
  - Use for: Web version E2E testing, accessibility validation
  - Why: Browser-based testing for web builds

### Integration Pattern
```
Pattern: Expo + Context7 Coordination
Flow:
  1. expo-mcp: Search documentation for feature (search_documentation)
  2. context7: Lookup React Native best practices
  3. expo-mcp: Install required library (add_library)
  4. serena: Navigate component structure
  5. xc-mcp: Test iOS build (if iOS-specific)
  6. expo-mcp: Generate AGENTS.md for project context
```

---

## Example 5: Full-Stack Database Migration (Moderate-High Complexity)

### Specification Domain Breakdown
```yaml
domains:
  Database: 0.60   # Schema migrations, data transformations
  Backend: 0.30    # API updates for schema changes
  Testing: 0.10    # Migration validation
total_complexity: 0.58
frameworks:
  - PostgreSQL
  - Prisma
  - Node.js
```

### MCP Recommendations

**RECOMMENDED**:
- **context7**: Prisma migration patterns and PostgreSQL best practices
  - Use for: Migration strategies, schema design, data type recommendations
  - Why: Database framework documentation and migration guides
- **serena**: Code impact analysis for schema changes
  - Use for: Find all database queries, analyze API dependencies, refactor database calls
  - Why: Semantic understanding of database usage across codebase
- **sequential**: Migration planning and risk analysis
  - Use for: Backward compatibility analysis, rollback strategy planning
  - Why: Systematic reasoning for complex migration decisions

**CONDITIONAL**:
- **morphllm**: If bulk code transformations required
  - Use for: Update all database queries, rename columns across codebase
  - Why: Pattern-based bulk transformations

### Integration Pattern
```
Pattern: Sequential Server Coordination (Pattern 2)
Flow:
  1. context7: Research Prisma migration best practices
  2. sequential: Analyze migration risks and rollback strategy
  3. serena: Find all affected database queries
  4. serena: Analyze API endpoint dependencies
  5. morphllm: Apply bulk query transformations (if needed)
  6. context7: Validate new schema patterns
```

---

## Example 6: Legacy Codebase Refactoring (Very High Complexity)

### Specification Domain Breakdown
```yaml
domains:
  Refactoring: 0.70  # Large-scale code reorganization
  Architecture: 0.20  # System design improvements
  Testing: 0.10       # Regression testing
total_complexity: 0.82
languages:
  - JavaScript
  - TypeScript
codebase_size: Large (50,000+ lines)
```

### MCP Recommendations

**RECOMMENDED**:
- **serena**: Primary tool for semantic refactoring
  - Use for: Symbol renaming, code navigation, dependency tracking, refactoring operations
  - Why: LSP-based semantic understanding prevents broken references
- **morphllm**: Bulk pattern transformations
  - Use for: Style enforcement, consistent naming, framework migrations
  - Why: Efficient bulk edits with pattern matching
- **sequential**: Refactoring strategy and planning
  - Use for: Analyze refactoring risks, plan execution order, evaluate trade-offs
  - Why: Systematic analysis for high-complexity refactoring
- **context7**: Best practices for target architecture
  - Use for: Modern JavaScript patterns, TypeScript migration guides
  - Why: Framework and language documentation

**CONDITIONAL**:
- **github**: If refactoring involves multiple PRs
  - Use for: PR creation, code review management, branch organization
  - Why: Coordinate large-scale changes across team

### Integration Pattern
```
Pattern: Parallel Server Execution + Sequential Coordination (Patterns 2 + 3)
Flow:
  Stage 1: Analysis (Parallel)
    - sequential: Analyze refactoring strategy
    - serena: Map code dependencies
    - context7: Research best practices
  Stage 2: Planning (Sequential)
    - sequential: Plan execution order
    - serena: Identify refactoring boundaries
  Stage 3: Execution (Sequential)
    - serena: Rename symbols
    - morphllm: Apply pattern transformations
    - serena: Validate no broken references
  Stage 4: Validation
    - Run tests (NO MOCKS)
    - github: Create PR with refactoring
```

---

## Example 7: Vue.js Admin Dashboard (Moderate Complexity)

### Specification Domain Breakdown
```yaml
domains:
  Frontend: 0.65   # Vue 3 components, Composition API
  Backend: 0.25    # API integration
  Testing: 0.10    # Component testing
total_complexity: 0.55
frameworks:
  - Vue 3
  - Vite
  - Pinia
```

### MCP Recommendations

**RECOMMENDED**:
- **magic**: Vue framework detected (NOT React)
  - Use for: Vue component generation, Composition API patterns
  - Why: Magic supports Vue framework for UI generation
- **context7**: Vue 3 and Pinia documentation
  - Use for: Composition API patterns, Pinia state management, Vue Router
  - Why: Framework-specific documentation
- **puppeteer**: Dashboard UI testing
  - Use for: Admin workflow testing, data table interactions, form validation
  - Why: Real browser validation (NO MOCKS)

**CONDITIONAL**:
- **playwright**: If cross-browser testing required
  - Use for: Firefox/Safari compatibility validation
  - Why: Multi-browser E2E testing

**FORBIDDEN**:
- **shadcn-ui**: NOT applicable (React/Next.js only)

### Integration Pattern
```
Pattern: Magic + Puppeteer Integration (Vue variant)
Flow:
  1. context7: Lookup Vue 3 Composition API patterns
  2. magic: Generate Vue dashboard components
  3. context7: Research Pinia state management patterns
  4. magic: Generate state management logic
  5. puppeteer: Test admin workflows (login, CRUD operations)
  6. puppeteer: Test accessibility (keyboard navigation)
```

---

## Example 8: DevOps CI/CD Pipeline (Moderate Complexity)

### Specification Domain Breakdown
```yaml
domains:
  DevOps: 0.70     # GitHub Actions, Docker, deployment
  Testing: 0.20    # Integration testing
  Backend: 0.10    # Service orchestration
total_complexity: 0.58
tools:
  - GitHub Actions
  - Docker
  - Kubernetes
```

### MCP Recommendations

**RECOMMENDED**:
- **github**: Primary tool for CI/CD workflows
  - Use for: GitHub Actions workflow creation, PR automation, repository management
  - Why: Native GitHub integration for CI/CD
- **context7**: GitHub Actions and Docker documentation
  - Use for: Workflow syntax, Docker best practices, Kubernetes patterns
  - Why: CI/CD tool documentation

**CONDITIONAL**:
- **MCP_DOCKER**: If Docker management required
  - Use for: Container operations, image building, volume management
  - Why: Docker-specific automation
- **sequential**: If complex deployment strategy analysis needed
  - Use for: Blue-green deployment planning, rollback strategies
  - Why: Systematic analysis for deployment decisions

### Integration Pattern
```
Pattern: GitHub + Context7 Coordination
Flow:
  1. context7: Research GitHub Actions best practices
  2. github: Create workflow file
  3. context7: Lookup Docker multi-stage build patterns
  4. github: Create PR with CI/CD changes
  5. MCP_DOCKER: Test container locally (if needed)
  6. github: Monitor PR checks and merge
```

---

## Summary: Domain-to-MCP Mapping Patterns

### Framework-Specific Rules (MANDATORY)

1. **React/Next.js** → **shadcn-ui** (MANDATORY)
   - Magic is FORBIDDEN for React projects
   - 50+ accessible components with Radix UI
   - Tailwind CSS integration

2. **iOS** → **xc-mcp** (MANDATORY)
   - Comprehensive Xcode and simulator tooling
   - UI testing via idb

3. **React Native + Expo** → **expo-mcp** (RECOMMENDED)
   - Specialized Expo development support
   - Documentation and library management

4. **Vue/Angular** → **magic** (RECOMMENDED)
   - UI component generation for non-React frameworks
   - shadcn-ui NOT applicable

### Domain Prioritization

**High Priority Domains** (≥60% of spec):
- Use multiple recommended MCPs
- Consider conditional MCPs
- Apply complexity-based patterns

**Moderate Priority Domains** (30-60%):
- Use 1-2 primary MCPs
- Selective conditional MCPs

**Low Priority Domains** (<30%):
- Use single MCP if needed
- Consider native tools

### Complexity Thresholds

- **0.0-0.3**: Native tools preferred, MCP cache only
- **0.3-0.6**: Single MCP server, targeted usage
- **0.6-0.8**: Multiple MCPs, specialized coordination
- **0.8-1.0**: All relevant MCPs, full orchestration

### Testing Requirements (NO MOCKS)

**Frontend Testing**:
- React/Next.js: shadcn-ui + puppeteer/playwright
- Vue/Angular: magic + puppeteer/playwright

**Mobile Testing**:
- iOS: xc-mcp (simctl, idb)
- React Native: expo-mcp + xc-mcp (conditional)

**Backend Testing**:
- Use real databases, real APIs
- NO MOCKS Iron Law enforcement

---

## Usage in Shannon V4

The mcp-discovery skill uses these examples as reference patterns when:

1. Analyzing domain breakdown from spec-analysis skill
2. Detecting frameworks from codebase analysis
3. Applying complexity-based selection logic
4. Enforcing mandatory MCP rules (React → shadcn, iOS → xc-mcp)
5. Recommending integration patterns (6 patterns available)
6. Validating MCP recommendations against domain requirements

**Output Format**:
```yaml
mcp_recommendations:
  mandatory:
    - name: shadcn-ui
      reason: React framework detected
  recommended:
    - name: puppeteer
      reason: E2E testing for complex UI flows
  conditional:
    - name: playwright
      reason: Cross-browser testing if required
  forbidden:
    - name: magic
      reason: DEPRECATED for React projects
  integration_pattern: shadcn_playwright_integration
  complexity_justification: "0.68 complexity → multiple MCPs recommended"
```

This structured approach ensures Shannon V4 always selects optimal MCPs based on specification domain analysis, framework detection, and proven integration patterns.
