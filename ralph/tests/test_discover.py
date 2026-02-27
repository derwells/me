import json
from datetime import date
from pathlib import Path

from ralph.config import Loop, LoopStatus, LoopType
from ralph.discover import discover_active_loops, format_github_matrix


def make_loops():
    return {
        "active-loop": Loop(
            description="Active",
            type=LoopType.REVERSE,
            status=LoopStatus.ACTIVE,
            max_iterations=10,
            timeout_seconds=60,
            created=date(2026, 1, 1),
        ),
        "paused-loop": Loop(
            description="Paused",
            type=LoopType.REVERSE,
            status=LoopStatus.PAUSED,
            max_iterations=10,
            timeout_seconds=60,
            created=date(2026, 1, 1),
        ),
        "converged-loop": Loop(
            description="Done",
            type=LoopType.REVERSE,
            status=LoopStatus.CONVERGED,
            max_iterations=10,
            timeout_seconds=60,
            created=date(2026, 1, 1),
            converged_at=date(2026, 1, 2),
        ),
    }


def test_discover_returns_only_active(tmp_path: Path):
    # Create loop dirs (no converged.txt)
    (tmp_path / "active-loop" / "status").mkdir(parents=True)
    (tmp_path / "paused-loop" / "status").mkdir(parents=True)
    (tmp_path / "converged-loop" / "status").mkdir(parents=True)

    active = discover_active_loops(make_loops(), tmp_path)
    assert "active-loop" in active
    assert "paused-loop" not in active
    assert "converged-loop" not in active


def test_discover_excludes_filesystem_converged(tmp_path: Path):
    """A loop marked ACTIVE in registry but with converged.txt on disk is excluded."""
    (tmp_path / "active-loop" / "status").mkdir(parents=True)
    (tmp_path / "active-loop" / "status" / "converged.txt").write_text("CONVERGED")

    active = discover_active_loops(make_loops(), tmp_path)
    assert "active-loop" not in active


def test_github_matrix_format(tmp_path: Path):
    (tmp_path / "active-loop" / "status").mkdir(parents=True)
    active = discover_active_loops(make_loops(), tmp_path)
    matrix_json = format_github_matrix(active)
    parsed = json.loads(matrix_json)
    assert "loop" in parsed
    assert "active-loop" in parsed["loop"]


def test_github_matrix_empty():
    matrix_json = format_github_matrix([])
    parsed = json.loads(matrix_json)
    assert parsed["loop"] == []
