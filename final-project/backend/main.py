# main.py
# FastAPI application entry point.
# Registers all routes and configures CORS so the React frontend can call the API.
#
# Run with: uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import summary, top_items, spreads, price_trends

app = FastAPI(title="Warframe Market API", version="0.1.0")

# ── CORS ──────────────────────────────────────────────────────────────────────
# Allows the React dev server (localhost:5173) to call this API.
# Update origins when you deploy to production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── ROUTES ────────────────────────────────────────────────────────────────────
app.include_router(summary.router,      prefix="/api")
app.include_router(top_items.router,    prefix="/api")
app.include_router(spreads.router,      prefix="/api")
app.include_router(price_trends.router, prefix="/api")

# ── HEALTH CHECK ──────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "ok", "message": "Warframe Market API is running"}