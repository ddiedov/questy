import logging

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse

from app.core.templates import templates
from app.core.services_factory import get_profiles_service

logger = logging.getLogger(__name__)

# =========================================================
# ONBOARDING ROUTER
# =========================================================

router = APIRouter(prefix="/profiles")


# -------------------------
# ONBOARDING PAGE
# -------------------------
@router.get("/onboarding")
async def onboarding(request: Request):

    return templates.TemplateResponse(
        name="profiles/me.html",
        request=request,
        context={
            "profile": request.state.profile
        }
    )

# -------------------------
# ONBOARDING SUBMIT
# -------------------------
@router.post("/onboarding")
async def onboarding_submit(
    request: Request,
    username: str = Form(...),
    display_name: str = Form("")
):
    user = request.state.user

    profiles_service = get_profiles_service()

    profiles_service.update(
        user.id,
        profiles_service.update_model(
            username=username,
            display_name=display_name,
            is_onboarding_completed=True
        )
    )

    return RedirectResponse("/", status_code=303)

# -------------------------
# PROFILE
# -------------------------
@router.get("/me")
async def profile_me(request: Request):

    return templates.TemplateResponse(
        name="profiles/me.html",
        request=request,
        context={
            "profile": request.state.profile
        }
    )

@router.post("/me")
async def profile_update(
    request: Request,
    username: str = Form(...),
    display_name: str = Form(""),
    avatar_url: str = Form(None)
):
    user = request.state.user

    profiles_service = get_profiles_service()

    profiles_service.update(
        user.id,
        profiles_service.update_model(
            username=username,
            display_name=display_name,
            avatar_url=avatar_url
        )
    )
    request.session["flash"] = "Profile updated"
    return RedirectResponse("/profiles/me", status_code=303)