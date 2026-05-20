import logging

from app.core.repository import BaseRepository


logger = logging.getLogger(__name__)


class ProfilesRepository(BaseRepository):
    table_name = "profiles"

    filter_map = {        
    }