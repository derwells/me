import pytest

from ralph.config import Loop, LoopStatus, LoopType
from ralph.preflight import CheckSeverity, run_preflight


@pytest.fixture
def sample_loop():
    from datetime import date

    return Loop(
        description="Test",
        type=LoopType.REVERSE,
        status=LoopStatus.ACTIVE,
        max_iterations=10,
        timeout_seconds=60,
        created=date(2026, 1, 1),
    )


def test_preflight_missing_prompt(tmp_path, sample_loop):
    """Preflight should report error when PROMPT.md is missing."""
    (tmp_path / "frontier").mkdir()
    (tmp_path / "frontier" / "aspects.md").write_text("# Frontier")
    results = run_preflight(
        loop_name="test-loop",
        loop_dir=tmp_path,
        loop_config=sample_loop,
        check_tools=False,
    )
    errors = [r for r in results if r.severity == CheckSeverity.ERROR]
    assert any("PROMPT.md" in r.message for r in errors)


def test_preflight_missing_frontier(tmp_path, sample_loop):
    """Preflight should report error when frontier/aspects.md is missing."""
    (tmp_path / "PROMPT.md").write_text("# Prompt")
    results = run_preflight(
        loop_name="test-loop",
        loop_dir=tmp_path,
        loop_config=sample_loop,
        check_tools=False,
    )
    errors = [r for r in results if r.severity == CheckSeverity.ERROR]
    assert any("frontier/aspects.md" in r.message for r in errors)


def test_preflight_already_converged(tmp_path, sample_loop):
    """Preflight should report error when converged.txt exists."""
    (tmp_path / "PROMPT.md").write_text("# Prompt")
    (tmp_path / "frontier").mkdir()
    (tmp_path / "frontier" / "aspects.md").write_text("# Frontier")
    (tmp_path / "status").mkdir()
    (tmp_path / "status" / "converged.txt").write_text("done")
    results = run_preflight(
        loop_name="test-loop",
        loop_dir=tmp_path,
        loop_config=sample_loop,
        check_tools=False,
    )
    errors = [r for r in results if r.severity == CheckSeverity.ERROR]
    assert any("converged" in r.message.lower() for r in errors)


def test_preflight_paused_loop(tmp_path, sample_loop):
    """Preflight should report error when paused.txt exists."""
    (tmp_path / "PROMPT.md").write_text("# Prompt")
    (tmp_path / "frontier").mkdir()
    (tmp_path / "frontier" / "aspects.md").write_text("# Frontier")
    (tmp_path / "status").mkdir()
    (tmp_path / "status" / "paused.txt").write_text("paused")
    results = run_preflight(
        loop_name="test-loop",
        loop_dir=tmp_path,
        loop_config=sample_loop,
        check_tools=False,
    )
    errors = [r for r in results if r.severity == CheckSeverity.ERROR]
    assert any("paused" in r.message.lower() for r in errors)


def test_preflight_all_good(tmp_path, sample_loop):
    """Preflight should return no errors when everything is valid."""
    (tmp_path / "PROMPT.md").write_text("# Prompt")
    (tmp_path / "frontier").mkdir()
    (tmp_path / "frontier" / "aspects.md").write_text("# Frontier")
    results = run_preflight(
        loop_name="test-loop",
        loop_dir=tmp_path,
        loop_config=sample_loop,
        check_tools=False,
    )
    errors = [r for r in results if r.severity == CheckSeverity.ERROR]
    assert len(errors) == 0
