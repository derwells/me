from pydantic_settings import BaseSettings, SettingsConfigDict


class RalphSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="")

    anthropic_api_key: str
    gh_token: str | None = None
