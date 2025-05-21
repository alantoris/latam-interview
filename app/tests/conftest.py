import pytest
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from fastapi.testclient import TestClient
from tests.factories import UserFactory
from app.db import Base, get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def override_get_db():
    def _get_db_override():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    Base.metadata.create_all(bind=engine)
    yield _get_db_override
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def user(db):
    UserFactory._meta.sqlalchemy_session = db
    return UserFactory()


@pytest.fixture
def multiple_users(db):
    UserFactory._meta.sqlalchemy_session = db
    return UserFactory.create_batch(5)
