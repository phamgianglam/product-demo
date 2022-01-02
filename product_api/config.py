from pydantic import BaseSettings
from pydantic.networks import PostgresDsn, AnyHttpUrl

DEFAULT_VERSION = "v1beta1"
DEFAULT_PREFIX = "api"


class AsyncPostgresDsn(PostgresDsn):
    default_scheme = "postgresql+asyncpg"
    allowed_schemes = {"postgresql+asyncpg", "postgres+asyncpg"}


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn
    API_PREFIX: str = DEFAULT_PREFIX
    version: str = DEFAULT_VERSION

    FILTER_RECORD_API: AnyHttpUrl

    @property
    def ASYNC_DATABASE_URL(self) -> AsyncPostgresDsn:
        # ASYNC_DATABASE_URL = self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        ASYNC_DATABASE_URL = self.DATABASE_URL.replace(
            "postgres://", "postgresql+asyncpg://"
        )
        return ASYNC_DATABASE_URL


config = Config()
