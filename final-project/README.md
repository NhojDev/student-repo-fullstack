# WFM Tracker — Warframe Market Analytics

A full-stack web application that collects, cleans, and visualizes trading data from the [Warframe Market](https://warframe.market) API. Built with React on the frontend, FastAPI on the backend, Pandas for data processing, and Supabase as the database.

---

## Features

- **Price Trends** — buy vs sell price over time for any item
- **Order Spreads** — visual buy/sell gap comparison across top items
- **Top Traded Items** — ranked table by order volume with 24h change
- **Market Quantity** — supply and demand counts with platinum totals
- **Live Data Sync** — automated data pipeline with daily CSV caching
- **Resurgence Tracking** — flags items currently in Void Trader resurgence windows

---

## Project Structure

```
final-project/
├── src/                        # React frontend
│   ├── components/
│   │   ├── StatCard.jsx
│   │   ├── SectionHeader.jsx
│   │   ├── PriceTrendChart.jsx
│   │   ├── SpreadChart.jsx
│   │   ├── TopItemsTable.jsx
│   │   └── VolumeBarChart.jsx
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
├── tests/                      # Frontend unit tests
│   ├── components.test.jsx
│   ├── vitest.config.js
│   └── setup.js
├── backend/                    # Python backend
│   ├── main.py                 # FastAPI app entry point
│   ├── database.py             # Supabase client
│   ├── models.py               # Pydantic response models
│   ├── data_pipeline.py        # Data collection and cleaning
│   ├── test_pipeline.py        # Backend unit tests
│   ├── .env                    # Credentials (never commit)
│   └── routes/
│       ├── summary.py          # GET /api/summary
│       ├── top_items.py        # GET /api/top-items
│       ├── spreads.py          # GET /api/spreads
│       └── price_trends.py     # GET /api/price-trends
├── .env                        # Frontend env vars
├── package.json
└── vite.config.js
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Recharts |
| Backend | Python, FastAPI, Uvicorn |
| Data Processing | Pandas |
| Database | Supabase (PostgreSQL) |
| Testing | Pytest (backend), Vitest + React Testing Library (frontend) |

---

## Prerequisites

- Node.js 18+
- Python 3.10+
- A [Supabase](https://supabase.com) project
- A [Warframe Market](https://warframe.market) account (API is public, no key needed)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/final-project.git
cd final-project
```

### 2. Frontend setup

```bash
npm install
```

Create a `.env` file in the project root:
```
VITE_API_URL=http://localhost:8000
```

### 3. Backend setup

```bash
cd backend
pip install fastapi uvicorn supabase pandas python-dotenv requests
```

Create a `.env` file inside `backend/`:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
```

> ⚠️ Use the **service role key** (not the anon key) for the backend. Never commit `.env` to version control.

### 4. Supabase tables

Run the following SQL in your Supabase SQL Editor:

```sql
-- Orders table
create table orders (
  id                 bigserial primary key,
  name               text,
  gameref            text,
  type               text,
  platinum           int,
  quantity           int,
  "perTrade"         int,
  vaulted            bool,
  date               date,
  tags               text,
  rarity             text,
  resurgance         bool,
  base_name          text,
  datetime_collected timestamp with time zone
);

-- Market quantity table
create table market_quantity (
  id                    bigserial primary key,
  name                  text,
  demand                int,
  supply                int,
  demand_platinum_total int,
  supply_platinum_total int,
  total_sell_listings   int,
  total_buy_listings    int,
  date                  date
);
```

### 5. Supabase SQL functions

Run these in the Supabase SQL Editor to enable fast aggregated queries:

```sql
-- Summary stats
create or replace function get_order_summary()
returns json as $$
  select json_build_object(
    'avg_sell',         avg(platinum) filter (where type = 'sell'),
    'avg_buy',          avg(platinum) filter (where type = 'buy'),
    'today_count',      sum(case when type = 'sell' and date = (now() at time zone 'America/Denver')::date then 1 else 0 end) +
                        sum(case when type = 'buy'  and date = (now() at time zone 'America/Denver')::date then 1 else 0 end),
    'yesterday_count',  sum(case when type = 'sell' and date = (now() at time zone 'America/Denver')::date - 1 then 1 else 0 end) +
                        sum(case when type = 'buy'  and date = (now() at time zone 'America/Denver')::date - 1 then 1 else 0 end)
  )
  from orders;
$$ language sql;

-- Active listings
create or replace function get_active_listings()
returns json as $$
  select json_build_object(
    'active_listings', coalesce(sum(total_sell_listings), 0) + coalesce(sum(total_buy_listings), 0)
  )
  from market_quantity;
$$ language sql;

-- Top items
create or replace function get_top_items()
returns json as $$
  with today_counts as (
    select name,
      sum(case when type = 'sell' then 1 else 0 end) as sell_listings,
      sum(case when type = 'buy'  then 1 else 0 end) as buy_listings,
      count(*) as total
    from orders
    where date = (now() at time zone 'America/Denver')::date
    group by name
  ),
  yesterday_counts as (
    select name, count(*) as total
    from orders
    where date = (now() at time zone 'America/Denver')::date - 1
    group by name
  )
  select json_agg(
    json_build_object(
      'name',          t.name,
      'sell_listings', t.sell_listings,
      'buy_listings',  t.buy_listings,
      'volume',        t.total,
      'change', round(
        case when y.total > 0
          then ((t.total - y.total)::numeric / y.total) * 100
          else 0
        end, 1
      )
    )
    order by t.total desc
  )
  from today_counts t
  left join yesterday_counts y on t.name = y.name
  limit 10;
$$ language sql;

-- Spreads
create or replace function get_spreads()
returns json as $$
  with buy_prices as (
    select name, max(platinum) as top_buy
    from orders where type = 'buy'
    group by name
  ),
  sell_prices as (
    select name, min(platinum) as lowest_sell
    from orders where type = 'sell'
    group by name
  )
  select json_agg(
    json_build_object(
      'item',   b.name,
      'buy',    b.top_buy,
      'sell',   s.lowest_sell,
      'spread', round((s.lowest_sell - b.top_buy)::numeric, 2)
    )
    order by (s.lowest_sell - b.top_buy) desc
  )
  from buy_prices b
  join sell_prices s on b.name = s.name
  limit 10;
$$ language sql;

-- Price trend
create or replace function get_price_trend(item_name text)
returns json as $$
  with daily as (
    select
      date,
      round(avg(platinum) filter (where type = 'buy')::numeric,  1) as buy,
      round(avg(platinum) filter (where type = 'sell')::numeric, 1) as sell
    from orders
    where name = item_name
    group by date
    order by date desc
    limit 10
  )
  select json_build_object(
    'item', item_name,
    'data', json_agg(
      json_build_object('date', date, 'buy', buy, 'sell', sell)
      order by date asc
    )
  )
  from daily;
$$ language sql;
```

---

## Running the App

### Run the data pipeline (collect data first)

```bash
cd backend
python data_pipeline.py
```

This fetches all prime item orders from Warframe Market, cleans the data, and writes it to Supabase. It caches results to a daily CSV so re-running on the same day loads from cache.

### Start the backend

```bash
cd backend
uvicorn main:app --reload
```

API available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

### Start the frontend

```bash
cd final-project
npm run dev
```

App available at `http://localhost:5173`

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/summary` | 4 stat cards — listings, avg price, spread, orders |
| GET | `/api/top-items` | Top 10 items by order volume with 24h change |
| GET | `/api/spreads` | Top 10 buy/sell spreads |
| GET | `/api/price-trends?item={name}` | Price trend for a specific item |

---

## Running Tests

### Backend

```bash
cd backend
pytest test_pipeline.py -v
```

### Frontend

```bash
cd final-project
npm test
```

---

## Data Pipeline Overview

```
warframe.market API
      ↓
fetch_item_list()       — pulls all tradeable items, splits into prime sets, parts, other
fetch_relic_maps()      — builds rarity + vaulted lookup from relic reward manifest
build_resurgence_df()   — builds resurgence window reference from RESURGENCE_WINDOWS config
fetch_orders()          — fetches top buy/sell orders per item (concurrent, cached daily)
clean_orders()          — cleans, casts types, adds rarity/resurgance/base_name columns
sync_orders_to_supabase() — inserts cleaned data into orders table in batches of 500
fetch_market_quantity() — fetches full order counts for supply/demand stats
sync_market_quantity_to_supabase() — inserts market quantity snapshot
```

---

## Adding New Resurgence Windows

In `data_pipeline.py`, add a new entry to `RESURGENCE_WINDOWS`:

```python
{
    "start": "2026-04-01",
    "end":   "2026-04-15",
    "items": (
        "excalibur", "mag", "skana", "lato",
    ),
},
```

---

## Environment Variables

| File | Variable | Description |
|---|---|---|
| `backend/.env` | `SUPABASE_URL` | Your Supabase project URL |
| `backend/.env` | `SUPABASE_KEY` | Service role key (keep secret) |
| `.env` | `VITE_API_URL` | FastAPI base URL for the frontend |

---

## License

MIT