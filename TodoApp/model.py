from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Todos(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    description = Column(String(200))
    priority = Column(Integer)
    completed = Column(Boolean, default=False)