-- Shannon CLI V3.0 Analytics Database Schema
-- Location: ~/.shannon/analytics.db
-- Purpose: Historical tracking, trends, and insights

-- Main sessions table: records each spec analysis execution
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    spec_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    complexity_score REAL NOT NULL,
    interpretation TEXT NOT NULL,  -- 'simple', 'moderate', 'complex', etc.
    timeline_days INTEGER NOT NULL,
    actual_timeline_days INTEGER,  -- NULL if not completed
    cost_total_usd REAL DEFAULT 0.0,
    waves_executed INTEGER DEFAULT 0,
    has_context BOOLEAN DEFAULT 0,
    project_id TEXT
);

-- Dimension scores: 8-dimensional breakdown per session
CREATE TABLE IF NOT EXISTS dimension_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    dimension TEXT NOT NULL,  -- 'structural', 'cognitive', 'coordination', etc.
    score REAL NOT NULL,
    weight REAL NOT NULL,
    contribution REAL NOT NULL,  -- score * weight
    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

-- Domains: domain breakdown per session (Frontend, Backend, etc.)
CREATE TABLE IF NOT EXISTS domains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    domain TEXT NOT NULL,  -- 'Frontend', 'Backend', 'Analytics', etc.
    percentage INTEGER NOT NULL,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

-- Wave executions: track each wave execution for performance analysis
CREATE TABLE IF NOT EXISTS wave_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    wave_number INTEGER NOT NULL,
    agent_count INTEGER NOT NULL,
    duration_minutes REAL NOT NULL,
    cost_usd REAL NOT NULL,
    speedup_factor REAL,  -- vs sequential execution
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

-- MCP usage tracking: which MCPs are recommended, installed, and used
CREATE TABLE IF NOT EXISTS mcp_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    mcp_name TEXT NOT NULL,
    installed BOOLEAN DEFAULT 0,
    used BOOLEAN DEFAULT 0,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

-- Cost savings tracking: analytics on cost optimization
CREATE TABLE IF NOT EXISTS cost_savings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    saving_type TEXT NOT NULL,  -- 'cache_hit', 'model_optimization', etc.
    amount_usd REAL NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_sessions_complexity ON sessions(complexity_score);
CREATE INDEX IF NOT EXISTS idx_sessions_created ON sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_sessions_project ON sessions(project_id);
CREATE INDEX IF NOT EXISTS idx_domains_domain ON domains(domain);
CREATE INDEX IF NOT EXISTS idx_waves_session ON wave_executions(session_id);
CREATE INDEX IF NOT EXISTS idx_dimension_scores_session ON dimension_scores(session_id);
CREATE INDEX IF NOT EXISTS idx_mcp_usage_session ON mcp_usage(session_id);
