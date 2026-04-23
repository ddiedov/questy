from pydantic import BaseModel
from app.tasks.model import Task

#   ======      DTO structures      ======
class QuestStructureItemDTO(BaseModel):
    id: int
    quest_id: int
    task_id: int
    position: int
    created_by: str | None = None

class CreateQuestStructureItemDTO(BaseModel):
    quest_id: int
    task_id: int
    position: int | None = None
    

#   ======      Service structures      ======
class QuestStructureItem(BaseModel):
    task: Task
    position: int | None = None

class QuestStructure(BaseModel):
    quest_id: int
    tasks: list[QuestStructureItem]
