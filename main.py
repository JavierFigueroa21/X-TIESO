from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import schemas
from database_connection import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn
from datetime import datetime


app = FastAPI()

schemas.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class User(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    last_name: str = Field(min_length=1, max_length=30)
    email: str = Field(min_length=1, max_length=50)
    age: int = Field(gt=0)
    gender: str = Field(min_length=1, max_length=10)
    role: str = Field(min_length=1, max_length=10)
    friends: list[int] | None = None

'''
class Post(BaseModel):
    id_user: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=30)
    content: str = Field(min_length=1, max_length=300)
    is_published: bool = Field(default=False)
'''

@app.post("/")
def create_user(user: User, db: Session = Depends(get_db)):

    user_model = schemas.User()

    user_model.name = user.name
    user_model.last_name = user.last_name
    user_model.email = user.email
    user_model.age = user.age
    user_model.gender = user.gender
    user_model.role = user.role

    if not user.friends is None:
        for friend_id in user.friends:
            friend_model = db.query(schemas.User).filter(schemas.User.id == friend_id).first()

            if friend_model is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"User id: {friend_id} Does not exist")

    user_model.friends = user.friends

    db.add(user_model)
    db.commit()

    return user


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=5000, log_level="info", reload=True)