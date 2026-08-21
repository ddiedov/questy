from pydantic import BaseModel, Field, field_validator
from app.core.html import sanitize_html
from app.quest_applications.model import QuestApplicationView
from app.quest_structure.model import QuestStep

from app.core.constants import PROPERTY_DEFAULTS

#------ DTO Models (Database structures)
class Quest(BaseModel):
    id: int
    title: str
    description: str | None = None
    image_url: str | None = None

    allow_replays: bool | None = None
    difficulty: int | None = None
    distance: int | None = None
    language: str | None = None
    player_mode: int | None = None
    duration: int | None = None
    age_group: int | None = None

    featured: bool | None = None

    created_by: str | None = None    

class QuestCreate(BaseModel):
    title: str = Field(min_length=5)

    allow_replays: bool = PROPERTY_DEFAULTS["allow_replays"]
    difficulty: int = PROPERTY_DEFAULTS["difficulty"]
    distance: int = PROPERTY_DEFAULTS["distance"]
    language: str = PROPERTY_DEFAULTS["language"]
    player_mode: int = PROPERTY_DEFAULTS["player_mode"]
    duration: int = PROPERTY_DEFAULTS["duration"]
    age_group: int = PROPERTY_DEFAULTS["age_group"]

class QuestUpdate(BaseModel):
    title: str
    description: str | None = None
    image_url: str | None = None
    allow_replays: bool | None = None
    difficulty: int | None = None
    distance: int | None = None
    language: str | None = None
    player_mode: int | None = None
    duration: int | None = None
    age_group: int | None = None

    @field_validator("description")
    @classmethod
    def sanitize_description(cls, value):
        return sanitize_html(value)

class QuestPatch(BaseModel):
    description: str | None = None
    featured: bool  | None = None
    image_url: str | None = None
    allow_replays: bool | None = None
    difficulty: int | None = None
    distance: int | None = None
    language: str | None = None
    player_mode: int | None = None
    duration: int | None = None
    age_group: int | None = None

    @field_validator("description")
    @classmethod
    def sanitize_description(cls, value):
        return sanitize_html(value)


#------ Use Case Models (UI usage structures)
class QuestState(BaseModel):
    state: str
    run_id: int | None = None

class QuestForView(Quest):
    is_author: bool
    state: QuestState | None = None

class QuestForUpdate(Quest):
    applications: list[QuestApplicationView]
    new_applications: list[QuestApplicationView]
    steps: list[QuestStep]

class QuestForRuntimeView(BaseModel):
    id: int
    title: str
    description: str | None = None
    image_url: str | None = None
