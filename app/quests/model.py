from pydantic import BaseModel
from app.quest_applications.model import QuestApplication
from app.quest_structure.model import QuestStructureItem


#------ DTO Models (Database structures)

class Quest(BaseModel):
    id: int
    title: str
    description: str | None = None
    featured: bool  | None = None
    image_url: str | None = None
    created_by: str | None = None

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


#------ Use Case Models (UI usage structures)

class QuestForUpdate(Quest):
    applications: list[QuestApplication]
    tasks: list[QuestStructureItem]