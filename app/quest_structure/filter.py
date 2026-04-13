from pydantic import BaseModel


class QuestStructureFilter(BaseModel):

    quest_id: int | None = None
    task_id: int | None = None
    
