"""Page handlers for the Streamlit navigation."""
from __future__ import annotations

import streamlit as st

from app_core.db import fetch_apartments, insert_apartment
from app_core.forms import build_apartment_form
from app_core.table import render_table


def page_add_apartment() -> None:
    """Render the Add Apartment page."""

    st.header("Add Apartment")
    st.write(
        "Fill in the details of an apartment in Sri Lanka. Required fields are validated."
    )

    payload = build_apartment_form()
    if payload is None:
        return

    try:
        insert_apartment(payload)
        st.success("Apartment saved successfully!")
    except Exception as exc:  # pylint: disable=broad-except
        st.error(f"Error while saving the apartment: {exc}")


def page_view_data() -> None:
    """Render the data viewing page."""

    st.header("View Collected Apartment Data")

    try:
        df = fetch_apartments()
    except Exception as exc:  # pylint: disable=broad-except
        st.error(f"Error while loading data: {exc}")
        return

    if df.empty:
        st.info("No data found yet. Please add some apartments first.")
        return

    render_table(df)
