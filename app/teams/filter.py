from pydantic import BaseModel


class TeamsFilter(BaseModel):

    captain_id: int | None = None