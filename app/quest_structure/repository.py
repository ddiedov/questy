from app.core.repository import BaseRepository
from app.core.supabase import supabase
from postgrest.exceptions import APIError
from typing import List


class QuestStructureRepository(BaseRepository):
    table_name = "quest-structures"
    filter_map = {
        "id": "id",
        "quest_id": "quest_id",
        "task_id": "task_id",
    }

    def get_by_quest(self, quest_id: int):
        try:
            response = self.table.select("*").eq("quest_id", quest_id).execute()
            return response.data or []
        except APIError as e:
            print(f"[Repository:{self.prefix}] ERROR:", e)
            return []