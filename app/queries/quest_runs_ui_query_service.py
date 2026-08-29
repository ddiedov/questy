import logging

from app.core.base_query_service import BaseQueryService
from app.queries.quest_structure_query_service import QuestStructureQueryService
from app.queries.quests_query_service import QuestsQueryService
from app.quest_runs.repository import QuestRunsRepository
from app.quest_runs.ui_model import QuestRun, QuestRunRuntimeView, StepStateBuilder
    

logger = logging.getLogger(__name__)


class QuestRunsUIQueryService(BaseQueryService):
    repository = QuestRunsRepository()
    model = QuestRun

    def __init__(self, 
                 quest_structure_query_service: QuestStructureQueryService, 
                 quests_query_service: QuestsQueryService):
        super().__init__()
        self.quest_structure_query_service = quest_structure_query_service
        self.quests_query_service = quests_query_service

    # =========================
    # RUNTIME VIEW
    # =========================
    def get(self, id: int) -> QuestRunRuntimeView | None:
        run = super().get(id)

        if not run:
            return None

        quest = self.quests_query_service.get_for_runtime_view(run.quest_id)

        if run.current_step_id is None:
            structure = self.quest_structure_query_service.get_by_quest(
                run.quest_id
            )
            completed_steps = (
                structure.steps
                if structure
                else []
            )
            view = QuestRunRuntimeView(
                run=run,
                quest=quest,
                current_step=None,
                completed_steps=completed_steps
            )
            return StepStateBuilder.idle(view)

        current_step = self.quest_structure_query_service.get_step_by_id(
            run.quest_id,
            run.current_step_id
        )

        completed_steps = self.quest_structure_query_service.get_previous_steps(
            run.quest_id,
            run.current_step_id
        )

        view = QuestRunRuntimeView(
            run=run,
            quest=quest,
            current_step=current_step,
            completed_steps=completed_steps
        )

        return StepStateBuilder.idle(view)

    def get_with_state(
        self,
        run_id: int,
        state: str,
        message: str | None = None
    ) -> QuestRunRuntimeView | None:
        view = self.get(run_id)

        if not view:
            return None

        if state == "wrong":
            return StepStateBuilder.wrong(view, message)

        if state == "completed":
            return StepStateBuilder.completed(view)

        return StepStateBuilder.correct_reveal(view)