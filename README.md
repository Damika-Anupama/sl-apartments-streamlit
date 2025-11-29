# 🏙️ Colombo Apartment Data Collection System

*A Streamlit application for capturing and exploring Sri Lankan apartment listings with PostgreSQL-backed storage.*

---

## 📌 Overview

This project is a **Streamlit web app** that records detailed apartment listings (rent or sale) across Sri Lanka. Data is persisted to a **Supabase-hosted PostgreSQL** database using SQLAlchemy, making it suitable for long-term growth and future ML workflows.

Key capabilities:

- 📄 **Add Apartment page** – comprehensive form covering the full `apartments` table schema with validation and price normalization.
- 📊 **View Data page** – filter, sort, and browse all stored rows directly from PostgreSQL.
- 🧱 **Modular codebase** – separated config, database helpers, form builders, and table rendering for maintainability.

---

## 🧱 Architecture

```
Streamlit (app.py)
    ├── app_core.config      # secrets/env lookup for DB URI
    ├── app_core.db          # SQLAlchemy engine + parameterized queries
    ├── app_core.forms       # full apartment form + validation
    ├── app_core.table       # filtering/sorting + dataframe rendering
    └── app_core.pages       # page routing for navigation
```

### Why PostgreSQL (Supabase)?

- Reliable relational store with strong typing for the rich apartment schema.
- Managed hosting and SSL out of the box from Supabase.
- Easy to query from notebooks for analytics/ML.

---

## 🗄️ Data Storage

- **Primary**: PostgreSQL via SQLAlchemy (tested with Supabase). Connections use `pool_pre_ping=True` for resiliency and are cached in Streamlit with `st.cache_resource`.
- **Schema**: The app targets the provided `apartments` table (see Supabase DDL) and uses parameterized inserts to avoid SQL injection.

Configure the database URI in one of the following locations (checked in order):

1. `.streamlit/secrets.toml` – `uri`, `database.uri`, or `postgres.uri` keys.
2. Environment variable `DATABASE_URI`.

Example secrets file:

```toml
uri = "postgresql://USER:PASSWORD@HOST:5432/DBNAME"
```

---

## 🚀 Getting Started

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Provide the database connection

Populate `.streamlit/secrets.toml` or set `DATABASE_URI` as described above.

### 3️⃣ Run the app

```bash
streamlit run app.py
```

Streamlit will start a local server and open the app in your browser.

---

## 🏗️ Data Entry Form

- Captures every field from the `apartments` schema, including pricing, location, amenities, security, lease/sale specifics, and restrictions.
- Auto-computes `price_lkr` based on transaction type (`lakhs` for rent, `millions` for sale).
- Validates critical numeric fields (price, bedrooms, bathrooms, size) before submission.

---

## 📊 Data Table Page

- Reads directly from PostgreSQL.
- Filters: transaction type and district text search.
- Sorting options: posted date (newest first), price (low/high), and size (high to low).
- Displays all schema columns in a consistent order for easy export or analysis.

---

## 📂 Project Structure

```
sl-apartments-streamlit/
├── app.py                 # Streamlit entrypoint
├── app_core/
│   ├── config.py          # DB URI lookup
│   ├── constants.py       # column ordering aligned to schema
│   ├── db.py              # cached SQLAlchemy engine + queries
│   ├── form_helpers.py    # reusable form widgets
│   ├── forms.py           # full apartment form + validation
│   ├── pages.py           # page routing logic
│   └── table.py           # filters, sorting, and dataframe display
├── data/                  # legacy CSV folder (unused with PostgreSQL)
└── requirements.txt
```

---

## 🧪 Testing

Run a quick syntax check to ensure modules import cleanly:

```bash
python -m compileall app.py app_core
```

---

## 🤖 Future Ideas

- Enrich filtering (price ranges, bedroom counts, amenities).
- Add analytics charts (price trends, price per sqft, area comparisons).
- Provide CSV export or notebook-friendly APIs for ML experiments.

---

## 📜 License

MIT License – free to use, modify, and distribute.

---

## 📬 Contact

For questions or enhancements:
- **Developer:** *Damika Anupama*
- **Location:** Colombo, Sri Lanka
- **Focus Areas:** Data Science, ML, Real Estate Analytics