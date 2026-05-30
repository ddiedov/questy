import logging

from app.core.base_query_service import BaseQueryService
from app.quest_structure.repository import QuestStructureRepository

from app.quest_structure.model import (
    QuestStructure,
    QuestStructureItem,
    QuestStructureItemDTO
)


logger = logging.getLogger(__name__)


class QuestStructureQueryService(BaseQueryService):
    repository = QuestStructureRepository()
    model = QuestStructureItemDTO

    def __init__(self, tasks_query_service):
        super().__init__()
        self.tasks_query_service = tasks_query_service

    # =========================
    # QUEST STRUCTURE
    # =========================

    def get_by_quest(
        self,
        quest_id: int,
        current_user_id=None
    ):

        rows = self.repository.get_by_quest(quest_id)

        links = [
            QuestStructureItemDTO(**row)
            for row in rows
        ]

        # сортировка для линейного квеста
        links = sorted(
            links,
            key=lambda x: x.position or 0
        )

        task_ids = [
            link.task_id
            for link in links
        ]

        task_map = self.tasks_query_service.get_map_by_ids(
            task_ids
        )

        items = [
            QuestStructureItem(
                id=link.id,
                task=task_map[link.task_id],
                position=link.position
            )
            for link in links
            if link.task_id in task_map
        ]

        return QuestStructure(
            quest_id=quest_id,
            tasks=items
        )