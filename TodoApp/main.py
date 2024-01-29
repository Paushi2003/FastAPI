from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
import model
from model import Todos
from database import SessionLocal, engine
from pydantic import BaseModel, Field
from routers import auth, todos

app = FastAPI()

model.Base.metadata.create_all(bind = engine)

app.include_router(auth.router)

app.include_router(todos.router)
