"""Configuration utilities for the Streamlit application."""
from __future__ import annotations

import os
from typing import Any

import streamlit as st


def _read_from_secrets(path: tuple[str, ...]) -> str | None:
    """Traverse Streamlit secrets using a key path and return the value if present."""

    current: Any = st.secrets
    for key in path:
        if key not in current:
            return None
        current = current[key]
    return str(current)


def get_database_uri() -> str:
    """Return the database URI from Streamlit secrets or environment variables.

    The lookup order is:
    1. Streamlit secrets under ``uri``, ``database.uri``, or ``postgres.uri``.
    2. ``DATABASE_URI`` environment variable.
    """

    secret_paths = (("uri",), ("database", "uri"), ("postgres", "uri"))
    for path in secret_paths:
        value = _read_from_secrets(path)
        if value:
            return _normalize_postgres_uri(value)

    env_uri = os.getenv("DATABASE_URI")
    if env_uri:
        return _normalize_postgres_uri(env_uri)

    raise RuntimeError(
        "Database URI not found. Add it to Streamlit secrets or set DATABASE_URI."
    )


def _normalize_postgres_uri(uri: str) -> str:
    """Coerce postgres URIs to the psycopg3 driver if none is provided."""

    if uri.startswith("postgresql+"):
        return uri

    # Handle the common shorthand some providers still use.
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    if uri.startswith("postgresql://"):
        return uri.replace("postgresql://", "postgresql+psycopg://", 1)

    return uri
