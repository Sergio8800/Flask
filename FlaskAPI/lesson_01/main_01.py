import logging
from typing import Optional

import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
# unicorn  lesson_01.main_01:app --reload >> in to config text
# pip install "uvicorn[standard]"

# curl -X 'PUT' 'http://127.0.0.1:8000/items/42' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"name": "NewName", "price": 77.7}'
from starlette.templating import Jinja2Templates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="templates")



app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.get("/")
async def root():
    logger.info('Отработал GET запрос.')
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: Item):
    logger.info('Отработал POST запрос.')
    return item
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    logger.info(f'Отработал PUT запрос для item id = {item_id}.')
    return {"item_id": item_id, "item": item}

if __name__ == "__main__":
    uvicorn.run("main_01:app", port=8000)