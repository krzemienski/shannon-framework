"""
Smart Context Loader - Task-specific relevance-based file loading

Implements smart loading strategy:
1. Parse task for keywords
2. Semantic search in Serena
3. Rank files by relevance
4. Load top-K most relevant files
5. Include related patterns/modules

Goal: Load 10% of codebase that is 90% relevant to task
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
import re
from collections import Counter

from .serena_adapter import SerenaAdapter


@dataclass
class LoadedContext:
    """Context loaded for a specific task"""
    project_summary: str
    relevant_files: Dict[str, str]  # path -> content
    patterns: List[Dict]
    modules: List[Dict]
    total_lines: int
    relevance_scores: List[Tuple[str, float]]


class SmartContextLoader:
    """
    Loads only relevant context for a given task

    Usage:
        loader = SmartContextLoader(serena_adapter)
        context = await loader.load_for_task(
            "Add JWT authentication to REST API",
            "myproject"
        )

    Features:
    - Keyword extraction from task
    - Semantic search in Serena
    - Relevance scoring
    - Top-K file selection
    - Pattern and module inclusion
    """

    # Common stop words to exclude
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
        'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was',
        'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'should', 'could',
        'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
        'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where',
        'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
        'most', 'other', 'some', 'such', 'than', 'too', 'very'
    }

    def __init__(
        self,
        serena_adapter: Optional[SerenaAdapter] = None,
        max_files: int = 10,
        max_total_lines: int = 5000
    ):
        """
        Initialize loader

        Args:
            serena_adapter: SerenaAdapter for knowledge graph access
            max_files: Maximum number of files to load
            max_total_lines: Maximum total lines across all files
        """
        self.serena = serena_adapter or SerenaAdapter()
        self.max_files = max_files
        self.max_total_lines = max_total_lines
        self.logger = logging.getLogger(__name__)

    async def load_for_task(
        self,
        task_description: str,
        project_id: str
    ) -> LoadedContext:
        """
        Load context relevant to task

        Args:
            task_description: Description of task to perform
            project_id: Project identifier

        Returns:
            LoadedContext with relevant files and metadata
        """
        # Step 1: Extract keywords from task
        keywords = self._extract_keywords(task_description)
        self.logger.debug(f"Extracted keywords: {keywords}")

        # Step 2: Search Serena graph
        search_query = f"{project_id} {' '.join(keywords)}"
        relevant_nodes = await self.serena.search_nodes(
            query=search_query,
            max_results=50
        )

        # Step 3: Rank files by relevance
        file_scores = self._rank_files(relevant_nodes, keywords)

        # Step 4: Load top files (respecting limits)
        loaded_files, total_lines = self._load_top_files(
            file_scores,
            project_id
        )

        # Step 5: Extract patterns and modules
        patterns = [
            node for node in relevant_nodes
            if node.get('entityType') == 'Pattern'
        ]

        modules = [
            node for node in relevant_nodes
            if node.get('entityType') == 'Module'
        ]

        # Step 6: Get project summary
        project_summary = await self._get_project_summary(project_id)

        return LoadedContext(
            project_summary=project_summary,
            relevant_files=loaded_files,
            patterns=patterns,
            modules=modules,
            total_lines=total_lines,
            relevance_scores=file_scores[:self.max_files]
        )

    def _extract_keywords(self, task: str) -> List[str]:
        """
        Extract important keywords from task description

        Uses:
        - Lowercase normalization
        - Stop word removal
        - Pattern matching for technical terms
        """
        # Lowercase
        task_lower = task.lower()

        # Extract technical terms (camelCase, snake_case, etc.)
        technical_terms = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', task)  # camelCase
        technical_terms += re.findall(r'\b[a-z]+_[a-z_]+\b', task_lower)  # snake_case
        technical_terms += re.findall(r'\b[A-Z]{2,}\b', task)  # ACRONYMS

        # Extract regular words
        words = re.findall(r'\b\w+\b', task_lower)

        # Filter stop words
        keywords = [
            word for word in words
            if word not in self.STOP_WORDS and len(word) > 2
        ]

        # Add technical terms
        keywords.extend([term.lower() for term in technical_terms])

        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen:
                seen.add(kw)
                unique_keywords.append(kw)

        return unique_keywords[:10]  # Top 10 keywords

    def _rank_files(
        self,
        nodes: List[Dict],
        keywords: List[str]
    ) -> List[Tuple[str, float]]:
        """
        Rank files by relevance to keywords

        Scoring:
        - Keyword matches in file path: +2.0 per match
        - Keyword matches in observations: +1.0 per match
        - File type relevance: +0.5 for code files
        """
        file_scores = []

        for node in nodes:
            if node.get('entityType') != 'File':
                continue

            entity_id = node.get('entityId', '')
            observations = node.get('observations', [])

            # Calculate score
            score = 0.0

            # Path matching
            path_lower = entity_id.lower()
            for keyword in keywords:
                if keyword in path_lower:
                    score += 2.0

            # Observation matching
            observations_text = ' '.join(observations).lower()
            for keyword in keywords:
                if keyword in observations_text:
                    score += 1.0

            # File type bonus
            if any(entity_id.endswith(ext) for ext in ['.py', '.js', '.ts', '.java', '.go']):
                score += 0.5

            if score > 0:
                file_scores.append((entity_id, score))

        # Sort by score (highest first)
        file_scores.sort(key=lambda x: x[1], reverse=True)

        return file_scores

    def _load_top_files(
        self,
        file_scores: List[Tuple[str, float]],
        project_id: str
    ) -> Tuple[Dict[str, str], int]:
        """
        Load top-ranked files respecting limits

        Args:
            file_scores: List of (file_path, score) tuples
            project_id: Project identifier

        Returns:
            (loaded_files_dict, total_lines)
        """
        loaded_files = {}
        total_lines = 0

        # Get project path from local metadata
        project_dir = Path.home() / ".shannon" / "projects" / project_id
        metadata_file = project_dir / "project.json"

        if not metadata_file.exists():
            self.logger.error(f"Project metadata not found: {project_id}")
            return {}, 0

        import json
        metadata = json.loads(metadata_file.read_text())
        project_path = Path(metadata.get('project_path', ''))

        # Load files up to limits
        for file_path, score in file_scores[:self.max_files]:
            # Convert to absolute path
            if not Path(file_path).is_absolute():
                abs_path = project_path / file_path
            else:
                abs_path = Path(file_path)

            if not abs_path.exists():
                self.logger.debug(f"File not found: {abs_path}")
                continue

            try:
                # Read file
                content = abs_path.read_text(encoding='utf-8', errors='ignore')
                lines = len(content.splitlines())

                # Check line limit
                if total_lines + lines > self.max_total_lines:
                    self.logger.debug(f"Line limit reached, skipping {file_path}")
                    break

                # Add to loaded files
                loaded_files[file_path] = content
                total_lines += lines

                self.logger.debug(f"Loaded {file_path} ({lines} lines, score={score:.1f})")

            except Exception as e:
                self.logger.error(f"Failed to load {file_path}: {e}")

        return loaded_files, total_lines

    async def _get_project_summary(self, project_id: str) -> str:
        """Get project summary from Serena"""
        try:
            nodes = await self.serena.open_nodes([f"project_{project_id}"])
            if nodes:
                observations = nodes[0].get('observations', [])
                return '\n'.join(observations)
            return "No project summary available"
        except Exception as e:
            self.logger.error(f"Failed to get project summary: {e}")
            return "Failed to load project summary"


class ContextLoadingStrategy:
    """
    Defines different context loading strategies

    Strategies:
    - MINIMAL: Load only directly relevant files (fast, may miss context)
    - BALANCED: Load relevant files + related patterns (default)
    - COMPREHENSIVE: Load relevant files + patterns + modules (thorough)
    """

    @staticmethod
    def minimal(max_files: int = 5, max_lines: int = 2000):
        """Minimal strategy for quick tasks"""
        return SmartContextLoader(
            max_files=max_files,
            max_total_lines=max_lines
        )

    @staticmethod
    def balanced(max_files: int = 10, max_lines: int = 5000):
        """Balanced strategy (default)"""
        return SmartContextLoader(
            max_files=max_files,
            max_total_lines=max_lines
        )

    @staticmethod
    def comprehensive(max_files: int = 20, max_lines: int = 10000):
        """Comprehensive strategy for complex tasks"""
        return SmartContextLoader(
            max_files=max_files,
            max_total_lines=max_lines
        )
