from app.core.base_command_service import BaseCommandService
from app.quests.repository import QuestsRepository
from .model import Quest, QuestCreate, QuestUpdate, QuestPatch


class QuestsService(BaseCommandService):
    repository=QuestsRepository()
    model=Quest
    create_model=QuestCreate
    update_model=QuestUpdate
    patch_model=QuestPatch
    