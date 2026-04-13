from app.core.base_service import BaseService
from app.quest_structure.repository import QuestStructureRepository
from .model import QuestStructure, QuestStructureCreate, QuestStructureUpdate, QuestStructurePatch
from .filter import QuestStructureFilter


class QuestStructureService():
    repository=QuestStructureRepository()
    quest_id: int
#    model=QuestStructure
#    create_model=QuestStructureCreate
#    update_model=QuestStructureUpdate
#    patch_model=QuestStructurePatch

    def __init__(self, tasks_service):
        super().__init__()
        self.tasks_service = tasks_service    
        
#    def get_redirect_url(self, entity, item):
#        return f"/quests/{item.quest_id}"
    

#   ======      filtered lists      ======
    def get_tasks_by_quest(self, quest_id: int, current_user_id=None):
        quest_tasks = self.list(
            filters = QuestStructureFilter(quest_id=quest_id),
            current_user_id=current_user_id
        )
        task_ids = [qt.task_id for qt in quest_tasks]
        task_map = self.tasks_service.get_map_by_ids(task_ids)
        return [
            {
                "task": task_map[qt.task_id],
                "position": qt.position
            }
            for qt in quest_tasks
            if qt.task_id in task_map
        ]

    
        


