import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from ralph.config import Loop
from ralph.settings import RalphSettings


@dataclass
class IterationResult:
    success: bool
    output: str | None = None
    error: str | None = None


def run_iteration(
    loop_name: str,
    loop_dir: Path,
    settings: RalphSettings,
    loop_config: Loop,
) -> IterationResult:
    """Run one claude iteration. Returns structured result."""
    prompt_file = loop_dir / "PROMPT.md"
    prompt = prompt_file.read_text()

    env = {**os.environ, "ANTHROPIC_API_KEY": settings.anthropic_api_key}
    if settings.gh_token:
        env["GH_TOKEN"] = settings.gh_token

    # Unset CLAUDECODE to allow nested sessions
    env.pop("CLAUDECODE", None)

    cmd = [
        "claude",
        "--print",
        "--model",
        loop_config.model,
        "--dangerously-skip-permissions",
        "--output-format",
        "text",
    ]

    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=loop_config.timeout_seconds,
            cwd=str(loop_dir),
            env=env,
        )
    except subprocess.TimeoutExpired:
        return IterationResult(
            success=False,
            error=f"Timeout after {loop_config.timeout_seconds}s",
        )

    if result.returncode != 0:
        return IterationResult(
            success=False,
            output=result.stdout or None,
            error=result.stderr or f"claude exited with code {result.returncode}",
        )

    return IterationResult(success=True, output=result.stdout)
