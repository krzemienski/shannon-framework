"""
Shannon CLI V3.0 - Analytics Database

SQLite database for historical tracking, trends, and insights.
Location: ~/.shannon/analytics.db

Tables:
- sessions: Main analysis sessions
- dimension_scores: 8D complexity breakdown
- domains: Domain distribution per session
- wave_executions: Wave performance tracking
- mcp_usage: MCP recommendation and usage
- cost_savings: Cost optimization tracking
"""

import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from contextlib import contextmanager
import hashlib
import json


class AnalyticsDatabase:
    """
    SQLite database for Shannon CLI analytics.

    Provides CRUD operations for all analytics tables with:
    - Parameterized queries (SQL injection prevention)
    - Context manager for connections
    - Graceful handling of missing database
    - Index-optimized queries
    """

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize analytics database.

        Args:
            db_path: Custom database path. Defaults to ~/.shannon/analytics.db
        """
        self.db_path = db_path or (Path.home() / ".shannon" / "analytics.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize schema on first use
        self._initialize_schema()

    @contextmanager
    def _get_connection(self):
        """
        Context manager for database connections.

        Yields connection with row_factory set to sqlite3.Row for dict-like access.
        Ensures proper cleanup even if exceptions occur.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return dicts instead of tuples
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _initialize_schema(self):
        """Create tables and indexes if they don't exist."""
        schema_path = Path(__file__).parent / "schema.sql"

        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        schema = schema_path.read_text()

        with self._get_connection() as conn:
            conn.executescript(schema)

    # ===== Session Operations =====

    def record_session(
        self,
        session_id: str,
        analysis_result: Dict[str, Any],
        has_context: bool = False,
        project_id: Optional[str] = None
    ) -> None:
        """
        Record analysis session with full complexity breakdown.

        Args:
            session_id: Unique session identifier
            analysis_result: Dict with complexity_score, interpretation, timeline_days, etc.
            has_context: Whether session had existing context loaded
            project_id: Optional project identifier for tracking
        """
        with self._get_connection() as conn:
            # Record main session
            conn.execute("""
                INSERT INTO sessions (
                    session_id, spec_hash, complexity_score,
                    interpretation, timeline_days, cost_total_usd,
                    has_context, project_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                analysis_result.get('spec_hash', ''),
                analysis_result.get('complexity_score', 0.0),
                analysis_result.get('interpretation', 'unknown'),
                analysis_result.get('timeline_days', 0),
                analysis_result.get('estimated_cost', 0.0),
                has_context,
                project_id
            ))

            # Record dimension scores
            dimensions = analysis_result.get('dimensions', {})
            for dim_name, dim_data in dimensions.items():
                conn.execute("""
                    INSERT INTO dimension_scores (
                        session_id, dimension, score, weight, contribution
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    session_id,
                    dim_name,
                    dim_data.get('score', 0.0),
                    dim_data.get('weight', 0.0),
                    dim_data.get('contribution', 0.0)
                ))

            # Record domains
            domains = analysis_result.get('domains', {})
            for domain_name, percentage in domains.items():
                conn.execute("""
                    INSERT INTO domains (
                        session_id, domain, percentage
                    ) VALUES (?, ?, ?)
                """, (
                    session_id,
                    domain_name,
                    percentage
                ))

    def update_session_actual_timeline(
        self,
        session_id: str,
        actual_days: int
    ) -> None:
        """
        Update session with actual completion timeline.

        Args:
            session_id: Session to update
            actual_days: Actual days taken to complete
        """
        with self._get_connection() as conn:
            conn.execute("""
                UPDATE sessions
                SET actual_timeline_days = ?
                WHERE session_id = ?
            """, (actual_days, session_id))

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve session by ID with full details.

        Args:
            session_id: Session to retrieve

        Returns:
            Dict with session data and related dimensions/domains, or None if not found
        """
        with self._get_connection() as conn:
            # Get main session
            session = conn.execute("""
                SELECT * FROM sessions WHERE session_id = ?
            """, (session_id,)).fetchone()

            if not session:
                return None

            result = dict(session)

            # Get dimensions
            dimensions = conn.execute("""
                SELECT dimension, score, weight, contribution
                FROM dimension_scores
                WHERE session_id = ?
            """, (session_id,)).fetchall()

            result['dimensions'] = {
                row['dimension']: {
                    'score': row['score'],
                    'weight': row['weight'],
                    'contribution': row['contribution']
                }
                for row in dimensions
            }

            # Get domains
            domains = conn.execute("""
                SELECT domain, percentage
                FROM domains
                WHERE session_id = ?
            """, (session_id,)).fetchall()

            result['domains'] = {
                row['domain']: row['percentage']
                for row in domains
            }

            return result

    # ===== Wave Execution Operations =====

    def record_wave(
        self,
        session_id: str,
        wave_number: int,
        agent_count: int,
        duration_minutes: float,
        cost_usd: float,
        speedup_factor: Optional[float] = None
    ) -> None:
        """
        Record wave execution metrics.

        Args:
            session_id: Parent session
            wave_number: Wave index (1-based)
            agent_count: Number of agents in wave
            duration_minutes: Actual duration
            cost_usd: Wave cost
            speedup_factor: Speedup vs sequential (optional)
        """
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO wave_executions (
                    session_id, wave_number, agent_count,
                    duration_minutes, cost_usd, speedup_factor
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                session_id, wave_number, agent_count,
                duration_minutes, cost_usd, speedup_factor
            ))

            # Update session wave count
            conn.execute("""
                UPDATE sessions
                SET waves_executed = ?
                WHERE session_id = ?
            """, (wave_number, session_id))

    # ===== MCP Usage Tracking =====

    def record_mcp_usage(
        self,
        session_id: str,
        mcp_name: str,
        installed: bool,
        used: bool
    ) -> None:
        """
        Record MCP recommendation and usage.

        Args:
            session_id: Parent session
            mcp_name: MCP identifier (e.g., 'serena', 'context7')
            installed: Whether MCP was installed
            used: Whether MCP was actually used
        """
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO mcp_usage (
                    session_id, mcp_name, installed, used
                ) VALUES (?, ?, ?, ?)
            """, (session_id, mcp_name, installed, used))

    # ===== Cost Savings Tracking =====

    def record_cost_saving(
        self,
        session_id: str,
        saving_type: str,
        amount_usd: float
    ) -> None:
        """
        Record cost optimization event.

        Args:
            session_id: Parent session
            saving_type: Type of saving (cache_hit, model_optimization, etc.)
            amount_usd: Amount saved
        """
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO cost_savings (
                    session_id, saving_type, amount_usd
                ) VALUES (?, ?, ?)
            """, (session_id, saving_type, amount_usd))

    # ===== Query Builders for Analytics =====

    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get most recent sessions.

        Args:
            limit: Maximum number of sessions to return

        Returns:
            List of session dicts ordered by created_at DESC
        """
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM sessions
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,)).fetchall()

            return [dict(row) for row in rows]

    def get_sessions_by_complexity(
        self,
        min_score: float = 0.0,
        max_score: float = 1.0
    ) -> List[Dict[str, Any]]:
        """
        Get sessions within complexity range.

        Args:
            min_score: Minimum complexity score (inclusive)
            max_score: Maximum complexity score (inclusive)

        Returns:
            List of session dicts
        """
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM sessions
                WHERE complexity_score BETWEEN ? AND ?
                ORDER BY created_at DESC
            """, (min_score, max_score)).fetchall()

            return [dict(row) for row in rows]

    def get_sessions_by_project(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get all sessions for a project.

        Args:
            project_id: Project identifier

        Returns:
            List of session dicts ordered by created_at DESC
        """
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM sessions
                WHERE project_id = ?
                ORDER BY created_at DESC
            """, (project_id,)).fetchall()

            return [dict(row) for row in rows]

    def get_total_sessions(self) -> int:
        """Get total number of sessions recorded."""
        with self._get_connection() as conn:
            result = conn.execute("""
                SELECT COUNT(*) as count FROM sessions
            """).fetchone()

            return result['count'] if result else 0

    def get_total_cost(self) -> float:
        """Get total cost across all sessions."""
        with self._get_connection() as conn:
            result = conn.execute("""
                SELECT SUM(cost_total_usd) as total FROM sessions
            """).fetchone()

            return result['total'] if result and result['total'] else 0.0
