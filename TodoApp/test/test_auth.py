from .utils import *
from ..routers.auth import authenticate_user, get_db, create_token, SECRET_KEY, ALGORITHM, get_current_user
from fastapi import status
from jose import jwt 
from datetime import timedelta
import pytest

app.dependency_overrides[get_db] = override_get_db

def test_read_all_users(test_user):
    response = client.get('/auth/users')
    assert response.status_code == status.HTTP_200_OK

def test_create_user(test_user):
    request = {
            "username": "paushi",
            "email": "paushi@gmail.in",
            "firstname": "paushi",
            "lastname": "s",
            "password": "paushigaa",
            "role": "student"
            }
    response = client.post('/auth/createuser', json=request)  
    assert response.status_code == status.HTTP_201_CREATED

def test_user_authenticated(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, 'paushigaa', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)
    token = create_token(username, user_id, expires_delta, role)
    decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signature': False})
    assert decode_token['sub'] == username
    assert decode_token['id'] == user_id
    assert decode_token['role'] == role

@pytest.mark.asyncio
async def test_valid_token():
    encode = {'sub': 'testuser',
              'id': 1,
              'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token)
    assert user == {'username': 'testuser', 'id': 1, 'role': 'admin'}
