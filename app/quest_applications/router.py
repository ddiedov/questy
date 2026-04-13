from app.core.router_factory import create_crud_router
from app.core.services_factory import get_quest_applications_service

router = create_crud_router(
    get_quest_applications_service(),
    "/quest-applications",
    True,
    True
)