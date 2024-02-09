from .utils import *
from ..routers.users import get_current_user, get_db
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_users(test_user):
    response = client.get('/user/')
    assert response.status_code == status.HTTP_200_OK

def test_change_password(test_user):
    response = client.put('/user/newpassword', json={'old_password': 'paushigaa', 'new_password': 'paushi'})
    response.status_code == status.HTTP_202_ACCEPTED