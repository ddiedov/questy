from app.core.api_factory import create_api_router

from .service import QuestApplicationsService
from .filter import QuestApplicationsFilter


router = create_api_router(
    service=QuestApplicationsService(),
    prefix="/api/quest-applications",
    filter_model=QuestApplicationsFilter,
)
