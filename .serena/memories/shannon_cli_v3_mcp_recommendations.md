# Shannon CLI V3 - MCP Recommendations

**Analysis ID**: spec_analysis_20250113_194500

## Tier 1: MANDATORY (1 MCP)

### 1. Serena MCP ⚡ REQUIRED
**Purpose**: Context preservation and knowledge graph storage for Shannon Framework  
**Usage**: Save analysis results, project context, agent state across waves  
**When**: Every Shannon operation (analyze, wave, checkpoint, restore)  
**Trigger**: Always (Shannon Framework core requirement)  
**Priority**: MANDATORY  
**Fallback**: Local file storage (DEGRADED - loses cross-session context)  
**Setup**: `claude mcp add serena` or `/shannon:check_mcps`

---

## Tier 2: PRIMARY (3 MCPs) - Domain ≥20%

### 2. Context7 MCP 📚
**Purpose**: Up-to-date Python, Rich library, and Claude SDK documentation  
**Usage**: Look up Rich API (Layout, Panel, Live), Python async patterns, SDK reference  
**When**: Implementing metrics dashboard, SDK integration, terminal UI  
**Trigger**: Backend/Infrastructure domain ≥20% (30% ✓)  
**Domain**: Backend 30%  
**Priority**: PRIMARY  
**Fallback**: Manual documentation lookup (slower, may be outdated)  
**Setup**: `claude mcp add context7`

### 3. Sequential MCP 🧠
**Purpose**: Deep systematic reasoning (100-200 step analysis) for complex architecture  
**Usage**: Analyze cache strategies, agent synchronization, cost algorithms  
**When**: Critical design decisions in Phase 2 (Architecture & Design)  
**Trigger**: Cognitive ≥0.70 (0.75 ✓) OR overall complexity ≥0.60 (0.60 ✓)  
**Priority**: PRIMARY  
**Fallback**: Native Claude reasoning (less structured, no hypothesis tracking)  
**Setup**: `claude mcp add sequential-thinking`

### 4. SQLite MCP 🗄️
**Purpose**: Database schema design and query optimization for analytics  
**Usage**: Create analytics.db schema, optimize trend queries, migrations  
**When**: Implementing historical analytics feature (Week 6-7)  
**Trigger**: Analytics 20% + explicit "SQLite database" mentioned  
**Domain**: Analytics 20%  
**Priority**: PRIMARY  
**Fallback**: Standard sqlite3 library (less optimized, manual queries)  
**Setup**: `claude mcp add sqlite` (if available)

---

## Tier 3: SECONDARY (2 MCPs)

### 5. GitHub MCP 🐙
**Purpose**: Repository management, issue tracking, CI/CD automation  
**Usage**: Manage shannon-cli repo, track issues, automate releases  
**When**: Throughout development for version control  
**Priority**: SECONDARY  
**Fallback**: Manual git/gh CLI commands  
**Setup**: `claude mcp add github`

### 6. Tavily MCP 🔍
**Purpose**: Research Rich library best practices, terminal UI patterns  
**Usage**: When encountering implementation questions  
**When**: As-needed during implementation  
**Priority**: SECONDARY  
**Fallback**: Manual web search  
**Setup**: `claude mcp add tavily`

---

## Tier 4: OPTIONAL (1 MCP)

### 7. PyPI MCP 📦
**Purpose**: Package distribution to Python Package Index  
**Usage**: Publish shannon-cli for pip installation  
**When**: Phase 5 (Deployment & Documentation)  
**Priority**: OPTIONAL  
**Fallback**: Manual twine upload  
**Setup**: `claude mcp add pypi` (if exists)

---

## Installation Priority

**Install Now** (before Phase 2):
- Serena MCP (mandatory)
- Context7 MCP (will use heavily for SDK/Rich docs)
- Sequential MCP (needed for architecture decisions)

**Install Later** (as needed):
- SQLite MCP (Week 6 when implementing analytics)
- GitHub MCP (when setting up CI/CD)
- Tavily MCP (if research questions arise)
- PyPI MCP (Week 10 for deployment)

---

## MCP Usage Patterns

**Serena**: Every command (context save/load)  
**Context7**: Phase 2-3 (architecture, implementation)  
**Sequential**: Phase 2 (critical decisions only, 2-3 times)  
**SQLite**: Phase 3 (analytics implementation, Week 6-7)  
**GitHub**: Phase 3-5 (repo management, CI/CD)  
**Tavily**: As-needed (research, best practices)  
**PyPI**: Phase 5 (deployment)

---

**Total**: 7 MCPs recommended (appropriate for 0.60 COMPLEX project)