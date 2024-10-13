from pydantic import BaseModel
from typing import List, Optional

class TaskBase(BaseModel):
    title: str
    is_completed: Optional[bool] = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True  


class BulkTaskCreate(BaseModel):
    tasks: List[TaskCreate]


class TaskDelete(BaseModel):
    id: int

class TaskId(BaseModel):
    id: int

class TasksBulkDelete(BaseModel):
    tasks: List[TaskId]