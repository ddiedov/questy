from fastapi import HTTPException
from app.core.base_service import BaseService
from app.quests.repository import QuestsRepository
from .model import Quest, QuestCreate, QuestUpdate

class QuestsService(BaseService):

    def __init__(self):
        super().__init__(
            repository=QuestsRepository(),
            model=Quest,
            create_model=QuestCreate,
            update_model=QuestUpdate
        )


    def create(self, data: QuestCreate):
        if len(data.title) < 3:
            raise HTTPException(
                status_code=400,
                detail="Title must contain at least 3 characters"
            )

        return super().create(data)
