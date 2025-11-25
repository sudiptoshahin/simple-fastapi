import pytest
from app.database import get_db, Base
from .database import TestClient, TestingSessionLocal, engine
from app.main import app
from app.oauth2 import create_access_token
from app import models



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
def test_user2(client):
    user_data = { "email": "sudipto.shine2@gmail.com", "password": "password" }
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


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        { "title": "Post title 1", "content": "Post content 1", "owner_id": test_user['id'] },
        { "title": "Post title 2", "content": "Post content 2", "owner_id": test_user['id'] },
        { "title": "Post title 3.1", "content": "Post content 3.1", "owner_id": test_user2['id'] },
        { "title": "Post title 3", "content": "Post content 3", "owner_id": test_user['id'] },
        { "title": "Post title 4", "content": "Post content 4", "owner_id": test_user2['id'] },
        { "title": "Post title 5", "content": "Post content 5", "owner_id": test_user2['id'] },
    ]

    # Convert this list of dict to model
    def create_user_model(post):
        return models.Post(**post)

    posts_map = map(create_user_model, posts_data)
    posts = list(posts_map)
    
    session.add_all(posts)
    # session.add_all([
    #     models.Post(title="Post title 1", content="Post content 1", owner_id=test_user['id']),
    #     models.Post(title="Post title 1", content="Post content 1", owner_id=test_user['id']),
    #     models.Post(title="Post title 1", content="Post content 1", owner_id=test_user['id'])
    # ])
    session.commit()
    all_post = session.query(models.Post).all()
    return all_post

