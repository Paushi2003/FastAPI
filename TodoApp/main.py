from fastapi import FastAPI
import model
from database import engine

app = FastAPI()

model.Base.metadata.create_all(bind = engine)