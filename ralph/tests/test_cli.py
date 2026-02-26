from typer.testing import CliRunner

from ralph.cli import app

runner = CliRunner()


def test_status_command():
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0


def test_discover_command(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    result = runner.invoke(app, ["discover"])
    assert result.exit_code == 0
    assert "loop" in result.stdout


def test_discover_github_matrix(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    result = runner.invoke(app, ["discover", "--output", "github-matrix"])
    assert result.exit_code == 0
    assert '"loop"' in result.stdout


def test_preflight_unknown_loop(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    result = runner.invoke(app, ["preflight", "nonexistent-loop"])
    assert result.exit_code == 1


def test_run_unknown_loop(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    result = runner.invoke(app, ["run", "nonexistent-loop"])
    assert result.exit_code == 1
