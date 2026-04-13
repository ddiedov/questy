from pydantic import BaseModel
from enum import Enum

class QuestStructure(BaseModel):
    id: int
    quest_id: int
    task_id: int

class QuestStructureCreate(BaseModel):
    quest_id: int
    task_id: int
    
class QuestStructureUpdate(BaseModel):
    quest_id: int
    task_id: int
    
class QuestStructurePatch(BaseModel):
    quest_id: int | None = None
    task_id: int | None = None