from fastapi import APIRouter
from database.connection import connect_db
from models.request.task import TaskCreation
from models.mongo.task import MongoTasks
from datetime import datetime
import json
from typing import Optional
from mongoengine.errors import DoesNotExist, ValidationError


tasks_api = APIRouter(prefix='/tasks')
tasks_api.include_router(tasks_api)


@tasks_api.on_event("startup")
async def startup_event():
    connect = connect_db()
    print(connect)


@tasks_api.post('',
                tags=["Tasks"])
async def create_tasks(task_creation: TaskCreation):
    task_dict = task_creation.model_dump()
    task_dict['created_at'] = datetime.utcnow()
    mongo_task = MongoTasks(**task_dict)
    mongo_task.save()

    return json.loads(mongo_task.to_json())


@tasks_api.get('',
               tags=["Tasks"])
async def get_tasks(task_id: Optional[str] = None):
    try:
        if task_id:
            mongo_task = MongoTasks.objects.get(id=task_id)
        else:
            mongo_task = MongoTasks.objects()

        return json.loads(mongo_task.to_json())
    except DoesNotExist:
        return {"error": "Task not found"}
    except ValidationError:
        return {"error": "Input Value is not valid"}


@tasks_api.get('/search/name',
               tags=["Tasks"])
async def search_task_by_name(query_str: Optional[str] = None):
    mongo_tasks = MongoTasks.objects(task_name__icontains=query_str)

    return json.loads(mongo_tasks.to_json())


@tasks_api.get('/search/status',
               tags=["Tasks"])
async def search_by_task_status(query_str: Optional[str] = None):
    mongo_tasks = MongoTasks.objects(status__icontains=query_str)

    return json.loads(mongo_tasks.to_json())


@tasks_api.put(' ',
               tags=["Tasks"])
async def edit_tasks(task_id: str, task_edit: TaskCreation):
    try:
        mongo_task = MongoTasks.objects.get(id=task_id)
        task_dict = task_edit.model_dump()
        mongo_task.update(**task_dict)
        mongo_task.reload()

        return json.loads(mongo_task.to_json())
    except DoesNotExist:
        return {"error": "Task not found"}
    except ValidationError:
        return {"error": "Input Value is not valid"}


@tasks_api.delete(' ',
                  tags=["Tasks"])
async def delete_task(task_id: str):
    try:
        mongo_task = MongoTasks.objects.get(id=task_id)
        mongo_task.delete()

        return {"status": "Success"}
    except DoesNotExist:
        return {"error": "Task not found"}
