from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """環境変数管理クラス"""

    PROJECT_ID: str = "sample-project-id"
    DATABASE: str = "coo-chan-daily-log"
    COLLECTION: str = "weight-log"


@lru_cache
def get_settings() -> Settings:
    """Get the settings

    Returns:
        Settings: The settings
    """
    return Settings()


settings = get_settings()
