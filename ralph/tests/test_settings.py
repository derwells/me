import pytest
from pydantic import ValidationError

from ralph.settings import RalphSettings


def test_settings_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-123")
    monkeypatch.setenv("GH_TOKEN", "ghp_test")
    settings = RalphSettings()
    assert settings.anthropic_api_key == "sk-test-123"
    assert settings.gh_token == "ghp_test"


def test_settings_missing_api_key_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ValidationError):
        RalphSettings()


def test_settings_gh_token_optional(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-123")
    monkeypatch.delenv("GH_TOKEN", raising=False)
    settings = RalphSettings()
    assert settings.gh_token is None
