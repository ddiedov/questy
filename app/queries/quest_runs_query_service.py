import logging

from app.core.base_query_service import BaseQueryService
from app.quest_runs.repository import QuestRunsRepository
from app.quest_runs.model import (
    QuestRun,
    QuestRunRuntimeView,
    QuestRunStatusType
)
from app.quest_runs.filter import QuestRunsFilter

logger = logging.getLogger(__name__)


class QuestRunsQueryService(BaseQueryService):
    repository = QuestRunsRepository()
    model = QuestRun

    def __init__(self, quest_structure_query_service, tasks_service):
        super().__init__()
        self.quest_structure_query_service = quest_structure_query_service
        self.tasks_service = tasks_service

    # =========================
    # RUNTIME VIEW
    # =========================
    def get(self, id: int) -> QuestRunRuntimeView | None:
        run = super().get(id)

        if not run:
            return None

        if run.current_step_id is None:
            return QuestRunRuntimeView(
                run=run,
                current_step=None,
                previous_steps=[]
            )

        current_step = (
            self.quest_structure_query_service.get_step_by_id(
                run.quest_id,
                run.current_step_id
            )
        )

        previous_steps = (
            self.quest_structure_query_service.get_previous_steps(
                run.quest_id,
                run.current_step_id
            )
        )

        return QuestRunRuntimeView(
            run=run,
            current_step=current_step,
            previous_steps=previous_steps
        )

    # =========================
    # ACTIVE RUN
    # =========================
    def get_active_run(self, quest_id: int, participant_id: str):
        runs = super().list(
            filters=QuestRunsFilter(
                quest_id=quest_id,
                participant_id=participant_id,
                status=QuestRunStatusType.ACTIVE.value
            )
        )

        return runs[0] if runs else None

    def get_run_state(self, quest_id: int, participant_id: str):
        active = self.get_active_run(quest_id, participant_id)

        if active:
            return {
                "state": "resume",
                "run_id": active.id
            }

        return {
            "state": "start",
            "run_id": None
        }