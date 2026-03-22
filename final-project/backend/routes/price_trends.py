# routes/price_trends.py
# GET /api/price-trends?item=ash_prime_set
# Returns avg buy and sell price per date for a specific item

from fastapi import APIRouter, HTTPException, Query
from collections import defaultdict
from database import supabase
from models import PriceTrend

router = APIRouter()

@router.get("/price-trends", response_model=PriceTrend)
def get_price_trends(item: str = Query(...)):
    try:
        response = supabase.rpc("get_price_trend", {"item_name": item}).execute()
        return response.data or {"item": item, "data": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))