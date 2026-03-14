from app.core.router_factory import create_crud_router
from .service import QuestsService

router = create_crud_router(QuestsService(), "/quests")