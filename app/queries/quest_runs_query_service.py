import logging

from app.core.base_query_service import BaseQueryService
from app.queries.quest_structure_query_service import QuestStructureQueryService
from app.quest_runs.repository import QuestRunsRepository
from app.quest_runs.model import (
    QuestRun,
    QuestRunStatusType
)
from app.quest_runs.filter import QuestRunsFilter
from app.tasks.service import TasksService

logger = logging.getLogger(__name__)


class QuestRunsQueryService(BaseQueryService):
    repository = QuestRunsRepository()
    model = QuestRun

    def __init__(self, 
                 quest_structure_query_service: QuestStructureQueryService,
                 tasks_service: TasksService):
        super().__init__()
        self.quest_structure_query_service = quest_structure_query_service
        self.tasks_service = tasks_service
    

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
    
    def has_runs(self, quest_id: int, participant_id: str):
        return self.repository.exists(quest_id, participant_id)
    