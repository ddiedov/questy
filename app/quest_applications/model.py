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
    participant_id: int
    participant_type: ParticipantType
    status: StatusType

class QuestApplicationCreate(BaseModel):
    quest_id: int
    participant_id: int
    participant_type: ParticipantType

class QuestApplicationUpdate(BaseModel):
    quest_id: int
    participant_id: int
    participant_type: ParticipantType
    status: StatusType

class QuestApplicationPatch(BaseModel):
    quest_id: int | None = None
    participant_id: int | None = None
    participant_type: ParticipantType | None = None
    status: StatusType | None = None