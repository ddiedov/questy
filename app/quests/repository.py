from app.core.repository import BaseRepository


class QuestsRepository(BaseRepository):
    table_name = "quests"

    filter_map = {
        "id": "id",
        "featured": "featured",
        "author_id": "author_id",
    }