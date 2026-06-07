import logging

from app.core.base_query_service import BaseQueryService
from app.quests.filter import QuestsFilter
from app.quests.repository import QuestsRepository
from app.quests.model import Quest
from app.quests.model import QuestForView, QuestForUpdate, QuestForRuntimeView
from app.quest_applications.model import StatusType, QuestApplicationView

logger = logging.getLogger(__name__)

class QuestsQueryService(BaseQueryService):
    repository=QuestsRepository()
    model=Quest

    def __init__(
        self,
        #quests_service,
        quest_applications_query_service,
        quest_runs_query_service,
        quest_structure_query_service,
        profiles_query_service
    ):
        #self.quests_service = quests_service
        self.quest_applications_query_service = quest_applications_query_service
        self.quest_runs_query_service = quest_runs_query_service
        self.quest_structure_query_service = quest_structure_query_service
        self.profiles_query_service = profiles_query_service


    def list(self, filters=None, current_user_id=None):
        quests = super().list(filters)

        result = []

        for q in quests:
            item = q.model_dump()

            application = None
            if current_user_id:
                application = self.quest_applications_query_service.get_by_quest_and_user(
                    quest_id=q.id,
                    participant_id=current_user_id
                )

            quest_run_state = self.quest_runs_query_service.get_run_state(q.id, current_user_id)

            item.update({
                "is_author": q.created_by == current_user_id,
                "application_status": application.status if application else None,
                "state": quest_run_state if quest_run_state else None,
            })

            result.append(item)

        return result
    
#   ======      filtered lists      ======
    def get_featured(self, current_user_id=None):
        return self.list(
            filters = QuestsFilter(featured=True),
            current_user_id=current_user_id
        )
    

#   ======      quest steps      ======
    def get_steps(self, quest_id: int, current_user_id=None):
        quest_structure = self.quest_structure_query_service.get_by_quest(
            quest_id=quest_id,
            current_user_id=current_user_id
        )
        return quest_structure.steps
    

    def get_for_view(self, id: int, current_user_id: str | None = None) -> QuestForView:
        quest = super().get(id)

        if not quest:
            return None

        item = quest.model_dump()

        # -----------------------------
        # steps (same as list-style enrichment)
        # -----------------------------
        steps = self.get_steps(
            quest_id=id,
            current_user_id=current_user_id
        )

        # -----------------------------
        # default enriched fields
        # -----------------------------
        application = None

        if current_user_id:
            application = (
                self.quest_applications_query_service
                .get_by_quest_and_user(
                    quest_id=id,
                    participant_id=current_user_id
                )
            )

        quest_run_state = self.quest_runs_query_service.get_run_state(id, current_user_id)

        # -----------------------------
        # extend item (same style as list)
        # -----------------------------
        item.update({
            "is_author": (
                current_user_id is not None
                and quest.created_by == current_user_id
            ),
            "application_status": application.status if application else None,
            "state": quest_run_state if quest_run_state else None,
            "steps": steps,
        })

        return QuestForView(**item)

    
    def get_for_update(self, id: int) -> QuestForUpdate:
        quest = super().get(id)
        if not quest:
            return None
        applications = self.quest_applications_query_service.get_list_by_quest(quest_id = id)

        enriched_applications = []
        for app in applications:
            profile = self.profiles_query_service.get(app.participant_id)
            enriched_applications.append(
                QuestApplicationView(
                    **app.model_dump(),
                    profile=profile
                )
            )

        new_applications = [
            app for app in enriched_applications
            if app.status == StatusType.NEW
        ]
        steps = self.get_steps(quest_id = id, current_user_id=None)
        logger.debug("Quest %s steps for update: %s", id, steps)
        return QuestForUpdate(
            **quest.model_dump(),
            applications = enriched_applications,
            new_applications = new_applications,
            steps = steps
        )  

    def get_for_runtime_view(self, id: int, current_user_id: str | None = None) -> QuestForRuntimeView:
        quest = super().get(id)

        if not quest:
            return None

        return QuestForRuntimeView(
            id=quest.id,
            title=quest.title,
            description=quest.description,
            image_url=quest.image_url
        )