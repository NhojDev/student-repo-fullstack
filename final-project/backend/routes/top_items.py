# routes/top_items.py
# GET /api/top-items
# Returns top 8 traded items by order count with 24h change

from fastapi import APIRouter, HTTPException
from typing import List
from collections import Counter
from database import supabase
from models import TopItem

router = APIRouter()

@router.get("/top-items", response_model=List[TopItem])
def get_top_items():
    try:
        response = supabase.rpc("get_top_items").execute()
        return response.data or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))