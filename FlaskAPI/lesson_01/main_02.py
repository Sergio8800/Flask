import logging

from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()
templates = Jinja2Templates(directory=".templates")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>Hello World</h1>"


@app.get("/message")
async def read_message():
    message = {"message": "Hello World"}
    return JSONResponse(content=message, status_code=200)


@app.get("/{name}", response_class=HTMLResponse)
async def read_item(request: Request, name: str):
    return templates.TemplateResponse("item.html", {"request": request, "name": name})



if __name__ == '__main__':
    uvicorn.run("main_02:app", port=8000)
