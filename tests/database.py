
import pytest
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from psycopg2 import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
from alembic import command
from fastapi.testclient import TestClient
from app.main import app
from app import schemas



#===========SETUP TESTDB=================
SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:postgres@127.0.0.1:5432/test-simple-fastapi'

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
except OperationalError as err:
    print(f"_____________Database connection failed!______________", err)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# database orm dependency
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
# end database orm dependecy
#========================================

# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)

# @pytest.fixture(scope='session')
@pytest.fixture
def session():
    print('my session fixture ran')
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1
# @pytest.fixture
# def client(session):
#     # Base.metadata.drop_all(bind=engine)
#     # Base.metadata.create_all(bind=engine)
#     # command.upgrade("head")
#     # Run code before we run tests
#     yield TestClient(app)
#     # command.downgrade('base')
#     # Run code after our test finishes


# @pytest.fixture(scope='module')
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
