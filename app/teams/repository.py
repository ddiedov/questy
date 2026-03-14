from app.core.repository import BaseRepository


class TeamsRepository(BaseRepository):

    def __init__(self):
        super().__init__("teams")