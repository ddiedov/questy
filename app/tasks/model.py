from pydantic import BaseModel

class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    image_url: str | None = None
    created_by: str | None = None

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    image_url: str | None = None

class TaskUpdate(BaseModel):
    title: str
    description: str
    image_url: str

class TaskPatch(BaseModel):
    description: str | None = None
    image_url: str | None = None
