# routes/summary.py
# GET /api/summary
# Returns the 4 stat cards: Active Listings, Avg Sell Price, Avg Spread, Orders Today
# Uses Supabase RPC for order stats — fast regardless of table size.
# Active Listings pulled from market_quantity.total_listings

from fastapi import APIRouter, HTTPException
from typing import List
from database import supabase
from models import StatSummary

router = APIRouter()

@router.get("/summary", response_model=List[StatSummary])
def get_summary():
    try:
        # ── Active Listings from market_quantity ──
        mq_response     = supabase.rpc("get_active_listings").execute()
        active_listings = mq_response.data.get("active_listings", 0) or 0

        # ── Order stats via RPC — database does the math ──
        rpc_response = supabase.rpc("get_order_summary").execute()
        stats        = rpc_response.data

        avg_sell        = round(stats.get("avg_sell",         0) or 0, 1)
        avg_buy         = round(stats.get("avg_buy",          0) or 0, 1)
        avg_spread      = round(avg_sell - avg_buy, 1)
        today_count     = stats.get("today_count",     0) or 0
        yesterday_count = stats.get("yesterday_count", 0) or 0
        orders_delta    = today_count - yesterday_count

        return [
            {
                "label": "Active Listings",
                "value": f"{active_listings:,}",
                "delta": "",
                "up":    True,
            },
            {
                "label": "Avg Sell Price",
                "value": f"{avg_sell} ₱",
                "delta": "",
                "up":    True,
            },
            {
                "label": "Avg Spread",
                "value": f"{avg_spread} ₱",
                "delta": "",
                "up":    avg_spread > 0,
            },
            {
                "label": "Orders Today",
                "value": f"{today_count:,}",
                "delta": f"{'+' if orders_delta >= 0 else ''}{orders_delta:,}",
                "up":    orders_delta >= 0,
            },
        ]

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))