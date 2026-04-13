from app.core.repository import BaseRepository


class TasksRepository(BaseRepository):
    table_name = "tasks"

    filter_map = {
        "id": "id",
        "author_id": "author_id",
    }