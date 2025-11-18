import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK_PATH = REPO_ROOT / "hooks" / "user_prompt_submit.py"


def run_hook(payload: dict) -> str:
    """Execute the user_prompt_submit hook with the given payload."""
    proc = subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input=json.dumps(payload),
        capture_output=True,
        check=True,
        cwd=REPO_ROOT,
        text=True,
    )
    return proc.stdout


def test_forced_reading_sentinel_triggers_on_large_prompt(tmp_path, monkeypatch):
    prompt = ("line\n" * 450) + "```python\n" + ("print('x')\n" * 210) + "```"
    payload = {"prompt": prompt}

    output = run_hook(payload)

    assert "Forced Reading Sentinel Activated" in output
    assert "skills/forced-reading-sentinel" in output
    assert "core/FORCED_READING_PROTOCOL.md" in output


def test_no_sentinel_for_small_prompt():
    payload = {"prompt": "short prompt"}
    output = run_hook(payload)

    assert "Forced Reading Sentinel Activated" not in output
