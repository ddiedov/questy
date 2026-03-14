from pydantic import BaseModel

class Quest(BaseModel):
    id: int
    title: str

class QuestCreate(BaseModel):
    title: str

class QuestUpdate(BaseModel):
    title: str
