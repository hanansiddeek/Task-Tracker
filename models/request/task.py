from pydantic import BaseModel
from typing import Optional


class TaskCreation(BaseModel):
    task_name: str
    description: Optional[str] | None
    status: str
