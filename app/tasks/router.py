from app.core.router_factory import create_crud_router

from app.core.services_factory import (
    get_tasks_service,
    get_tasks_query_service
)


router = create_crud_router(
    command_service=get_tasks_service(),
    query_service=get_tasks_query_service(),
    prefix="/tasks",
    require_auth_for_write=True,
    require_auth_for_read=True
)