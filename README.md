# 🏙️ Colombo Apartment Data Collection System

*A Streamlit-based data entry + visualization platform for building a long-term apartment dataset for ML analysis.*

---

## 📌 Overview

This project is a lightweight **Streamlit web application** built to continuously collect structured data about apartments in **Colombo, Sri Lanka**—both **rent** and **sale** listings.
The goal is to build a **clean, ML-ready dataset** over months, enabling analysis, price modeling, trend detection, and deeper domain knowledge.

The app currently supports:

* 📄 **Form Page** – Add structured apartment data
* 📊 **Table Page** – View all collected data with filters
* 💾 **CSV storage (initial version)**
* 🗄️ **PostgreSQL storage (upgraded version)**—recommended for long-term use

The entire stack is built with **Python**, keeping the project tightly aligned with future machine learning workflows.

---

## 🧱 Architecture

```
Streamlit App (UI + Frontend)
        ↓
Business Logic (Validation + Processing)
        ↓
Data Layer:
    - v1: CSV (local storage)
    - v2: PostgreSQL via SQLAlchemy (production)
```

### Why Streamlit?

* Very fast development
* Python-native
* Great for incremental upgrades
* Free deployment on Streamlit Cloud
* Easy integration with ML models later

### Why PostgreSQL?

* Best relational DB for analytical workloads
* Free on Supabase, Neon, Railway
* Accessible from both Streamlit AND Jupyter notebooks
* Scales cleanly when the dataset grows

---

## 🚀 Features

### 🏗️ Data Entry Form

Collectors can enter structured data for each apartment, including:

* Transaction Type (Rent / Sale)
* Posted Date
* Location / Area
* Bedrooms & Bathrooms
* Size (sqft)
* Furnished Status
* Apartment Complex
* Price Inputs:

  * Rent → Input in **Lakhs**
  * Sale → Input in **Millions**
  * Auto-calculated `price_lkr`
* Optional Notes

All inputs are validated before saving.

---

### 📊 Data Table Page

* Combines Rent + Sale entries
* Provides filtering:

  * Transaction Type
  * Location
  * Bedrooms
* Displays the dataset using `st.dataframe`
* Designed for future:

  * Sorting
  * Advanced filtering
  * Visual analytics

---

## 🗄️ Data Storage — PostgreSQL

Uses SQLAlchemy + psycopg2.

Connection URL stored in:

```
.streamlit/secrets.toml
```

Example:

```toml
[postgres]
url = "postgres://USER:PASSWORD@HOST:PORT/DBNAME"
```

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/apartment-data-streamlit.git
cd apartment-data-streamlit
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ If using PostgreSQL

Create `.streamlit/secrets.toml`:

```
[postgres]
url = "your-postgresql-connection-url"
```

### 4️⃣ Run the app locally

```bash
streamlit run app.py
```

Open:

```
http://localhost:8501
```

---

## 🌐 Deployment (Streamlit Community Cloud)

1. Push code to GitHub
2. Go to **share.streamlit.io**
3. Add a new app → Choose this repo
4. Add DB credentials under **Settings → Secrets**
5. Deploy

Streamlit Cloud will:

* Install requirements
* Run `app.py`
* Expose your public URL

---

## 🧬 Database Schema (PostgreSQL)

A single table: **`apartments`**

Contains fields for:

### Core

* `id`
* `transaction_type`
* `posted_date`
* `data_source`

### Location

* `city`, `area`, `district`, `address_line`

### Price

* `price_input_value`
* `price_input_unit` (`lakhs`/`millions`)
* `price_lkr`
* `maintenance_fee_lkr`
* `rent_frequency`

### Property Attributes

* `bedrooms`, `bathrooms`, `size_sqft`
* `furnished_status`
* `apartment_complex`
* `floor_number`, `total_floors`
* `unit_type`, `occupancy_status`

### Amenities (booleans)

* `has_swimming_pool`, `has_gym`, `has_cctv`, etc.

### Lease-Specific (Rent)

* `min_lease_months`, `key_money_months`, etc.

### Sale-Specific

* `bank_loan_eligible`, `coc_available`, etc.

### Misc

* `notes`

This schema is designed to support:

* ML models (regression, clustering)
* Long-term analytics
* Filtering & dashboarding

---

## 📂 Project Structure

```
project/
│
├── app.py                   # Main Streamlit app
├── requirements.txt         # Dependencies
├── data/                    # CSV storage (legacy)
│   ├── apartments_rent.csv
│   └── apartments_sale.csv
│
├── core/
│   ├── db.py                # SQLAlchemy engine helpers
│   ├── models.py            # SQLAlchemy models
│   └── io_utils.py          # CSV-to-DB migration helpers (optional)
│
├── notebooks/               # For future ML analysis
│   └── 01_eda_baseline.ipynb
└── README.md
```

---

## 🔄 Migration: CSV → PostgreSQL

To migrate existing CSV data:

1. Read CSVs with pandas
2. Normalize/clean if needed
3. Map columns to the `apartments` table schema
4. Insert using SQLAlchemy session

A sample migration script (`migrate_csv_to_db.py`) can be easily added.

---

## 🤖 Future Roadmap

### 🔹 Phase 1 — Data Collection (Today)

* Form input
* Table view
* PostgreSQL storage

### 🔹 Phase 2 — Data Quality Tools

* Validation rules
* Duplicate detection
* Missing-value signals

### 🔹 Phase 3 — Analytics & Visualization

* Price vs bedrooms
* Price per sqft
* Area-wise heatmaps
* Trend charts (time-series)

### 🔹 Phase 4 — ML Modeling

* Rent price prediction
* Sale price estimation
* Clustering (luxury vs budget apartments)
* Feature importance analysis

### 🔹 Phase 5 — Advanced App Features

* Predict price for a user-entered hypothetical apartment
* Compare neighborhoods
* Auto-scraping from property websites
* Alerts for unusual price deviations

---

## ✔️ Goals of This Repository

This project is built to:

* Maintain a **clean, structured dataset** for Sri Lankan apartment listings
* Serve as a platform for **daily data collection**
* Provide an upgrade-friendly architecture
* Act as the foundation for **future ML research**
* Allow fast iteration and deployment using Streamlit

---

## 🧑‍💻 Contributing

This is primarily a personal research tool, but the structure supports:

* Adding new fields
* Adding new pages
* Upgrading the data model
* Incorporating ML models
* Data visualization dashboards

PRs and enhancements are welcome.

---

## 📜 License

MIT License – free to use, modify, and distribute.

---

## 📬 Contact

For questions or enhancements:
- **Developer:** *Damika Anupama*
- **Location:** Colombo, Sri Lanka
- **Focus Areas:** Data Science, ML, Real Estate Analytics

