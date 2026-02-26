import shutil
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from ralph.config import Loop


class CheckSeverity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    OK = "ok"


@dataclass
class CheckResult:
    name: str
    severity: CheckSeverity
    message: str


def run_preflight(
    loop_name: str,
    loop_dir: Path,
    loop_config: Loop,
    check_tools: bool = True,
) -> list[CheckResult]:
    """Run all preflight checks. Returns all results (no short-circuit)."""
    results: list[CheckResult] = []

    # File structure checks
    prompt_path = loop_dir / "PROMPT.md"
    if prompt_path.exists():
        results.append(CheckResult("prompt_file", CheckSeverity.OK, "PROMPT.md found"))
    else:
        results.append(
            CheckResult(
                "prompt_file",
                CheckSeverity.ERROR,
                f"PROMPT.md not found at {prompt_path}",
            )
        )

    frontier_path = loop_dir / "frontier" / "aspects.md"
    if frontier_path.exists():
        results.append(CheckResult("frontier_file", CheckSeverity.OK, "frontier/aspects.md found"))
    else:
        results.append(
            CheckResult(
                "frontier_file",
                CheckSeverity.ERROR,
                f"frontier/aspects.md not found at {frontier_path}",
            )
        )

    # Status checks
    converged_path = loop_dir / "status" / "converged.txt"
    if converged_path.exists():
        results.append(
            CheckResult(
                "not_converged",
                CheckSeverity.ERROR,
                "Loop already converged (status/converged.txt exists)",
            )
        )
    else:
        results.append(CheckResult("not_converged", CheckSeverity.OK, "Not yet converged"))

    paused_path = loop_dir / "status" / "paused.txt"
    if paused_path.exists():
        results.append(
            CheckResult(
                "not_paused",
                CheckSeverity.ERROR,
                "Loop is paused (status/paused.txt exists)",
            )
        )
    else:
        results.append(CheckResult("not_paused", CheckSeverity.OK, "Not paused"))

    # Tool checks (skippable for testing)
    if check_tools:
        if shutil.which("claude"):
            results.append(CheckResult("claude_cli", CheckSeverity.OK, "claude CLI found"))
        else:
            results.append(
                CheckResult(
                    "claude_cli",
                    CheckSeverity.ERROR,
                    "claude CLI not found on PATH",
                )
            )

        if shutil.which("gh"):
            results.append(CheckResult("gh_cli", CheckSeverity.OK, "gh CLI found"))
        else:
            results.append(
                CheckResult(
                    "gh_cli",
                    CheckSeverity.WARNING,
                    "gh CLI not found on PATH — GitHub operations will fail",
                )
            )

    return results


def has_errors(results: list[CheckResult]) -> bool:
    """Check if any preflight result is an error."""
    return any(r.severity == CheckSeverity.ERROR for r in results)
