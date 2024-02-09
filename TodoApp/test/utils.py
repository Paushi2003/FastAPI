from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
import pytest
from sqlalchemy import text
from ..main import app
from fastapi.testclient import TestClient
from ..model import Todos, Users
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'paushigaa', 'id': 1, 'role': 'admin'}


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = 'todo1',
        description = 'test todo',
        priority = 2,
        completed = False,
        owner = 1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("Delete from todos;"))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        username = 'paushigaa',
        email = 'paushi@gmail.com',
        firstname = 'paushigaa',
        lastname = 'shan',
        hashedpassword = bcrypt_context.hash('paushigaa'),
        role = 'admin'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("Delete from users;"))
        connection.commit()
