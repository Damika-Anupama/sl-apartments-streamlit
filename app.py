"""Streamlit app for collecting apartment data backed by PostgreSQL (Supabase)."""

import os
from datetime import date
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# ---------- CONFIG ----------
# Column order mirrors the apartments table schema.
APARTMENT_COLUMNS: List[str] = [
    "id",
    "transaction_type",
    "posted_date",
    "data_source",
    "scraped_date",
    "city",
    "area",
    "district",
    "address_line",
    "latitude",
    "longitude",
    "price_input_value",
    "price_input_unit",
    "price_lkr",
    "price_currency",
    "price_negotiable",
    "maintenance_fee_lkr",
    "maintenance_fee_per_sqft",
    "other_monthly_fees_lkr",
    "rent_frequency",
    "bedrooms",
    "bathrooms",
    "size_sqft",
    "furnished_status",
    "apartment_complex",
    "unit_type",
    "floor_number",
    "total_floors",
    "building_age_years",
    "completion_year",
    "is_brand_new",
    "occupancy_status",
    "project_name",
    "tower_name",
    "developer_name",
    "coc_available",
    "handover_status",
    "expected_completion_year",
    "has_living_room",
    "has_dining_area",
    "kitchen_type",
    "has_maids_room",
    "has_maids_bathroom",
    "has_servant_room",
    "balcony_count",
    "has_private_rooftop",
    "store_room_available",
    "parking_slots",
    "parking_type",
    "view_type",
    "is_high_floor",
    "is_corner_unit",
    "has_swimming_pool",
    "has_gym",
    "has_kids_play_area",
    "has_tennis_court",
    "has_basketball_court",
    "has_rooftop_area",
    "has_bbq_area",
    "has_clubhouse",
    "has_function_hall",
    "has_jogging_track",
    "has_spa",
    "has_sauna",
    "has_steam_room",
    "has_jacuzzi",
    "has_daycare_center",
    "has_library",
    "has_mini_market",
    "has_medical_center",
    "has_laundry_service",
    "has_salon",
    "has_shuttle_service",
    "has_community_lounge",
    "security_24_7",
    "has_cctv",
    "is_gated_community",
    "has_access_control",
    "has_backup_generator",
    "has_elevator",
    "elevator_count",
    "garbage_disposal_system",
    "central_gas_system",
    "hot_water_system",
    "internet_fiber_ready",
    "cable_tv_ready",
    "min_lease_months",
    "max_lease_months",
    "key_money_months",
    "advance_months",
    "security_deposit_months",
    "agent_fee_months",
    "electricity_separate",
    "water_separate",
    "maintenance_included_in_rent",
    "furnished_included_in_rent",
    "short_term_allowed",
    "short_term_min_nights",
    "title_deed_type",
    "bank_loan_eligible",
    "mortgage_status",
    "installment_plan_available",
    "is_resale",
    "foreigners_only",
    "families_only",
    "bachelors_allowed",
    "no_brokers",
    "pets_allowed",
    "smoking_allowed",
    "business_use_allowed",
    "notes",
]


# ---------- DATABASE HELPERS ----------

def _get_database_uri() -> str:
    """Fetch the database URI from Streamlit secrets or environment variables."""

    secret_paths = (
        ("uri",),
        ("database", "uri"),
        ("postgres", "uri"),
    )

    for path in secret_paths:
        current: Any = st.secrets
        for key in path:
            if key not in current:
                current = None
                break
            current = current[key]
        if current:
            return str(current)

    env_uri = os.getenv("DATABASE_URI")
    if env_uri:
        return env_uri

    raise RuntimeError(
        "Database URI not found. Please add it to Streamlit secrets or DATABASE_URI env var."
    )


@st.cache_resource(show_spinner=False)
def get_engine() -> Engine:
    """Create and cache a SQLAlchemy engine with connection pooling."""

    return create_engine(_get_database_uri(), pool_pre_ping=True, future=True)


def fetch_apartments() -> pd.DataFrame:
    """Retrieve all apartments from the database."""

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


# ---------- FORM HELPERS ----------

def optional_text(label: str, help_text: Optional[str] = None) -> Optional[str]:
    value = st.text_input(label, help=help_text)
    return value.strip() if value.strip() else None


def optional_select(label: str, options: List[str]) -> Optional[str]:
    value = st.selectbox(label, ["--"] + options)
    return value if value != "--" else None


def number_input_int(label: str, min_value: int = 0, step: int = 1, value: int = 0) -> int:
    return int(st.number_input(label, min_value=min_value, step=step, value=value))


def number_input_float(
    label: str,
    min_value: float = 0.0,
    step: float = 0.1,
    format_str: str = "%.2f",
    value: float = 0.0,
) -> float:
    return float(st.number_input(label, min_value=min_value, step=step, format=format_str, value=value))


def checkbox(label: str, value: bool = False) -> bool:
    return bool(st.checkbox(label, value=value))


# ---------- UI BUILDERS ----------

def build_apartment_form() -> Optional[Dict[str, Any]]:
    """Render the apartment input form and return validated payload or None."""

    with st.form("apartment_form"):
        st.subheader("Core Details")
        transaction_type = st.radio("Transaction Type", ["rent", "sale"], horizontal=True)
        posted_date = st.date_input("Posted Date", value=date.today())
        scraped_date = st.date_input("Scraped Date", value=date.today())
        data_source = optional_text("Data Source (e.g., ikman.lk)")

        st.markdown("---")
        st.subheader("Location")
        city = optional_text("City")
        area = optional_text("Area")
        district = optional_text("District")
        address_line = optional_text("Address Line")

        col_lat, col_lng = st.columns(2)
        with col_lat:
            latitude = number_input_float("Latitude", min_value=-90.0, step=0.0001, format_str="%.6f")
        with col_lng:
            longitude = number_input_float("Longitude", min_value=-180.0, step=0.0001, format_str="%.6f")

        st.markdown("---")
        st.subheader("Pricing & Financials")
        price_input_unit = "lakhs" if transaction_type == "rent" else "millions"
        price_input_value = number_input_float(
            "Price (lakhs for rent, millions for sale)", min_value=0.0, step=0.1, format_str="%.2f"
        )
        price_currency = st.text_input("Currency", value="LKR") or "LKR"
        price_negotiable = checkbox("Price negotiable")

        maintenance_fee_lkr = number_input_int("Maintenance fee (LKR)", min_value=0, value=0)
        maintenance_fee_per_sqft = number_input_float(
            "Maintenance fee per sqft", min_value=0.0, step=0.01, format_str="%.2f"
        )
        other_monthly_fees_lkr = number_input_int("Other monthly fees (LKR)", min_value=0, value=0)
        rent_frequency = optional_select("Rent frequency", ["per_month", "per_day", "per_week", "per_year"])

        st.markdown("---")
        st.subheader("Property Attributes")
        col1, col2, col3 = st.columns(3)
        with col1:
            bedrooms = number_input_int("Bedrooms", min_value=1, value=1)
            floor_number = number_input_int("Floor number", min_value=0, value=0)
            building_age_years = number_input_float(
                "Building age (years)", min_value=0.0, step=0.1, format_str="%.2f"
            )
        with col2:
            bathrooms = number_input_int("Bathrooms", min_value=1, value=1)
            total_floors = number_input_int("Total floors", min_value=0, value=0)
            completion_year = number_input_int("Completion year", min_value=0, step=1, value=0)
        with col3:
            size_sqft = number_input_int("Size (sqft)", min_value=1, value=1, step=10)
            balcony_count = number_input_int("Balcony count", min_value=0, value=0)
            expected_completion_year = number_input_int("Expected completion year", min_value=0, step=1, value=0)

        furnished_status = st.selectbox(
            "Furnished Status",
            ["Unfurnished", "Semi Furnished", "Fully Furnished"],
        )
        apartment_complex = optional_text("Apartment Complex")
        unit_type = optional_text("Unit Type")
        is_brand_new = checkbox("Brand new")
        occupancy_status = optional_text("Occupancy status")

        project_name = optional_text("Project name")
        tower_name = optional_text("Tower name")
        developer_name = optional_text("Developer name")
        coc_available = checkbox("COC available")
        handover_status = optional_text("Handover status")

        st.markdown("---")
        st.subheader("Layout & Interior")
        col_l1, col_l2, col_l3 = st.columns(3)
        with col_l1:
            has_living_room = checkbox("Living room")
            has_maids_room = checkbox("Maid's room")
            has_servant_room = checkbox("Servant room")
            has_private_rooftop = checkbox("Private rooftop")
        with col_l2:
            has_dining_area = checkbox("Dining area")
            has_maids_bathroom = checkbox("Maid's bathroom")
            store_room_available = checkbox("Store room")
            kitchen_type = optional_text("Kitchen type")
        with col_l3:
            parking_slots = number_input_int("Parking slots", min_value=0, value=0)
            parking_type = optional_text("Parking type")
            view_type = optional_text("View type (e.g., Sea, City)")
            is_high_floor = checkbox("High floor")

        is_corner_unit = checkbox("Corner unit")

        st.markdown("---")
        st.subheader("Amenities")
        col_a1, col_a2, col_a3 = st.columns(3)
        with col_a1:
            has_swimming_pool = checkbox("Swimming pool")
            has_bbq_area = checkbox("BBQ area")
            has_function_hall = checkbox("Function hall")
            has_spa = checkbox("Spa")
            has_steam_room = checkbox("Steam room")
            has_daycare_center = checkbox("Daycare center")
            has_medical_center = checkbox("Medical center")
            has_salon = checkbox("Salon")
        with col_a2:
            has_gym = checkbox("Gym")
            has_kids_play_area = checkbox("Kids play area")
            has_jogging_track = checkbox("Jogging track")
            has_sauna = checkbox("Sauna")
            has_jacuzzi = checkbox("Jacuzzi")
            has_library = checkbox("Library")
            has_laundry_service = checkbox("Laundry service")
            has_shuttle_service = checkbox("Shuttle service")
        with col_a3:
            has_tennis_court = checkbox("Tennis court")
            has_basketball_court = checkbox("Basketball court")
            has_rooftop_area = checkbox("Rooftop area")
            has_clubhouse = checkbox("Clubhouse")
            has_mini_market = checkbox("Mini market")
            has_community_lounge = checkbox("Community lounge")

        st.markdown("---")
        st.subheader("Security & Services")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            security_24_7 = checkbox("24/7 security")
            has_access_control = checkbox("Access control")
            has_backup_generator = checkbox("Backup generator")
            garbage_disposal_system = checkbox("Garbage disposal system")
            hot_water_system = checkbox("Hot water system")
        with col_s2:
            has_cctv = checkbox("CCTV")
            is_gated_community = checkbox("Gated community")
            has_elevator = checkbox("Elevator")
            central_gas_system = checkbox("Central gas system")
            internet_fiber_ready = checkbox("Internet fiber ready")
        with col_s3:
            elevator_count = number_input_int("Elevator count", min_value=0, value=0)
            cable_tv_ready = checkbox("Cable TV ready")

        st.markdown("---")
        st.subheader("Lease Details (Rent)")
        col_le1, col_le2, col_le3 = st.columns(3)
        with col_le1:
            min_lease_months = number_input_int("Min lease months", min_value=0, value=0)
            key_money_months = number_input_float("Key money (months)", min_value=0.0, step=0.1)
            electricity_separate = checkbox("Electricity separate")
            furnished_included_in_rent = checkbox("Furnished included in rent")
        with col_le2:
            max_lease_months = number_input_int("Max lease months", min_value=0, value=0)
            advance_months = number_input_float("Advance (months)", min_value=0.0, step=0.1)
            water_separate = checkbox("Water separate")
            short_term_allowed = checkbox("Short term allowed")
        with col_le3:
            maintenance_included_in_rent = checkbox("Maintenance included in rent")
            security_deposit_months = number_input_float(
                "Security deposit (months)", min_value=0.0, step=0.1
            )
            agent_fee_months = number_input_float("Agent fee (months)", min_value=0.0, step=0.1)
            short_term_min_nights = number_input_int("Short term minimum nights", min_value=0, value=0)

        st.markdown("---")
        st.subheader("Sale Details")
        col_sale1, col_sale2 = st.columns(2)
        with col_sale1:
            title_deed_type = optional_text("Title deed type")
            mortgage_status = optional_text("Mortgage status")
            is_resale = checkbox("Resale")
        with col_sale2:
            bank_loan_eligible = checkbox("Bank loan eligible")
            installment_plan_available = checkbox("Installment plan available")

        st.markdown("---")
        st.subheader("Restrictions / Target Tenants")
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            foreigners_only = checkbox("Foreigners only")
            bachelors_allowed = checkbox("Bachelors allowed")
            pets_allowed = checkbox("Pets allowed")
        with col_r2:
            families_only = checkbox("Families only")
            no_brokers = checkbox("No brokers")
            smoking_allowed = checkbox("Smoking allowed")
        with col_r3:
            business_use_allowed = checkbox("Business use allowed")

        notes = st.text_area("Notes", height=120)

        submitted = st.form_submit_button("Save Apartment")

    if not submitted:
        return None

    errors: List[str] = []
    if price_input_value <= 0:
        errors.append("Price must be greater than 0.")
    if bedrooms <= 0:
        errors.append("Bedrooms must be greater than 0.")
    if bathrooms <= 0:
        errors.append("Bathrooms must be greater than 0.")
    if size_sqft <= 0:
        errors.append("Size (sqft) must be greater than 0.")

    if errors:
        st.error("Please fix the following issues before saving:")
        for err in errors:
            st.write(f"- {err}")
        return None

    price_multiplier = 100_000 if price_input_unit == "lakhs" else 1_000_000
    price_lkr = int(price_input_value * price_multiplier)

    payload: Dict[str, Any] = {
        "transaction_type": transaction_type,
        "posted_date": posted_date.isoformat(),
        "data_source": data_source,
        "scraped_date": scraped_date.isoformat() if scraped_date else None,
        "city": city,
        "area": area,
        "district": district,
        "address_line": address_line,
        "latitude": latitude,
        "longitude": longitude,
        "price_input_value": price_input_value,
        "price_input_unit": price_input_unit,
        "price_lkr": price_lkr,
        "price_currency": price_currency,
        "price_negotiable": price_negotiable,
        "maintenance_fee_lkr": maintenance_fee_lkr,
        "maintenance_fee_per_sqft": maintenance_fee_per_sqft,
        "other_monthly_fees_lkr": other_monthly_fees_lkr,
        "rent_frequency": rent_frequency,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "size_sqft": size_sqft,
        "furnished_status": furnished_status,
        "apartment_complex": apartment_complex,
        "unit_type": unit_type,
        "floor_number": floor_number,
        "total_floors": total_floors,
        "building_age_years": building_age_years,
        "completion_year": completion_year,
        "is_brand_new": is_brand_new,
        "occupancy_status": occupancy_status,
        "project_name": project_name,
        "tower_name": tower_name,
        "developer_name": developer_name,
        "coc_available": coc_available,
        "handover_status": handover_status,
        "expected_completion_year": expected_completion_year,
        "has_living_room": has_living_room,
        "has_dining_area": has_dining_area,
        "kitchen_type": kitchen_type,
        "has_maids_room": has_maids_room,
        "has_maids_bathroom": has_maids_bathroom,
        "has_servant_room": has_servant_room,
        "balcony_count": balcony_count,
        "has_private_rooftop": has_private_rooftop,
        "store_room_available": store_room_available,
        "parking_slots": parking_slots,
        "parking_type": parking_type,
        "view_type": view_type,
        "is_high_floor": is_high_floor,
        "is_corner_unit": is_corner_unit,
        "has_swimming_pool": has_swimming_pool,
        "has_gym": has_gym,
        "has_kids_play_area": has_kids_play_area,
        "has_tennis_court": has_tennis_court,
        "has_basketball_court": has_basketball_court,
        "has_rooftop_area": has_rooftop_area,
        "has_bbq_area": has_bbq_area,
        "has_clubhouse": has_clubhouse,
        "has_function_hall": has_function_hall,
        "has_jogging_track": has_jogging_track,
        "has_spa": has_spa,
        "has_sauna": has_sauna,
        "has_steam_room": has_steam_room,
        "has_jacuzzi": has_jacuzzi,
        "has_daycare_center": has_daycare_center,
        "has_library": has_library,
        "has_mini_market": has_mini_market,
        "has_medical_center": has_medical_center,
        "has_laundry_service": has_laundry_service,
        "has_salon": has_salon,
        "has_shuttle_service": has_shuttle_service,
        "has_community_lounge": has_community_lounge,
        "security_24_7": security_24_7,
        "has_cctv": has_cctv,
        "is_gated_community": is_gated_community,
        "has_access_control": has_access_control,
        "has_backup_generator": has_backup_generator,
        "has_elevator": has_elevator,
        "elevator_count": elevator_count,
        "garbage_disposal_system": garbage_disposal_system,
        "central_gas_system": central_gas_system,
        "hot_water_system": hot_water_system,
        "internet_fiber_ready": internet_fiber_ready,
        "cable_tv_ready": cable_tv_ready,
        "min_lease_months": min_lease_months,
        "max_lease_months": max_lease_months,
        "key_money_months": key_money_months,
        "advance_months": advance_months,
        "security_deposit_months": security_deposit_months,
        "agent_fee_months": agent_fee_months,
        "electricity_separate": electricity_separate,
        "water_separate": water_separate,
        "maintenance_included_in_rent": maintenance_included_in_rent,
        "furnished_included_in_rent": furnished_included_in_rent,
        "short_term_allowed": short_term_allowed,
        "short_term_min_nights": short_term_min_nights,
        "title_deed_type": title_deed_type,
        "bank_loan_eligible": bank_loan_eligible,
        "mortgage_status": mortgage_status,
        "installment_plan_available": installment_plan_available,
        "is_resale": is_resale,
        "foreigners_only": foreigners_only,
        "families_only": families_only,
        "bachelors_allowed": bachelors_allowed,
        "no_brokers": no_brokers,
        "pets_allowed": pets_allowed,
        "smoking_allowed": smoking_allowed,
        "business_use_allowed": business_use_allowed,
        "notes": notes.strip() if notes else None,
    }

    return payload


# ---------- TABLE RENDERING ----------

def render_table(df: pd.DataFrame) -> None:
    st.subheader("Collected Apartments")

    filter_type = st.selectbox("Filter by transaction type", ["All", "rent", "sale"])
    if filter_type != "All":
        df = df[df["transaction_type"] == filter_type]

    district_filter = st.text_input("Filter by district")
    if district_filter:
        df = df[df["district"].fillna("").str.contains(district_filter, case=False)]

    sort_option = st.selectbox(
        "Sort by",
        [
            "posted_date (newest first)",
            "price_lkr (low to high)",
            "price_lkr (high to low)",
            "size_sqft (high to low)",
        ],
    )

    if sort_option == "posted_date (newest first)":
        df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")
        df = df.sort_values(by="posted_date", ascending=False)
    elif sort_option == "price_lkr (low to high)":
        df = df.sort_values(by="price_lkr", ascending=True)
    elif sort_option == "price_lkr (high to low)":
        df = df.sort_values(by="price_lkr", ascending=False)
    elif sort_option == "size_sqft (high to low)":
        df = df.sort_values(by="size_sqft", ascending=False)

    missing_cols = [col for col in APARTMENT_COLUMNS if col not in df.columns]
    for col in missing_cols:
        df[col] = None

    st.dataframe(df.reset_index(drop=True)[APARTMENT_COLUMNS])


# ---------- PAGE HANDLERS ----------

def page_add_apartment() -> None:
    st.header("Add Apartment")
    st.write("Fill in the details of an apartment in Sri Lanka. Required fields are validated.")

    payload = build_apartment_form()
    if payload is None:
        return

    try:
        insert_apartment(payload)
        st.success("Apartment saved successfully!")
    except Exception as exc:  # pylint: disable=broad-except
        st.error(f"Error while saving the apartment: {exc}")


def page_view_data() -> None:
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


# ---------- MAIN APP ----------

def main() -> None:
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
