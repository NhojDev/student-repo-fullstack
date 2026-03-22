# test_pipeline.py
# Unit tests for data_pipeline.py functions
# Run with: pytest test_pipeline.py -v

import pytest
import pandas as pd
import numpy as np
from datetime import date
from unittest.mock import MagicMock
import sys

# ── Mock database so tests don't need a real Supabase connection ──────────────
sys.modules["database"] = MagicMock()

from data_pipeline import (
    _name_to_gameref,
    clean_orders,
    build_resurgence_df,
)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def make_prime_order_row(**kwargs):
    """Returns a minimal valid prime order row dict."""
    base = {
        "name":     "ash_prime_set",
        "gameRef":  "AshPrimeSet",
        "type":     "sell",
        "platinum": 155.0,
        "quantity": 1.0,
        "perTrade": 1.0,
        "vaulted":  None,
        "date":     "2026-03-21",
        "tags":     "prime,set",
    }
    base.update(kwargs)
    return base


def make_other_order_row(**kwargs):
    """Returns a minimal valid non-prime order row dict."""
    base = {
        "name":     "blind_rage",
        "gameRef":  "BlindRage",
        "type":     "sell",
        "platinum": 45.0,
        "quantity": 1.0,
        "perTrade": 1.0,
        "vaulted":  False,
        "date":     "2026-03-21",
        "tags":     "mod,rare",
        "rarity":   "RARE",
    }
    base.update(kwargs)
    return base


def make_parts_df():
    return pd.DataFrame([
        {"name": "ash_prime_neuroptics",    "gameRef": "AshPrimeNeuroptics",    "tags": ["prime"]},
        {"name": "harrow_prime_neuroptics", "gameRef": "HarrowPrimeNeuroptics", "tags": ["prime"]},
        {"name": "nekros_prime_neuroptics", "gameRef": "NekrosPrimeNeuroptics", "tags": ["prime"]},
    ])


def make_sets_df():
    return pd.DataFrame([
        {"name": "harrow_prime_set", "gameRef": "HarrowPrimeSet", "tags": ["prime", "set"]},
        {"name": "ash_prime_set",    "gameRef": "AshPrimeSet",    "tags": ["prime", "set"]},
    ])


def make_resurgance_df():
    return pd.DataFrame([{
        "name":    "harrow_prime_neuroptics",
        "gameRef": "HarrowPrimeNeuroptics",
        "start":   pd.Timestamp("2026-01-15"),
        "end":     pd.Timestamp("2026-02-12"),
    }])


# ─────────────────────────────────────────────────────────────────────────────
# 1. _name_to_gameref
# ─────────────────────────────────────────────────────────────────────────────

class TestNameToGameref:

    def test_basic_conversion(self):
        assert _name_to_gameref("ancient_fusion_core") == "AncientFusionCore"

    def test_single_word(self):
        assert _name_to_gameref("adaptation") == "Adaptation"

    def test_prime_set(self):
        assert _name_to_gameref("ash_prime_set") == "AshPrimeSet"

    def test_two_words(self):
        assert _name_to_gameref("blind_rage") == "BlindRage"

    def test_numeric_in_name(self):
        assert _name_to_gameref("forma_blueprint") == "FormaBlueprint"

    def test_long_name(self):
        assert _name_to_gameref("silva_and_aegis_prime_set") == "SilvaAndAegisPrimeSet"

    def test_handles_string_input(self):
        assert isinstance(_name_to_gameref("blind_rage"), str)


# ─────────────────────────────────────────────────────────────────────────────
# 2. build_resurgence_df
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildResurgenceDf:

    def test_returns_dataframe(self):
        result = build_resurgence_df(make_parts_df(), make_sets_df())
        assert isinstance(result, pd.DataFrame)

    def test_contains_resurgence_parts(self):
        result = build_resurgence_df(make_parts_df(), make_sets_df())
        assert "harrow_prime_neuroptics" in result["name"].values

    def test_contains_resurgence_sets(self):
        result = build_resurgence_df(make_parts_df(), make_sets_df())
        assert "harrow_prime_set" in result["name"].values

    def test_non_resurgence_items_excluded(self):
        result = build_resurgence_df(make_parts_df(), make_sets_df())
        assert "ash_prime_neuroptics" not in result["name"].values

    def test_has_start_column(self):
        result = build_resurgence_df(make_parts_df(), make_sets_df())
        assert "start" in result.columns

    def test_has_end_column(self):
        result = build_resurgence_df(make_parts_df(), make_sets_df())
        assert "end" in result.columns

    def test_start_end_are_datetime(self):
        result = build_resurgence_df(make_parts_df(), make_sets_df())
        assert pd.api.types.is_datetime64_any_dtype(result["start"])
        assert pd.api.types.is_datetime64_any_dtype(result["end"])




# ─────────────────────────────────────────────────────────────────────────────
# 4. clean_orders — other path (empty rarity_dict + empty resurgance_df)
# ─────────────────────────────────────────────────────────────────────────────

class TestCleanOrdersOtherPath:

    def make_df(self):
        return pd.DataFrame([
            make_other_order_row(),
            make_other_order_row(
                name="adaptation",
                gameRef="Adaptation",
                tags="mod",
            ),
        ])

    def test_returns_dataframe(self):
        result = clean_orders(self.make_df(), {}, pd.DataFrame())
        assert isinstance(result, pd.DataFrame)

    def test_base_name_equals_name(self):
        result    = clean_orders(self.make_df(), {}, pd.DataFrame())
        base_name = result[result["name"] == "blind_rage"]["base_name"].iloc[0]
        assert base_name == "blind_rage"

    def test_vaulted_set_to_false(self):
        result = clean_orders(self.make_df(), {}, pd.DataFrame())
        assert (result["vaulted"] == False).all()

    def test_rarity_filled_with_RARE(self):
        result = clean_orders(self.make_df(), {}, pd.DataFrame())
        assert (result["rarity"] == "RARE").all()

    def test_resurgance_set_to_false(self):
        result = clean_orders(self.make_df(), {}, pd.DataFrame())
        assert (result["resurgance"] == False).all()

    def test_missing_gameref_filled_from_name(self):
        df            = self.make_df()
        df["gameRef"] = np.nan
        result        = clean_orders(df, {}, pd.DataFrame())
        gameref_col   = "gameref" if "gameref" in result.columns else "gameRef"
        assert result[gameref_col].iloc[0] == "BlindRage"

    def test_gameref_renamed_to_lowercase(self):
        result = clean_orders(self.make_df(), {}, pd.DataFrame())
        assert "gameref"  in result.columns
        assert "gameRef" not in result.columns


# ─────────────────────────────────────────────────────────────────────────────
# 5. clean_orders — mixed prime + other
# ─────────────────────────────────────────────────────────────────────────────

class TestCleanOrdersMixed:

    def make_df(self):
        return pd.DataFrame([
            make_prime_order_row(name="ash_prime_set", gameRef="AshPrimeSet", vaulted=None),
            make_other_order_row(name="blind_rage",    gameRef="BlindRage"),
        ])

    def test_both_items_present(self):
        result = clean_orders(self.make_df(), {}, make_resurgance_df())
        names  = result["name"].tolist()
        assert "ash_prime_set" in names
        assert "blind_rage"    in names

    def test_has_required_columns(self):
        result   = clean_orders(self.make_df(), {}, make_resurgance_df())
        required = [
            "name", "type", "platinum", "quantity", "perTrade",
            "vaulted", "date", "rarity", "resurgance",
            "base_name", "datetime_collected", "gameref",
        ]
        for col in required:
            assert col in result.columns, f"Missing column: {col}"

    def test_no_gameRef_in_output(self):
        result = clean_orders(self.make_df(), {}, make_resurgance_df())
        assert "gameRef" not in result.columns

    def test_row_count_preserved(self):
        df     = self.make_df()
        result = clean_orders(df, {}, make_resurgance_df())
        assert len(result) == len(df)

    def test_platinum_is_integer(self):
        result = clean_orders(self.make_df(), {}, make_resurgance_df())
        assert result["platinum"].dtype == int