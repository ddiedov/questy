from fastapi import HTTPException

class BaseService:

    def __init__(self, repository, model, create_model, update_model, patch_model):

        self.repo = repository
        self.model = model
        self.create_model = create_model
        self.update_model = update_model
        self.patch_model = patch_model


    def list(self, filters=None):
        rows = self.repo.list(filters)
        return [self.model(**row) for row in rows]


    def get(self, id: int):
        row = self.repo.get(id)
        if not row:
            return None
        return self.model(**row)


    def create(self, data):
        row = self.repo.create(data.model_dump())
        if not row:
            return None
        return self.model(**row[0])


    def update(self, id: int, data):
        row = self.repo.update(id, data.model_dump())
        if not row:
            return None
        return self.model(**row[0])
    
    def patch(self, id, data):
        row = self.repo.update(id, data.model_dump(exclude_unset=True))
        if not row:
            return None
        return self.model(**row[0])
    
    def upload_image(self, id: int, data: bytes):
        url = self.repo.upload_image(id, "main.png", data)
        if not url:
            return None
        return url
    
    def ensure_owner(self, id: int, user_id: str):
        obj = self.get(id)
        if not obj:
            raise HTTPException(status_code=404)
        if str(obj.user_id) != str(user_id):
            raise HTTPException(status_code=403, detail="You do not have permission to modify this resource")
        return True