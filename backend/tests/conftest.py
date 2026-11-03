import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.session import get_db
from app.main import create_app


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )

    def test_db():
        with Session(engine) as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_db] = test_db
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
    engine.dispose()
