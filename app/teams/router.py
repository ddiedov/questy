from app.core.router_factory import create_crud_router

from app.core.services_factory import (
    get_teams_service,
    get_teams_query_service
)

router = create_crud_router(
    command_service=get_teams_service(),
    query_service=get_teams_query_service(),
    prefix="/teams",
    require_auth_for_write=True,
    require_auth_for_read=True
)