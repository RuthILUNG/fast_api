from sqlalchemy import Column, Integer, String, Enum, DateTime
from database import Base
import enum
from datetime import datetime

class StatusEnum(str, enum.Enum):
    pending = "Pending"
    completed = "Completed"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
