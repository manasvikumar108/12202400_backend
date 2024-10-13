from sqlalchemy.orm import Session
from typing import List
from app import models, schemas

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session):
    return db.query(models.Task).all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(title=task.title, is_completed=task.is_completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if db_task:
        db_task.title = task.title
        db_task.is_completed = task.is_completed
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def bulk_create_tasks(db: Session, tasks: schemas.BulkTaskCreate):
    db_tasks = [models.Task(title=task.title, is_completed=task.is_completed) for task in tasks.tasks]
    db.add_all(db_tasks)
    db.commit()
    return db_tasks

def bulk_delete_tasks(db: Session, task_ids: List[int]):
    tasks_to_delete = db.query(models.Task).filter(models.Task.id.in_(task_ids)).all()

    if not tasks_to_delete:
        raise HTTPException(status_code=404, detail="No tasks found with the provided IDs")

    for task in tasks_to_delete:
        db.delete(task)
        db.commit()
    return tasks_to_delete


