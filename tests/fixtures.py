import pytest
from fastapi.testclient import TestClient

from app.auth import create_access_token
from app.main import app
from app.database import get_db, Base
from app.schemas.user import UserCreate
from app.crud import create_user_db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # Важно для in-memory SQLite!
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True, scope="function")
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture
def registered_user(db_session):
    user_data = UserCreate(username="testuser", password="testpass")
    user = create_user_db(db_session, user_data)
    return user

@pytest.fixture
def auth_headers(registered_user):
    token = create_access_token(data={"sub": registered_user.username})
    return {"Authorization": f"Bearer {token}"}
