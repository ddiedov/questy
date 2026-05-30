from app.core.base_command_service import BaseCommandService
from app.quest_applications.repository import QuestApplicationsRepository
from .model import QuestApplication, QuestApplicationCreate, QuestApplicationUpdate, QuestApplicationPatch, StatusType



class QuestApplicationsService(BaseCommandService):
    repository=QuestApplicationsRepository()
    model=QuestApplication
    create_model=QuestApplicationCreate
    update_model=QuestApplicationUpdate
    patch_model=QuestApplicationPatch

               
        
    def get_redirect_url(self, entity, item):
        return f"/quests/{item.quest_id}"
    


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
    
