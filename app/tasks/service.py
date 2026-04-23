from fastapi import HTTPException
from app.core.base_service import BaseService
from .repository import TasksRepository
from .model import Task, TaskCreate, TaskUpdate, TaskPatch
from .filter import TasksFilter

class TasksService(BaseService):
    repository=TasksRepository()
    model=Task
    create_model=TaskCreate
    update_model=TaskUpdate
    patch_model=TaskPatch
        

#    def get_redirect_url(self, entity, item):
#        return f"/quests/{item.quest_id}"

    def create(self, data: TaskCreate, user_id):
        if len(data.title) < 3:
            raise HTTPException(
                status_code=400,
                detail="Title must contain at least 3 characters"
            )
        return super().create(data, user_id)
    
    def apply_user_scope(self, filters, current_user_id):
        if current_user_id:
            filters.created_by = current_user_id
        return filters

    def list(self, filters=None, current_user_id=None):
        filters = filters or TasksFilter()
        filters = self.apply_user_scope(filters, current_user_id)
        return super().list(filters)
