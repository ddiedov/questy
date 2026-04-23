from app.core.router_factory import create_crud_router
from app.core.services_factory import get_quests_service

router = create_crud_router(
    get_quests_service(),
    "/quests",
    True,
    False
)

