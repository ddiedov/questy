from fastapi import HTTPException
from app.core.base_command_service import BaseCommandService
from app.teams.repository import TeamsRepository
from .model import Team, TeamCreate, TeamUpdate, TeamPatch

class TeamsService(BaseCommandService):
    repository=TeamsRepository()
    model=Team
    create_model=TeamCreate
    update_model=TeamUpdate
    patch_model=TeamPatch
        

    def create(self, data: TeamCreate, user_id=None):
        if len(data.name) < 3:
            raise HTTPException(
                status_code=400,
                detail="Name must contain at least 3 characters"
            )

        return super().create(data, user_id)
