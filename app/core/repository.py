import logging
from typing import List

from app.core.supabase import supabase
from .apply_filters import apply_filters
from postgrest.exceptions import APIError


logger = logging.getLogger(__name__)

class BaseRepository:
    table_name: str
    filter_map = {}

    def __init__(self):
        self.table = supabase.table(self.table_name)
        self.bucket = "questy-assets"
        self.prefix = self.table_name  
        logger.debug("[Repository] Using table: %s", self.table_name)

    def list(self, filters=None):
        try:
            query = self.table.select("*")
            query = apply_filters(query, filters, self.filter_map)
            response = query.execute()
            return response.data or []
        except APIError:
            logger.exception("[Repository:%s] ERROR", self.prefix)
            return []
        
    def get_list_by_ids(self, ids: List[int]):
        try:
            if not ids:
                return []
            response = self.table.select("*").in_("id", ids).execute()
            return response.data or []
        except APIError:
            logger.exception("[Repository:%s] ERROR", self.prefix)
            return []

    def create(self, data):
        try:
            response = self.table.insert(data).execute()
            if not response.data:
                raise Exception(f"Supabase insert failed: {response}")
            return response.data[0]
        except APIError:
            logger.exception("[Repository:%s] CREATE ERROR", self.prefix)
            raise
    
    def get(self, id):
        try:
            response = self.table.select("*").eq("id", id).maybe_single().execute()
            if response is None:
                return None
            return response.data
        except APIError:
            logger.exception("[Repository:%s] ERROR", self.prefix)
            return None
    
    def update(self, id, data):
        try:
            response = self.table.update(data).eq("id", id).execute()
            if not response.data:
                return None
            return response.data[0]
        except APIError:
            logger.exception("[Repository:%s] UPDATE ERROR", self.prefix)
            raise
        
    def upload_image(self, id, filename: str, data: bytes):
        try:
            path = f"{self.prefix}/{id}/{filename}"
            supabase.storage.from_(self.bucket).upload(path, data, {"upsert": "true"})
            url = supabase.storage.from_(self.bucket).get_public_url(path)
            return url
        except APIError:
            logger.exception("[Repository:%s] ERROR", self.prefix)
            return None
        
    def delete(self, id):
        try:
            response = self.table.delete().eq("id", id).execute()
            return bool(response.data)
        except APIError:
            logger.exception("[Repository:%s] ERROR", self.prefix)
            raise
