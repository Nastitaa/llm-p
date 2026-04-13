from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    app_name: str = "llm-p"
    env: str = "local"

    # JWT
    jwt_secret: str
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 60

    # Database
    sqlite_path: str = "./app.db"

    # OpenRouter
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "stepfun/step-3.5-flash:free"
    openrouter_site_url: str = "https://example.com"
    openrouter_app_name: str = "llm-fastapi-openrouter"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()