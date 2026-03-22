# models.py
# Pydantic models define the exact shape of data each API route returns.
# FastAPI uses these to validate and serialize responses automatically.
#
# Usage in routes:
#   from models import StatSummary, TopItem, SpreadItem, PriceTrend
#   @router.get("/summary", response_model=List[StatSummary])

from pydantic import BaseModel
from typing import List, Optional


# ── STAT SUMMARY ──────────────────────────────────────────────────────────────
# Used by: GET /api/summary
class StatSummary(BaseModel):
    label: str
    value: str
    delta: str
    up:    bool


# ── TOP ITEM ──────────────────────────────────────────────────────────────────
# Used by: GET /api/top-items
class TopItem(BaseModel):
    name:          str
    sell_listings: int
    buy_listings:  int
    volume:        int
    change:        float


# ── SPREAD ITEM ───────────────────────────────────────────────────────────────
# Used by: GET /api/spreads
class SpreadItem(BaseModel):
    item:   str
    buy:    float
    sell:   float
    spread: float


# ── PRICE POINT (single point on a trend line) ────────────────────────────────
# Used by: GET /api/price-trends
class PricePoint(BaseModel):
    date: str
    buy:  Optional[float] = None
    sell: Optional[float] = None


# ── PRICE TREND (full trend for one item) ─────────────────────────────────────
# Used by: GET /api/price-trends
class PriceTrend(BaseModel):
    item: str
    data: List[PricePoint]