# routes/spreads.py
# GET /api/spreads
# Returns buy/sell spread for top 6 items

from fastapi import APIRouter, HTTPException
from typing import List
from database import supabase
from models import SpreadItem

router = APIRouter()

@router.get("/spreads", response_model=List[SpreadItem])
def get_spreads():
    try:
        response = supabase.rpc("get_spreads").execute()
        return response.data or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))