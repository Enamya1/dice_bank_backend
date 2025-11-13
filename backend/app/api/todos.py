from fastapi import APIRouter, Depends
from supabase import Client
from ..utils.supabase import get_supabase_client

router = APIRouter()

@router.get("/todos")
async def get_todos(supabase: Client = Depends(get_supabase_client)):
    response = supabase.table("todos").select("*").execute()
    if response.data:
        return response.data
    return []