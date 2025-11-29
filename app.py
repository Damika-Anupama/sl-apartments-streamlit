"""Streamlit entrypoint for the Sri Lanka apartments collector."""
from __future__ import annotations

import streamlit as st

from app_core.pages import page_add_apartment, page_view_data


def main() -> None:
    """Render the Streamlit application with navigation."""

    st.set_page_config(
        page_title="Sri Lanka Apartments Collector",
        page_icon="🏙️",
        layout="wide",
    )

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Add Apartment", "View Data"],
    )

    if page == "Add Apartment":
        page_add_apartment()
    else:
        page_view_data()


if __name__ == "__main__":
    main()
