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

        structure = self.quest_structure_query_service.get_by_quest(run.quest_id)
        tasks = structure.tasks if structure else []

        if not tasks:
            return QuestRunRuntimeView(
                run=run,
                current_task=None,
                previous_tasks=[]
            )

        current_index = None

        if run.current_task_id is not None:
            current_index = next(
                (i for i, t in enumerate(tasks) if t.id == run.current_task_id),
                None
            )

        if current_index is None:
            current_index = 0

        current_task = tasks[current_index]
        previous_tasks = tasks[:current_index]

        return QuestRunRuntimeView(
            run=run,
            current_task=current_task,
            previous_tasks=previous_tasks
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