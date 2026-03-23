from pydantic import BaseModel


class QuestApplicationsFilter(BaseModel):

    quest_id: int | None = None
    participant_id: int | None = None
    participant_type: str | None = None
    status: str | None = None
