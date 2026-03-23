from app.core.api_factory import create_api_router

from .service import QuestsService
from .filter import QuestsFilter


router = create_api_router(
    service=QuestsService(),
    prefix="/api/quests",
    filter_model=QuestsFilter,
)
