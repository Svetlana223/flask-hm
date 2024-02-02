# Необходимо создать API для управления списком задач.
# Каждая задача должна содержать заголовок и описание.
# Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
#
# API должен содержать следующие конечные точки:
# — GET /tasks — возвращает список всех задач.
# — GET /tasks/{id} — возвращает задачу с указанным идентификатором.
# — POST /tasks — добавляет новую задачу.
# — PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
# — DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.
#
# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
# Для этого использовать библиотеку Pydantic.

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from pydantic import BaseModel


app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool


tasks = []


@app.get('/tasks/', response_class=HTMLResponse)
async def get_tasks(request: Request):
    task_table = pd.DataFrame([vars(task) for task in tasks]).to_html()
    return templates.TemplateResponse('tasks.html', {'request': request, 'table': task_table})


@app.post('/tasks/', response_model=Task)
async def create_task(task: Task):
    task_id = len(tasks) + 1
    task.id = task_id
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    for i, stor_task in enumerate(tasks):
        if stor_task.id == task_id:
            task.id = task_id
            tasks[i] = task
            return task


@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    for i, stor_task in enumerate(tasks):
        if stor_task.id == task_id:
            return tasks.pop(i)
