from app.core.base_service import BaseService
from app.quest_applications.repository import QuestApplicationsRepository
from .model import QuestApplication, QuestApplicationCreate, QuestApplicationUpdate, QuestApplicationPatch, StatusType
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
    
    def get_by_quest_and_user(self, quest_id: int, participant_id: str):
        apps = self.list(
            filters=QuestApplicationsFilter(
                quest_id=quest_id,
                participant_id=participant_id
            ),
            current_user_id=None
        )
        return apps[0] if apps else None

#   ======      actions      ======
    def approve(self, application_id: int) -> tuple[int | None, str | None]:
        raw = self.repository.get(application_id)

        if not raw:
            return None, "Application not found"

        application = QuestApplication(**raw)
        
        if application.status != StatusType.NEW:
            return None, "Applications in that status cannot be approved"

        application.status = StatusType.APPROVED
        updated = self.repository.update(
            id=application_id,
            data={"status": application.status}
        )
        if not updated:
            return None, "Failed to update application"
        
        return application.quest_id, None


    def reject(self, application_id: int) -> tuple[int | None, str | None]:
        raw = self.repository.get(application_id)

        if not raw:
            return None, "Application not found"

        application = QuestApplication(**raw)
        
        if application.status != StatusType.NEW:
            return None, "Applications in that status cannot be rejected"

        application.status = StatusType.REJECTED
        updated = self.repository.update(
            id=application_id,
            data={"status": application.status}
        )
        if not updated:
            return None, "Failed to update application"
        
        return application.quest_id, None
    
