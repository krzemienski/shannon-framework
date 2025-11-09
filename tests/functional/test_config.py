"""
Functional tests for configuration system
NO MOCKS - Real file I/O
"""

import pytest
from pathlib import Path
import json
import shutil


@pytest.mark.functional
def test_config_loads_defaults():
    """Config should load with sensible defaults"""
    from shannon.config import ShannonConfig

    config = ShannonConfig()

    assert config.default_model == "claude-sonnet-4-5"
    assert config.max_parallel_agents <= 10
    assert config.enforce_no_mocks == True
    assert config.minimum_complexity_for_waves == 0.50


@pytest.mark.functional
def test_config_save_and_load():
    """Config should save to file and reload correctly"""
    from shannon.config import ShannonConfig

    # Create config with custom values
    config1 = ShannonConfig(
        default_model="claude-opus-4",
        max_parallel_agents=5,
        enforce_no_mocks=False,
    )

    # Save
    config1.save()

    # Verify file exists
    config_file = Path.home() / ".shannon" / "config.json"
    assert config_file.exists()

    # Load in new instance
    config2 = ShannonConfig.load()

    # Verify values match
    assert config2.default_model == "claude-opus-4"
    assert config2.max_parallel_agents == 5
    assert config2.enforce_no_mocks == False

    # Cleanup
    if config_file.exists():
        config_file.unlink()


@pytest.mark.functional
def test_config_validation():
    """Config should validate constraints"""
    from shannon.config import ShannonConfig

    # max_parallel_agents must be >= 1
    with pytest.raises(ValueError):
        ShannonConfig(max_parallel_agents=0)

    # max_parallel_agents must be <= 25
    with pytest.raises(ValueError):
        ShannonConfig(max_parallel_agents=30)


@pytest.mark.functional
def test_config_path_serialization():
    """Config should serialize Path objects correctly"""
    from shannon.config import ShannonConfig

    config = ShannonConfig()
    config.save()

    # Verify file contains string paths, not Path objects
    config_file = Path.home() / ".shannon" / "config.json"
    with open(config_file) as f:
        data = json.load(f)

    # session_dir should be serialized as string
    assert isinstance(data["session_dir"], str)
    assert ".shannon/sessions" in data["session_dir"]

    # Cleanup
    if config_file.exists():
        config_file.unlink()
