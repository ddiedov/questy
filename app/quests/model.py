from pydantic import BaseModel
from app.quest_applications.model import QuestApplicationView
from app.quest_structure.model import QuestStructureItem


#------ DTO Models (Database structures)

class Quest(BaseModel):
    id: int
    title: str
    description: str | None = None
    featured: bool | None = None
    image_url: str | None = None
    display_incompleted: bool | None = None
    created_by: str | None = None

class QuestCreate(BaseModel):
    title: str

class QuestUpdate(BaseModel):
    title: str
    description: str
    image_url: str
    display_incompleted: bool = False

class QuestPatch(BaseModel):
    description: str | None = None
    featured: bool  | None = None
    image_url: str | None = None
    display_incompleted: bool | None = None


#------ Use Case Models (UI usage structures)

class QuestForUpdate(Quest):
    applications: list[QuestApplicationView]
    new_applications: list[QuestApplicationView]
    tasks: list[QuestStructureItem]


class QuestForRuntimeView(BaseModel):
    id: int
    title: str
    description: str | None = None
    display_incompleted: bool = False