from app.core.base_query_service import BaseQueryService
from app.profiles.repository import ProfilesRepository
from app.profiles.model import Profile

class ProfilesQueryService(BaseQueryService):
    repository=ProfilesRepository()
    model=Profile