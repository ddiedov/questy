from pydantic import BaseModel
from enum import Enum

class ParticipantType(str, Enum):
    INDIVIDUAL = "individual"
    TEAM = "team"

class StatusType(str, Enum):
    NEW = "new"

class QuestApplication(BaseModel):
    id: int
    quest_id: int
    participant_id: str
    participant_type: ParticipantType
    status: StatusType
    created_by: str | None = None

class QuestApplicationCreate(BaseModel):
    quest_id: int
    participant_id: str
    participant_type: ParticipantType
    status: StatusType = "new"

class QuestApplicationUpdate(BaseModel):
    quest_id: int
    participant_id: str
    participant_type: ParticipantType
    status: StatusType

class QuestApplicationPatch(BaseModel):
    quest_id: int | None = None
    participant_id: str | None = None
    participant_type: ParticipantType | None = None
    status: StatusType | None = None