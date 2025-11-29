"""Reusable form helper widgets."""
from __future__ import annotations

from typing import Optional

import streamlit as st


def optional_text(label: str, *, help_text: str | None = None) -> Optional[str]:
    """Return trimmed text input or None if left blank."""

    value = st.text_input(label, help=help_text)
    return value.strip() if value.strip() else None


def optional_select(label: str, options: list[str]) -> Optional[str]:
    """Return selected option or None when no choice is made."""

    value = st.selectbox(label, ["--"] + options)
    return value if value != "--" else None


def number_input_int(
    label: str, *, min_value: int = 0, step: int = 1, value: int = 0
) -> int:
    """Integer number input with consistent defaults."""

    return int(st.number_input(label, min_value=min_value, step=step, value=value))


def number_input_float(
    label: str,
    *,
    min_value: float = 0.0,
    step: float = 0.1,
    format_str: str = "%.2f",
    value: float = 0.0,
) -> float:
    """Floating point number input with consistent defaults."""

    return float(
        st.number_input(
            label,
            min_value=min_value,
            step=step,
            format=format_str,
            value=value,
        )
    )


def checkbox(label: str, *, value: bool = False) -> bool:
    """Checkbox wrapper returning a bool."""

    return bool(st.checkbox(label, value=value))
