import logging

from app.core.base_query_service import BaseQueryService
from app.quests.filter import QuestsFilter
from app.quests.repository import QuestsRepository
from app.quests.model import Quest
from app.quests.model import QuestState, QuestForView, QuestForUpdate, QuestForRuntimeView
from app.quest_applications.model import StatusType, QuestApplicationView

logger = logging.getLogger(__name__)

class QuestsQueryService(BaseQueryService):
    repository=QuestsRepository()
    model=Quest

    def __init__(
        self,
        quest_applications_query_service,
        quest_runs_query_service,
        quest_structure_query_service,
        profiles_query_service
    ):
        self.quest_applications_query_service = quest_applications_query_service
        self.quest_runs_query_service = quest_runs_query_service
        self.quest_structure_query_service = quest_structure_query_service
        self.profiles_query_service = profiles_query_service

    def can_start(self, quest_id: int, user_id: str) -> bool:
        quest = super().get(quest_id)
        state = self.get_ui_state(quest, user_id)
        return state.state in ("start", "start_again")

    def get_ui_state(self, quest: Quest, user_id: str) -> QuestState:

        active = self.quest_runs_query_service.get_active_run(
            quest.id,
            user_id
        )

        if active:
            return QuestState(
                state="resume",
                run_id=active.id
            )

        has_runs = self.quest_runs_query_service.has_runs(quest.id, user_id)
        has_approved = self.quest_applications_query_service.has_approved_application(quest.id, user_id)
        has_pending = self.quest_applications_query_service.has_pending_application(quest.id, user_id)
        allow_replays = (quest.allow_replays if quest else False)

        # ----------------------------------
        # User has already completed runs
        # ----------------------------------
        if has_runs:

            if allow_replays:
                return QuestState(
                    state="start_again",
                    run_id=None
                )

            if has_approved:
                return QuestState(
                    state="start_again",
                    run_id=None
                )

            if has_pending:
                return QuestState(
                    state="pending_approval",
                    run_id=None
                )

            return QuestState(
                state="apply_again",
                run_id=None
            )

        # ----------------------------------
        # User never had runs
        # ----------------------------------

        if has_approved:
            return QuestState(
                state="start",
                run_id=None
            )

        if has_pending:
            return QuestState(
                state="pending_approval",
                run_id=None
            )

        return QuestState(
            state="apply",
            run_id=None
        )


    def list(self, filters=None, current_user_id=None):
        quests = super().list(filters)

        result = []

        for q in quests:
            item = q.model_dump()

            quest_run_state = self.get_ui_state(q, current_user_id)

            item.update({
                "is_author": q.created_by == current_user_id,
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
    

    def get_for_view(self, id: int, current_user_id: str | None = None) -> QuestForView | None:
        quest = super().get(id)

        if not quest:
            return None

        # -----------------------------
        # quest additional attributes - quest run state
        # -----------------------------
        quest_run_state = self.get_ui_state(
            quest,
            current_user_id
        )

        # -----------------------------
        # extend quest with additional attributes
        # -----------------------------
        return QuestForView(
            **quest.model_dump(),
            is_author=(
                current_user_id is not None
                and quest.created_by == current_user_id
            ),
            state=quest_run_state,
        )

    
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