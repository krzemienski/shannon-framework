# shadcn/ui Integration Guide for Shannon Framework

Complete guide to using shadcn/ui components in Shannon Framework via MCP server integration.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [MCP Server Setup](#mcp-server-setup)
4. [shadcn Component Workflow](#shadcn-component-workflow)
5. [Shannon Integration Patterns](#shannon-integration-patterns)
6. [Component Catalog](#component-catalog)
7. [Block Usage](#block-usage)
8. [Testing Patterns](#testing-patterns)
9. [Migration from Magic MCP](#migration-from-magic-mcp)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)
12. [Examples](#examples)

---

## Overview

### What is shadcn/ui?

shadcn/ui is a collection of beautifully designed, accessible React components built with:

- **Radix UI**: Unstyled, accessible component primitives
- **Tailwind CSS**: Utility-first styling framework
- **TypeScript**: Full type safety and IntelliSense support

**Key Distinction**: shadcn/ui is NOT a component library or npm package. It's a **collection of reusable components** that you copy directly into your project and own completely.

### Why Shannon Enforces shadcn/ui

Shannon Framework mandates shadcn/ui for all React/Next.js UI development:

**✅ Accessibility First**
- Built on Radix UI primitives (WCAG 2.1 AA compliant)
- Keyboard navigation, focus management, screen reader support
- ARIA attributes included by default

**✅ Complete Ownership**
- Components copied into your codebase
- Full control over styling and behavior
- No breaking changes from external library updates
- Zero bundle bloat from unused components

**✅ TypeScript Excellence**
- Full TypeScript definitions
- IntelliSense support in editors
- Type-safe component props

**✅ Customization Freedom**
- Modify components directly in your project
- Extend with additional features
- Adapt to design system requirements

**✅ Modern Best Practices (2025)**
- React Server Components compatible
- Next.js 14+ optimized
- Tailwind CSS 3.4+ features

### Benefits for Shannon Development

1. **Consistency**: All Shannon agents use same component patterns
2. **Quality**: Production-ready, battle-tested components
3. **Speed**: MCP integration enables instant component discovery
4. **Testability**: Accessible components are easier to test with Puppeteer
5. **Maintainability**: Own the code, understand every detail

---

## Prerequisites

### Required Setup

**1. React/Next.js Project**
```bash
# Next.js 14+ (recommended)
npx create-next-app@latest my-app --typescript --tailwind --app

# Or React with Vite
npm create vite@latest my-app -- --template react-ts
```

**2. Tailwind CSS Configured**

Your project must have Tailwind CSS properly configured:

```javascript
// tailwind.config.js
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        // ... additional color tokens
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
```

**3. shadcn CLI Initialized**
```bash
npx shadcn@latest init
```

This creates:
- `components.json` configuration file
- `lib/utils.ts` with cn() helper
- CSS variables in your globals.css

**4. shadcn MCP Server Installed**

See [MCP Server Setup](#mcp-server-setup) section below.

---

## MCP Server Setup

### Installation

The Shannon Framework uses `@jpisnice/shadcn-ui-mcp-server` for component discovery and installation.

**Step 1: Add to Claude Desktop Configuration**

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "shadcn": {
      "command": "npx",
      "args": [
        "-y",
        "@jpisnice/shadcn-ui-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_token_here"
      }
    }
  }
}
```

**Step 2: Create GitHub Personal Access Token**

1. Go to GitHub Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Set scopes: `public_repo` (sufficient for public repositories)
4. Copy token and add to configuration above

**Step 3: Restart Claude Desktop**

After configuration changes, restart Claude Desktop to load the MCP server.

**Step 4: Verify Installation**

In Claude Code, test the connection:

```bash
# List available components
list_components()

# Should return: button, card, dialog, input, etc.
```

If successful, you'll see a list of 50+ shadcn components.

### Configuration Options

**Custom Component Path**
```json
{
  "shadcn": {
    "command": "npx",
    "args": ["-y", "@jpisnice/shadcn-ui-mcp-server"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "token",
      "SHADCN_COMPONENTS_PATH": "./src/components/ui"
    }
  }
}
```

**TypeScript Mode**
```json
{
  "env": {
    "SHADCN_TYPESCRIPT": "true"
  }
}
```

---

## shadcn Component Workflow

### Standard Component Integration Process

**Step 1: Browse Available Components**

```typescript
// Use MCP tool to list all components
list_components()

// Returns:
// - accordion
// - alert
// - alert-dialog
// - avatar
// - badge
// - button
// - calendar
// - card
// ... (50+ components)
```

**Step 2: Get Component Source Code**

```typescript
// Retrieve component implementation
get_component({ name: "button" })

// Returns full component source with:
// - TypeScript interface definitions
// - Component implementation
// - Variant definitions (using class-variance-authority)
// - Usage examples
```

**Step 3: View Component Demo**

```typescript
// See usage examples
get_component_demo({ name: "button" })

// Returns:
// - Basic usage examples
// - All variant combinations
// - Integration patterns
// - Accessibility notes
```

**Step 4: Install Component**

```bash
# Using shadcn CLI
npx shadcn@latest add button

# Multiple components at once
npx shadcn@latest add button card dialog

# With dependencies automatically resolved
npx shadcn@latest add data-table
# Installs: table, dropdown-menu, checkbox, etc.
```

**Step 5: Import and Use**

```typescript
import { Button } from "@/components/ui/button"

export default function MyComponent() {
  return (
    <Button variant="default" size="lg">
      Click Me
    </Button>
  )
}
```

### Workflow Best Practices

**1. Discovery First**
- Always use `list_components()` to see what's available
- Check `get_component_demo()` before implementing
- Review variants and props before adding to project

**2. Dependency Awareness**
- Complex components have dependencies (e.g., Select requires Popover)
- shadcn CLI auto-installs dependencies
- Verify all required components are installed

**3. Customization After Installation**
- Components are copied to your project
- Edit directly in `components/ui/`
- Changes persist across updates

**4. Version Control**
- Commit shadcn components to git
- Track customizations in your repository
- Document modifications in component files

---

## Shannon Integration Patterns

### FRONTEND Agent Integration

Shannon's FRONTEND agent automatically uses shadcn MCP for UI tasks:

**Auto-Detection Triggers**:
- Keywords: "component", "button", "form", "dialog", "card"
- UI-related commands: `/implement`, `/build`, `/design`
- React/Next.js project context

**Agent Workflow**:
```yaml
1. Detect UI requirement
2. Query shadcn MCP for matching component
3. Retrieve component source and demo
4. Install via shadcn CLI
5. Integrate into project with customization
6. Generate Puppeteer tests for validation
```

**Example Agent Decision**:
```
User: "Create a login form"

FRONTEND Agent:
1. list_components() → identifies "form", "input", "button", "card"
2. get_component_demo({ name: "form" }) → reviews react-hook-form integration
3. Installs: npx shadcn add form input button card
4. Generates login form with validation
5. Creates Puppeteer test for form submission
```

### Command Integration

**`/implement` with shadcn**
```bash
/implement login-form --type component

# Agent workflow:
# 1. Identifies shadcn components needed (form, input, button)
# 2. Retrieves component demos
# 3. Installs components
# 4. Creates LoginForm.tsx with validation
# 5. Generates Puppeteer test
```

**`/build` with shadcn**
```bash
/build dashboard-ui

# Agent workflow:
# 1. Checks for shadcn blocks (get_block({ name: "dashboard" }))
# 2. Installs block with all dependencies
# 3. Customizes for project requirements
# 4. Integrates with existing layout
```

**`/design` with shadcn**
```bash
/design data-table --framework react

# Agent workflow:
# 1. get_component({ name: "data-table" })
# 2. Reviews tanstack-table integration
# 3. Installs data-table component
# 4. Creates example with sorting, filtering, pagination
```

### Wave Execution with shadcn

**Wave-Enabled UI Development**:
```yaml
complexity_threshold: 0.7
operations: [discover, install, integrate, test, validate]
waves: 3-5

Wave 1 - Discovery:
  - list_components()
  - get_component_demo() for all candidates
  - Identify component dependencies

Wave 2 - Installation:
  - npx shadcn add [components]
  - Verify installation success
  - Review component source

Wave 3 - Integration:
  - Create component compositions
  - Apply project-specific styling
  - Integrate with state management

Wave 4 - Testing:
  - Generate Puppeteer tests
  - Validate accessibility
  - Test responsive behavior

Wave 5 - Validation:
  - Review implementation
  - Performance check
  - Documentation
```

### MCP Tool Usage Patterns

**Component Discovery Pattern**:
```typescript
// 1. List all components
const components = await list_components()

// 2. Filter by category (form components)
const formComponents = components.filter(c =>
  ['input', 'textarea', 'select', 'checkbox', 'radio'].includes(c)
)

// 3. Get details for each
for (const component of formComponents) {
  const demo = await get_component_demo({ name: component })
  // Review usage patterns
}
```

**Block Discovery Pattern**:
```typescript
// 1. List available blocks
const blocks = await list_blocks()

// 2. Get specific block
const dashboardBlock = await get_block({ name: "dashboard-01" })

// 3. Review block composition
// Blocks include multiple components pre-composed
```

---

## Component Catalog

### Complete Component List (50+ components)

**Forms & Input**
- `input` - Text input with variants
- `textarea` - Multi-line text input
- `select` - Dropdown select (with search)
- `checkbox` - Checkbox with label
- `radio-group` - Radio button group
- `switch` - Toggle switch
- `slider` - Range slider
- `form` - Form with react-hook-form integration
- `label` - Form label
- `combobox` - Searchable select

**Buttons & Actions**
- `button` - Button with variants (default, destructive, outline, ghost, link)
- `dropdown-menu` - Dropdown menu with items
- `context-menu` - Right-click context menu
- `menubar` - Application menu bar

**Navigation**
- `navigation-menu` - Horizontal navigation
- `tabs` - Tab navigation
- `breadcrumb` - Breadcrumb navigation
- `pagination` - Pagination controls
- `command` - Command palette (⌘K)

**Feedback & Overlays**
- `alert` - Alert message
- `alert-dialog` - Modal alert dialog
- `dialog` - Generic modal dialog
- `sheet` - Slide-in panel
- `toast` - Toast notification
- `popover` - Popover tooltip
- `tooltip` - Simple tooltip
- `hover-card` - Hover card with content
- `progress` - Progress bar
- `skeleton` - Loading skeleton
- `spinner` - Loading spinner

**Data Display**
- `table` - Data table
- `data-table` - Advanced table with sorting/filtering
- `card` - Content card
- `avatar` - User avatar with fallback
- `badge` - Status badge
- `separator` - Visual separator
- `accordion` - Collapsible sections
- `collapsible` - Collapsible content
- `aspect-ratio` - Aspect ratio container

**Date & Time**
- `calendar` - Calendar picker
- `date-picker` - Date input with calendar
- `date-range-picker` - Date range selector

**Layout**
- `scroll-area` - Custom scrollbar
- `resizable` - Resizable panels
- `toggle` - Toggle button
- `toggle-group` - Toggle button group

**Advanced**
- `command` - Command palette
- `sonner` - Toast notifications (sonner library)
- `drawer` - Bottom drawer (mobile)
- `carousel` - Image carousel
- `chart` - Chart components (recharts integration)

### Usage Examples for Common Components

**Button**
```typescript
import { Button } from "@/components/ui/button"

// Variants
<Button variant="default">Default</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>

// Sizes
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>
<Button size="icon"><Icon /></Button>
```

**Form with Validation**
```typescript
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const formSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

export function LoginForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="you@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input type="password" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Sign In</Button>
      </form>
    </Form>
  )
}
```

**Dialog**
```typescript
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

<Dialog>
  <DialogTrigger asChild>
    <Button>Open Dialog</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Are you sure?</DialogTitle>
      <DialogDescription>
        This action cannot be undone.
      </DialogDescription>
    </DialogHeader>
    <div className="flex justify-end gap-2">
      <Button variant="outline">Cancel</Button>
      <Button variant="destructive">Delete</Button>
    </div>
  </DialogContent>
</Dialog>
```

**Data Table**
```typescript
import { DataTable } from "@/components/ui/data-table"
import { ColumnDef } from "@tanstack/react-table"

interface User {
  id: string
  name: string
  email: string
  role: string
}

const columns: ColumnDef<User>[] = [
  {
    accessorKey: "name",
    header: "Name",
  },
  {
    accessorKey: "email",
    header: "Email",
  },
  {
    accessorKey: "role",
    header: "Role",
  },
]

export function UsersTable({ users }: { users: User[] }) {
  return <DataTable columns={columns} data={users} />
}
```

---

## Block Usage

### What are shadcn Blocks?

Blocks are **pre-composed sections** built from multiple shadcn components:
- Authentication flows (login, signup, password reset)
- Dashboard layouts (sidebar, header, content)
- Settings pages (profile, account, notifications)
- Landing page sections (hero, features, pricing)
- E-commerce components (product cards, checkout)

**Key Difference from Components**:
- **Components**: Individual UI elements (button, input, card)
- **Blocks**: Complete sections combining multiple components

### Available Blocks

**Dashboard Blocks**
- `dashboard-01` - Sidebar layout with navigation
- `dashboard-02` - Top navigation layout
- `dashboard-03` - Minimal sidebar layout
- `dashboard-04` - Full-width dashboard
- `dashboard-05` - Split view dashboard
- `dashboard-06` - Kanban board layout
- `dashboard-07` - Analytics dashboard

**Authentication Blocks**
- `authentication-01` - Centered login form
- `authentication-02` - Split screen login
- `authentication-03` - Login with social providers
- `authentication-04` - Sign up form

**Settings Blocks**
- `settings-01` - Tabbed settings page
- `settings-02` - Sidebar settings page
- `settings-03` - Minimal settings page

**Charts & Analytics**
- `charts-01` - Line chart with legend
- `charts-02` - Bar chart with tooltip
- `charts-03` - Area chart with gradient
- `charts-04` - Pie chart with labels

### Using Blocks

**Step 1: List Available Blocks**
```typescript
list_blocks()

// Returns block IDs and descriptions
```

**Step 2: Get Block Source**
```typescript
get_block({ name: "dashboard-01" })

// Returns:
// - Full React component code
// - All required shadcn components
// - Example data structures
// - Integration instructions
```

**Step 3: Install Block**
```bash
# Blocks are installed manually
# Copy the block code into your project
# Install required components:

npx shadcn add sidebar navigation-menu avatar dropdown-menu
```

**Step 4: Customize Block**
```typescript
// Blocks are starting points for customization
// Modify layout, styling, and functionality
// Add project-specific features
```

### Block Examples

**Dashboard Block Integration**
```typescript
// 1. Get dashboard block
const block = await get_block({ name: "dashboard-01" })

// 2. Install dependencies
npx shadcn add \
  sidebar \
  navigation-menu \
  avatar \
  dropdown-menu \
  sheet

// 3. Create layout component
// app/dashboard/layout.tsx
import { DashboardShell } from "@/components/dashboard-shell"

export default function DashboardLayout({ children }) {
  return <DashboardShell>{children}</DashboardShell>
}

// 4. Customize navigation items
const navItems = [
  { title: "Overview", href: "/dashboard", icon: Home },
  { title: "Analytics", href: "/dashboard/analytics", icon: BarChart },
  { title: "Settings", href: "/dashboard/settings", icon: Settings },
]
```

**Authentication Block Integration**
```typescript
// 1. Get auth block
const block = await get_block({ name: "authentication-01" })

// 2. Install dependencies
npx shadcn add form input button card

// 3. Create login page
// app/login/page.tsx
import { LoginForm } from "@/components/auth/login-form"

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <LoginForm />
    </div>
  )
}

// 4. Add authentication logic
// Use NextAuth, Supabase, Clerk, etc.
```

**Settings Block Integration**
```typescript
// 1. Get settings block
const block = await get_block({ name: "settings-01" })

// 2. Install dependencies
npx shadcn add tabs form input switch

// 3. Create settings page
// app/settings/page.tsx
import { SettingsShell } from "@/components/settings-shell"

export default function SettingsPage() {
  return <SettingsShell />
}

// 4. Add settings tabs
const tabs = [
  { value: "profile", label: "Profile", component: ProfileSettings },
  { value: "account", label: "Account", component: AccountSettings },
  { value: "notifications", label: "Notifications", component: NotificationSettings },
]
```

---

## Testing Patterns

### NO MOCKS - Real Browser Testing

Shannon Framework enforces **real browser testing** with Puppeteer. NO jest, NO react-testing-library, NO mocks.

**Why Puppeteer for shadcn Components?**

1. **Accessibility Testing**: Verify Radix UI keyboard navigation and focus management
2. **Visual Validation**: Screenshot testing for responsive design
3. **Real User Interactions**: Test actual click, type, and navigation behaviors
4. **Cross-Browser**: Validate in Chrome, Firefox, Safari
5. **Integration Testing**: Test component interactions in real DOM

### Component Testing Examples

**Button Test**
```typescript
// tests/components/button.test.ts
import { test, expect } from '@playwright/test'

test.describe('Button Component', () => {
  test('renders all variants', async ({ page }) => {
    await page.goto('/test-pages/button')

    // Default variant
    const defaultBtn = page.locator('button:has-text("Default")')
    await expect(defaultBtn).toBeVisible()
    await expect(defaultBtn).toHaveClass(/bg-primary/)

    // Destructive variant
    const destructiveBtn = page.locator('button:has-text("Delete")')
    await expect(destructiveBtn).toHaveClass(/bg-destructive/)
  })

  test('handles click events', async ({ page }) => {
    await page.goto('/test-pages/button')

    let clickCount = 0
    page.on('console', msg => {
      if (msg.text().includes('Button clicked')) clickCount++
    })

    await page.click('button:has-text("Click Me")')
    expect(clickCount).toBe(1)
  })

  test('keyboard navigation', async ({ page }) => {
    await page.goto('/test-pages/button')

    await page.keyboard.press('Tab') // Focus first button
    await page.keyboard.press('Enter') // Activate

    // Verify action occurred
    await expect(page.locator('[data-testid="click-result"]')).toHaveText('Clicked')
  })
})
```

**Form Test**
```typescript
// tests/components/form.test.ts
import { test, expect } from '@playwright/test'

test.describe('Login Form', () => {
  test('validates email format', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[name="email"]', 'invalid-email')
    await page.click('button[type="submit"]')

    // Verify error message appears
    await expect(page.locator('text=Invalid email address')).toBeVisible()
  })

  test('requires password length', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[name="email"]', 'user@example.com')
    await page.fill('input[name="password"]', 'short')
    await page.click('button[type="submit"]')

    await expect(page.locator('text=Password must be at least 8 characters')).toBeVisible()
  })

  test('submits valid form', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[name="email"]', 'user@example.com')
    await page.fill('input[name="password"]', 'securepassword123')
    await page.click('button[type="submit"]')

    // Verify redirect or success
    await expect(page).toHaveURL('/dashboard')
  })
})
```

**Dialog Test**
```typescript
// tests/components/dialog.test.ts
import { test, expect } from '@playwright/test'

test.describe('Dialog Component', () => {
  test('opens and closes', async ({ page }) => {
    await page.goto('/test-pages/dialog')

    // Dialog initially hidden
    await expect(page.locator('[role="dialog"]')).not.toBeVisible()

    // Open dialog
    await page.click('button:has-text("Open Dialog")')
    await expect(page.locator('[role="dialog"]')).toBeVisible()

    // Close with X button
    await page.click('button[aria-label="Close"]')
    await expect(page.locator('[role="dialog"]')).not.toBeVisible()
  })

  test('traps focus within dialog', async ({ page }) => {
    await page.goto('/test-pages/dialog')
    await page.click('button:has-text("Open Dialog")')

    // Tab through dialog elements
    await page.keyboard.press('Tab')
    await expect(page.locator('button:has-text("Cancel")')).toBeFocused()

    await page.keyboard.press('Tab')
    await expect(page.locator('button:has-text("Confirm")')).toBeFocused()

    await page.keyboard.press('Tab')
    // Focus should return to first element (close button)
    await expect(page.locator('button[aria-label="Close"]')).toBeFocused()
  })

  test('closes on escape key', async ({ page }) => {
    await page.goto('/test-pages/dialog')
    await page.click('button:has-text("Open Dialog")')

    await page.keyboard.press('Escape')
    await expect(page.locator('[role="dialog"]')).not.toBeVisible()
  })
})
```

**Data Table Test**
```typescript
// tests/components/data-table.test.ts
import { test, expect } from '@playwright/test'

test.describe('Data Table', () => {
  test('sorts columns', async ({ page }) => {
    await page.goto('/test-pages/data-table')

    // Click name column header to sort
    await page.click('th:has-text("Name")')

    // Verify first row
    const firstRow = page.locator('tbody tr:first-child')
    await expect(firstRow.locator('td:first-child')).toHaveText('Alice')

    // Click again to reverse sort
    await page.click('th:has-text("Name")')
    await expect(firstRow.locator('td:first-child')).toHaveText('Zoe')
  })

  test('filters rows', async ({ page }) => {
    await page.goto('/test-pages/data-table')

    await page.fill('input[placeholder="Filter..."]', 'john')

    // Verify only matching rows visible
    const rows = page.locator('tbody tr')
    await expect(rows).toHaveCount(1)
    await expect(rows.first().locator('td:first-child')).toContainText('John')
  })

  test('paginates results', async ({ page }) => {
    await page.goto('/test-pages/data-table')

    // Verify initial page
    await expect(page.locator('text=Page 1 of')).toBeVisible()

    // Go to next page
    await page.click('button[aria-label="Next page"]')
    await expect(page.locator('text=Page 2 of')).toBeVisible()

    // Verify different data
    const firstRow = page.locator('tbody tr:first-child td:first-child')
    await expect(firstRow).not.toHaveText('Alice') // First item from page 1
  })
})
```

### Accessibility Testing

```typescript
// tests/a11y/components.test.ts
import { test, expect } from '@playwright/test'
import { injectAxe, checkA11y } from 'axe-playwright'

test.describe('Accessibility', () => {
  test.beforeEach(async ({ page }) => {
    await injectAxe(page)
  })

  test('button meets WCAG AA', async ({ page }) => {
    await page.goto('/test-pages/button')
    await checkA11y(page, 'button')
  })

  test('form has proper labels', async ({ page }) => {
    await page.goto('/login')

    // Every input should have associated label
    const emailInput = page.locator('input[name="email"]')
    const labelId = await emailInput.getAttribute('aria-labelledby')
    await expect(page.locator(`#${labelId}`)).toBeVisible()
  })

  test('dialog announces to screen readers', async ({ page }) => {
    await page.goto('/test-pages/dialog')
    await page.click('button:has-text("Open Dialog")')

    const dialog = page.locator('[role="dialog"]')
    await expect(dialog).toHaveAttribute('aria-modal', 'true')
    await expect(dialog).toHaveAttribute('aria-describedby')
  })
})
```

### Performance Testing

```typescript
// tests/performance/components.test.ts
import { test, expect } from '@playwright/test'

test.describe('Performance', () => {
  test('data table renders 1000 rows efficiently', async ({ page }) => {
    await page.goto('/test-pages/data-table-large')

    // Measure render time
    const startTime = Date.now()
    await page.waitForSelector('tbody tr')
    const renderTime = Date.now() - startTime

    expect(renderTime).toBeLessThan(1000) // < 1 second

    // Verify virtual scrolling works
    const visibleRows = await page.locator('tbody tr').count()
    expect(visibleRows).toBeLessThan(100) // Only visible rows rendered
  })

  test('form validation is responsive', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[name="email"]', 'invalid')

    // Measure validation feedback time
    const startTime = Date.now()
    await page.locator('text=Invalid email').waitFor()
    const feedbackTime = Date.now() - startTime

    expect(feedbackTime).toBeLessThan(100) // < 100ms
  })
})
```

---

## Migration from Magic MCP

### What Changed in Shannon

**Before (Magic MCP)**:
- AI-generated UI components from 21st.dev patterns
- Custom component implementations
- Variable quality and accessibility
- Limited customization control
- Magic-specific syntax and workflows

**After (shadcn MCP)**:
- Production-ready shadcn/ui components
- Radix UI primitives with accessibility built-in
- Full control over component source code
- Industry-standard patterns (2025)
- Direct component ownership in codebase

### Migration Strategy

**Step 1: Identify Magic Components**
```bash
# Find Magic-generated components
grep -r "// Generated by Magic MCP" src/components
```

**Step 2: Map to shadcn Equivalents**
| Magic Component | shadcn Component |
|-----------------|------------------|
| Magic Button | button |
| Magic Input | input |
| Magic Modal | dialog |
| Magic Form | form |
| Magic Card | card |
| Magic Table | data-table |
| Magic Dropdown | dropdown-menu |
| Magic Tooltip | tooltip |

**Step 3: Install shadcn Components**
```bash
# Install all needed components
npx shadcn add button input dialog form card data-table dropdown-menu tooltip
```

**Step 4: Replace Imports**
```typescript
// Before
import { MagicButton } from "@/components/magic/button"
import { MagicInput } from "@/components/magic/input"

// After
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
```

**Step 5: Update Props**
```typescript
// Before (Magic)
<MagicButton
  theme="primary"
  onClick={handleClick}
>
  Click Me
</MagicButton>

// After (shadcn)
<Button
  variant="default"
  onClick={handleClick}
>
  Click Me
</Button>
```

**Step 6: Test Replacement**
```typescript
// Create Puppeteer test for new component
test('button works after migration', async ({ page }) => {
  await page.goto('/test-page')
  await page.click('button:has-text("Click Me")')
  // Verify behavior
})
```

**Step 7: Remove Magic Components**
```bash
# After testing passes
rm -rf src/components/magic
```

### Workflow Adaptations

**Old Workflow (Magic)**:
```yaml
1. Request UI component
2. Magic MCP generates custom component
3. Review generated code
4. Accept or regenerate
5. Manually test in browser
```

**New Workflow (shadcn)**:
```yaml
1. Request UI component
2. list_components() to find match
3. get_component_demo() to review
4. npx shadcn add [component]
5. Customize in your project
6. Puppeteer test validates
```

### Key Benefits of Migration

**Accessibility**: Radix UI primitives provide WCAG 2.1 AA compliance
**Ownership**: Components in your codebase, full control
**Consistency**: Industry-standard patterns, not custom implementations
**Testing**: Easier to test with Puppeteer (semantic HTML, ARIA attributes)
**Maintenance**: Update components directly, no external dependency issues

---

## Best Practices

### Component Selection Guidelines

**When to Use shadcn Components**:
✅ Building forms with validation (use `form`, `input`, `button`)
✅ Creating data tables with sorting/filtering (use `data-table`)
✅ Implementing modals and overlays (use `dialog`, `sheet`, `popover`)
✅ Building dashboards (use shadcn blocks)
✅ Need accessibility compliance (Radix UI primitives)

**When to Build Custom**:
❌ Highly specialized domain-specific components
❌ Components requiring unique animations not supported by shadcn
❌ Legacy system integration with specific markup requirements

### Customization Patterns

**Theme Customization**:
```css
/* app/globals.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    /* ... customize all tokens */
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... dark mode tokens */
  }
}
```

**Component Extension**:
```typescript
// components/ui/button.tsx
import { Button as ShadcnButton } from "@/components/ui/button"

// Add new variant
export const Button = React.forwardRef<
  HTMLButtonElement,
  ButtonProps & { variant?: "custom" | ... }
>(({ variant, ...props }, ref) => {
  if (variant === "custom") {
    return <ShadcnButton className="custom-styles" {...props} ref={ref} />
  }
  return <ShadcnButton variant={variant} {...props} ref={ref} />
})
```

**Composition Patterns**:
```typescript
// components/composite/search-dialog.tsx
import { Dialog, DialogContent } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Command } from "@/components/ui/command"

export function SearchDialog() {
  return (
    <Dialog>
      <DialogContent>
        <Command>
          <Input placeholder="Search..." />
          {/* Command results */}
        </Command>
      </DialogContent>
    </Dialog>
  )
}
```

### Performance Optimization

**1. Tree Shaking**
```typescript
// ✅ Import only what you need
import { Button } from "@/components/ui/button"

// ❌ Don't import entire modules
import * as Components from "@/components/ui"
```

**2. Code Splitting**
```typescript
// Dynamic import for heavy components
const DataTable = dynamic(() => import("@/components/ui/data-table"))
const Chart = dynamic(() => import("@/components/ui/chart"))
```

**3. Memoization**
```typescript
import { memo } from "react"
import { Button } from "@/components/ui/button"

export const MemoizedButton = memo(Button)
```

**4. Virtual Scrolling for Large Lists**
```typescript
import { DataTable } from "@/components/ui/data-table"
import { useVirtualizer } from "@tanstack/react-virtual"

// Use with data-table for 1000+ rows
```

### Accessibility Standards (2025)

**WCAG 2.1 AA Compliance**:
- Color contrast ratios ≥ 4.5:1 for text
- Keyboard navigation for all interactive elements
- Focus indicators visible and distinct
- Screen reader announcements for dynamic content
- ARIA labels and descriptions

**shadcn Accessibility Features**:
- Radix UI primitives handle keyboard navigation
- Focus management in dialogs and popovers
- ARIA attributes included by default
- Semantic HTML structure

**Testing Accessibility**:
```typescript
// Use axe-playwright for automated testing
import { injectAxe, checkA11y } from 'axe-playwright'

test('component meets WCAG AA', async ({ page }) => {
  await page.goto('/component')
  await injectAxe(page)
  await checkA11y(page)
})
```

---

## Troubleshooting

### MCP Server Issues

**Issue**: `list_components()` returns empty or errors

**Solutions**:
1. Verify GitHub token is set in configuration
2. Restart Claude Desktop after config changes
3. Check network connectivity to GitHub
4. Ensure token has `public_repo` scope

**Issue**: `get_component()` returns 404

**Solutions**:
1. Verify component name is correct (use `list_components()` first)
2. Check shadcn/ui repository is accessible
3. Ensure component exists in latest shadcn version

### Component Installation Errors

**Issue**: `npx shadcn add button` fails

**Solutions**:
1. Verify `components.json` exists in project root
2. Run `npx shadcn@latest init` if missing
3. Check Tailwind CSS is properly configured
4. Ensure all peer dependencies are installed

**Issue**: Component styling doesn't apply

**Solutions**:
1. Verify Tailwind CSS is processing component files
2. Check `tailwind.config.js` content paths include components
3. Ensure CSS variables are defined in `globals.css`
4. Run Tailwind build process

**Issue**: TypeScript errors in shadcn components

**Solutions**:
1. Install `@types/node` and `@types/react`
2. Update TypeScript to latest version
3. Check `tsconfig.json` includes component paths
4. Verify all component dependencies are installed

### Testing Failures

**Issue**: Puppeteer can't find component

**Solutions**:
1. Ensure component is rendered in DOM
2. Use `data-testid` attributes for reliable selection
3. Wait for component to be visible: `await page.waitForSelector()`
4. Check component isn't hidden by CSS

**Issue**: Accessibility tests fail

**Solutions**:
1. Review axe-core error messages
2. Verify color contrast ratios in design tokens
3. Ensure all form inputs have labels
4. Add ARIA labels where semantic HTML isn't sufficient

**Issue**: Form validation tests fail

**Solutions**:
1. Verify react-hook-form is properly configured
2. Check zod schema matches expected validation
3. Ensure error messages are rendered in DOM
4. Wait for async validation to complete

### Common Mistakes

**Mistake**: Treating shadcn as an npm package
```typescript
// ❌ Wrong
import { Button } from "shadcn-ui"

// ✅ Correct
import { Button } from "@/components/ui/button"
```

**Mistake**: Not customizing components
```typescript
// ❌ Using default without customization
<Button>Click Me</Button>

// ✅ Customizing for project needs
<Button className="w-full" variant="primary">Click Me</Button>
```

**Mistake**: Ignoring dependencies
```bash
# ❌ Installing complex component alone
npx shadcn add data-table

# ✅ Installing with dependencies
npx shadcn add data-table table dropdown-menu checkbox
```

**Mistake**: Not testing accessibility
```typescript
// ❌ Skipping accessibility tests
test('button works', async ({ page }) => { /* ... */ })

// ✅ Including accessibility validation
test('button is accessible', async ({ page }) => {
  await injectAxe(page)
  await checkA11y(page, 'button')
})
```

---

## Examples

### Login Form with shadcn

```typescript
// components/auth/login-form.tsx
"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"

const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
})

export function LoginForm() {
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const form = useForm<z.infer<typeof loginSchema>>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  })

  async function onSubmit(values: z.infer<typeof loginSchema>) {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      })

      if (!response.ok) {
        throw new Error("Invalid credentials")
      }

      // Redirect on success
      window.location.href = "/dashboard"
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Welcome Back</CardTitle>
        <CardDescription>Sign in to your account to continue</CardDescription>
      </CardHeader>
      <CardContent>
        {error && (
          <Alert variant="destructive" className="mb-4">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input
                      type="email"
                      placeholder="you@example.com"
                      autoComplete="email"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <Input
                      type="password"
                      placeholder="••••••••"
                      autoComplete="current-password"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Signing in..." : "Sign In"}
            </Button>
          </form>
        </Form>
      </CardContent>
      <CardFooter className="flex justify-center">
        <Button variant="link" size="sm">
          Forgot your password?
        </Button>
      </CardFooter>
    </Card>
  )
}
```

**Puppeteer Test**:
```typescript
// tests/auth/login-form.test.ts
import { test, expect } from '@playwright/test'

test.describe('Login Form', () => {
  test('validates email format', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[type="email"]', 'invalid-email')
    await page.click('button[type="submit"]')

    await expect(page.locator('text=Invalid email address')).toBeVisible()
  })

  test('validates password length', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[type="email"]', 'user@example.com')
    await page.fill('input[type="password"]', 'short')
    await page.click('button[type="submit"]')

    await expect(page.locator('text=Password must be at least 8 characters')).toBeVisible()
  })

  test('shows error on invalid credentials', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[type="email"]', 'wrong@example.com')
    await page.fill('input[type="password"]', 'wrongpassword')
    await page.click('button[type="submit"]')

    await expect(page.locator('text=Invalid credentials')).toBeVisible()
  })

  test('redirects on successful login', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[type="email"]', 'user@example.com')
    await page.fill('input[type="password"]', 'correctpassword')
    await page.click('button[type="submit"]')

    await expect(page).toHaveURL('/dashboard')
  })
})
```

### Dashboard with shadcn Blocks

```typescript
// components/dashboard/dashboard-shell.tsx
"use client"

import { useState } from "react"
import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { Sheet, SheetContent } from "@/components/ui/sheet"

export function DashboardShell({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex lg:w-64 lg:flex-col border-r">
        <Sidebar />
      </aside>

      {/* Mobile Sidebar */}
      <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
        <SheetContent side="left" className="w-64 p-0">
          <Sidebar />
        </SheetContent>
      </Sheet>

      {/* Main Content */}
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header onMenuClick={() => setSidebarOpen(true)} />
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
    </div>
  )
}

// components/dashboard/sidebar.tsx
import { Home, BarChart, Settings, Users } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { usePathname } from "next/navigation"
import Link from "next/link"

const navItems = [
  { title: "Overview", href: "/dashboard", icon: Home },
  { title: "Analytics", href: "/dashboard/analytics", icon: BarChart },
  { title: "Team", href: "/dashboard/team", icon: Users },
  { title: "Settings", href: "/dashboard/settings", icon: Settings },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <div className="flex flex-col h-full">
      <div className="p-6">
        <h2 className="text-2xl font-bold">Dashboard</h2>
      </div>
      <nav className="flex-1 px-4 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href

          return (
            <Link key={item.href} href={item.href}>
              <Button
                variant={isActive ? "secondary" : "ghost"}
                className="w-full justify-start"
              >
                <Icon className="mr-2 h-4 w-4" />
                {item.title}
              </Button>
            </Link>
          )
        })}
      </nav>
      <div className="p-4 border-t">
        <div className="flex items-center gap-3">
          <Avatar>
            <AvatarImage src="/avatar.png" />
            <AvatarFallback>JD</AvatarFallback>
          </Avatar>
          <div>
            <p className="text-sm font-medium">John Doe</p>
            <p className="text-xs text-muted-foreground">john@example.com</p>
          </div>
        </div>
      </div>
    </div>
  )
}

// components/dashboard/header.tsx
import { Menu } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

export function Header({ onMenuClick }: { onMenuClick: () => void }) {
  return (
    <header className="border-b">
      <div className="flex h-16 items-center px-6">
        <Button
          variant="ghost"
          size="icon"
          className="lg:hidden"
          onClick={onMenuClick}
        >
          <Menu className="h-6 w-6" />
        </Button>
        <div className="ml-auto">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                <Avatar className="h-8 w-8">
                  <AvatarImage src="/avatar.png" />
                  <AvatarFallback>JD</AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>My Account</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>Profile</DropdownMenuItem>
              <DropdownMenuItem>Settings</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem>Log out</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  )
}
```

### Data Table with shadcn

```typescript
// components/data-table/users-table.tsx
"use client"

import { ColumnDef } from "@tanstack/react-table"
import { DataTable } from "@/components/ui/data-table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { MoreHorizontal } from "lucide-react"

interface User {
  id: string
  name: string
  email: string
  role: "admin" | "user" | "guest"
  status: "active" | "inactive"
}

export const columns: ColumnDef<User>[] = [
  {
    accessorKey: "name",
    header: "Name",
  },
  {
    accessorKey: "email",
    header: "Email",
  },
  {
    accessorKey: "role",
    header: "Role",
    cell: ({ row }) => {
      const role = row.getValue("role") as string
      return (
        <Badge variant={role === "admin" ? "default" : "secondary"}>
          {role}
        </Badge>
      )
    },
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.getValue("status") as string
      return (
        <Badge variant={status === "active" ? "default" : "outline"}>
          {status}
        </Badge>
      )
    },
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const user = row.original

      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <span className="sr-only">Open menu</span>
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Actions</DropdownMenuLabel>
            <DropdownMenuItem onClick={() => navigator.clipboard.writeText(user.id)}>
              Copy user ID
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem>View details</DropdownMenuItem>
            <DropdownMenuItem>Edit user</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )
    },
  },
]

export function UsersTable({ data }: { data: User[] }) {
  return <DataTable columns={columns} data={data} />
}
```

---

## Additional Resources

- **shadcn/ui Documentation**: https://ui.shadcn.com
- **Radix UI Documentation**: https://www.radix-ui.com
- **Tailwind CSS**: https://tailwindcss.com
- **Playwright Testing**: https://playwright.dev
- **Shannon Framework**: https://github.com/nickpending/shannon

---

**Last Updated**: 2025-01-28
**Shannon Version**: 1.0.0
**shadcn/ui Version**: Latest (2025)