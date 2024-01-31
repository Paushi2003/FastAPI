from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from model import Todos
from database import SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool
    

@router.get('/')
async def read_todos(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized user')
    return db.query(Todos).filter(Todos.owner == user.get('id')).all()

@router.get('/todos/{todo_id}', status_code=status.HTTP_200_OK)
async def get_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt = 0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized user')
    todo_model = db.query(Todos).filter(Todos.owner == user.get('id')).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail='Id not found')

@router.post('/createtodo', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todorequest: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized user')
    todo_model = Todos(**todorequest.model_dump(), owner = user.get('id'))
    db.add(todo_model)
    db.commit()

@router.put('/updatetodo/{todo_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_todo(user: user_dependency, db: db_dependency, todorequest: TodoRequest, todo_id: int = Path(gt = 0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized user')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Id not found')
    else:
        todo_model.title = todorequest.title
        todo_model.description = todorequest.description
        todo_model.priority = todorequest.priority
        todo_model.completed = todorequest.completed
        db.add(todo_model)
        db.commit()

@router.delete('/deletetodo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt = 0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized user')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Id not found')
    else:
        db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner == user.get('id')).delete()
        db.commit()
