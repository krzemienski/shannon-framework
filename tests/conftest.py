"""
Pytest configuration for Shannon Framework tests.

Provides real data fixtures, temporary directories, and test utilities.
"""

import asyncio
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Generator

import pytest


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_workspace() -> Generator[Path, None, None]:
    """
    Create temporary workspace for real file operations.

    Yields:
        Path to temporary directory
    """
    temp_dir = tempfile.mkdtemp(prefix="shannon_test_")
    workspace = Path(temp_dir)

    try:
        yield workspace
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


@pytest.fixture
def real_task_complex() -> Dict[str, Any]:
    """
    Real complex task for Shannon execution.

    Returns:
        Complex task specification
    """
    return {
        'objective': 'Analyze and optimize Python codebase',
        'scope_indicators': {
            'file_count': 25,
            'dir_count': 8,
            'line_count': 6000
        },
        'dependencies': ['typing', 'asyncio', 'dataclasses', 'logging'],
        'operations': [
            {'type': 'analyze', 'target': 'all_files'},
            {'type': 'optimize', 'target': 'performance'},
            {'type': 'validate', 'target': 'types'}
        ],
        'domains': ['performance', 'quality', 'architecture'],
        'parallel_opportunities': 5,
        'sequential_dependencies': 2,
        'clarity_score': 0.8,
        'risk_indicators': {
            'production_impact': False,
            'data_loss_risk': False,
            'security_impact': False,
            'reversibility': True
        },
        'scale_indicators': {
            'user_count': 1000,
            'data_volume_gb': 10,
            'request_rate': 100
        }
    }


@pytest.fixture
def real_task_simple() -> Dict[str, Any]:
    """
    Real simple task for Shannon execution.

    Returns:
        Simple task specification
    """
    return {
        'objective': 'Format Python file',
        'scope_indicators': {
            'file_count': 1,
            'dir_count': 1,
            'line_count': 100
        },
        'dependencies': [],
        'operations': [{'type': 'format', 'target': 'single_file'}],
        'domains': ['quality'],
        'parallel_opportunities': 0,
        'sequential_dependencies': 1,
        'clarity_score': 1.0,
        'risk_indicators': {
            'production_impact': False,
            'data_loss_risk': False,
            'security_impact': False,
            'reversibility': True
        },
        'scale_indicators': {
            'user_count': 0,
            'data_volume_gb': 0,
            'request_rate': 0
        }
    }


@pytest.fixture
def shannon_config() -> Dict[str, Any]:
    """
    Real Shannon orchestrator configuration.

    Returns:
        Orchestrator configuration
    """
    return {
        'complexity_threshold': 0.7,
        'max_concurrent_agents': 10,
        'enable_validation': True,
        'enable_metrics': True
    }


@pytest.fixture
def project_root() -> Path:
    """
    Shannon project root directory.

    Returns:
        Path to project root
    """
    return Path(__file__).parent.parent


@pytest.fixture
def src_directory(project_root: Path) -> Path:
    """
    Shannon source directory.

    Returns:
        Path to src directory
    """
    return project_root / 'src'


@pytest.fixture
def examples_directory(project_root: Path) -> Path:
    """
    Shannon examples directory.

    Returns:
        Path to examples directory
    """
    return project_root / 'examples'