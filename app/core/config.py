from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    ENV: str = "development"

    DATABASE_URL: str
    SQLALCHEMY_POOL_SIZE: int = 20
    SQLALCHEMY_MAX_OVERFLOW: int = 40

    # Pool recycle — recycle koneksi DB tiap 30 menit
    # Penting untuk DB remote/online agar koneksi stale tidak menyebabkan error
    # Brief RIASEC halaman 65 & 102: nilai 1800 (30 menit)
    DB_POOL_RECYCLE: int = 1800

    # Redis
    REDIS_URL: str

    # Celery
    CELERY_BROKER_URL: str

    # OpenRouter AI
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "google/gemini-3-flash-preview"

    # AI Settings
    AI_MAX_TOKENS: int = 2000
    AI_TEMPERATURE: float = 0.7

    # Security
    SECRET_KEY: str

    # Monitoring
    SENTRY_DSN: str | None = None
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
