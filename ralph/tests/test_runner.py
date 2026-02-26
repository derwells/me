from datetime import date
from unittest.mock import patch

import pytest

from ralph.config import Loop, LoopStatus, LoopType
from ralph.runner import IterationResult, run_iteration
from ralph.settings import RalphSettings


@pytest.fixture
def sample_loop():
    return Loop(
        description="Test",
        type=LoopType.REVERSE,
        status=LoopStatus.ACTIVE,
        max_iterations=10,
        timeout_seconds=60,
        created=date(2026, 1, 1),
    )


@pytest.fixture
def loop_dir(tmp_path):
    (tmp_path / "PROMPT.md").write_text("Analyze the thing.")
    (tmp_path / "frontier").mkdir()
    (tmp_path / "frontier" / "aspects.md").write_text("# Frontier")
    return tmp_path


@pytest.fixture
def settings(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-123")
    return RalphSettings()


def test_iteration_result_structure():
    """IterationResult should have success, output, error fields."""
    result = IterationResult(success=True, output="done", error=None)
    assert result.success is True
    assert result.output == "done"
    assert result.error is None


def test_run_iteration_success(loop_dir, sample_loop, settings):
    """Successful claude invocation returns success result."""
    with patch("ralph.runner.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Analysis complete."
        mock_run.return_value.stderr = ""
        result = run_iteration("test-loop", loop_dir, settings, sample_loop)
    assert result.success is True
    assert result.output == "Analysis complete."


def test_run_iteration_failure(loop_dir, sample_loop, settings):
    """Failed claude invocation returns failure result."""
    with patch("ralph.runner.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = "API error"
        result = run_iteration("test-loop", loop_dir, settings, sample_loop)
    assert result.success is False
    assert "API error" in result.error


def test_run_iteration_timeout(loop_dir, sample_loop, settings):
    """Timeout should return failure with timeout message."""
    import subprocess as sp

    with patch("ralph.runner.subprocess.run") as mock_run:
        mock_run.side_effect = sp.TimeoutExpired(cmd="claude", timeout=60)
        result = run_iteration("test-loop", loop_dir, settings, sample_loop)
    assert result.success is False
    assert "timeout" in result.error.lower()
