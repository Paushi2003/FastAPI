from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from ..model import Users
from passlib.context import CryptContext
from ..database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import jwt, JWTError

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
oauth2bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

SECRET_KEY = '5edb92f9ff85ed3c3688a51f966a3f697e849fd901d3e8cdc7cc037aaaee331b'
ALGORITHM = 'HS256'

class CreateUserRequest(BaseModel):
    username: str
    email: str
    firstname: str
    lastname: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if bcrypt_context.verify(password, user.hashedpassword):
        return user
    else:
        return False
    
def create_token(username: str, user_id: int, expires_delta: timedelta, role: str):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.utcnow()+expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: int = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Could not find user')
        return {'username': username, 'id': user_id, 'role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Could not find user')

@router.get('/users')
async def read_users(db: db_dependency):
    users = db.query(Users).all()
    return users

@router.post('/createuser', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, userrequest: CreateUserRequest):
    user_model = Users(
        email = userrequest.email,
        username = userrequest.username,
        firstname = userrequest.firstname,
        lastname = userrequest.lastname,
        hashedpassword = bcrypt_context.hash(userrequest.password),
        role = userrequest.role, 
        is_active = True
    )
    db.add(user_model)
    db.commit()

@router.post('/login', response_model=Token)
async def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if user:
        token = create_token(user.username, user.id, timedelta(minutes=60), role = user.role)
        return {'access_token': token, 'token_type': 'bearer'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Could not find user')