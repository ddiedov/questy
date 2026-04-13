from app.core.api_factory import create_api_router
from app.core.services_factory import get_teams_service

from .filter import TeamsFilter

router = create_api_router(
    service=get_teams_service(),
    prefix="/api/teams",
    filter_model=TeamsFilter
)
