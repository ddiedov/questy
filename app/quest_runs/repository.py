import logging

from app.core.repository import BaseRepository


logger = logging.getLogger(__name__)


class QuestRunsRepository(BaseRepository):
    table_name = "quest-runs"
    filter_map = {
        "id": "id",
        "quest_id": "quest_id",
        "participant_id": "participant_id",
        "status": "status",
    }

