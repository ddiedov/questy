import logging

from app.core.base_service import BaseService
from app.profiles.repository import ProfilesRepository
from .model import Profile, CreateProfileDTO, UpdateProfileDTO, PatchProfileDTO


logger = logging.getLogger(__name__)

class ProfilesService(BaseService):
    repository=ProfilesRepository()
    
    model=Profile
    create_model=CreateProfileDTO
    update_model=UpdateProfileDTO
    patch_model=PatchProfileDTO

    with_owner = False

    def create(self, data, user_id=None):
        payload = data.model_dump()

        row = self.repository.create(payload)
        return self.model(**row[0])