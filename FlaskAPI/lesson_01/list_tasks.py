import logging
from typing import Optional

import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()
templates = Jinja2Templates(directory=".templates")


# curl -X 'POST' 'http://127.0.0.1:8000/items/42' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"task_name": "NewName", "task_description":'77.7'}'


class Tasks(BaseModel):
    task_id : Optional[int]
    task_name: str
    task_description: Optional[str] = None


task1 = Tasks(task_id=1, task_name="Task name 1", task_description=" task description 1")
task2 = Tasks(task_id=2, task_name="Task name 2", task_description=" task description 33")
task3 = Tasks(task_id=3, task_name="Task name 3", task_description=" task description 2424")
task4 = Tasks(task_id=4, task_name="Task name 4", task_description=" task description 365324")

tasks = [task3, task4, task1, task2]


@app.get("/tasks/")
async def root():
    logger.info('Отработал GET запрос.')
    return tasks


@app.get("/tasks/{id_task}")
async def root_task_id(id_task: int):
    logger.info(f'Отработал GET запрос id#{id_task}')
    for i in range(len(tasks)):
        if id_task == tasks[i].task_id:
            return tasks[i]
    return HTTPException(status_code=404, detail='Tasks not found')


@app.get("/tasks/{name_task}")
async def root_task_name(name_task: str):
    logger.info(f'Отработал GET запрос id#{name_task}')
    res_list = []
    for i in range(len(tasks)):
        if name_task == tasks[i].task_name:
            res_list.append(tasks[i])
    # return res_list if res_list else HTTPException(status_code=404, detail='Tasks not found')
    return HTTPException(status_code=404, detail='Tasks not found') if not res_list else res_list


@app.post("/tasks/")
async def create_task(task: Tasks):
    logger.info('Отработал POST запрос.')
    tasks.append(task)
    return task


@app.put("/tasks/{tasks_id}")
async def update_task(task_id: int, task: Tasks):
    logger.info(f'Отработал PUT запрос для tasks id = {task_id}.')
    for i in range(len(tasks)):
        if task_id == tasks[i].task_id:
            tasks[i] = task
    return {"tasks_id": task_id, "task_update": task}

@app.delete("/tasks/{tasks_id}")
async def delete_task(task_id: int):
    for i in range(len(tasks)):
        if task_id == tasks[i].task_id:
            return {"movie_id": tasks.pop(i)}
    return HTTPException(status_code=404, detail='Task not found')


if __name__ == '__main__':
    uvicorn.run("list_tasks:app", port=8000)
