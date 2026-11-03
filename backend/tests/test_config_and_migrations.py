from pathlib import Path

from alembic.config import Config
from sqlalchemy import create_engine, text

from alembic import command
from app.core.config import PROJECT_ROOT, Settings


def test_sqlite_path_is_stable_across_working_directories():
    settings = Settings(_env_file=None, sqlite_path="backend/data/example.db")
    assert settings.sqlalchemy_url.database == str(PROJECT_ROOT / "backend/data/example.db")


def test_mysql_url_handles_special_characters():
    settings = Settings(_env_file=None, database_backend="mysql", mysql_password="p@ss:/?#%")
    assert settings.sqlalchemy_url.password == "p@ss:/?#%"
    assert settings.sqlalchemy_url.drivername == "mysql+pymysql"
    assert "p@ss" not in repr(settings)


def test_migration_upgrade_downgrade_and_upgrade(tmp_path, monkeypatch):
    path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{path}")
    from app.core.config import get_settings
    from app.db.session import get_engine

    get_settings.cache_clear()
    get_engine.cache_clear()
    config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    try:
        command.upgrade(config, "head")
        engine = create_engine(f"sqlite:///{path}")
        with engine.connect() as connection:
            assert (
                connection.scalar(text("SELECT version_num FROM alembic_version"))
                == "0001_baseline"
            )
        command.check(config)
        command.downgrade(config, "base")
        with engine.connect() as connection:
            assert connection.scalar(text("SELECT COUNT(*) FROM alembic_version")) == 0
        command.upgrade(config, "head")
        engine.dispose()
    finally:
        get_engine().dispose()
        get_engine.cache_clear()
        get_settings.cache_clear()
