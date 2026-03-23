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

    def get_featured(self):
        return self.list(QuestsFilter(featured=True))