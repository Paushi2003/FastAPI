from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from model import Todos
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user and user.get('role') == 'admin':
        return db.query(Todos).all()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Only admin can access')
    
@router.delete('/deletetodo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt = 0)):
    if user is None or user.get('role')!='admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Only admin can access')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Id not found')
    else:
        db.query(Todos).filter(Todos.id == todo_id).delete()
        db.commit()

    