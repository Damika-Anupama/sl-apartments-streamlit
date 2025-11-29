"""Configuration utilities for the Streamlit application."""
from __future__ import annotations

import os
from typing import Any

import streamlit as st
from sqlalchemy.engine import make_url


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
            return _apply_overrides(_normalize_postgres_uri(value))

    env_uri = os.getenv("DATABASE_URI")
    if env_uri:
        return _apply_overrides(_normalize_postgres_uri(env_uri))

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


def _apply_overrides(uri: str) -> str:
    """Apply optional environment-based overrides to the database URI.

    Two tweaks are supported to improve connectivity on IPv6-restricted networks:

    - ``DATABASE_IPV4_HOST``: replace the host portion of the URI with an IPv4
      address or hostname.
    - ``DATABASE_IPV4_PORT``: optionally override the port in tandem with the
      host change.

    This is useful when the default secret contains an IPv6-only endpoint that
    fails with "Cannot assign requested address" on some hosting providers.
    """

    override_host = os.getenv("DATABASE_IPV4_HOST")
    override_port = os.getenv("DATABASE_IPV4_PORT")
    if not override_host:
        return uri

    url = make_url(uri)
    url = url.set(host=override_host)

    if override_port:
        url = url.set(port=int(override_port))

    # Render with the password visible so SQLAlchemy can re-parse it downstream.
    return url.render_as_string(hide_password=False)
