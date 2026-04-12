"""Application configuration via environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    redis_url: str = "redis://localhost:6379"
    database_url: str = "postgresql+asyncpg://localhost:5432/recommendations"
    model_path: str = "models/recommender_v1.pt"
    max_recommendations: int = 20
    default_recommendations: int = 10
    trending_window_hours: int = 24
    trending_cache_ttl: int = 300
    ab_test_enabled: bool = True
    feature_store_ttl: int = 3600

    model_config = {"env_prefix": "REC_"}


settings = Settings()
