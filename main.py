from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from typing import List, Optional
from datetime import datetime, timedelta

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend access (React/Next.js running at localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, updates: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

@app.get("/tasks/", response_model=List[schemas.TaskOut])
def get_tasks(status: Optional[schemas.StatusEnum] = None, db: Session = Depends(get_db)):
    if status:
        return db.query(models.Task).filter(models.Task.status == status).all()
    return db.query(models.Task).all()

@app.get("/tasks/completion-percentage")
def completion_percentage(db: Session = Depends(get_db)):
    start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())
    tasks = db.query(models.Task).filter(models.Task.created_at >= start_of_week).all()
    if not tasks:
        return {"percentage_completed": 0.0}
    completed = [t for t in tasks if t.status == schemas.StatusEnum.completed]
    return {"percentage_completed": (len(completed) / len(tasks)) * 100}
