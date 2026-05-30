from app.core.base_query_service import BaseQueryService
from app.tasks.filter import TasksFilter
from app.tasks.repository import TasksRepository
from app.tasks.model import Task

class TasksQueryService(BaseQueryService):
    repository=TasksRepository()
    model=Task
    
    def list(self, filters=None, current_user_id=None):
        filters = filters or TasksFilter()
        filters = self.apply_user_scope(filters, current_user_id)
        return super().list(filters)
    
    def apply_user_scope(self, filters, current_user_id):
        if current_user_id:
            filters.created_by = current_user_id
        return filters