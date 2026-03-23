from app.core.api_factory import create_api_router

from .service import TeamsService
from .filter import TeamsFilter


router = create_api_router(
    service=TeamsService(),
    prefix="/api/teams",
    filter_model=TeamsFilter,
)
