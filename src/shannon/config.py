"""Shannon CLI configuration"""

from pydantic import BaseModel, Field
from pathlib import Path
import os
import json


class ShannonConfig(BaseModel):
    """Global Shannon CLI configuration"""

    # API Configuration
    anthropic_api_key: str = Field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", "")
    )
    default_model: str = Field(default="claude-sonnet-4-5")

    # Storage
    session_dir: Path = Field(
        default_factory=lambda: Path.home() / ".shannon" / "sessions"
    )

    # Execution
    default_permission_mode: str = Field(default="acceptEdits")
    max_parallel_agents: int = Field(default=10, ge=1, le=25)

    # Shannon Patterns
    enforce_forced_reading: bool = Field(default=True)
    enforce_no_mocks: bool = Field(default=True)
    minimum_complexity_for_waves: float = Field(default=0.50)

    # Testing
    enable_api_tests: bool = Field(default=False)
    test_budget_usd: float = Field(default=10.0)

    class Config:
        # Allow arbitrary types (Path)
        arbitrary_types_allowed = True

    @classmethod
    def load(cls) -> "ShannonConfig":
        """Load from ~/.shannon/config.json or create default"""
        config_file = Path.home() / ".shannon" / "config.json"

        if config_file.exists():
            with open(config_file) as f:
                data = json.load(f)
            # Convert string paths back to Path objects
            if "session_dir" in data and isinstance(data["session_dir"], str):
                data["session_dir"] = Path(data["session_dir"])
            return cls(**data)
        else:
            config = cls()
            config.save()
            return config

    def save(self):
        """Save to ~/.shannon/config.json"""
        config_file = Path.home() / ".shannon" / "config.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)

        # Convert to dict and serialize Path objects as strings
        data = self.model_dump()
        if "session_dir" in data and isinstance(data["session_dir"], Path):
            data["session_dir"] = str(data["session_dir"])

        with open(config_file, "w") as f:
            json.dump(data, f, indent=2)
