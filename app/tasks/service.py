from fastapi import HTTPException
from app.core.base_command_service import BaseCommandService
from .repository import TasksRepository
from .model import Task, TaskCreate, TaskUpdate, TaskPatch
from .filter import TasksFilter

class TasksService(BaseCommandService):
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
    
    
     # =========================
    # ANSWER VALIDATION
    # =========================
    def validate_answer(self, task: Task, answer: str):
        if not task.answer:
            return False, "This task has no answer configured"

        expected = task.answer.strip().lower()
        actual = answer.strip().lower()

        if expected != actual:
            return False, "Wrong answer"

        return True, None
