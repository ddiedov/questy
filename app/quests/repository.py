from app.core.repository import BaseRepository


class QuestsRepository(BaseRepository):

    def __init__(self):
        super().__init__("quests")