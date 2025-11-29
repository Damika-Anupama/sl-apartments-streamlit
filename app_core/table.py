"""Utilities for rendering the apartments table."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from app_core.constants import APARTMENT_COLUMNS


SORT_OPTIONS = [
    "posted_date (newest first)",
    "price_lkr (low to high)",
    "price_lkr (high to low)",
    "size_sqft (high to low)",
]


def _apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply UI filters to the dataframe and return the filtered result."""

    filter_type = st.selectbox("Filter by transaction type", ["All", "rent", "sale"])
    if filter_type != "All":
        df = df[df["transaction_type"] == filter_type]

    district_filter = st.text_input("Filter by district")
    if district_filter:
        df = df[df["district"].fillna("").str.contains(district_filter, case=False)]

    return df


def _apply_sort(df: pd.DataFrame, sort_option: str) -> pd.DataFrame:
    """Sort the dataframe based on the selected option."""

    if sort_option == "posted_date (newest first)":
        df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")
        df = df.sort_values(by="posted_date", ascending=False)
    elif sort_option == "price_lkr (low to high)":
        df = df.sort_values(by="price_lkr", ascending=True)
    elif sort_option == "price_lkr (high to low)":
        df = df.sort_values(by="price_lkr", ascending=False)
    elif sort_option == "size_sqft (high to low)":
        df = df.sort_values(by="size_sqft", ascending=False)

    return df


def render_table(df: pd.DataFrame) -> None:
    """Render filters and the apartments dataframe."""

    st.subheader("Collected Apartments")
    df = _apply_filters(df)

    sort_option = st.selectbox("Sort by", SORT_OPTIONS)
    df = _apply_sort(df, sort_option)

    missing_cols = [col for col in APARTMENT_COLUMNS if col not in df.columns]
    for col in missing_cols:
        df[col] = None

    st.dataframe(df.reset_index(drop=True)[APARTMENT_COLUMNS])
