from app.core.router_factory import create_crud_router
from .service import QuestApplicationsService

router = create_crud_router(QuestApplicationsService(), "/quest_applications", True, True)