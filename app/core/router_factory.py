import logging

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from app.core.templates import templates
from pydantic import ValidationError
from app.core.errors import validation_errors_to_dict
from fastapi import UploadFile, File
from app.core.auth import build_user_dependency


logger = logging.getLogger(__name__)


def create_crud_router(
        command_service,
        query_service,   # <-- добавили, пока не используем
        prefix: str,
        require_auth_for_write: bool = True,
        require_auth_for_read: bool = False
    ):

    router = APIRouter(prefix=prefix)

    entity = prefix.removeprefix("/")

    create_model = command_service.create_model
    update_model = command_service.update_model
    patch_model = command_service.patch_model

    get_user_for_read = build_user_dependency(require_auth_for_read)
    get_user_for_write = build_user_dependency(require_auth_for_write)

    # =========================
    # LIST 
    # =========================
    @router.get("/")
    async def list_items(request: Request, user_id = Depends(get_user_for_read)):
        logger.debug("CRUD service for %s: %s", entity, type(command_service))

        items = query_service.list(current_user_id=user_id)

        return templates.TemplateResponse(
            name=f"{entity}/list.html",
            request=request,
            context={
                "items": items,
                "entity": entity
            }
        )

    # =========================
    # CREATE FORM
    # =========================
    @router.get("/add")
    async def add_form(request: Request, user_id = Depends(get_user_for_write)):
        return templates.TemplateResponse(
            name=f"{entity}/add.html",
            request=request,
            context={
                "entity": entity,
                "url": f"/{entity}"
            }
        )

    # =========================
    # CREATE
    # =========================
    @router.post("/")
    async def create_item(request: Request, user_id = Depends(get_user_for_write)):
        form = await request.form()
        data_dict = dict(form)

        try:
            data = create_model(**data_dict)
        except ValidationError as e:
            return templates.TemplateResponse(
                name=f"{entity}/add.html",
                request=request,
                context={
                    "entity": entity,
                    "url": f"/{entity}",
                    "item": data_dict,
                    "errors": validation_errors_to_dict(e)
                }
            )

        new_item = command_service.create(data, user_id)

        redirect_url = command_service.get_redirect_url(entity=entity, item=new_item)

        request.session["flash"] = "New item succesfully created"

        return RedirectResponse(
            url=redirect_url,
            status_code=303
        )

    # =========================
    # DETAILS
    # =========================
    @router.get("/{id}")
    async def details_form(request: Request, id: int, user_id = Depends(get_user_for_read)):
        item = query_service.get(id)

        if not item:
            raise HTTPException(status_code=404)

        return templates.TemplateResponse(
            name=f"{entity}/details.html",
            request=request,
            context={
                "item": item,
                "entity": entity
            }
        )

    # =========================
    # EDIT FORM
    # =========================
    @router.get("/{id}/edit")
    async def edit_form(request: Request, id: int, user_id = Depends(get_user_for_write)):
        item = query_service.get_for_update(id)

        if not item:
            raise HTTPException(status_code=404)

        return templates.TemplateResponse(
            name=f"{entity}/update.html",
            request=request,
            context={
                "item": item,
                "entity": entity,
                "page_title": f"Edit {entity.title()}: {item.title}",
                "submit_label": "Save",
                "url": f"/{entity}/{id}",
                "back_url": f"/{entity}/edit",
                "cancel_url": f"/{entity}/edit",
            }
        )

    # =========================
    # UPDATE
    # =========================
    @router.post("/{id}")
    async def save_item(request: Request, id: int, user_id = Depends(get_user_for_write)):
        form = await request.form()
        data = update_model(**dict(form))

        if user_id:
            command_service.ensure_owner(id, user_id)

        command_service.update(id, data)

        return RedirectResponse(
            url=f"/{entity}/",
            status_code=303
        )

    # =========================
    # IMAGE UPLOAD
    # =========================
    @router.post("/{id}/image")
    async def upload_image(id: int, file: UploadFile = File(...), user_id = Depends(get_user_for_write)):
        if user_id:
            command_service.ensure_owner(id, user_id)

        contents = await file.read()

        url = command_service.upload_image(id, contents)

        command_service.patch(id, patch_model(image_url=url))

        return {"image_url": url}

    return router