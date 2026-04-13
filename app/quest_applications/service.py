from app.core.base_service import BaseService
from app.quest_applications.repository import QuestApplicationsRepository
from .model import QuestApplication, QuestApplicationCreate, QuestApplicationUpdate, QuestApplicationPatch
from .filter import QuestApplicationsFilter


class QuestApplicationsService(BaseService):
    repository=QuestApplicationsRepository()
    model=QuestApplication
    create_model=QuestApplicationCreate
    update_model=QuestApplicationUpdate
    patch_model=QuestApplicationPatch
        
        
    def get_redirect_url(self, entity, item):
        return f"/quests/{item.quest_id}"
    

#   ======      filtered lists      ======
    def get_list_by_quest(self, quest_id: int):
        return self.list(
            filters = QuestApplicationsFilter(quest_id=quest_id),
            current_user_id=None
        )
    
    def get_list_by_applicant(self, participant_id: int):
        return self.list(
            filters = QuestApplicationsFilter(participant_id=participant_id),
            current_user_id=None
        )
    


