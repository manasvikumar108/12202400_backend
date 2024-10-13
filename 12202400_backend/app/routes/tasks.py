from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/v1/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)

@router.get("/v1/tasks", response_model=List[schemas.Task])
def list_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

@router.get("/v1/tasks/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/v1/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    updated_task = crud.update_task(db, task_id, task)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/v1/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.delete_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}

@router.post("/v1/tasks/bulk", response_model=List[schemas.Task])
def bulk_create_tasks(bulk_task_create: schemas.BulkTaskCreate, db: Session = Depends(get_db)):
    return crud.bulk_create_tasks(db, bulk_task_create)

@router.delete("/v1/tasks/bulk", status_code=204)
def bulk_delete_tasks(tasks_data: schemas.TasksBulkDelete, db: Session = Depends(get_db)):
    task_ids = [task.id for task in tasks_data.tasks]    
    crud.bulk_delete_tasks(db=db, task_ids=task_ids)    
    return {"detail": "Tasks deleted successfully"}


