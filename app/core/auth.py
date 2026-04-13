from fastapi import Request, HTTPException
from app.core.supabase import supabase
from typing import Optional, Callable


def build_user_dependency(required: bool) -> Callable:
    async def dependency(request: Request) -> Optional[str]:
        user = getattr(request.state, "user", None)

        if not user:
            if required:
                form = await request.form()
                next_url = form.get("next") or request.url.path

                raise HTTPException(
                    status_code=303,
                    headers={"Location": f"/login?next={next_url}"}
                )
            return None

        return user.id

    return dependency


from starlette.middleware.base import BaseHTTPMiddleware
from supabase_auth.errors import AuthApiError

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        request.state.user = None
        new_session = None

        if access_token:
            try:
                user = supabase.auth.get_user(access_token)
                request.state.user = user.user

            except AuthApiError as e:
                if "expired" in str(e) and refresh_token:
                    try:
                        new_session = supabase.auth.refresh_session(refresh_token)
                        access_token = new_session.session.access_token
                        user = supabase.auth.get_user(access_token)
                        request.state.user = user.user
                    except Exception:
                        request.state.user = None
                else:
                    request.state.user = None

        response = await call_next(request)

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