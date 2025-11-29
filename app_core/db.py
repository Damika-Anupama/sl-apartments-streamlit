"""Database helpers for interacting with the apartments table."""
from __future__ import annotations

import os
import socket
from typing import Any, Dict

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app_core.config import get_database_uri
from app_core.constants import APARTMENT_COLUMNS


@st.cache_resource(show_spinner=False)
def get_engine() -> Engine:
    """Create and cache a SQLAlchemy engine with connection pooling."""

    connect_args = {}
    if os.getenv("DATABASE_PREFER_IPV4", "").lower() in {"1", "true", "yes"}:
        connect_args["gai_family"] = socket.AF_INET

    return create_engine(
        get_database_uri(),
        pool_pre_ping=True,
        future=True,
        connect_args=connect_args or None,
    )


def fetch_apartments() -> pd.DataFrame:
    """Retrieve all apartments from the database sorted by posted_date and id."""

    engine = get_engine()
    query = text("SELECT * FROM apartments ORDER BY posted_date DESC, id DESC")
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df


def insert_apartment(payload: Dict[str, Any]) -> None:
    """Insert a new apartment row using a parameterized query."""

    columns = [col for col in APARTMENT_COLUMNS if col != "id"]
    col_names = ", ".join(columns)
    placeholders = ", ".join([f":{col}" for col in columns])
    query = text(f"INSERT INTO apartments ({col_names}) VALUES ({placeholders})")

    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(query, payload)
