from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from model import Todos
from database import SessionLocal
from pydantic import BaseModel, Field

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool
    

@router.get('/')
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@router.get('/todos/{todo_id}', status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(gt = 0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail='Id not found')

@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todorequest: TodoRequest):
    todo_model = Todos(**todorequest.model_dump())
    db.add(todo_model)
    db.commit()

@router.put('/update/{todo_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_todo(db: db_dependency, todorequest: TodoRequest, todo_id: int = Path(gt = 0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Id not found')
    else:
        todo_model.title = todorequest.title
        todo_model.description = todorequest.description
        todo_model.priority = todorequest.priority
        todo_model.completed = todorequest.completed

        db.add(todo_model)
        db.commit()

@router.delete('/delete/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt = 0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id)
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Id not found')
    else:
        db.query(Todos).filter(Todos.id == todo_id).delete()
        db.commit()
