"""Test fixture skills for integration testing.

These are mock skill implementations used for testing the orchestration layer.
"""

import asyncio
from typing import Dict, Any
from shannon.skills.models import SkillResult, ExecutionContext


class AnalysisSkill:
    """Mock analysis skill"""

    @staticmethod
    async def execute(parameters: Dict[str, Any], context: ExecutionContext) -> SkillResult:
        """Execute analysis"""
        await asyncio.sleep(0.1)  # Simulate work

        return SkillResult(
            skill_name="analysis",
            success=True,
            data={"analysis_complete": True, "findings": ["pattern_detected"]},
            duration=0.1
        )


class CodeGenSkill:
    """Mock code generation skill"""

    @staticmethod
    async def execute(parameters: Dict[str, Any], context: ExecutionContext) -> SkillResult:
        """Execute code generation"""
        await asyncio.sleep(0.1)  # Simulate work

        return SkillResult(
            skill_name="code_generation",
            success=True,
            data={"files_generated": ["auth.py", "models.py"]},
            duration=0.1
        )


class ValidationSkill:
    """Mock validation skill"""

    @staticmethod
    async def execute(parameters: Dict[str, Any], context: ExecutionContext) -> SkillResult:
        """Execute validation"""
        await asyncio.sleep(0.1)  # Simulate work

        return SkillResult(
            skill_name="validation",
            success=True,
            data={"tests_passed": True, "coverage": 0.95},
            duration=0.1
        )


class GitOpsSkill:
    """Mock git operations skill"""

    @staticmethod
    async def execute(parameters: Dict[str, Any], context: ExecutionContext) -> SkillResult:
        """Execute git operations"""
        await asyncio.sleep(0.1)  # Simulate work

        return SkillResult(
            skill_name="git_operations",
            success=True,
            data={"committed": True, "commit_hash": "abc123"},
            duration=0.1
        )
