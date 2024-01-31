from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from model import Users
from database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['User']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserVerification(BaseModel):
    old_password: str
    new_password: str = Field(min_length=6)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/newpassword', status_code=status.HTTP_202_ACCEPTED)
async def change_password(user: user_dependency, db: db_dependency, password: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='not authenticated')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(password.old_password, user_model.hashedPassword):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Incorrect current password')
    user_model.hashedPassword = bcrypt_context.hash(password.new_password)
    db.add(user_model)
    db.commit()
