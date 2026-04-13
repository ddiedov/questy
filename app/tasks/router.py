from app.core.router_factory import create_crud_router
from app.core.services_factory import get_tasks_service

router = create_crud_router(
    get_tasks_service(),
    "/tasks",
    True,
    True
)