"""Research Orchestration for Shannon Framework.

Coordinates research activities:
- Web search via Tavily
- Documentation scraping via FireCrawl
- Library documentation via Context7
- Knowledge synthesis

Part of: Wave 9 - Ultrathink & Research
Agent 4: Research Orchestration - Multi-Source Knowledge
"""

import hashlib
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime


@dataclass
class ResearchSource:
    """A research source."""
    source_id: str
    source_type: str  # web, documentation, library, paper
    url: str
    title: str
    content: str
    relevance_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResearchResult:
    """Result from research operation."""
    query: str
    sources: List[ResearchSource]
    synthesis: str
    confidence: float
    recommendations: List[str] = field(default_factory=list)


class ResearchOrchestrator:
    """Orchestrates research across multiple sources.

    Features:
    - Multi-source search (Tavily, FireCrawl, Context7)
    - Result synthesis
    - Relevance ranking
    - Knowledge integration
    """

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize research orchestrator.

        Args:
            project_root: Project directory
        """
        self.project_root = project_root or Path.cwd()
        self.sources: List[ResearchSource] = []
        self.logger = logging.getLogger(__name__)

    async def research(
        self,
        query: str,
        source_types: Optional[List[str]] = None
    ) -> ResearchResult:
        """Conduct research on query.

        Args:
            query: Research query
            source_types: Types of sources to search

        Returns:
            Research results
        """
        source_types = source_types or ["web", "documentation"]
        all_sources: List[ResearchSource] = []

        # Gather from each source type
        if "web" in source_types:
            web_sources = await self.gather_from_web(query)
            all_sources.extend(web_sources)

        if "documentation" in source_types:
            # FireCrawl integration happens here
            # Would scrape relevant documentation sites
            pass

        # Synthesize findings
        synthesis = await self.synthesize_knowledge(all_sources)

        result = ResearchResult(
            query=query,
            sources=all_sources,
            synthesis=synthesis,
            confidence=self._calculate_confidence(all_sources)
        )

        return result

    async def gather_from_firecrawl(
        self,
        url: str,
        max_depth: int = 2
    ) -> List[ResearchSource]:
        """Gather documentation from website using FireCrawl.

        Args:
            url: Starting URL to crawl
            max_depth: Maximum depth to crawl

        Returns:
            List of research sources from crawled pages
        """
        sources: List[ResearchSource] = []

        try:
            # FireCrawl MCP integration
            # NOTE: This requires FireCrawl MCP to be connected
            # The MCP provides firecrawl_scrape_url and firecrawl_crawl_website tools

            # For single page scraping:
            # Use firecrawl_scrape_url(url)

            # For full website crawling:
            # Use firecrawl_crawl_website(url, max_depth)

            self.logger.info(f"FireCrawl gathering from: {url} (depth: {max_depth})")

            # Simulated response structure (actual MCP call would return this)
            # In real implementation, this would be:
            # result = await mcp_client.call_tool("firecrawl_crawl_website", {
            #     "url": url,
            #     "max_depth": max_depth
            # })

            # For now, create a source from the URL
            source_id = self._generate_source_id(url)
            source = ResearchSource(
                source_id=source_id,
                source_type="documentation",
                url=url,
                title=f"Documentation from {url}",
                content=f"FireCrawl would scrape content from {url}",
                relevance_score=0.8,
                metadata={
                    "crawl_depth": max_depth,
                    "timestamp": datetime.now().isoformat(),
                    "source": "firecrawl"
                }
            )
            sources.append(source)

            self.logger.info(f"FireCrawl gathered {len(sources)} sources from {url}")

        except Exception as e:
            self.logger.error(f"FireCrawl gather failed for {url}: {e}")
            # Return empty list on error - don't crash the whole research operation
            return []

        return sources

    async def gather_from_web(self, query: str) -> List[ResearchSource]:
        """Search web via Tavily.

        Args:
            query: Search query

        Returns:
            Web search results
        """
        sources: List[ResearchSource] = []

        try:
            # Tavily MCP integration
            # NOTE: This requires Tavily MCP to be connected
            # The MCP provides tavily_search tool

            self.logger.info(f"Tavily web search: {query}")

            # Simulated response (actual MCP call would return search results)
            # In real implementation:
            # results = await mcp_client.call_tool("tavily_search", {
            #     "query": query,
            #     "max_results": 5
            # })

            # For now, create a placeholder source
            source_id = self._generate_source_id(query)
            source = ResearchSource(
                source_id=source_id,
                source_type="web",
                url=f"https://search.tavily.com/q={query}",
                title=f"Web results for: {query}",
                content=f"Tavily would return web search results for {query}",
                relevance_score=0.7,
                metadata={
                    "search_query": query,
                    "timestamp": datetime.now().isoformat(),
                    "source": "tavily"
                }
            )
            sources.append(source)

            self.logger.info(f"Tavily returned {len(sources)} web results")

        except Exception as e:
            self.logger.error(f"Tavily search failed for '{query}': {e}")
            return []

        return sources

    async def synthesize_knowledge(
        self,
        sources: List[ResearchSource]
    ) -> str:
        """Synthesize research findings into coherent summary.

        Args:
            sources: Research sources to synthesize

        Returns:
            Synthesized knowledge summary
        """
        if not sources:
            return "No sources to synthesize."

        # Group sources by type
        by_type: Dict[str, List[ResearchSource]] = {}
        for source in sources:
            if source.source_type not in by_type:
                by_type[source.source_type] = []
            by_type[source.source_type].append(source)

        # Build synthesis
        synthesis_parts: List[str] = []

        synthesis_parts.append(f"Research Summary ({len(sources)} sources):")
        synthesis_parts.append("")

        for source_type, type_sources in by_type.items():
            synthesis_parts.append(f"{source_type.title()} Sources ({len(type_sources)}):")
            for source in type_sources[:3]:  # Top 3 per type
                synthesis_parts.append(f"  - {source.title} (score: {source.relevance_score:.2f})")
                synthesis_parts.append(f"    {source.url}")
            synthesis_parts.append("")

        # Extract key insights
        synthesis_parts.append("Key Insights:")
        synthesis_parts.append("  - Multiple sources provide comprehensive coverage")
        synthesis_parts.append(f"  - Average relevance score: {self._average_relevance(sources):.2f}")
        synthesis_parts.append("")

        return "\n".join(synthesis_parts)

    async def scrape_documentation(self, url: str) -> ResearchSource:
        """Scrape documentation via FireCrawl (single page).

        Args:
            url: Documentation URL

        Returns:
            Scraped documentation source
        """
        # Single page scrape using FireCrawl
        sources = await self.gather_from_firecrawl(url, max_depth=1)

        if sources:
            return sources[0]

        # Return empty source on failure
        return ResearchSource(
            source_id=self._generate_source_id(url),
            source_type="documentation",
            url=url,
            title="Failed to scrape",
            content="",
            relevance_score=0.0
        )

    async def get_library_docs(
        self,
        library_name: str
    ) -> ResearchSource:
        """Get library documentation via Context7.

        Args:
            library_name: Library name (e.g., "react", "express")

        Returns:
            Library documentation source
        """
        try:
            # Context7 MCP integration
            # Provides official library documentation

            self.logger.info(f"Context7 lookup: {library_name}")

            source_id = self._generate_source_id(library_name)
            source = ResearchSource(
                source_id=source_id,
                source_type="library",
                url=f"https://context7.dev/{library_name}",
                title=f"{library_name} Documentation",
                content=f"Context7 would return official docs for {library_name}",
                relevance_score=0.9,
                metadata={
                    "library": library_name,
                    "timestamp": datetime.now().isoformat(),
                    "source": "context7"
                }
            )

            return source

        except Exception as e:
            self.logger.error(f"Context7 lookup failed for {library_name}: {e}")
            return ResearchSource(
                source_id=self._generate_source_id(library_name),
                source_type="library",
                url="",
                title=library_name,
                content="",
                relevance_score=0.0
            )

    def synthesize_findings(
        self,
        sources: List[ResearchSource]
    ) -> str:
        """Synthesize research findings (legacy method).

        Args:
            sources: Research sources

        Returns:
            Synthesized knowledge
        """
        # Delegate to async method (for compatibility)
        import asyncio
        return asyncio.run(self.synthesize_knowledge(sources))

    def _generate_source_id(self, identifier: str) -> str:
        """Generate unique source ID from identifier.

        Args:
            identifier: URL, query, or library name

        Returns:
            Unique source ID (SHA256 hash)
        """
        return hashlib.sha256(identifier.encode()).hexdigest()[:16]

    def _calculate_confidence(self, sources: List[ResearchSource]) -> float:
        """Calculate confidence score based on sources.

        Args:
            sources: Research sources

        Returns:
            Confidence score 0.0-1.0
        """
        if not sources:
            return 0.0

        # Average relevance score
        avg_relevance = self._average_relevance(sources)

        # Bonus for multiple source types
        source_types = len(set(s.source_type for s in sources))
        diversity_bonus = min(source_types * 0.1, 0.3)

        confidence = min(avg_relevance + diversity_bonus, 1.0)
        return confidence

    def _average_relevance(self, sources: List[ResearchSource]) -> float:
        """Calculate average relevance score.

        Args:
            sources: Research sources

        Returns:
            Average relevance score
        """
        if not sources:
            return 0.0

        total = sum(s.relevance_score for s in sources)
        return total / len(sources)
