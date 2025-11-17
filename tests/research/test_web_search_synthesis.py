"""
GATE 4.2: Web Search + Synthesis Tests

Tests for ResearchOrchestrator web search and knowledge synthesis:
- gather_from_web() using Tavily
- synthesize_knowledge() method
- Full research() orchestration

Part of: Agent 4 - Research Orchestration
"""

import pytest
import asyncio
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from shannon.research.orchestrator import (
    ResearchOrchestrator,
    ResearchSource,
    ResearchResult
)


@pytest.mark.asyncio
async def test_web_search_tavily():
    """
    Test 1/3: Tavily web search integration

    Verifies:
    - gather_from_web() returns search results
    - Results have web source type
    - Tavily metadata is present
    """
    orchestrator = ResearchOrchestrator()

    query = "React hooks"
    sources = await orchestrator.gather_from_web(query)

    # Should return search results
    assert isinstance(sources, list), "gather_from_web must return list"
    assert len(sources) >= 1, "Should return at least one search result"

    # Check first result
    source = sources[0]
    assert isinstance(source, ResearchSource), "Result must be ResearchSource"
    assert source.source_type == "web", "Should be web type"
    assert "tavily" in source.metadata.get("source", ""), "Should indicate Tavily source"
    assert query in source.metadata.get("search_query", ""), "Should include search query"

    print(f"✓ Tavily web search test passed: {len(sources)} results for '{query}'")


@pytest.mark.asyncio
async def test_knowledge_synthesis():
    """
    Test 2/3: Knowledge synthesis from multiple sources

    Verifies:
    - synthesize_knowledge() produces coherent summary
    - Groups sources by type
    - Calculates relevance scores
    """
    orchestrator = ResearchOrchestrator()

    # Create mock sources
    sources = [
        ResearchSource(
            source_id="web1",
            source_type="web",
            url="https://example.com/article1",
            title="Article 1",
            content="Content 1",
            relevance_score=0.8
        ),
        ResearchSource(
            source_id="doc1",
            source_type="documentation",
            url="https://docs.example.com",
            title="Official Docs",
            content="Documentation content",
            relevance_score=0.9
        ),
        ResearchSource(
            source_id="web2",
            source_type="web",
            url="https://example.com/article2",
            title="Article 2",
            content="Content 2",
            relevance_score=0.7
        )
    ]

    synthesis = await orchestrator.synthesize_knowledge(sources)

    # Should produce non-empty synthesis
    assert isinstance(synthesis, str), "Synthesis must be string"
    assert len(synthesis) > 0, "Synthesis should not be empty"
    assert "Research Summary" in synthesis, "Should include summary header"
    assert "Web Sources" in synthesis or "Documentation Sources" in synthesis, "Should group by type"
    assert "Key Insights" in synthesis, "Should include insights section"

    print(f"✓ Knowledge synthesis test passed: {len(synthesis)} chars synthesized")


@pytest.mark.asyncio
async def test_full_research_orchestration():
    """
    Test 3/3: Full research workflow

    Verifies:
    - research() orchestrates multiple sources
    - Returns ResearchResult with synthesis
    - Calculates confidence score
    """
    orchestrator = ResearchOrchestrator()

    query = "Python async patterns"
    result = await orchestrator.research(query, source_types=["web"])

    # Should return complete research result
    assert isinstance(result, ResearchResult), "Must return ResearchResult"
    assert result.query == query, "Query should match input"
    assert isinstance(result.sources, list), "Sources must be list"
    assert len(result.sources) >= 1, "Should have at least one source"
    assert isinstance(result.synthesis, str), "Synthesis must be string"
    assert len(result.synthesis) > 0, "Synthesis should not be empty"
    assert 0.0 <= result.confidence <= 1.0, "Confidence must be in range [0,1]"

    print(f"✓ Full research orchestration passed: {len(result.sources)} sources, confidence {result.confidence:.2f}")


# Run tests if executed directly
if __name__ == "__main__":
    print("Running GATE 4.2: Web Search + Synthesis Tests")
    print("=" * 60)

    # Run test 1
    try:
        asyncio.run(test_web_search_tavily())
    except Exception as e:
        print(f"✗ Test 1 failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Run test 2
    try:
        asyncio.run(test_knowledge_synthesis())
    except Exception as e:
        print(f"✗ Test 2 failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Run test 3
    try:
        asyncio.run(test_full_research_orchestration())
    except Exception as e:
        print(f"✗ Test 3 failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("=" * 60)
    print("✓ GATE 4.2 PASSED: 3/3 tests passing")
    print("Web search and synthesis working correctly")
