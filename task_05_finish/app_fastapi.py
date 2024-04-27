from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn
# pip install sqlalchemy
# pip install databases[aiosqlite]
import databases
import sqlalchemy
from sqlalchemy import create_engine
from models import *

DATABASE_URL = "sqlite:///instance/events_api.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table("users", metadata, sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("name", sqlalchemy.String(32)),
                         sqlalchemy.Column("email", sqlalchemy.String(128)), )
goods = sqlalchemy.Table("goods", metadata, sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("title", sqlalchemy.String(32)),
                         sqlalchemy.Column("content", sqlalchemy.String(32)),
                         sqlalchemy.Column("price", sqlalchemy.Float(12)), )

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)
app = FastAPI()


class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    email: str = Field(max_length=128)
    # password: int = Field(default=123, title="Password")


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    email: str = Field(max_length=128)
    # password: int = Field(default=123, title="Password")


class Goods(BaseModel):
    id: int
    title: str = Field(max_length=30)
    content: str
    price: float = Field(default=110)
    # img: list = []


class Goods1(BaseModel):
    title: str = Field(max_length=30)
    content: str
    price: float = Field(default=110)


class Order(BaseModel):
    goods: List[Goods]
    user: User


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    print(database)
    print(DATABASE_URL)
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(User.c.id == user_id)
    return await database.fetch_one(query)


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name, email=user.email)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(User.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(User.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run("app_fastapi:app", port=8008)
