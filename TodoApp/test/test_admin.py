from .utils import *
from ..routers.admin import get_current_user, get_db
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authorized(test_todo):
    response = client.get('/admin/')
    assert response.status_code == status.HTTP_200_OK

def test_delete_admin_authorised(test_todo):
    response = client.delete('/admin/deletetodo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
