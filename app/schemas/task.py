from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=3)
    status: Literal["new", "in_progress", "done"] = "new"


class TaskPut(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=3)
    status: Literal["new", "in_progress", "done"]


class TaskPatch(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=3)
    status: Optional[Literal["new", "in_progress", "done"]] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime


class PaginationParams(BaseModel):
    page: int = Field(1, gt=0)
    limit: int = Field(10, ge=1, le=100)


class PaginationMeta(BaseModel):
    total: int
    page: int
    limit: int
    totalPages: int


class TaskListResponse(BaseModel):
    data: list[TaskResponse]
    meta: PaginationMeta