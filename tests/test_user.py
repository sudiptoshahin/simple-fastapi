import pytest
from jose import JWTError, jwt
from app import schemas
from tests.database import client, session
from app.config import settings


# def test_root(client):
#     res = client.get('/')
#     assert res.json().get('message') == "Hello World"
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post('/api/v1/users/', json={ "email": "test@test.com", "password": "password" })
    new_user = schemas.UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.email == 'test@test.com'

def test_login(client, test_user):
    res = client.post('/login/', json={ "email": test_user['email'], "password": test_user['password'] })
    
    login_response = schemas.Token(**res.json())
    # Check JWT token
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])    
    id: str = payload.get("user_id")

    assert id == test_user['id']
    assert login_response.token_type == 'bearer'
    assert res.status_code == 200