from app.core.supabase import supabase
from .apply_filters import apply_filters
from postgrest.exceptions import APIError
from typing import List

class BaseRepository:
    table_name: str
    filter_map = {}

    def __init__(self):
        self.table = supabase.table(self.table_name)
        self.bucket = "questy-assets"
        self.prefix = self.table_name  
        print(f"[Repository] Using table: {self.table_name}")      

    def list(self, filters=None):
        try:
            query = self.table.select("*")
            query = apply_filters(query, filters, self.filter_map)
            response = query.execute()
            return response.data or []
        except APIError as e:
            print(f"[Repository:{self.prefix}] ERROR:", e)
            return []
        
    def get_list_by_ids(self, ids: List[int]):
        try:
            if not ids:
                return []
            response = self.table.select("*").in_("id", ids).execute()
            return response.data or []
        except APIError as e:
            print(f"[Repository:{self.prefix}] ERROR:", e)
            return []

    def create(self, data):
        try:
            response = self.table.insert(data).execute()
            return response.data or []
        except APIError as e:
            print(f"[Repository:{self.prefix}] ERROR:", e)
            return []
    
    def get(self, id):
        try:
            response = self.table.select("*").eq("id", id).maybe_single().execute()
            if response is None:
                return None
            return response.data
        except APIError as e:
            print(f"[Repository:{self.prefix}] ERROR:", e)
            return None
    
    def update(self, id, data):
        try:
            response = self.table.update(data).eq("id", id).execute()
            return response.data or []
        except APIError as e:
            print(f"[Repository:{self.prefix}] ERROR:", e)
            return []
        
    def upload_image(self, id, filename: str, data: bytes):
        try:
            path = f"{self.prefix}/{id}/{filename}"
            supabase.storage.from_(self.bucket).upload(path, data, {"upsert": "true"})
            url = supabase.storage.from_(self.bucket).get_public_url(path)
            return url
        except APIError as e:
            print(f"[Repository:{self.prefix}] ERROR:", e)
            return None