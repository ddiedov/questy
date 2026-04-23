from app.core.base_service import BaseService
from app.quest_structure.repository import QuestStructureRepository
from .model import QuestStructure, QuestStructureItem, QuestStructureItemDTO, CreateQuestStructureItemDTO
from .filter import QuestStructureFilter


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
        next_position = self.get_next_position(quest_id)

        self.repository.create({
            "quest_id": quest_id,
            "task_id": task_id,
            "position": next_position
        })

    def remove_task(self, quest_id: int, task_id: int):
        # пока можно просто delete через repo (если есть)
        pass
        

    
        


