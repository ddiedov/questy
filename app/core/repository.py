from app.core.supabase import supabase

class BaseRepository:

    def __init__(self, table):
        self.table = table

    def list(self):
        try:
            response = supabase.table(self.table).select("*").execute()
            if response is None:
                return None
            return response.data
        except APIError:
            return None

    def create(self, data):
        try:
            response = supabase.table(self.table).insert(data).execute()
            if response is None:
                return None
            return response.data
        except APIError:
            return None
    
    def get(self, id):
        try:
            response = supabase.table(self.table).select("*").eq("id", id).maybe_single().execute()
            if response is None:
                return None
            return response.data
        except APIError:
            return None
    
    def update(self, id, data):
        try:
            response = supabase.table(self.table).update(data).eq("id", id).execute()
            if response is None:
                return None
            return response.data
        except APIError:
            return None