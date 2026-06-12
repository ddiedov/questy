import logging

from app.core.repository import BaseRepository
from postgrest.exceptions import APIError


logger = logging.getLogger(__name__)


class QuestRunsRepository(BaseRepository):
    table_name = "quest-runs"
    filter_map = {
        "id": "id",
        "quest_id": "quest_id",
        "participant_id": "participant_id",
        "status": "status",
    }

    def exists(self, quest_id: int, participant_id: str):
        if not participant_id:
            return False
        try:
            response = (
                self.table
                .select("id")
                .eq("quest_id", quest_id)
                .eq("participant_id", participant_id)
                .limit(1)
                .execute()
            )

            if not response:
                return False

            if not hasattr(response, "data"):
                return False

            return response.data is not None

        except APIError:
            logger.exception("[Repository:%s] EXISTS ERROR", self.prefix)
            raise

