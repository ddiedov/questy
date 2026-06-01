from pydantic import BaseModel, Field

class Team(BaseModel):
    id: int
    name: str

class TeamCreate(BaseModel):
    name: str = Field(min_length=5)

class TeamUpdate(BaseModel):
    name: str

class TeamPatch(BaseModel):
    name: str
