from sqlalchemy import Column, Integer, String, Boolean, ARRAY, TIMESTAMP
from database_connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String)
    age = Column(Integer)
    gender = Column(String)
    role = Column(String)
    friends = Column(ARRAY(String), nullable=True)


class Post(Base):
    __tablename__ = "posts"

    id_post = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer)
    date_posted = Column(TIMESTAMP)
    date_updated = Column(TIMESTAMP)
    title = Column(String)
    content = Column(String)
    is_published = Column(Boolean)
