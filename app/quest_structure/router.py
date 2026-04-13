from app.core.router_factory import create_crud_router
from app.core.services_factory import get_quest_structure_service

router = create_crud_router(
    get_quest_structure_service(),
    "/quest-structure",
    True,
    True
)