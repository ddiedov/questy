from app.core.router_factory import create_crud_router

from app.core.services_factory import (
    get_quests_service,
    get_quests_query_service
)

router = create_crud_router(
    command_service=get_quests_service(),
    query_service=get_quests_query_service(),
    prefix="/quests",
    require_auth_for_write=True,
    require_auth_for_read=False
)