---
name: scaffold
description: Generate Shannon-optimized project structure with functional test scaffolding
usage: /shannon:scaffold <project_type> [--template <name>]
---

# Project Scaffolding Command (V4)

## Overview

Generates complete Shannon-optimized project structure by orchestrating multiple skills: spec-analysis for project type detection, project-indexing for structure creation, and functional-testing for test scaffold generation. Creates production-ready projects following Shannon conventions.

## Prerequisites

- Project name/type defined
- Serena MCP recommended for saving scaffold metadata
- MCP dependencies based on project type (detected automatically)

## Workflow

### Step 1: Validate Input

Parse project type and template:

**Project Type Detection**:
- Required argument: `<project_type>` (e.g., `web-app`, `api`, `mobile-app`, `fullstack`)
- Optional: `--template <name>` for pre-defined templates

**Supported Project Types**:
- `web-app` - React/Vue frontend application
- `api` - REST/GraphQL API backend
- `fullstack` - Combined frontend + backend
- `mobile-app` - iOS/Android native app
- `cli-tool` - Command-line application
- `library` - Reusable package/library
- `microservice` - Microservice component
- `monorepo` - Multi-package repository

### Step 2: Invoke spec-analysis Skill (Project Type Analysis)

Use `@skill spec-analysis` to understand project requirements:

**Invocation:**
```
@skill spec-analysis
- Input:
  * spec: {project_type} + {template_info}
  * mode: "scaffold"
  * analyze_structure: true
- Output: project_analysis
```

The skill will:
1. Interpret project type
2. Detect required domains (Frontend/Backend/Database/etc.)
3. Recommend tech stack
4. Identify MCP requirements
5. Estimate complexity

### Step 3: Invoke project-indexing Skill (Structure Creation)

Use `@skill project-indexing` to generate directory structure:

**Invocation:**
```
@skill project-indexing
- Input:
  * project_type: {from Step 2}
  * domains: {domain_percentages from Step 2}
  * template: {template_name if provided}
- Options:
  * create_directories: true
  * create_config_files: true
  * create_readme: true
  * shannon_conventions: true
- Output: project_structure
```

The skill will:
1. Create directory hierarchy
2. Generate configuration files
3. Setup package manifests
4. Create README with Shannon conventions
5. Add .gitignore, .editorconfig, etc.

### Step 4: Invoke functional-testing Skill (Test Scaffolding)

Use `@skill functional-testing` to create test infrastructure:

**Invocation:**
```
@skill functional-testing
- Input:
  * mode: "scaffold"
  * project_type: {from Step 2}
  * platform: {detected_platform}
  * domains: {domain_percentages}
- Options:
  * no_mocks: true (enforced)
  * create_test_dir: true
  * create_fixtures: true
  * create_helpers: true
- Output: test_scaffold
```

The skill will:
1. Create test directory structure
2. Generate test configuration
3. Setup test fixtures
4. Create test helper utilities
5. Generate example tests (NO MOCKS)

### Step 5: Present Results

Format and display scaffold summary:

```markdown
📦 Shannon Project Scaffold Generated
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Project Type**: {project_type}
**Template**: {template_name | "default"}
**Domains**: {domain_breakdown}
**Complexity**: {complexity_score}/1.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Directory Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{project_tree}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated Files
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Configuration:
{for each config_file}
✅ {file_path}
   - Purpose: {purpose}

Source Code:
{for each source_file}
✅ {file_path}
   - Type: {file_type}

Tests:
{for each test_file}
✅ {file_path}
   - Platform: {platform}
   - NO MOCKS: ✅

Documentation:
{for each doc_file}
✅ {file_path}
   - Content: {description}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tech Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{if frontend_domain}
Frontend:
├─ Framework: {frontend_framework}
├─ Language: {language}
└─ Build Tool: {build_tool}

{if backend_domain}
Backend:
├─ Framework: {backend_framework}
├─ Language: {language}
└─ Runtime: {runtime}

{if database_domain}
Database:
├─ Type: {database_type}
└─ ORM: {orm_tool}

{if mobile_domain}
Mobile:
├─ Platform: {platform}
├─ Language: {language}
└─ Framework: {framework}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Shannon Conventions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ NO MOCKS test framework configured
✅ Functional test directory structure
✅ Shannon-compatible README
✅ Project indexing metadata
✅ North Star goal placeholder
✅ Wave execution preparation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Required MCPs (Detected)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tier 1 - MANDATORY:
1. Serena MCP - Context preservation

Tier 2 - PRIMARY:
{for each primary_mcp}
{index}. {mcp_name}
   Purpose: {purpose}
   Setup: /shannon:check_mcps --setup {mcp_name}

Tier 3 - SECONDARY:
{for each secondary_mcp}
{index}. {mcp_name}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Review generated structure:
   cd {project_directory}
   ls -la

2. Install dependencies:
   {install_command}

3. Configure MCPs:
   /shannon:check_mcps

4. Set North Star goal:
   /shannon:north_star "Your project goal"

5. Run example tests:
   /shannon:\1

6. Start development:
   {start_command}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scaffold Metadata
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{if saved_to_serena}
💾 Scaffold metadata saved to Serena MCP
Key: {scaffold_key}
Retrieve: /shannon:restore {timestamp}
{else}
⚠️  Metadata not saved (Serena MCP unavailable)
{end if}

Created: {timestamp}
Shannon Version: 4.0.0
Template: {template_name}
```

### Step 6: Generate Project-Specific Documentation

Create project-specific Shannon documentation:

**Files Created**:
1. **README.md** - Project overview with Shannon integration notes
2. **AGENTS.md** - Agent onboarding context (Shannon V4 pattern)
3. **TESTING.md** - NO MOCKS testing guide for this project
4. **CONTRIBUTING.md** - Development workflow with Shannon commands

**README.md includes**:
- Project description
- Quick start guide
- Shannon Framework integration notes
- MCP requirements
- Testing approach (NO MOCKS)
- Development workflow

**AGENTS.md includes**:
- Project architecture overview
- Key directories explained
- Tech stack details
- Common development tasks
- Shannon command reference

## Output Format

See Step 5 presentation template above.

## Skill Dependencies

- spec-analysis (REQUIRED for project type detection)
- project-indexing (REQUIRED for structure creation)
- functional-testing (REQUIRED for test scaffolding)

## MCP Dependencies

**Always Required**:
- Serena MCP (save scaffold metadata)

**Domain-Specific** (detected automatically):
- Frontend projects: Magic MCP, Puppeteer MCP, Context7 MCP
- Backend projects: Context7 MCP, Sequential MCP
- Mobile projects: iOS Simulator MCPs
- Database projects: Database-specific MCPs

## Templates

### Built-in Templates

**web-app** - Single-page application
```
project/
├─ src/
│  ├─ components/
│  ├─ pages/
│  ├─ hooks/
│  └─ utils/
├─ tests/
│  └─ functional/
├─ public/
└─ package.json
```

**api** - REST/GraphQL backend
```
project/
├─ src/
│  ├─ routes/
│  ├─ controllers/
│  ├─ services/
│  ├─ models/
│  └─ middleware/
├─ tests/
│  └─ functional/
└─ package.json
```

**fullstack** - Combined frontend + backend
```
project/
├─ frontend/
│  ├─ src/
│  └─ tests/
├─ backend/
│  ├─ src/
│  └─ tests/
└─ package.json
```

**mobile-app** - iOS native app
```
project/
├─ App/
│  ├─ Views/
│  ├─ ViewModels/
│  ├─ Models/
│  └─ Services/
├─ Tests/
│  └─ UITests/
└─ Package.swift
```

**microservice** - Service component
```
project/
├─ src/
│  ├─ handlers/
│  ├─ services/
│  ├─ clients/
│  └─ config/
├─ tests/
│  └─ functional/
├─ docker/
└─ package.json
```

**monorepo** - Multi-package workspace
```
project/
├─ packages/
│  ├─ package-a/
│  ├─ package-b/
│  └─ shared/
├─ tests/
└─ package.json
```

### Custom Templates

Users can define custom templates in:
```
shannon-plugin/templates/{template-name}/
```

## Examples

### Example 1: Web Application

```bash
/shannon:scaffold web-app
```

Generates React SPA with Puppeteer tests.

### Example 2: REST API

```bash
/shannon:scaffold api
```

Generates Express API with functional API tests.

### Example 3: Fullstack with Template

```bash
/shannon:scaffold fullstack --template nextjs
```

Generates Next.js fullstack app using nextjs template.

### Example 4: Mobile App

```bash
/shannon:scaffold mobile-app --template ios-swiftui
```

Generates iOS app with SwiftUI and XCUITest scaffolds.

### Example 5: Microservice

```bash
/shannon:scaffold microservice --template nodejs-grpc
```

Generates Node.js microservice with gRPC and Docker.

## Shannon Conventions Applied

The scaffold enforces Shannon Framework conventions:

1. **NO MOCKS Testing**
   - All test scaffolds use real dependencies
   - Puppeteer for web, iOS Simulator for mobile
   - No mock libraries included

2. **Project Indexing**
   - AGENTS.md for agent onboarding
   - CLAUDE.md (optional) for project context
   - Clear directory structure

3. **Functional Test Structure**
   - `tests/functional/` directory
   - Test helpers for real dependencies
   - Example tests following NO MOCKS

4. **MCP Integration**
   - Detects required MCPs from project type
   - Provides setup instructions
   - Configures MCP usage patterns

5. **Wave-Ready**
   - Structure supports wave-based execution
   - Clear phase boundaries
   - Checkpoint-friendly architecture

## Notes

- **NEW in V4**: This is a new command that orchestrates 3 skills
- **Purpose**: Quickly bootstrap Shannon-compatible projects
- **Customization**: Generated structure is a starting point; customize as needed
- **Philosophy**: Opinionated scaffolding following Shannon best practices
- **Testing**: All scaffolds include functional tests (NO MOCKS)
