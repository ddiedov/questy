from pydantic import BaseModel
from .model import QuestRunStatusType


class QuestRunsFilter(BaseModel):
    quest_id: int | None = None
    participant_id: str | None = None
    status: QuestRunStatusType | None = None
    
    
