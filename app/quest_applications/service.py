from fastapi import HTTPException
from app.core.base_service import BaseService
from app.quest_applications.repository import QuestApplicationsRepository
from .model import QuestApplication, QuestApplicationCreate, QuestApplicationUpdate, QuestApplicationPatch
# from .filter import QuestsApplicationsFilter

class QuestApplicationsService(BaseService):

    def __init__(self):
        super().__init__(
            repository=QuestApplicationsRepository(),
            model=QuestApplication,
            create_model=QuestApplicationCreate,
            update_model=QuestApplicationUpdate,
            patch_model=QuestApplicationPatch
        )
