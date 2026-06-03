from pydantic import BaseModel
from enum import Enum
from app.quest_structure.model import QuestStep


class QuestRunStatusType(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"

class QuestRun(BaseModel):
    id: int
    quest_id: int
    participant_id: str
    current_step_id: int | None = None
    status: QuestRunStatusType
    created_by: str | None = None


class QuestRunCreate(BaseModel):
    quest_id: int
    participant_id: str
    current_step_id: int | None = None
    status: QuestRunStatusType = QuestRunStatusType.ACTIVE


class QuestRunUpdate(BaseModel):
    quest_id: int
    participant_id: str
    current_step_id: int | None
    status: QuestRunStatusType


class QuestRunPatch(BaseModel):
    current_step_id: int | None = None
    status: QuestRunStatusType | None = None



#------ Use Case Models (UI usage structures)
class QuestState(BaseModel):
    state: str
    run_id: int | None = None


class QuestRunRuntimeView(BaseModel):
    run: QuestRun
#    quest: QuestForRuntimeView
    current_step: QuestStep | None
    previous_steps: list[QuestStep]