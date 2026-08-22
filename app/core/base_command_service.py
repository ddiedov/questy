from fastapi import HTTPException


class BaseCommandService:
    repository = None

    model = None
    create_model = None
    update_model = None
    patch_model = None

    with_owner = True

   
    # =========================
    # CREATE
    # =========================
    def create(self, data, user_id):
        payload = data.model_dump(mode="json")

        if self.with_owner:
            payload["created_by"] = user_id

        row = self.repository.create(payload)

        if not row:
            raise Exception("Object was not created in repository")

        return self.model(**row)

    # =========================
    # UPDATE
    # =========================

    def update(self, id: int, data):
        row = self.repository.update(id, data.model_dump(mode="json"))

        if not row:
            return None

        return self.model(**row)

    def patch(self, id, data):
        row = self.repository.update(
            id,
            data.model_dump(mode="json", exclude_unset=True)
        )

        if not row:
            return None

        return self.model(**row)

    # =========================
    # DELETE
    # =========================

    def delete(self, id: int):
        return self.repository.delete(id)

    # =========================
    # FILES
    # =========================

    def upload_image(
        self,
        id: int,
        image_type: str,
        data: bytes
    ):
        filename = f"{image_type}.png"

        url = self.repository.upload_image(
            id,
            filename,
            data
        )

        if not url:
            return None

        return url

    # =========================
    # SECURITY
    # =========================

    def ensure_owner(self, id: int, user_id: str):
        row = self.repository.get(id)

        if not row:
            raise HTTPException(status_code=404)

        if str(row.get("created_by")) != str(user_id):
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to modify this resource"
            )

        return True

    # =========================
    # UI HELPERS (TEMPORARY LAYER)
    # =========================

    def get_redirect_url(self, entity, item):
        return f"/{entity}/{item.id}/edit"
