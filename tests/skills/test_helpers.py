"""
Test helper classes for SkillExecutor tests

Provides mock implementations for testing various execution scenarios.
"""

from pathlib import Path
from typing import Dict, Any


class TestNativeClass:
    """Mock class for native skill testing"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root

    async def execute(self, input: str = None, count: int = 1, **kwargs):
        """Mock async method"""
        return {
            'input': input,
            'count': count,
            'result': f"Processed {input} x {count}" if input else "Processed",
            'project_root': str(self.project_root) if self.project_root else None,
            'kwargs': kwargs
        }

    def sync_execute(self, input: str):
        """Mock sync method"""
        return {'input': input, 'result': f"Sync processed {input}"}


class SlowNativeClass:
    """Mock class for timeout testing"""

    def __init__(self):
        pass

    async def slow_execute(self):
        """Method that takes a long time"""
        import asyncio
        await asyncio.sleep(10)
        return {'result': 'completed'}


class FailingNativeClass:
    """Mock class that always fails"""

    def __init__(self):
        pass

    async def execute(self, **kwargs):
        """Method that always fails"""
        raise Exception("Simulated failure")
