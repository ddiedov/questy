from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class QuestRunStatusType(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"

class QuestRun(BaseModel):
    id: int
    quest_id: int
    participant_id: str
    current_step_id: int | None = None
    status: QuestRunStatusType
    started_at: datetime | None = None 
    completed_at: datetime | None = None 
    duration: int | None = None  
    created_by: str | None = None

class QuestRunCreate(BaseModel):
    quest_id: int
    participant_id: str
    current_step_id: int | None = None
    started_at: datetime | None = None
    status: QuestRunStatusType = QuestRunStatusType.ACTIVE

class QuestRunUpdate(BaseModel):
    quest_id: int
    participant_id: str
    current_step_id: int | None
    started_at: datetime | None = None 
    completed_at: datetime | None = None 
    duration: int | None = None  
    status: QuestRunStatusType

class QuestRunPatch(BaseModel):
    current_step_id: int | None = None
    status: QuestRunStatusType | None = None
    started_at: datetime | None = None 
    completed_at: datetime | None = None 
    duration: int | None = None  



#------ Use Case Models (UI usage structures)
