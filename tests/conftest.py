import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models import Event, Location, Question

# Create a temporary SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture to set up the database
@pytest.fixture(scope="function")
def db():
    """Creates a new database session for each test."""
    Base.metadata.create_all(bind=engine)  # Create tables
    db = TestingSessionLocal()
    try:
        yield db  # Provide the test database session
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Clean up tables after test

# Override FastAPI dependency for tests
@pytest.fixture(scope="function")
def client():
    from fastapi.testclient import TestClient
    from app.main import app

    app.dependency_overrides[get_db] = lambda: db()
    return TestClient(app)
