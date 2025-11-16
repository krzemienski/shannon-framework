"""Research orchestration for Shannon Framework.

Provides research capabilities:
- Web search via Tavily
- Documentation scraping via FireCrawl
- Library docs via Context7
- Knowledge synthesis

Part of: Wave 9 - Research
"""

from .orchestrator import (
    ResearchOrchestrator,
    ResearchSource,
    ResearchResult
)

__all__ = [
    'ResearchOrchestrator',
    'ResearchSource',
    'ResearchResult'
]
