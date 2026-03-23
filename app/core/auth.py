from fastapi import Request, HTTPException
from app.core.supabase import supabase


def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=303,
            headers={"Location": f"/login?next={request.url.path}"}
        )

    user = supabase.auth.get_user(token)

    if not user or not user.user:
        raise HTTPException(401, "Invalid token")

    return user.user.id