from app.core.api_factory import create_api_router
from app.core.services_factory import get_quests_service

from .filter import QuestsFilter

router = create_api_router(
    service=get_quests_service(),
    prefix="/api/quests",
    filter_model=QuestsFilter
)
