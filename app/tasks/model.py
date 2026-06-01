from pydantic import BaseModel, Field

class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    image_url: str | None = None
    question: str | None = None
    question_image_url: str | None = None 
    answer: str | None = None
    outer_description: str | None = None
    outer_image_url: str | None = None
    created_by: str | None = None

class TaskCreate(BaseModel):
    title: str = Field(min_length=5)
    description: str | None = None
    image_url: str | None = None
    question: str
    question_image_url: str | None = None 
    answer: str
    outer_description: str | None = None
    outer_image_url: str | None = None

class TaskUpdate(BaseModel):
    title: str
    description: str
    image_url: str
    question: str
    question_image_url: str
    answer: str
    outer_description: str
    outer_image_url: str

class TaskPatch(BaseModel):
    description: str | None = None
    image_url: str | None = None
    question: str | None = None
    question_image_url: str | None = None 
    answer: str | None = None
    outer_description: str | None = None
    outer_image_url: str | None = None
