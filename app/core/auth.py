from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from app.core.supabase import supabase
from typing import Optional, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from supabase_auth.errors import AuthApiError

from app.core.services_factory import get_profiles_service, get_profiles_query_service


# =========================================================
# Dependency for routes
# =========================================================

def build_user_dependency(required: bool) -> Callable:
    async def dependency(request: Request) -> Optional[str]:
        user = getattr(request.state, "user", None)

        if not user:
            if required:
                form = await request.form()
                next_url = form.get("next") or request.url.path

                raise HTTPException(
                    status_code=303,
                    headers={"Location": f"/auth/login?next={next_url}"}
                )
            return None

        return user.id

    return dependency


# =========================================================
# AUTH MIDDLEWARE
# =========================================================

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        request.state.user = None
        request.state.profile = None
        new_session = None

        # -------------------------------------------------
        # 1. AUTH USER
        # -------------------------------------------------
        if access_token:
            try:
                user = supabase.auth.get_user(access_token)
                request.state.user = user.user

            except AuthApiError:
                # try refresh
                if refresh_token:
                    try:
                        new_session = supabase.auth.refresh_session(refresh_token)

                        access_token = new_session.session.access_token
                        user = supabase.auth.get_user(access_token)

                        request.state.user = user.user

                    except Exception:
                        request.state.user = None
                else:
                    request.state.user = None

        # -------------------------------------------------
        # 2. PROFILE (SAFE BOOTSTRAP)
        # -------------------------------------------------
        request.state.profile = None

        if request.state.user:
            try:
                profiles_service = get_profiles_service()
                profiles_query_service = get_profiles_query_service()

                profile = profiles_query_service.get(request.state.user.id)

                # Create a missing profile without breaking the request.
                if not profile:
                    try:
                        profile = profiles_service.create(
                            profiles_service.create_model(
                                id=request.state.user.id,
                                username=None,
                                display_name=None,
                                avatar_url=None
                            ),
                            request.state.user.id
                        )
                    except Exception as e:
                        # Do not break the request.
                        profile = None

                request.state.profile = profile

            except Exception:
                request.state.profile = None


        # =================================================
        # 2.5 ONBOARDING GUARD  
        # =================================================
        if request.state.user and request.state.profile:

            if not getattr(request.state.profile, "username", None):

                # Prevent redirect loops.
                if not request.url.path.startswith("/profiles/onboarding") \
                and not request.url.path.startswith("/auth") \
                and not request.url.path.startswith("/static"):

                    return RedirectResponse(
                        "/profiles/onboarding",
                        status_code=303
                    )

        # -------------------------------------------------
        # 3. RESPONSE
        # -------------------------------------------------
        response = await call_next(request)

        # -------------------------------------------------
        # 4. REFRESH COOKIES IF NEEDED
        # -------------------------------------------------
        if new_session:
            response.set_cookie(
                "access_token",
                new_session.session.access_token,
                httponly=True,
                samesite="lax"
            )
            response.set_cookie(
                "refresh_token",
                new_session.session.refresh_token,
                httponly=True,
                samesite="lax"
            )

        return response
