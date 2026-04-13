from app.core.api_factory import create_api_router
from app.core.services_factory import get_quest_applications_service

from .filter import QuestApplicationsFilter

router = create_api_router(
    service=get_quest_applications_service(),
    prefix="/api/quest-applications",
    filter_model=QuestApplicationsFilter
)
