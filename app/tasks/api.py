from app.core.api_factory import create_api_router
from app.core.services_factory import get_tasks_service

from .filter import TasksFilter

router = create_api_router(
    service=get_tasks_service(),
    prefix="/api/tasks",
    filter_model=TasksFilter
)
