from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, make_url

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_name: str = "Industrial Fault Prediction API"
    app_env: Literal["development", "test", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    database_backend: Literal["sqlite", "mysql"] = "sqlite"
    sqlite_path: str = "backend/data/development.db"
    database_url: SecretStr = SecretStr("")
    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3307
    mysql_database: str = "industrial_fault_prediction"
    mysql_user: str = "ifp_dev"
    mysql_password: SecretStr = SecretStr("")

    @property
    def sqlalchemy_url(self) -> URL:
        override = self.database_url.get_secret_value()
        if override:
            url = make_url(override)
        elif self.database_backend == "mysql":
            if not self.mysql_password.get_secret_value():
                raise ValueError("MySQL requires MYSQL_PASSWORD in the root .env")
            url = URL.create(
                "mysql+pymysql",
                username=self.mysql_user,
                password=self.mysql_password.get_secret_value(),
                host=self.mysql_host,
                port=self.mysql_port,
                database=self.mysql_database,
                query={"charset": "utf8mb4"},
            )
        else:
            url = URL.create("sqlite", database=self.sqlite_path)
        if url.drivername not in {"sqlite", "mysql+pymysql"}:
            raise ValueError("Only sqlite and mysql+pymysql are supported")
        if url.drivername == "sqlite" and url.database not in {None, "", ":memory:"}:
            db_path = Path(url.database).expanduser()
            if not db_path.is_absolute():
                db_path = PROJECT_ROOT / db_path
            url = url.set(database=str(db_path.resolve()))
        return url


@lru_cache
def get_settings() -> Settings:
    return Settings()
