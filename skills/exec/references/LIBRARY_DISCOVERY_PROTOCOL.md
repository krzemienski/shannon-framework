# Library Discovery Protocol

**Version:** Shannon V3.5
**Status:** Production
**Last Updated:** November 15, 2025

## Overview

The Library Discovery Protocol is a mandatory research phase that occurs BEFORE implementing any major feature or functionality. This protocol prevents reinventing the wheel by ensuring agents discover and evaluate existing open-source libraries instead of building custom solutions.

## Purpose

- **Reduce Development Time**: Leverage battle-tested libraries instead of building from scratch
- **Improve Code Quality**: Use well-maintained, peer-reviewed solutions
- **Minimize Technical Debt**: Avoid maintaining custom implementations of solved problems
- **Enhance Reliability**: Benefit from community testing and bug fixes

## Mandatory Process

### 1. Identify Feature Needs

Before writing any substantial code, clearly identify what functionality is required.

**Examples:**
- Authentication and authorization
- UI component library
- HTTP client and networking
- Database ORM and migrations
- State management
- Form handling and validation
- Chart rendering and data visualization
- File upload and processing

### 2. Search Package Registries

Search the appropriate package registry for your technology stack:

| Technology | Primary Registry | Search URL |
|------------|-----------------|------------|
| JavaScript/TypeScript | npm | https://npmjs.com |
| Python | PyPI | https://pypi.org |
| Swift/iOS | Swift Package Manager | https://swiftpackageindex.com |
| Swift/iOS | CocoaPods | https://cocoapods.org |
| Java/Android | Maven Central | https://search.maven.org |
| Rust | Crates.io | https://crates.io |
| Go | Go Packages | https://pkg.go.dev |
| Ruby | RubyGems | https://rubygems.org |

**Search Strategy:**
1. Use descriptive keywords (e.g., "react authentication", "python orm", "ios networking")
2. Sort by relevance and popularity
3. Check official "awesome" lists (e.g., awesome-react, awesome-python)
4. Review technology-specific recommendations

### 3. Evaluate Top Candidates

For each of the top 3-5 options, evaluate based on these criteria:

#### Critical Evaluation Criteria

| Criterion | Target | Why It Matters |
|-----------|--------|----------------|
| GitHub Stars | >1,000 for production | Indicates community adoption and trust |
| Last Update | Within 6 months | Shows active maintenance |
| Weekly Downloads | High for category | Proves real-world usage |
| Open Issues | Low ratio to stars | Indicates maintainer responsiveness |
| License | MIT, Apache 2.0, BSD | Permissive for commercial use |
| Documentation | Comprehensive | Easier integration and debugging |
| TypeScript Support | Yes (for JS/TS) | Better developer experience |
| Breaking Changes | Semantic versioning | Predictable upgrade path |

#### Evaluation Example

```markdown
## Evaluating React Form Libraries

### Option 1: react-hook-form
- Stars: 39.5k ⭐
- Last update: 2 weeks ago ✅
- Weekly downloads: 3.2M ✅
- License: MIT ✅
- Docs: Excellent with live examples ✅
- TypeScript: Full support ✅
- Bundle size: 8.6kB (smallest) ✅

### Option 2: Formik
- Stars: 33.2k ⭐
- Last update: 6 months ago ⚠️
- Weekly downloads: 2.1M ✅
- License: Apache 2.0 ✅
- Docs: Good ✅
- TypeScript: Community types ⚠️
- Bundle size: 15kB (larger) ⚠️

### Option 3: Final Form
- Stars: 7.3k ⭐
- Last update: 1 year ago ❌
- Weekly downloads: 180k ⚠️
- License: MIT ✅
- Docs: Good ✅
- TypeScript: Partial support ⚠️
- Bundle size: 5.2kB ✅

**Decision: react-hook-form**
- Most actively maintained
- Best TypeScript support
- Highest downloads (proven at scale)
- Smallest bundle size
- Best documentation
```

### 4. Document Selection Decision

Create a clear record of your decision:

```markdown
## Library Selection: react-hook-form

**Version:** ^7.48.2

**Why this library:**
- Most actively maintained (updated 2 weeks ago)
- Excellent TypeScript support out of the box
- Smallest bundle size (8.6kB) - important for performance
- Highest weekly downloads (3.2M) - battle-tested at scale
- Superior documentation with interactive examples
- Built-in validation with zod/yup integration
- Better performance (uncontrolled components)

**Alternatives considered:**
- Formik: Less active maintenance, no built-in TS support
- Final Form: Outdated, lower adoption

**Installation:**
```bash
npm install react-hook-form zod @hookform/resolvers
```

**Basic usage pattern:**
```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
});

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema)
  });

  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("email")} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="password" {...register("password")} />
      {errors.password && <span>{errors.password.message}</span>}

      <button type="submit">Login</button>
    </form>
  );
}
```
```

### 5. Add to Project Dependencies

Install the library using the appropriate package manager:

#### Node.js/JavaScript/TypeScript
```bash
# npm
npm install <package-name>

# yarn
yarn add <package-name>

# pnpm
pnpm add <package-name>
```

#### Python
```bash
# pip
pip install <package-name>

# poetry
poetry add <package-name>

# pipenv
pipenv install <package-name>
```

#### Swift/iOS
```ruby
# CocoaPods (Podfile)
pod 'Alamofire', '~> 5.8'

# Swift Package Manager (Package.swift)
dependencies: [
    .package(url: "https://github.com/Alamofire/Alamofire.git", from: "5.8.0")
]
```

#### Java/Android
```groovy
// Gradle (build.gradle)
dependencies {
    implementation 'com.squareup.okhttp3:okhttp:4.12.0'
}
```

### 6. Use in Implementation

Once installed, use the library in your implementation. Do NOT build a custom alternative.

## Common Libraries by Category

### Authentication & Authorization

#### Web Applications
- **next-auth** (Next.js): Comprehensive auth for Next.js apps
- **Auth0 SDK**: Enterprise-grade authentication service
- **passport.js**: Flexible authentication middleware for Express
- **clerk**: Modern auth with pre-built UI components
- **supabase/auth-js**: Open-source Firebase alternative

#### Mobile Applications
- **expo-auth-session** (React Native/Expo): OAuth flows for Expo apps
- **react-native-app-auth**: Native OAuth 2.0 support for RN
- **AuthenticationServices** (iOS): Built-in Sign in with Apple

#### Python
- **FastAPI-Users**: Complete user management for FastAPI
- **django-allauth**: Integrated authentication for Django
- **authlib**: OAuth 1.0/2.0 client and server library

### UI Components & Design Systems

#### React
- **shadcn/ui**: Accessible, customizable components (Radix UI + Tailwind)
- **Material-UI (MUI)**: Google's Material Design in React
- **Chakra UI**: Simple, modular, accessible component library
- **Headless UI**: Unstyled, accessible UI components
- **Radix UI**: Low-level UI primitives for design systems

#### React Native
- **react-native-paper**: Material Design for React Native
- **NativeBase**: Universal component library (iOS + Android + Web)
- **react-native-elements**: Cross-platform UI toolkit

#### Vue
- **Vuetify**: Material Design component framework
- **PrimeVue**: Rich UI component suite
- **Quasar**: Cross-platform Vue framework

#### SwiftUI
- Use built-in components (Apple strongly recommends native)

### Networking & HTTP Clients

#### JavaScript/TypeScript
- **axios**: Promise-based HTTP client (most popular)
- **ky**: Tiny HTTP client with retry and timeout
- **got**: Human-friendly HTTP library with advanced features
- **ofetch**: Fetch-based HTTP client with better defaults

#### Swift/iOS
- **Alamofire**: Elegant HTTP networking in Swift
- **URLSession**: Built-in (prefer native for simple use cases)

#### Python
- **httpx**: Modern async HTTP client
- **requests**: Simple HTTP library (sync)
- **aiohttp**: Async HTTP client/server framework

#### Java/Android
- **OkHttp**: Efficient HTTP client for Android and Java
- **Retrofit**: Type-safe HTTP client for Android

### State Management

#### React
- **Redux Toolkit**: Official Redux toolset (batteries-included)
- **Zustand**: Lightweight state management (minimal boilerplate)
- **Jotai**: Atomic state management (primitive + flexible)
- **Recoil**: Graph-based state management from Meta
- **TanStack Query**: Server state management (caching + fetching)

#### React Native
- **Redux**: Popular for complex apps
- **Zustand**: Lightweight alternative (recommended for new projects)
- **MobX**: Observable-based state management

#### Vue
- **Pinia**: Official Vue state management (replaces Vuex)
- **Vuex**: Legacy Vue state management

### Forms & Validation

#### React
- **react-hook-form**: Performant forms with easy validation
- **formik**: Complete form solution (more boilerplate)
- **zod**: TypeScript-first schema validation
- **yup**: JavaScript schema validation

#### Python
- **Pydantic**: Data validation using Python type annotations (built into FastAPI)
- **marshmallow**: Object serialization/deserialization

### Data Fetching & Caching

#### React
- **TanStack Query** (formerly React Query): Powerful data fetching/caching
- **SWR**: Stale-while-revalidate data fetching from Vercel
- **Apollo Client**: GraphQL client with caching

#### Python
- **SQLAlchemy**: SQL toolkit and ORM
- **Tortoise ORM**: Easy async ORM inspired by Django
- **Prisma Client Python**: Type-safe database client

### Database & ORM

#### JavaScript/TypeScript
- **Prisma**: Next-gen ORM with type safety
- **TypeORM**: TypeScript ORM for SQL databases
- **Sequelize**: Promise-based ORM for Node.js
- **Drizzle ORM**: Lightweight TypeScript ORM
- **Kysely**: Type-safe SQL query builder

#### Python
- **SQLAlchemy**: Most popular Python ORM
- **Tortoise ORM**: Async ORM for FastAPI
- **Django ORM**: Built into Django framework
- **Peewee**: Small, expressive ORM

#### Database Migrations
- **Alembic** (Python): Database migrations for SQLAlchemy
- **Drizzle Kit**: Schema migrations for Drizzle
- **TypeORM migrations**: Built into TypeORM
- **Prisma Migrate**: Declarative migrations

### Testing

#### JavaScript/TypeScript
- **Jest**: Comprehensive testing framework
- **Vitest**: Fast Vite-native testing framework
- **Playwright**: End-to-end testing for web apps
- **Cypress**: E2E testing with great DX

#### Python
- **pytest**: Feature-rich testing framework
- **pytest-asyncio**: Async test support
- **httpx**: For testing async HTTP APIs
- **pytest-cov**: Coverage plugin

#### Swift/iOS
- **XCTest**: Built-in testing framework (prefer native)
- **Quick/Nimble**: BDD-style testing (alternative)

### Charts & Visualization

#### React
- **recharts**: Composable charting library
- **victory**: Modular charting components
- **chart.js**: Simple yet flexible JavaScript charting
- **visx**: Low-level visualization primitives

#### React Native
- **react-native-chart-kit**: Simple charts for RN
- **victory-native**: Victory for React Native

### Icons

#### React
- **react-icons**: Popular icon sets in one package
- **lucide-react**: Beautiful, consistent icon set
- **heroicons**: Icons from Tailwind CSS makers

#### React Native
- **@expo/vector-icons**: Icon fonts for Expo (easiest)
- **react-native-vector-icons**: Popular icon sets for RN

#### Web
- **Font Awesome**: Comprehensive icon library
- **Material Icons**: Google's icon set

## DO NOT Implement from Scratch

**Never build custom implementations of these:**

❌ **Authentication systems** - Use next-auth, Auth0, clerk, passport.js
❌ **UI component libraries** - Use shadcn/ui, MUI, Chakra UI, NativeBase
❌ **HTTP clients** - Use axios, fetch, Alamofire, httpx
❌ **State management** - Use Redux Toolkit, Zustand, Pinia
❌ **Form validation** - Use react-hook-form, formik, Pydantic
❌ **Database ORMs** - Use Prisma, SQLAlchemy, TypeORM
❌ **WebSocket implementations** - Use socket.io, ws
❌ **Date/time handling** - Use date-fns, dayjs, luxon
❌ **Markdown parsing** - Use marked, remark, react-markdown
❌ **PDF generation** - Use jsPDF, pdfkit, ReportLab

## Always Prefer

✅ **Battle-tested libraries** with proven track record
✅ **Libraries with >1,000 GitHub stars** (for production)
✅ **Active maintenance** (updated within last 6 months)
✅ **Good documentation** (with examples and API reference)
✅ **Stack compatibility** (works with your dependencies)
✅ **TypeScript support** (for JS/TS projects)
✅ **Permissive licenses** (MIT, Apache 2.0, BSD)

## Exceptions: When to Build Custom

Build custom implementations ONLY in these cases:

1. **Highly specific business logic** unique to your domain
2. **Simple utilities** (<50 lines of code)
3. **Performance-critical code** where libraries add unacceptable overhead
4. **No suitable library exists** after thorough search and evaluation
5. **Library would pull in massive dependencies** for tiny functionality

**Before building custom, ask:**
> "Has someone already solved this problem with an open-source library?"

- **If YES** → Research, evaluate, use the library
- **If NO** → Verify with web search, then build custom with justification

## Quick Reference Decision Tree

```
Need to implement feature/functionality
    ↓
Does it involve common patterns?
    ↓
YES → Search package registry
    ↓
Found suitable libraries? (>=3 options)
    ↓
YES → Evaluate based on criteria
    ↓
Selected best option
    ↓
Document decision + Install + Use
    ↓
DONE ✅

---

Is functionality highly specific to domain?
    ↓
YES → Can you extract common parts?
    ↓
YES → Use library for common parts, custom for specific
NO → Build fully custom (document why)
```

## Best Practices

### 1. Document Library Decisions

Create a `docs/architecture/decisions/` directory with ADR (Architecture Decision Records):

```markdown
# ADR-003: Use TanStack Query for Data Fetching

## Status
Accepted

## Context
Need efficient server state management with caching, background updates,
and optimistic UI updates for our React application.

## Decision
Use TanStack Query (React Query) instead of Redux for server state.

## Consequences
- Automatic caching and background refetching
- Reduced boilerplate compared to Redux for API data
- Better developer experience with devtools
- Need to learn new mental model
- Will use Zustand for client-only state
```

### 2. Pin Dependencies

Always specify version ranges in package.json:

```json
{
  "dependencies": {
    "react-hook-form": "^7.48.2",  // ✅ Caret allows patches/minor
    "axios": "~1.6.0",              // ✅ Tilde allows patches only
    "lodash": "4.17.21"             // ✅ Exact version for stability
  }
}
```

### 3. Review Security Advisories

Before adding any library:
```bash
# npm
npm audit

# Check library on Snyk
https://snyk.io/advisor/npm-package/<package-name>
```

### 4. Check Bundle Size Impact

For frontend libraries, check bundle size:
```bash
# Use bundlephobia
https://bundlephobia.com/package/<package-name>

# Or install and analyze
npm install <package-name>
npx webpack-bundle-analyzer
```

### 5. Read the Source Code

For critical dependencies, briefly review the source:
- Check code quality
- Look for security red flags
- Understand how it works (for debugging)

## Common Pitfalls

### Pitfall 1: "Not Invented Here" Syndrome

**Problem:** Building custom solutions when good libraries exist.

**Solution:** Force yourself to search first, build second.

### Pitfall 2: Choosing Based on GitHub Stars Alone

**Problem:** Popular library might be abandoned or unsuitable for your needs.

**Solution:** Use all evaluation criteria, not just stars.

### Pitfall 3: Over-Engineering with Libraries

**Problem:** Adding heavy libraries for simple functionality.

**Example:**
```javascript
// ❌ Bad: Using lodash for simple operation
import _ from 'lodash';
const doubled = _.map(numbers, n => n * 2);

// ✅ Good: Use native array methods
const doubled = numbers.map(n => n * 2);
```

### Pitfall 4: Not Reading Documentation

**Problem:** Misusing library because you didn't read the docs.

**Solution:** Always read "Getting Started" and "Best Practices" sections.

### Pitfall 5: Ignoring License Compatibility

**Problem:** Using GPL library in proprietary project.

**Solution:** Check license compatibility before adoption.

## Integration Checklist

After selecting a library, complete this checklist:

- [ ] Installed with correct package manager
- [ ] Version pinned in package.json/requirements.txt
- [ ] Added to dependencies (not devDependencies if needed at runtime)
- [ ] Documented in ADR or ARCHITECTURE.md
- [ ] Security audit passed
- [ ] Basic usage example created
- [ ] TypeScript types available (if applicable)
- [ ] Tests updated to cover new library usage
- [ ] Team notified of new dependency

## Summary

The Library Discovery Protocol ensures agents:
1. **Research first, code second**
2. **Evaluate systematically** using defined criteria
3. **Document decisions** for future maintainers
4. **Prefer proven solutions** over custom implementations
5. **Build custom only when justified**

**Remember:** Every hour spent researching libraries saves days of implementation and maintenance.

---

**Next Steps:**
- After library selection, proceed to implementation
- Follow [Functional Validation Protocol](./FUNCTIONAL_VALIDATION_PROTOCOL.md) to verify integration
- Use [Git Workflow Protocol](./GIT_WORKFLOW_PROTOCOL.md) for atomic commits
