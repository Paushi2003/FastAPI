from ..routers.todos import get_db
from ..main import app
from ..routers.auth import get_current_user
from fastapi import status
from .utils import override_get_current_user, override_get_db, client, test_todo

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get('/todos/')
    assert response.status_code == status.HTTP_200_OK

def test_one_todo_authenticated(test_todo):
    response = client.get('/todos/todos/1')
    assert response.status_code == status.HTTP_200_OK

def test_create_todo(test_todo):
    request = {
        'title': 'todo2',
        'description': 'this is test todo 2',
        'priority': 3,
        'completed': False,
        'owner': 1
    }
    response = client.post('/todos/createtodo', json=request)
    assert response.status_code == status.HTTP_201_CREATED

def test_update_todo(test_todo):
    request = {
        'title': 'test todo2',
        'description': 'this is test todo 2 which is updated',
        'priority': 4,
        'completed': True,
        'owner': 1
    }
    response = client.put('/todos/updatetodo/1', json=request)
    assert response.status_code == status.HTTP_202_ACCEPTED

def test_delete_one_todo(test_todo):
    response = client.delete('/todos/deletetodo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT

