from math import ceil
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskPut, TaskPatch
from app.utils.exceptions import NotFoundError, ConflictError


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, dto: TaskCreate) -> Task:
        task = Task(
            title=dto.title,
            description=dto.description,
            status=dto.status
        )
        self.db.add(task)
        try:
            self.db.commit()
            self.db.refresh(task)
            return task
        except IntegrityError:
            self.db.rollback()
            raise ConflictError("Task with this title already exists")

    def get_tasks(self, page: int = 1, limit: int = 10):
        offset = (page - 1) * limit

        total_stmt = select(func.count()).select_from(Task).where(Task.deleted_at.is_(None))
        total = self.db.execute(total_stmt).scalar_one()

        stmt = (
            select(Task)
            .where(Task.deleted_at.is_(None))
            .order_by(Task.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        tasks = self.db.execute(stmt).scalars().all()

        return {
            "data": tasks,
            "meta": {
                "total": total,
                "page": page,
                "limit": limit,
                "totalPages": ceil(total / limit) if total > 0 else 1
            }
        }

    def get_task_by_id(self, task_id: str) -> Task:
        stmt = select(Task).where(Task.id == task_id, Task.deleted_at.is_(None))
        task = self.db.execute(stmt).scalar_one_or_none()
        if not task:
            raise NotFoundError("Task not found")
        return task

    def put_task(self, task_id: str, dto: TaskPut) -> Task:
        task = self.get_task_by_id(task_id)
        task.title = dto.title
        task.description = dto.description
        task.status = dto.status

        try:
            self.db.commit()
            self.db.refresh(task)
            return task
        except IntegrityError:
            self.db.rollback()
            raise ConflictError("Task with this title already exists")

    def patch_task(self, task_id: str, dto: TaskPatch) -> Task:
        task = self.get_task_by_id(task_id)

        update_data = dto.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        try:
            self.db.commit()
            self.db.refresh(task)
            return task
        except IntegrityError:
            self.db.rollback()
            raise ConflictError("Task with this title already exists")

    def delete_task(self, task_id: str) -> None:
        task = self.get_task_by_id(task_id)
        task.deleted_at = datetime.utcnow()
        self.db.commit()