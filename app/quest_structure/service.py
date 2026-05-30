import logging

from app.core.base_command_service import BaseCommandService
from app.quest_structure.repository import QuestStructureRepository
from .model import (
    QuestStructureItemDTO,
    CreateQuestStructureItemDTO
)


logger = logging.getLogger(__name__)


class QuestStructureService(BaseCommandService):

    repository = QuestStructureRepository()

    model = QuestStructureItemDTO

    create_model = CreateQuestStructureItemDTO
    update_model = QuestStructureItemDTO
    patch_model = QuestStructureItemDTO

    quest_id: int

    # =========================
    # CREATE
    # =========================

    def create(self, data, user_id):

        if data.position is None:
            data.position = self.get_next_position(data.quest_id)

        return super().create(data, user_id)

    # =========================
    # UI HELPERS
    # =========================

    def get_redirect_url(self, entity, item):
        return f"/quests/{item.quest_id}/edit"

    # =========================
    # INTERNAL HELPERS
    # =========================

    def get_next_position(self, quest_id: int):

        links = self.repository.get_by_quest(quest_id)

        return len(links)

    # =========================
    # QUEST TASKS
    # =========================

    def add_task(self, quest_id: int, task_id: int):

        if self.repository.exists(quest_id, task_id):
            logger.warning(
                "Task %s already exists in quest %s",
                task_id,
                quest_id
            )
            return

        next_position = self.get_next_position(quest_id)

        logger.debug(
            "Link task %s to quest %s with order %s",
            task_id,
            quest_id,
            next_position
        )

        self.repository.create({
            "quest_id": quest_id,
            "task_id": task_id,
            "position": next_position
        })

    def remove_task(self, quest_id: int, task_id: int):

        row = self.repository.get_quest_task(
            quest_id,
            task_id
        )

        if not row:
            return

        quest_task = QuestStructureItemDTO(**row)

        deleted_position = quest_task.position

        deleted = self.repository.delete(quest_task.id)

        if not deleted:
            return

        self.shift_positions_down(
            quest_id=quest_id,
            from_position=deleted_position
        )

    # =========================
    # POSITIONS
    # =========================

    def shift_positions_down(
        self,
        quest_id: int,
        from_position: int
    ):

        rows = self.repository.get_by_quest(quest_id)

        for row in rows:

            if row["position"] > from_position:

                self.repository.update_position(
                    id=row["id"],
                    position=row["position"] - 1
                )

    def reorder_tasks(
        self,
        quest_id: int,
        ordered_ids: list[int]
    ):

        items = self.repository.get_by_quest(quest_id)

        # защита: убедимся, что все id принадлежат этому квесту
        valid_ids = {
            item["id"]
            for item in items
        }

        for i in ordered_ids:

            if i not in valid_ids:
                logger.warning(
                    "Invalid quest_task_id in reorder: %s",
                    i
                )
                return

        # обновляем позиции
        for position, quest_task_id in enumerate(ordered_ids):

            self.repository.update_position(
                id=quest_task_id,
                position=position
            )