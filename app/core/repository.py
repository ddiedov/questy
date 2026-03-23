from app.core.supabase import supabase
from .apply_filters import apply_filters
from postgrest.exceptions import APIError

class BaseRepository:

    def __init__(self, table_name: str):
        self.table = supabase.table(table_name)
        self.bucket = "questy-assets"
        self.prefix = table_name        

    filter_map = {}

    def list(self, filters=None):
        try:
            query = self.table.select("*")
            query = apply_filters(query, filters, self.filter_map)
            response = query.execute()
            if response is None:
                return None
            return response.data
        except APIError:
            return None

    def create(self, data):
        try:
            response = self.table.insert(data).execute()
            if response is None:
                return None
            return response.data
        except APIError:
            return None
    
    def get(self, id):
        try:
            response = self.table.select("*").eq("id", id).maybe_single().execute()
            if response is None:
                return None
            return response.data
        except APIError:
            return None
    
    def update(self, id, data):
        try:
            response = self.table.update(data).eq("id", id).execute()
            if response is None:
                return None
            return response.data
        except APIError:
            return None
        
    def upload_image(self, id, filename: str, data: bytes):
        try:
            path = f"{self.prefix}/{id}/{filename}"
            supabase.storage.from_(self.bucket).upload(path, data, {"upsert": "true"})
            url = supabase.storage.from_(self.bucket).get_public_url(path)
            if url is None:
                return None
            return url
        except APIError:
            return None