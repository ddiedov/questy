import logging

from app.core.base_query_service import BaseQueryService
from app.quest_applications.repository import QuestApplicationsRepository
from app.quest_applications.model import QuestApplication
from app.quest_applications.filter import QuestApplicationsFilter

logger = logging.getLogger(__name__)

class QuestApplicationsQueryService(BaseQueryService):
    repository = QuestApplicationsRepository()
    model = QuestApplication

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
    
    def get_by_quest_and_user(self, quest_id: int, participant_id: str):
        apps = self.list(
            filters=QuestApplicationsFilter(
                quest_id=quest_id,
                participant_id=participant_id
            ),
            current_user_id=None
        )
        return apps[0] if apps else None
    
    def has_applications(self, quest_id: int, participant_id: str) -> bool:
        apps = self.list(
            filters=QuestApplicationsFilter(
                quest_id=quest_id,
                participant_id=participant_id
            ),
            current_user_id=None
        )
        return bool(apps)

    def has_approved_application(
        self,
        quest_id: int,
        participant_id: str
    ) -> bool:
        
        apps = self.list(
            filters=QuestApplicationsFilter(
                quest_id=quest_id,
                participant_id=participant_id,
                status="approved"
            ),
            current_user_id=None
        )

        return bool(apps)
    
    def has_pending_application(
        self,
        quest_id: int,
        participant_id: str
    ) -> bool:
        
        apps = self.list(
            filters=QuestApplicationsFilter(
                quest_id=quest_id,
                participant_id=participant_id,
                status="new"
            ),
            current_user_id=None
        )

        return bool(apps)