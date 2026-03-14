from fastapi import HTTPException
from app.core.base_service import BaseService
from app.teams.repository import TeamsRepository
from .model import Team, TeamCreate, TeamUpdate

class TeamsService(BaseService):

    def __init__(self):
        super().__init__(
            repository=TeamsRepository(),
            model=Team,
            create_model=TeamCreate,
            update_model=TeamUpdate
        )


    def create(self, data: TeamCreate):
        if len(data.name) < 3:
            raise HTTPException(
                status_code=400,
                detail="Name must contain at least 3 characters"
            )

        return super().create(data)