from pydantic import BaseModel
from typing import Optional
import enum
from datetime import datetime

class StatusEnum(str, enum.Enum):
    pending = "Pending"
    completed = "Completed"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.pending

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[StatusEnum]

class TaskOut(TaskBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
