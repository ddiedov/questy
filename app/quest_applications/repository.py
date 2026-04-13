from app.core.repository import BaseRepository


class QuestApplicationsRepository(BaseRepository):
    table_name = "quest-applications"

    filter_map = {
        "id": "id",
        "quest_id": "quest_id",
        "participant_id": "participant_id",
    }