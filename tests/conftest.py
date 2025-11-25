import pytest
from app.database import get_db, Base
from .database import TestClient, TestingSessionLocal, engine
from app.main import app
from app.oauth2 import create_access_token



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

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = { "email": "sudipto.shine@gmail.com", "password": "password" }
    res = client.post('/api/v1/users/', json=user_data)
    
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({ "user_id": test_user['id'] })

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client
