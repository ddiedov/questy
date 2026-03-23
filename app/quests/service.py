from fastapi import HTTPException
from app.core.base_service import BaseService
from app.quests.repository import QuestsRepository
from .model import Quest, QuestCreate, QuestUpdate, QuestPatch
from .filter import QuestsFilter

class QuestsService(BaseService):

    def __init__(self):
        super().__init__(
            repository=QuestsRepository(),
            model=Quest,
            create_model=QuestCreate,
            update_model=QuestUpdate,
            patch_model=QuestPatch
        )

    def create(self, data: QuestCreate):
        if len(data.title) < 3:
            raise HTTPException(
                status_code=400,
                detail="Title must contain at least 3 characters"
            )
        return super().create(data)
    
    def list(self, current_user_id=None):
        quests = super().list()

        result = []
        for q in quests:
#            application = self.get_user_application(q.id, current_user_id)
#            quest_run = self.get_user_quest_run(q.id, current_user_id)

            result.append({
                "id": q.id,
                "title": q.title,
                "description": q.description,
                "image_url": q.image_url,
                "is_author": q.author_id == current_user_id,
 #               "application_status": application.status if application else None,
 #               "quest_run_id": quest_run.id if quest_run else None,
            })
        return result

    def get_featured(self):
        return self.list(QuestsFilter(featured=True))