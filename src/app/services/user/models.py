from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from core.db.sessions import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String, index=True, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
