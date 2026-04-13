from app.core.api_factory import create_api_router
from app.core.services_factory import get_quest_structure_service

from .filter import QuestStructureFilter

router = create_api_router(
    service=get_quest_structure_service(),
    prefix="/api/quest-structure",
    filter_model=QuestStructureFilter
)
