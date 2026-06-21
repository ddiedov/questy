import logging

from app.core.base_query_service import BaseQueryService
from app.quest_runs.repository import QuestRunsRepository
from app.quest_runs.ui_model import QuestRun, QuestRunRuntimeView, StepStateBuilder
    

logger = logging.getLogger(__name__)


class QuestRunsUIQueryService(BaseQueryService):
    repository = QuestRunsRepository()
    model = QuestRun

    def __init__(self, quest_structure_query_service, tasks_service, quests_query_service):
        super().__init__()
        self.quest_structure_query_service = quest_structure_query_service
        self.tasks_service = tasks_service
        self.quests_query_service = quests_query_service

    # =========================
    # RUNTIME VIEW
    # =========================
    def get(self, id: int) -> StepStateBuilder | None:
        run = super().get(id)

        if not run:
            return None

        quest = self.quests_query_service.get_for_runtime_view(run.quest_id)

        if run.current_step_id is None:
            structure = self.quest_structure_query_service.get_by_quest(
                run.quest_id
            )
            previous_steps = (
                structure.steps
                if structure
                else []
            )
            view = QuestRunRuntimeView(
                run=run,
                quest=quest,
                current_step=None,
                previous_steps=previous_steps
            )
            return StepStateBuilder.idle(view)

        current_step = self.quest_structure_query_service.get_step_by_id(
            run.quest_id,
            run.current_step_id
        )

        previous_steps = self.quest_structure_query_service.get_previous_steps(
            run.quest_id,
            run.current_step_id
        )

        view = QuestRunRuntimeView(
            run=run,
            quest=quest,
            current_step=current_step,
            previous_steps=previous_steps
        )

        return StepStateBuilder.idle(view)