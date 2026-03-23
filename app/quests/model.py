from pydantic import BaseModel

class Quest(BaseModel):
    id: int
    title: str
    description: str | None = None
    featured: bool  | None = None
    image_url: str | None = None

class QuestCreate(BaseModel):
    title: str

class QuestUpdate(BaseModel):
    title: str
    description: str
    image_url: str

class QuestPatch(BaseModel):
    description: str | None = None
    featured: bool  | None = None
    image_url: str | None = None
