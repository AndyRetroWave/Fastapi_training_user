from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    MODE: Literal["DEV", "TEST", "PROD"] = "DEV"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_HOSR: str

    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_DB: str
    TEST_POSTGRES_PORT: int
    TEST_POSTGRES_HOSR: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://\
{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOSR}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def TEST_DB_URL(self):
        return f"postgresql+asyncpg://\
{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}@{self.TEST_POSTGRES_HOSR}:{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DB}"


settings = Settings()
