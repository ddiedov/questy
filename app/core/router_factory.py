from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from app.core.templates import templates
from fastapi import UploadFile, File
from app.core.auth import build_user_dependency


def create_crud_router(
        service,
        prefix: str,
        require_auth_for_write: bool = True,
        require_auth_for_read: bool = False
    ):

    
    router = APIRouter(prefix=prefix)

    entity = prefix.removeprefix("/")

    create_model = service.create_model
    update_model = service.update_model
    patch_model = service.patch_model

    get_user_for_read = build_user_dependency(require_auth_for_read)
    get_user_for_write = build_user_dependency(require_auth_for_write)

    @router.get("/")
    async def list_items(request: Request, user_id = Depends(get_user_for_read)):
        print("SERVICE:", type(service))
        items = service.list(current_user_id = user_id)
 
        return templates.TemplateResponse(
            f"{entity}/list.html",
            {
                "request": request,
                "items": items,
                "entity": entity
            }
        )

    @router.get("/add")
    async def add_form(request: Request, user_id = Depends(get_user_for_write)):
        return templates.TemplateResponse(
            f"{entity}/add.html",
            {
                "request": request,
                "entity": entity,
                "url": f"/{entity}"
            }
        )

    @router.post("/")
    async def create_item(request: Request, user_id = Depends(get_user_for_write)):
        form = await request.form()
        data_dict = dict(form)
        data = create_model(**data_dict)

        new_item = service.create(data, user_id)
    
        redirect_url = service.get_redirect_url(entity=entity, item=new_item)
        
        request.session["flash"] = "New item succesfully created"

        return RedirectResponse(
            url=redirect_url,
            status_code=303
        )

    @router.get("/{id}")
    async def details_form(request: Request, id: int, user_id = Depends(get_user_for_read)):
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

    @router.get("/{id}/edit")
    async def edit_form(request: Request, id: int, user_id = Depends(get_user_for_write)):
        item = service.get_for_update(id)
        if not item:
            raise HTTPException(status_code=404)

        return templates.TemplateResponse(
            f"{entity}/update.html",
            {
                "request": request,
                "item": item,
                "entity": entity
            }
        )

    @router.post("/{id}")
    async def save_item(request: Request, id: int, user_id = Depends(get_user_for_write)):
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
    async def upload_image(id: int, file: UploadFile = File(...), user_id = Depends(get_user_for_write)):
        if user_id:
            service.ensure_owner(id, user_id)
        contents = await file.read()
        
        url = service.upload_image(id, contents)
        service.patch(id, patch_model(image_url = url))
        return {"image_url": url}

    return router