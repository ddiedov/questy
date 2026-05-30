import logging

from fastapi import HTTPException
from app.core.base_command_service import BaseCommandService
from app.quests.repository import QuestsRepository
from .model import Quest, QuestCreate, QuestUpdate, QuestPatch



logger = logging.getLogger(__name__)


class QuestsService(BaseCommandService):
    repository=QuestsRepository()
    model=Quest
    create_model=QuestCreate
    update_model=QuestUpdate
    patch_model=QuestPatch

    def create(self, data: QuestCreate, user_id):
        if len(data.title) < 3:
            raise HTTPException(
                status_code=400,
                detail="Title must contain at least 3 characters"
            )
        return super().create(data, user_id)
    
    