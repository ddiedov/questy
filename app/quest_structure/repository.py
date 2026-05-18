import logging

from app.core.repository import BaseRepository
from app.core.supabase import supabase
from postgrest.exceptions import APIError
from typing import List


logger = logging.getLogger(__name__)


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
        except APIError:
            logger.exception("[Repository:%s] ERROR", self.prefix)
            return []
        
    def get_quest_task(self, quest_id: int, task_id: int):
        try:
            return (
                self.table
                .select("*")
                .eq("quest_id", quest_id)
                .eq("task_id", task_id)
                .maybe_single()
                .execute()
                .data
            )
        except APIError:
            logger.exception("[Repository:%s] ERROR", self.prefix)
            return None

    def exists(self, quest_id: int, task_id: int):
        try:
            row = (
                self.table
                .select("id")
                .eq("quest_id", quest_id)
                .eq("task_id", task_id)
                .maybe_single()
                .execute()
                .data
            )

            return row is not None

        except APIError:
            logger.exception("[Repository:%s] EXISTS ERROR", self.prefix)
            return False

    def shift_positions_down(self, quest_id: int, from_position: int):
        try:
            response = (
                self.table
                .select("id, position")
                .eq("quest_id", quest_id)
                .gt("position", from_position)
                .execute()
            )

            rows = response.data or []

            for row in rows:
                self.table.update({
                    "position": row["position"] - 1
                }).eq("id", row["id"]).execute()

        except APIError:
            logger.exception("[Repository:%s] SHIFT ERROR", self.prefix)