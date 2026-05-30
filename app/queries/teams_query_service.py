from app.core.base_query_service import BaseQueryService
from app.teams.repository import TeamsRepository
from app.teams.model import Team

class TeamsQueryService(BaseQueryService):
    repository=TeamsRepository()
    model=Team