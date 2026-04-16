from fastapi import APIRouter, Depends, Response, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.task import (
    TaskCreate,
    TaskPut,
    TaskPatch,
    TaskResponse,
    TaskListResponse,
)
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=TaskListResponse)
def get_tasks(
    page: int = Query(1, gt=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    return service.get_tasks(page=page, limit=limit)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.get_task_by_id(task_id)


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(dto: TaskCreate, db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.create_task(dto)


@router.put("/{task_id}", response_model=TaskResponse)
def put_task(task_id: str, dto: TaskPut, db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.put_task(task_id, dto)


@router.patch("/{task_id}", response_model=TaskResponse)
def patch_task(task_id: str, dto: TaskPatch, db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.patch_task(task_id, dto)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    service = TaskService(db)
    service.delete_task(task_id)
    return Response(status_code=204)