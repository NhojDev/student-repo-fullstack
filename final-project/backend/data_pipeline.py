# data_pipeline.py
# Fetches, cleans, and writes Warframe Market data to Supabase.
#
# Run manually:   python data_pipeline.py
# Auto-schedule:  see bottom of file for APScheduler setup

import pandas as pd
import requests
import os
from datetime import date, datetime, timezone
from database import supabase


# ── RESURGENCE WINDOWS ────────────────────────────────────────────────────────
# Add new resurgence windows here as they are announced in-game.

RESURGENCE_WINDOWS = [
    {
        "start": "2026-01-15",
        "end":   "2026-02-12",
        "items": (
            "harrow", "nekros", "galatine", "knell", "scourge", "tigris",
            "saryn", "valkyr", "cernos", "nikana", "spira", "venka",
            "garuda", "khora", "dual_keres", "hystrix", "nagantaka",
            "corvas", "ivara", "oberon", "aksomati", "baza",
            "silva_and_aegis", "sybaris",
        ),
    },
    {
        "start": "2026-02-12",
        "end":   "2026-02-19",
        "items": (
            "harrow", "nekros", "galatine", "knell", "scourge", "tigris",
            "saryn", "valkyr", "cernos", "nikana", "spira", "venka",
            "garuda", "khora", "dual_keres", "hystrix", "nagantaka",
            "corvas", "ivara", "oberon", "aksomati", "baza",
            "silva_and_aegis", "sybaris", "ember", "frost", "glaive",
            "latron", "reaper", "sicarus", "hydroid", "mesa", "akjagara",
            "ballistica", "nami_skyla", "redeemer", "loki", "volt",
            "bo", "wyrm", "odonata",
        ),
    },
    {
        "start": "2026-02-20",
        "end":   "2026-03-19",
        "items": (
            "atlas", "vauban", "tekko", "dethcube", "akstiletto", "fragor",
        ),
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — ORDERS TABLE
# ─────────────────────────────────────────────────────────────────────────────

# ── FETCH ITEM LIST ───────────────────────────────────────────────────────────

def fetch_item_list() -> tuple:
    """
    Pulls the full item list from warframe.market v2 API.
    Returns:
      filtered_sets_df  — prime sets only
      filtered_parts_df — prime parts only (no sets)
      base_item_df      — raw full item list (needed for relic lookups)
    """
    print("Fetching item list...")

    response = requests.get("https://api.warframe.market/v2/items")
    response.raise_for_status()
    base_item_df = pd.DataFrame(response.json()["data"])

    # Keep tags before dropping — we want it in the final table
    cleaned_item_df = base_item_df.drop(columns=[
        "id", "i18n", "subtypes", "maxAmberStars", "maxCyanStars",
        "maxRank", "bulkTradable", "vaulted", "baseEndo", "endoMultiplier"
    ], errors="ignore")
    cleaned_item_df = cleaned_item_df.rename(columns={"slug": "name"})
    cleaned_item_df["gameRef"] = cleaned_item_df["gameRef"].map(
        lambda x: x.rsplit("/", 1)[-1]
    )

    # Filter to prime items only — keep tags column intact
    mask = cleaned_item_df["tags"].apply(
        lambda x: "prime" in x if isinstance(x, list) else False
    )
    filtered_item_df = cleaned_item_df[mask].sort_values(by="name")

    mask_sets         = filtered_item_df["name"].str.contains(r"_set$", case=False, na=False)
    filtered_sets_df  = filtered_item_df[mask_sets]
    filtered_parts_df = filtered_item_df[~mask_sets]

    print(f"  {len(filtered_sets_df)} prime sets | {len(filtered_parts_df)} prime parts")
    return filtered_sets_df, filtered_parts_df, base_item_df


# ── FETCH RARITY + VAULTED MAPS ───────────────────────────────────────────────

def fetch_relic_maps(filtered_parts_df: pd.DataFrame, base_item_df: pd.DataFrame) -> tuple:
    """
    Builds rarity_dict and vaulted_dict from relic reward manifest.
    """
    print("Fetching relic data...")

    cleaned_relic_df = base_item_df.drop(columns=[
        "id", "maxAmberStars", "i18n", "ducats", "subtypes", "maxCyanStars",
        "maxRank", "bulkTradable", "baseEndo", "endoMultiplier"
    ], errors="ignore")
    cleaned_relic_df = cleaned_relic_df.rename(columns={"slug": "name"})

    mask = cleaned_relic_df["tags"].apply(
        lambda x: "relic" in x if isinstance(x, list) else False
    )
    filtered_relic_df = cleaned_relic_df[mask].sort_values(by="name")
    filtered_relic_df["gameRef"] = filtered_relic_df["gameRef"].apply(
        lambda x: x.rsplit("/", 1)[-1]
    )

    manifest_url = (
        "http://content.warframe.com/PublicExport/Manifest/"
        "ExportRelicArcane_en.json!00_fdH29UBNM7od0XMI54PlOQ"
    )
    response = requests.get(manifest_url)
    response.raise_for_status()
    rewards_df = pd.DataFrame(response.json()["ExportRelicArcane"])

    cleaned_rewards_df = rewards_df.drop(columns=[
        "name", "codexSecret", "description", "excludeFromCodex",
        "rarity", "levelStats"
    ], errors="ignore")
    cleaned_rewards_df = cleaned_rewards_df.rename(columns={"uniqueName": "gameRef"})
    cleaned_rewards_df["gameRef"] = (
        cleaned_rewards_df["gameRef"]
        .apply(lambda x: x.rsplit("/", 1)[-1])
        .str.replace("Bronze", "")
    )

    merged_relic_df = pd.merge(filtered_relic_df, cleaned_rewards_df, on="gameRef")

    rarity_dict = {}
    for _, row in merged_relic_df.iterrows():
        for reward in row["relicRewards"]:
            reward_ref = reward["rewardName"].rsplit("/", 1)[-1]
            rarity_dict[reward_ref] = reward["rarity"]

    vaulted_dict = {x: True for x in filtered_parts_df["gameRef"]}
    for _, row in merged_relic_df[merged_relic_df["vaulted"] == False].iterrows():
        for reward in row["relicRewards"]:
            reward_ref = reward["rewardName"].rsplit("/", 1)[-1]
            vaulted_dict[reward_ref] = False

    print(f"  Rarity: {len(rarity_dict)} | Vaulted: {len(vaulted_dict)}")
    return rarity_dict, vaulted_dict


# ── BUILD RESURGENCE DATAFRAME ────────────────────────────────────────────────

def build_resurgence_df(filtered_parts_df: pd.DataFrame, filtered_sets_df: pd.DataFrame) -> pd.DataFrame:
    dfs = []
    for window in RESURGENCE_WINDOWS:
        prefixes = tuple(window["items"])
        df = pd.concat([
            filtered_parts_df[filtered_parts_df["name"].str.startswith(prefixes)].copy(),
            filtered_sets_df[filtered_sets_df["name"].str.startswith(prefixes)].copy(),
        ])
        df["start"] = pd.to_datetime(window["start"])
        df["end"]   = pd.to_datetime(window["end"])
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


# ── FETCH TOP ORDERS ──────────────────────────────────────────────────────────

def fetch_orders(
    filtered_parts_df: pd.DataFrame,
    filtered_sets_df: pd.DataFrame,
    vaulted_dict: dict,
    save_folder: str = "Data/Price_Data",
) -> pd.DataFrame:
    """
    Fetches top buy/sell orders for every prime item.
    Caches to daily CSV to avoid re-fetching on same-day re-runs.
    """
    today       = date.today()
    os.makedirs(save_folder, exist_ok=True)
    output_path = os.path.join(os.getcwd(), save_folder, f"{today}.csv")

    if os.path.isfile(output_path):
        print(f"  Orders already fetched today — loading from CSV")
        return pd.read_csv(output_path)

    print("Fetching orders (this may take a few minutes)...")

    filtered_df = pd.concat([filtered_parts_df, filtered_sets_df], ignore_index=True)
    dfs = []

    for _, row in filtered_df.iterrows():
        api_url  = f"https://api.warframe.market/v2/orders/item/{row['name']}/top"
        response = requests.get(api_url)

        if response.status_code != 200:
            print(f"  Failed {row['name']}: {response.status_code}")
            continue

        order_data    = response.json()
        sell_order_df = pd.DataFrame(order_data["data"]["sell"])
        buy_order_df  = pd.DataFrame(order_data["data"]["buy"])

        for df, order_type in [(sell_order_df, "sell"), (buy_order_df, "buy")]:
            df["gameRef"] = row["gameRef"]
            df["name"]    = row["name"]
            df["type"]    = order_type
            df["date"]    = today
            # Preserve tags as a comma-separated string for storage
            df["tags"]    = ",".join(row["tags"]) if isinstance(row["tags"], list) else row["tags"]
            df["vaulted"] = None if "_set" in row["name"].lower() else vaulted_dict.get(row["gameRef"], True)

        dfs.extend([buy_order_df, sell_order_df])

    base_order_df = pd.concat(dfs, ignore_index=True)
    base_order_df.to_csv(output_path, index=False)
    print(f"  Saved {len(base_order_df)} rows to {output_path}")
    return base_order_df


# ── CLEAN ORDERS ──────────────────────────────────────────────────────────────

def clean_orders(
    base_order_df: pd.DataFrame,
    rarity_dict: dict,
    resurgance_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Full cleaning pipeline. Final DataFrame columns:
      name, gameRef, type, platinum, quantity, perTrade,
      vaulted, date, tags, rarity, resurgance,
      base_name, datetime_collected
    """
    print("Cleaning orders...")

    df = base_order_df.copy()

    # ── base_name: derived from item name ──
    df["base_name"] = (
        df["name"].str.lower().str.split("_prime").str[0] + "_prime"
    )

    # ── Infer vaulted status for sets from their parts ──
    part_vaulted_map = (
        df[~df["name"].str.contains(r"_set$", case=False, na=False)]
        .groupby("base_name")["vaulted"]
        .max()
    )
    is_set = df["name"].str.contains(r"_set$", case=False, na=False)
    df.loc[is_set, "vaulted"] = df.loc[is_set, "base_name"].map(part_vaulted_map)

    # ── Drop API-only columns not needed in the final table ──
    drop_cols = ["id", "createdAt", "updatedAt", "itemId", "user", "visible", "rank"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns]).dropna()

    # ── Type casting ──
    df["platinum"] = df["platinum"].astype(int)
    df["quantity"] = df["quantity"].astype(int)
    df["perTrade"] = df["perTrade"].astype(int)
    df["vaulted"]  = df["vaulted"].astype(bool)
    df["date"]     = pd.to_datetime(df["date"])

    # ── Rarity column ──
    df["rarity"] = df["gameRef"].map(rarity_dict)
    df.loc[df["name"].str.contains(r"_set$", case=False, na=False), "rarity"] = "SET"

    # ── Resurgance column ──
    df["index"] = range(len(df))
    if not resurgance_df.empty:
        df_merged = df.merge(
            resurgance_df[["gameRef", "start", "end"]], on="gameRef", how="left"
        )
        df_merged["in_range"] = (
            (df_merged["date"] >= df_merged["start"]) &
            (df_merged["date"] <= df_merged["end"])
        )
        resurgance_status = df_merged.groupby("index")["in_range"].any()
        df["resurgance"]  = df["index"].map(resurgance_status).fillna(False)
    else:
        df["resurgance"] = False

    df = df.drop(columns=["index"])

    # ── datetime_collected: timezone-aware UTC timestamp ──
    df["datetime_collected"] = datetime.now(timezone.utc).isoformat()

    # ── Final column order ──
    final_columns = [
        "name", "gameRef", "type", "platinum", "quantity", "perTrade",
        "vaulted", "date", "tags", "rarity", "resurgance",
        "base_name", "datetime_collected",
    ]
    # Only keep columns that exist (guards against missing cols from CSV reloads)
    df = df[[c for c in final_columns if c in df.columns]]
    df = df.rename(columns={"gameRef": "gameref"})

    print(f"  Cleaned {len(df)} rows")
    print(f"  Columns: {list(df.columns)}")
    return df


# ── SYNC ORDERS TO SUPABASE ───────────────────────────────────────────────────

def sync_orders_to_supabase(orders_df: pd.DataFrame):
    """
    Inserts all cleaned orders into the `orders` table in Supabase.

    Supabase table schema:
      name               text
      gameRef            text
      type               text         (buy | sell)
      platinum           int
      quantity           int
      perTrade           int
      vaulted            bool
      date               date
      tags               text         (comma-separated)
      rarity             text         (Common | Uncommon | Rare | SET)
      resurgance         bool
      base_name          text
      datetime_collected timestamp with time zone
    """
    print("Writing orders to Supabase...")

    df = orders_df.copy()
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    rows = df.to_dict(orient="records")

    for i in range(0, len(rows), 500):
        chunk = rows[i:i + 500]
        supabase.table("orders").insert(chunk).execute()
        print(f"  Inserted rows {i}–{min(i + 500, len(rows))}")

    print(f"  Done — {len(rows)} rows written to orders table")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — MARKET QUANTITY TABLE (PLACEHOLDER)
# Tracks supply and demand counts per item per day.
#
# Supabase table schema:
#   name      text   — item url_name
#   demand    int    — number of active buy orders on the market
#   supply    int    — number of active sell orders on the market
#   date      date   — date this snapshot was taken
# ─────────────────────────────────────────────────────────────────────────────

def fetch_market_quantity() -> pd.DataFrame:
    """
    PLACEHOLDER — Fetches supply (sell order count) and demand (buy order count)
    per item from warframe.market.

    TODO: Replace this placeholder with a real API call.
    The warframe.market v2 orders endpoint returns all orders for an item —
    count buy orders for demand, count sell orders for supply.

    Expected output DataFrame columns:
      name     (str)  — item url_name
      demand   (int)  — count of active buy orders
      supply   (int)  — count of active sell orders
      date     (date) — today's date
    """
    print("PLACEHOLDER: fetch_market_quantity() not yet implemented")

    # ── Replace everything below with real logic ──────────────────────────
    # Example of what the real implementation would look like:
    #
    # today = date.today()
    # rows  = []
    #
    # for item in TRACKED_ITEMS:
    #     api_url  = f"https://api.warframe.market/v2/orders/item/{item}"
    #     response = requests.get(api_url)
    #     if response.status_code != 200:
    #         continue
    #     orders   = response.json()["data"]
    #     demand   = sum(1 for o in orders if o["type"] == "buy")
    #     supply   = sum(1 for o in orders if o["type"] == "sell")
    #     rows.append({"name": item, "demand": demand, "supply": supply, "date": today})
    #
    # return pd.DataFrame(rows)
    # ─────────────────────────────────────────────────────────────────────

    return pd.DataFrame(columns=["name", "demand", "supply", "date"])


def sync_market_quantity_to_supabase(quantity_df: pd.DataFrame):
    """
    PLACEHOLDER — Writes supply/demand snapshot to the `market_quantity` table.

    Supabase table schema:
      name     text
      demand   int
      supply   int
      date     date

    TODO: Uncomment the insert below once fetch_market_quantity() is implemented.
    """
    if quantity_df.empty:
        print("PLACEHOLDER: market_quantity sync skipped — no data yet")
        return

    # ── Uncomment when ready ──────────────────────────────────────────────
    # print("Writing market quantity to Supabase...")
    # df = quantity_df.copy()
    # df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    # supabase.table("market_quantity").insert(
    #     df.to_dict(orient="records")
    # ).execute()
    # print(f"  Wrote {len(df)} rows to market_quantity")
    # ─────────────────────────────────────────────────────────────────────

    print("PLACEHOLDER: market_quantity sync not yet implemented")


# ─────────────────────────────────────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────────────────────────────────────

def run_pipeline():
    print(f"\n── Pipeline started at {datetime.now(timezone.utc).isoformat()} ──")

    # ── Section 1: Orders ──
    filtered_sets_df, filtered_parts_df, base_item_df = fetch_item_list()
    rarity_dict, vaulted_dict  = fetch_relic_maps(filtered_parts_df, base_item_df)
    resurgance_df              = build_resurgence_df(filtered_parts_df, filtered_sets_df)
    base_order_df              = fetch_orders(filtered_parts_df, filtered_sets_df, vaulted_dict)
    orders_df                  = clean_orders(base_order_df, rarity_dict, resurgance_df)
    sync_orders_to_supabase(orders_df)

    # ── Section 2: Market Quantity (placeholder) ──
    quantity_df = fetch_market_quantity()
    sync_market_quantity_to_supabase(quantity_df)

    print("── Pipeline complete ──\n")


if __name__ == "__main__":
    run_pipeline()


# ── OPTIONAL: AUTO-SCHEDULE ───────────────────────────────────────────────────
# pip install apscheduler
#
# from apscheduler.schedulers.blocking import BlockingScheduler
#
# if __name__ == "__main__":
#     run_pipeline()
#     scheduler = BlockingScheduler()
#     scheduler.add_job(run_pipeline, "interval", minutes=5)
#     scheduler.start()