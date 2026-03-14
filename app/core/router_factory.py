from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from app.core.templates import templates


def create_crud_router(service, prefix: str):

    router = APIRouter(prefix=prefix)

    entity = prefix.removeprefix("/")

    create_model = service.create_model
    update_model = service.update_model

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
    async def add_form(request: Request):

        return templates.TemplateResponse(
            f"{entity}/add.html",
            {
                "request": request,
                "entity": entity,
                "url": f"/{entity}"
            }
        )

    @router.post("/")
    async def create_item(request: Request):

        form = await request.form()
        data = create_model(**dict(form))

        service.create(data)

        return RedirectResponse(
            url=f"/{entity}/",
            status_code=303
        )

    @router.get("/{id}")
    async def details_form(request: Request, id: int):

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
    async def save_item(request: Request, id: int):

        form = await request.form()
        data = update_model(**dict(form))

        service.update(id, data)

        return RedirectResponse(
            url=f"/{entity}/",
            status_code=303
        )

    return router