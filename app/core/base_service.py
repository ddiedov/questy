from fastapi import HTTPException

class BaseService:
    repository = None
    model = None
    create_model = None
    update_model = None
    patch_model = None

    def list(self, filters=None, current_user_id=None):
        rows = self.repository.list(filters)
        return [self.model(**row) for row in rows]
    
    def get_list_by_ids(self, ids):
        rows = self.repository.get_list_by_ids(ids)
        if not rows:
            return []
        return [self.model(**row) for row in rows]

    def get_map_by_ids(self, ids):
        items = self.get_list_by_ids(ids)
        return {item.id: item for item in items}

    def get(self, id: int):
        row = self.repository.get(id)
        if not row:
            return None
        return self.model(**row)
    
    def get_for_update(self, id: int):
        return self.get(id)

    def get_redirect_url(self, entity, item):
        return f"/{entity}/{item.id}/edit"

    def create(self, data, user_id):
        payload = {
            **data.model_dump(),
            "created_by": user_id
        }
        row = self.repository.create(payload)
        if not row:
            return None
        return self.model(**row[0])

    def update(self, id: int, data):
        row = self.repository.update(id, data.model_dump())
        if not row:
            return None
        return self.model(**row[0])
    
    def patch(self, id, data):
        row = self.repository.update(id, data.model_dump(exclude_unset=True))
        if not row:
            return None
        return self.model(**row[0])
    
    def upload_image(self, id: int, data: bytes):
        url = self.repository.upload_image(id, "main.png", data)
        if not url:
            return None
        return url
    
    def ensure_owner(self, id: int, user_id: str):
        obj = self.get(id)
        if not obj:
            raise HTTPException(status_code=404)
        if str(obj.created_by) != str(user_id):
            raise HTTPException(status_code=403, detail="You do not have permission to modify this resource")
        return True
    
    def apply_user_scope(self, filters, current_user_id):
        return filters