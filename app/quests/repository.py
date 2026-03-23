from app.core.repository import BaseRepository


class QuestsRepository(BaseRepository):

    def __init__(self):
        super().__init__("quests")

    filter_map = {
        "id": "id",
        "featured": "featured",
        "author_id": "author_id",
    }