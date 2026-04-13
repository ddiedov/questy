from app.core.repository import BaseRepository


class QuestStructureRepository(BaseRepository):
    table_name = "quest-structure"

    filter_map = {
        "id": "id",
        "quest_id": "quest_id",
        "task_id": "task_id",
    }