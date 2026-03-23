from app.core.repository import BaseRepository


class QuestApplicationsRepository(BaseRepository):

    def __init__(self):
        super().__init__("quest_applications")

    filter_map = {
        "id": "id",
        "quest_id": "quest_id",
        "participant_id": "participant_id",
    }