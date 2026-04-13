from fastapi import HTTPException
from app.core.base_service import BaseService
from app.quests.repository import QuestsRepository
from .model import Quest, QuestCreate, QuestUpdate, QuestPatch
from .model import QuestForUpdate
from .filter import QuestsFilter

class QuestsService(BaseService):
    repository=QuestsRepository()
    model=Quest
    create_model=QuestCreate
    update_model=QuestUpdate
    patch_model=QuestPatch

    def __init__(self, quest_applications_service, quest_tasks_service):
        super().__init__()
        self.quest_applications_service = quest_applications_service
        self.quest_tasks_service = quest_tasks_service


    def create(self, data: QuestCreate, user_id):
        if len(data.title) < 3:
            raise HTTPException(
                status_code=400,
                detail="Title must contain at least 3 characters"
            )
        return super().create(data, user_id)
    
    def list(self, filters=None, current_user_id=None):
        quests = super().list(filters)

        result = []

        for q in quests:
            item = q.model_dump()

#            application = self.get_user_application(q.id, current_user_id)
#            quest_run = self.get_user_quest_run(q.id, current_user_id)

            item.update({
                "is_author": q.created_by == current_user_id,
                "application_status": None,
#               "application_status": application.status if application else None,
#               "quest_run_id": quest_run.id if quest_run else None,
            })

            result.append(item)

        return result
    

    def get_for_update(self, id: int) -> QuestForUpdate:
        quest = super().get(id)
        if not quest:
            return None
        applications = self.quest_applications_service.get_list_by_quest(quest_id = id)
        tasks = self.get_tasks(quest_id = id, current_user_id=None)
        return QuestForUpdate(
            **quest.model_dump(),
            applications = applications,
            tasks = tasks
        )  

#   ======      filtered lists      ======
    def get_featured(self, current_user_id=None):
        return self.list(
            filters = QuestsFilter(featured=True),
            current_user_id=current_user_id
        )
    

#   ======      quest tasks      ======
    def get_tasks(self, quest_id: int, current_user_id=None):
        quest_tasks = self.quest_tasks_service.get_tasks_by_quest(
            quest_id=quest_id,
            current_user_id=current_user_id
        )
        return quest_tasks