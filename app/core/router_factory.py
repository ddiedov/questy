from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from app.core.templates import templates
from fastapi import UploadFile, File
from app.core.auth import get_current_user


def create_crud_router(
        service,
        prefix: str,
        require_auth_for_write: bool = True,
        require_auth_for_read: bool = False
    ):

    dependencies = []
    if require_auth_for_read or require_auth_for_write:
        dependencies.append(Depends(get_current_user))

#    router = APIRouter(prefix=prefix, dependencies=dependencies)
    router = APIRouter(prefix=prefix)

    entity = prefix.removeprefix("/")

    create_model = service.create_model
    update_model = service.update_model
    patch_model = service.patch_model

    def auth_dependency(user_id=Depends(get_current_user)):
        if require_auth_for_write:
            return user_id
        return None

    @router.get("/")
    async def list_items(request: Request):
        items = service.list()
 
        return templates.TemplateResponse(
            f"{entity}/list.html",
            {
                "request": request,
                "items": items,
                "entity": entity
            }
        )

    @router.get("/add")
    async def add_form(request: Request, user_id = Depends(auth_dependency)):
        return templates.TemplateResponse(
            f"{entity}/add.html",
            {
                "request": request,
                "entity": entity,
                "url": f"/{entity}"
            }
        )

    @router.post("/")
    async def create_item(request: Request, user_id = Depends(auth_dependency)):
        form = await request.form()
        data = create_model(**dict(form))

        new_item = service.create(data)
        return RedirectResponse(
            url=f"/{entity}/{new_item.id}",
            status_code=303
        )

    @router.get("/{id}")
    async def details_form(request: Request, id: int, user_id = Depends(auth_dependency)):
        item = service.get(id)
        if not item:
            raise HTTPException(status_code=404)

        return templates.TemplateResponse(
            f"{entity}/details.html",
            {
                "request": request,
                "item": item,
                "entity": entity
            }
        )

    @router.post("/{id}")
    async def save_item(request: Request, id: int, user_id = Depends(auth_dependency)):
        form = await request.form()
        data = update_model(**dict(form))

        if user_id:
            service.ensure_owner(id, user_id)
        service.update(id, data)
        return RedirectResponse(
            url=f"/{entity}/",
            status_code=303
        )
    
    @router.post("/{id}/image")
    async def upload_image(id: int, file: UploadFile = File(...), user_id = Depends(auth_dependency)):
        if user_id:
            service.ensure_owner(id, user_id)
        contents = await file.read()
        
        url = service.upload_image(id, contents)
        service.patch(id, patch_model(image_url = url))
        return {"image_url": url}

    return router