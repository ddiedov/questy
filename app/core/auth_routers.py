from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from app.core.supabase import supabase
from app.core.templates import templates
from pydantic import BaseModel

from app.core.services_factory import get_profiles_service

from config import BASE_URL
from app.core.helpers import safe_next_url


class SessionDTO(BaseModel):
    access_token: str
    refresh_token: str
    next: str = "/"


def create_auth_router(prefix: str):
        
    router = APIRouter(prefix=prefix)
    
    # -------------------------
    # SIGNUP
    # -------------------------
    @router.get("/signup", response_class=HTMLResponse)
    async def signup_form(request: Request):
        return templates.TemplateResponse(
            name="auth/signup.html",
            request=request, 
            context={}
        )            

    @router.post("/signup")
    async def signup(
        request: Request,
        email: str = Form(...), 
        password: str = Form(...),
        next: str = Form("/")
    ):
        supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {
                    "email_redirect_to": f"{BASE_URL}/auth/callback?next={safe_next_url(next)}"
                }
            }
        )

        return templates.TemplateResponse(
            name="auth/check_email.html",
            request=request,
            context={}
        )


    # -------------------------
    # CALLBACK
    # -------------------------
    @router.get("/callback")
    async def auth_callback(request: Request):
        return templates.TemplateResponse(
            name="auth/auth_callback.html",
            request=request,
            context={}
        )


    # -------------------------
    # SESSION
    # -------------------------
    @router.post("/session")
    async def create_session(data: SessionDTO):

        redirect_to = safe_next_url(data.next)

        response = JSONResponse({
            "redirect_to": redirect_to
        })

        response.set_cookie(
            "access_token",
            data.access_token,
            httponly=True,
            samesite="lax"
        )

        response.set_cookie(
            "refresh_token",
            data.refresh_token,
            httponly=True,
            samesite="lax"
        )

        return response

    # -------------------------
    # FORGOT PASSWORD
    # -------------------------
    @router.get("/forgot-password")
    def forgot_password(request: Request):
        return templates.TemplateResponse(
            name="auth/forgot_password.html",
            request=request,
            context={}
        )


    # -------------------------
    # LOGIN
    # -------------------------
    @router.get("/login", response_class=HTMLResponse)
    async def login_form(request: Request):
        return templates.TemplateResponse(
            name="auth/login.html",
            request=request,
            context={}
        )


    @router.post("/login")
    async def login(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        next: str = Form("/")
    ):
        try:
            session = supabase.auth.sign_in_with_password({"email": email, "password": password})
        except Exception as e:
            return {"error": str(e)}

        access_token = session.session.access_token
        refresh_token = session.session.refresh_token
        if not access_token:
            raise HTTPException(401, "Login failed")

        response = RedirectResponse(url=safe_next_url(next), status_code=303)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="lax"
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="lax"
        )
        return response


    # -------------------------
    # LOGOUT
    # -------------------------
    @router.get("/logout")
    def logout():
        response = RedirectResponse("/")
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    

    return router
