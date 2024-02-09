from fastapi import FastAPI
from .model import Base
from .database import engine
from .routers import auth, todos, admin, users

app = FastAPI()

@app.get('/')
async def hello():
    return {"Welcome Message": "Welcome to Todo App"}

Base.metadata.create_all(bind = engine)

app.include_router(auth.router)

app.include_router(todos.router)

app.include_router(admin.router)

app.include_router(users.router)
