from pydantic import BaseModel

class Team(BaseModel):
    id: int
    name: str

class TeamCreate(BaseModel):
    name: str

class TeamUpdate(BaseModel):
    name: str
