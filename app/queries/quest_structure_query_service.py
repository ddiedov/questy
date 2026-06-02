import logging

from app.core.base_query_service import BaseQueryService
from app.quest_structure.repository import QuestStructureRepository

from app.quest_structure.model import (
    QuestStructure,
    QuestStep,
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

        # Sort steps for a linear quest.
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
            QuestStep(
                id=link.id,
                task=task_map[link.task_id],
                position=link.position
            )
            for link in links
            if link.task_id in task_map
        ]

        return QuestStructure(
            quest_id=quest_id,
            steps=items
        )
    
    # =========================
    # QUEST TASKS
    # =========================

    def get_first_step(self, quest_id: int):
        structure = self.get_by_quest(quest_id)

        if not structure or not structure.steps:
            return None

        return structure.steps[0]
    

    def get_step_position(
        self,
        quest_id: int,
        step_id: int
    ):
        structure = self.get_by_quest(quest_id)

        if not structure:
            return None

        return next(
            (
                i
                for i, step in enumerate(structure.steps)
                if step.id == step_id
            ),
            None
        )
    

    def get_step_by_id(
        self,
        quest_id: int,
        step_id: int
    ):
        position = self.get_step_position(
            quest_id,
            step_id
        )

        if position is None:
            return None

        structure = self.get_by_quest(quest_id)

        return structure.steps[position]
    

    def get_previous_steps(
        self,
        quest_id: int,
        step_id: int
    ):
        position = self.get_step_position(
            quest_id,
            step_id
        )

        if position is None:
            return []

        structure = self.get_by_quest(quest_id)

        return structure.steps[:position]
