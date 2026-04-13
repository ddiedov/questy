from app.core.repository import BaseRepository


class TeamsRepository(BaseRepository):
    table_name = "teams"

    filter_map = {
        "owner_id": "owner_id",
        "member_id": "member_id",
    }