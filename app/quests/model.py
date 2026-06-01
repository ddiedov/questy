from pydantic import BaseModel, Field
from app.quest_applications.model import QuestApplicationView
from app.quest_structure.model import QuestStep


#------ DTO Models (Database structures)

class Quest(BaseModel):
    id: int
    title: str
    description: str | None = None
    featured: bool | None = None
    image_url: str | None = None
    created_by: str | None = None

class QuestCreate(BaseModel):
    title: str = Field(min_length=5)

class QuestUpdate(BaseModel):
    title: str
    description: str
    image_url: str

class QuestPatch(BaseModel):
    description: str | None = None
    featured: bool  | None = None
    image_url: str | None = None


#------ Use Case Models (UI usage structures)

class QuestForUpdate(Quest):
    applications: list[QuestApplicationView]
    new_applications: list[QuestApplicationView]
    steps: list[QuestStep]


class QuestForRuntimeView(BaseModel):
    id: int
    title: str
    description: str | None = None
