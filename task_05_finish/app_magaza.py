from typing import List
from pydantic import BaseModel, Field
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# pip install sqlalchemy
# pip install databases[aiosqlite]
import databases
import sqlalchemy

DATABASE_URL = "sqlite:///.magaza.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
...
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
app = FastAPI()


class Item(BaseModel):
    id : int
    name: str = Field(title="Name", max_length=50)
    price: float = Field(title="Price", gt=0, le=100000)
    description: str = Field(default=None, title="Description", max_length=1000)
    tax: float = Field(0, title="Tax", ge=0, le=10)


class User(BaseModel):
    id: int
    username: str = Field(title="Username", max_length=50)
    full_name: str = Field(None, title="Full Name", max_length=100)


class Order(BaseModel):
    id: int
    items: List[Item]
    user: User

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/items/")
async def create_item(item: Item):
    return {"item": item}


if __name__ == '__main__':
    uvicorn.run("app_magaza:app", port=8000)
