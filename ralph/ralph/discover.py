import json
from pathlib import Path

from ralph.config import Loop, LoopStatus, LoopType


def discover_active_loops(
    loops: dict[str, Loop],
    loops_dir: Path,
    loop_type: LoopType | None = None,
) -> list[str]:
    """Return names of active loops, optionally filtered by type.

    Checks both registry status and filesystem — a loop with
    status/converged.txt on disk is excluded even if the registry
    still says ACTIVE.
    """
    return [
        name
        for name, loop in loops.items()
        if loop.status == LoopStatus.ACTIVE
        and (loop_type is None or loop.type == loop_type)
        and not (loops_dir / name / "status" / "converged.txt").exists()
    ]


def format_github_matrix(loop_names: list[str]) -> str:
    """Format loop names as a GitHub Actions matrix JSON."""
    return json.dumps({"loop": loop_names})
