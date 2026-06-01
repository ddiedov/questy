from app.core.base_command_service import BaseCommandService
from app.teams.repository import TeamsRepository
from .model import Team, TeamCreate, TeamUpdate, TeamPatch

class TeamsService(BaseCommandService):
    repository=TeamsRepository()
    model=Team
    create_model=TeamCreate
    update_model=TeamUpdate
    patch_model=TeamPatch
        
