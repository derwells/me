import json
from datetime import date

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


def test_discover_returns_only_active():
    active = discover_active_loops(make_loops())
    assert "active-loop" in active
    assert "paused-loop" not in active
    assert "converged-loop" not in active


def test_github_matrix_format():
    active = discover_active_loops(make_loops())
    matrix_json = format_github_matrix(active)
    parsed = json.loads(matrix_json)
    assert "loop" in parsed
    assert "active-loop" in parsed["loop"]


def test_github_matrix_empty():
    matrix_json = format_github_matrix([])
    parsed = json.loads(matrix_json)
    assert parsed["loop"] == []
