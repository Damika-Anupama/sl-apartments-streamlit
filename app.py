import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date

# ---------- CONFIG ----------
DATA_DIR = Path("data")
RENT_CSV = DATA_DIR / "apartments_rent.csv"
SALE_CSV = DATA_DIR / "apartments_sale.csv"

COLUMNS = [
    "transaction_type",  # "Rent" | "Sale"
    "posted_date",  # YYYY-MM-DD string
    "location",
    "bedrooms",
    "bathrooms",
    "size_sqft",
    "furnished_status",  # Unfurnished / Semi Furnished / Fully Furnished
    "apartment_complex",
    "price_input_value",  # what user typed
    "price_lkr",  # normalized LKR price
    "notes",
]


# ---------- HELPER FUNCTIONS ----------

def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_csv_path(transaction_type: str) -> Path:
    if transaction_type.lower() == "rent":
        return RENT_CSV
    if transaction_type.lower() == "sale":
        return SALE_CSV
    raise ValueError(f"Unknown transaction_type: {transaction_type}")


def init_csv_if_needed(csv_path: Path):
    """Create CSV with header if it does not exist."""
    if not csv_path.exists():
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(csv_path, index=False)


def append_row_to_csv(row: dict):
    """Append a single row dict to the appropriate CSV based on transaction_type."""
    ensure_data_dir()
    transaction_type = row.get("transaction_type")
    csv_path = get_csv_path(transaction_type)
    init_csv_if_needed(csv_path)

    df_existing = pd.read_csv(csv_path)
    df_new = pd.DataFrame([row])[COLUMNS]
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_csv(csv_path, index=False)


def load_dataset(csv_path: Path, transaction_type: str) -> pd.DataFrame:
    """Load a dataset for a given transaction type and ensure required columns."""
    if not csv_path.exists():
        return pd.DataFrame(columns=COLUMNS)

    df = pd.read_csv(csv_path)
    if "transaction_type" not in df.columns:
        df["transaction_type"] = transaction_type
    else:
        df["transaction_type"] = df["transaction_type"].fillna(transaction_type)

    for col in COLUMNS:
        if col not in df.columns:
            df[col] = None

    return df[COLUMNS]


def load_all_data() -> pd.DataFrame:
    """Load both rent and sale CSVs (if they exist) into a single DataFrame."""
    ensure_data_dir()
    df_rent = load_dataset(RENT_CSV, "Rent")
    df_sale = load_dataset(SALE_CSV, "Sale")

    if df_rent.empty and df_sale.empty:
        return pd.DataFrame(columns=COLUMNS)

    return pd.concat([df_rent, df_sale], ignore_index=True)


# ---------- UI HELPERS ----------

def build_apartment_form():
    """Render the apartment input form and return the row data if valid."""

    with st.form("apartment_form"):
        transaction_type = st.radio("Transaction Type", ["Rent", "Sale"], horizontal=True)

        posted_date = st.date_input(
            "Posted Date",
            value=date.today(),
            help="Date the ad was posted on the listing site.",
        )

        location = st.text_input("Location (e.g. Colombo 3, Rajagiriya)")

        col1, col2, col3 = st.columns(3)
        with col1:
            bedrooms = st.number_input("Bedrooms", min_value=0, step=1, value=0)
        with col2:
            bathrooms = st.number_input("Bathrooms", min_value=0, step=1, value=0)
        with col3:
            size_sqft = st.number_input("Size (sqft)", min_value=0, step=10, value=0)

        furnished_status = st.selectbox(
            "Furnished Status",
            ["Unfurnished", "Semi Furnished", "Fully Furnished"],
        )

        apartment_complex = st.text_input(
            "Apartment Complex (optional)",
            help="Name of the complex, e.g. Iconic Rajagiriya, Trillium, etc.",
        )

        if transaction_type == "Rent":
            price_label = "Price per month (in lakhs)"
            multiplier = 100_000
        else:
            price_label = "Price (in millions)"
            multiplier = 1_000_000

        price_input_value = st.number_input(
            price_label,
            min_value=0.0,
            step=0.1,
            format="%.2f",
        )

        price_lkr = int(price_input_value * multiplier)
        st.text_input("Price in LKR (computed)", value=str(price_lkr), disabled=True)

        notes = st.text_area("Notes (optional)", height=80)

        submitted = st.form_submit_button("Save Apartment")

        if not submitted:
            return None

        # ---------- VALIDATION ----------
        errors = []
        if not posted_date:
            errors.append("Posted date is required.")
        if not location.strip():
            errors.append("Location is required.")
        if bedrooms <= 0:
            errors.append("Bedrooms must be greater than 0.")
        if bathrooms <= 0:
            errors.append("Bathrooms must be greater than 0.")
        if size_sqft <= 0:
            errors.append("Size (sqft) must be greater than 0.")
        if price_input_value <= 0:
            errors.append("Price must be greater than 0.")

        if errors:
            st.error("Please fix the following issues before saving:")
            for e in errors:
                st.write(f"- {e}")
            return None

        return {
            "transaction_type": transaction_type,
            "posted_date": posted_date.isoformat(),
            "location": location.strip(),
            "bedrooms": int(bedrooms),
            "bathrooms": int(bathrooms),
            "size_sqft": int(size_sqft),
            "furnished_status": furnished_status,
            "apartment_complex": apartment_complex.strip(),
            "price_input_value": float(price_input_value),
            "price_lkr": price_lkr,
            "notes": notes.strip(),
        }


def render_table(df: pd.DataFrame):
    """Render filters and table for viewing stored apartments."""

    filter_type = st.selectbox("Filter by type", ["All", "Rent", "Sale"])

    df_filtered = df.copy()
    if filter_type != "All":
        df_filtered = df_filtered[df_filtered["transaction_type"] == filter_type]

    sort_by = st.selectbox(
        "Sort by",
        ["posted_date (newest first)", "price_lkr (low to high)", "price_lkr (high to low)"],
    )

    if sort_by == "posted_date (newest first)":
        df_filtered["posted_date"] = pd.to_datetime(df_filtered["posted_date"], errors="coerce")
        df_filtered = df_filtered.sort_values(by="posted_date", ascending=False)
    elif sort_by == "price_lkr (low to high)":
        df_filtered = df_filtered.sort_values(by="price_lkr", ascending=True)
    elif sort_by == "price_lkr (high to low)":
        df_filtered = df_filtered.sort_values(by="price_lkr", ascending=False)

    st.dataframe(df_filtered.reset_index(drop=True))


# ---------- UI PAGES ----------

def page_add_apartment():
    st.header("Add Apartment")
    st.write("Fill in the details of an apartment in Colombo, Sri Lanka.")

    row = build_apartment_form()

    if row is None:
        return

    try:
        append_row_to_csv(row)
        st.success("Apartment saved successfully!")
    except Exception as ex:
        st.error(f"Error while saving the apartment: {ex}")


def page_view_data():
    st.header("View Collected Apartment Data")

    df = load_all_data()

    if df.empty:
        st.info("No data found yet. Please add some apartments first.")
        return

    render_table(df)


# ---------- MAIN APP ----------

def main():
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
