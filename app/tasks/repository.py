from app.core.repository import BaseRepository


class TasksRepository(BaseRepository):
    table_name = "tasks"

    filter_map = {
        "id": "id",
        "created_by": "created_by",
    }