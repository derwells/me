import sys
from pathlib import Path

# Add loops/ to sys.path so we can import registry
# parents[2] is the repo root (ralph/ -> ralph-typed-runner/)
LOOPS_DIR = Path(__file__).resolve().parents[2] / "loops"
sys.path.insert(0, str(LOOPS_DIR))

from registry import LOOPS  # noqa: E402

from ralph.config import Loop, LoopStatus  # noqa: E402


def test_registry_is_dict():
    assert isinstance(LOOPS, dict)
    assert len(LOOPS) > 0


def test_all_entries_are_loop_instances():
    for name, loop in LOOPS.items():
        assert isinstance(name, str), f"Key {name!r} is not a string"
        assert isinstance(loop, Loop), f"{name} is not a Loop instance"


def test_all_names_match_directory():
    """Every registry key must have a corresponding loops/{key}/ directory."""
    for name in LOOPS:
        loop_dir = LOOPS_DIR / name
        assert loop_dir.is_dir(), f"Registry key '{name}' has no directory at {loop_dir}"


def test_all_loop_dirs_in_registry():
    """Every loop directory (except _templates) must be in the registry."""
    for d in LOOPS_DIR.iterdir():
        if d.is_dir() and not d.name.startswith("_"):
            assert d.name in LOOPS, f"Directory '{d.name}' exists but is not in registry"


def test_active_loops_have_no_converged_at():
    for name, loop in LOOPS.items():
        if loop.status == LoopStatus.ACTIVE:
            assert loop.converged_at is None, f"Active loop {name} has converged_at set"


def test_converged_loops_have_converged_at():
    for name, loop in LOOPS.items():
        if loop.status == LoopStatus.CONVERGED:
            assert loop.converged_at is not None, f"Converged loop {name} missing converged_at"
