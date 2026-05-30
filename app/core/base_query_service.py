class BaseQueryService:

    repository = None

    model = None

    # =========================
    # LIST
    # =========================

    def list(self, filters=None, current_user_id=None):
        filters = self.apply_user_scope(
            filters,
            current_user_id
        )

        rows = self.repository.list(filters)

        return [
            self.model(**row)
            for row in rows
        ]

    # =========================
    # GET (DETAILS)
    # =========================
    def get(self, id: int):
        row = self.repository.get(id)

        if not row:
            return None

        return self.model(**row)

    # =========================
    # EDIT FORM DATA
    # =========================
    def get_for_update(self, id: int):
        return self.get(id)

    # =========================
    # BULK READ
    # =========================

    def get_list_by_ids(self, ids):
        rows = self.repository.get_list_by_ids(ids)
 
        if not rows:
            return []

        return [
            self.model(**row)
            for row in rows
        ]

    def get_map_by_ids(self, ids):
        items = self.get_list_by_ids(ids)

        return {
            item.id: item
            for item in items
        }

    # =========================
    # FILTERS
    # =========================

    def apply_user_scope(self, filters, current_user_id):
        return filters