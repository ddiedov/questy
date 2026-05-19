import logging

from app.core.base_service import BaseService
from app.quest_structure.repository import QuestStructureRepository
from .model import QuestStructure, QuestStructureItem, QuestStructureItemDTO, CreateQuestStructureItemDTO
from .filter import QuestStructureFilter


logger = logging.getLogger(__name__)

class QuestStructureService(BaseService):
    repository=QuestStructureRepository()
    quest_id: int
    model=QuestStructureItemDTO
    create_model=CreateQuestStructureItemDTO
    update_model=QuestStructureItemDTO
    patch_model=QuestStructureItemDTO

    def __init__(self, tasks_service):
        super().__init__()
        self.tasks_service = tasks_service 

    def create(self, data, user_id):
        if data.position is None:
            data.position = self.get_next_position(data.quest_id)
        return super().create(data, user_id)   

    def get_redirect_url(self, entity, item):
        return f"/quests/{item.quest_id}/edit"        

    def get_next_position(self, quest_id: int):
        links = self.repository.get_by_quest(quest_id)
        return len(links)
    
    def get_by_quest(self, quest_id: int, current_user_id=None):
        
        rows = self.repository.get_by_quest(quest_id)

        links = [QuestStructureItemDTO(**row) for row in rows]

        # сортировка для линейного квеста
        links = sorted(links, key=lambda x: x.position or 0)

        task_ids = [link.task_id for link in links]
        task_map = self.tasks_service.get_map_by_ids(task_ids)

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
    
    def add_task(self, quest_id: int, task_id: int):
        if self.repository.exists(quest_id, task_id):
            logger.warning("Task %s already exists in quest %s", task_id, quest_id)
            return
        
        next_position = self.get_next_position(quest_id)
        logger.debug("Link task %s to quest %s with order %s", task_id, quest_id, next_position)
        self.repository.create({
            "quest_id": quest_id,
            "task_id": task_id,
            "position": next_position
        })

    def remove_task(self, quest_id: int, task_id: int):
        quest_task = QuestStructureItemDTO(**self.repository.get_quest_task(quest_id, task_id))

        if not quest_task:
            return

        deleted_position = quest_task.position

        deleted = self.repository.delete(quest_task.id)

        if not deleted:
            return

        self.repository.shift_positions_down(
            quest_id=quest_id,
            from_position=deleted_position
        )
        
    def reorder_tasks(self, quest_id: int, ordered_ids: list[int]):
        items = self.repository.get_by_quest(quest_id)

        # защита: убедимся, что все id принадлежат этому квесту
        valid_ids = {item["id"] for item in items}

        for i in ordered_ids:
            if i not in valid_ids:
                logger.warning("Invalid quest_task_id in reorder: %s", i)
                return

        # обновляем позиции
        for position, quest_task_id in enumerate(ordered_ids):
            self.repository.update(
                id=quest_task_id,
                data={"position": position}
            )

    
        


