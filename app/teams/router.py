from app.core.router_factory import create_crud_router
from .service import TeamsService

router = create_crud_router(TeamsService(), "/teams")