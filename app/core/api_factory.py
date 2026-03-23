from fastapi import APIRouter, Depends


def create_api_router(service, prefix: str, filter_model=None):

    router = APIRouter(prefix=prefix)

    create_model = service.create_model
    update_model = service.update_model
    patch_model = service.patch_model


    if filter_model:
        @router.get("/")
        def list_items(filters: filter_model = Depends()):
            return service.list(filters)
    else:
        @router.get("/")
        def list_items():
            return service.list()


    @router.get("/{id}")
    def get_item(id: int):
        item = service.get(id)
        if not item:
            raise HTTPException(status_code=404)
        return item

    if create_model:
        @router.post("/")
        def create_item(data: create_model):
            return service.create(data)

    if update_model:
        @router.put("/{id}")
        def update_item(id: int, data: update_model):
            item = service.update(id, data)
            if not item:
                raise HTTPException(status_code=404)
            return item

    if patch_model:
        @router.patch("/{id}")
        def patch_item(id: int, data: patch_model):
            item = service.patch(id, data)
            if not item:
                raise HTTPException(status_code=404)
            return item

    return router