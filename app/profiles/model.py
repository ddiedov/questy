from pydantic import BaseModel


# ===== DTO =====
class CreateProfileDTO(BaseModel):
    id: str


class UpdateProfileDTO(BaseModel):
    username: str
    display_name: str | None = None
    avatar_url: str | None = None
    is_onboarding_completed: bool = True


class PatchProfileDTO(BaseModel):
    username: str | None = None
    display_name: str | None = None
    avatar_url: str | None = None
    is_onboarding_completed: bool | None = None


# ===== SERVICE =====
class Profile(BaseModel):
    id: str
    username: str | None = None
    display_name: str | None = None
    avatar_url: str | None = None
    is_onboarding_completed: bool = False