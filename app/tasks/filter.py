from pydantic import BaseModel


class TasksFilter(BaseModel):
    title: str | None = None
    description: str | None = None
    created_by: str | None = None