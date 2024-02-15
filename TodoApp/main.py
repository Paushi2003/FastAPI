from fastapi import FastAPI
from .model import Base
from .database import engine
from .routers import auth, todos, admin, users
from starlette.staticfiles import StaticFiles
import os

app = FastAPI()

@app.get('/')
async def hello():
    return {"Welcome Message": "Welcome to Todo App"}

Base.metadata.create_all(bind = engine)

current_dir = os.path.dirname(os.path.abspath(__file__))
app.mount('/static', StaticFiles(directory=os.path.join(current_dir, 'static')), name='static')

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
