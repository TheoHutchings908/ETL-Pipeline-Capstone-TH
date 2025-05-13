# ETL Pipeline Capstone Project 🧀


## Overview

This repository contains a complete ETL (Extract, Transform, Load) pipeline and a Streamlit dashboard for visualizing car sales data. The pipeline extracts raw CSV data, transforms it, and loads it into a PostgreSQL database. The Streamlit app connects to the database to display interactive charts and metrics.

## Features

- **Dockerized** services for PostgreSQL, ETL, and Streamlit  
- ETL scripts to extract from CSV, transform data, and load into Postgres  
- Streamlit dashboard with filters, metrics, and visualizations  
- Configuration via environment variables and `.env` file  

## Prerequisites

- Docker & Docker Compose installed on your machine  
- (Optional) Local Python environment for development  

---

## Getting Started

1. **Clone the repo**

   ```bash
   git clone https://github.com/TheoHutchings908/ETL-Pipeline-Capstone.git
   cd ETL-Pipeline-Capstone
   ```

2. **Create `.env` file**  
   Copy `.env.example` or create a `.env` with:

   ```dotenv
   POSTGRES_USER=etl_user
   POSTGRES_PASSWORD=DfIsTheBest
   POSTGRES_DB=car_sales
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
   ```

3. **Build & run services separately**  

   - **Start database & initialize schema**  
  
     ```bash
     docker-compose up -d db
     ```

     Wait until the `db` service is healthy.

   - **Run ETL to load data**  

     ```bash
     docker-compose build etl
     docker-compose run --rm etl
     ```

   - **Launch Streamlit dashboard**  

     ```bash
      docker-compose build streamlit
      docker-compose up streamlit
     ```

4. **Access the dashboard**  
   Open your browser and navigate to:

   ```
   http://localhost:8501
   ```

---

## Services

- **db**: PostgreSQL 15  
- **etl**: Python ETL pipeline (entry: `scripts/run_etl.py`)  
- **streamlit**: Streamlit dashboard (entry: `app/streamlit_app.py`)  

---

## Project Structure

```
ETL-Pipeline-Capstone/
├── Dockerfile.etl             # ETL service Dockerfile
├── Dockerfile.streamlit       # Streamlit service Dockerfile
├── docker-compose.yml         # Compose file orchestrating all services
├── .env.example               # Example environment variables file
├── setup.py                   # Package & entry-point setup
├── requirements.txt           # Python dependencies
├── src/
│   └── etl/
│       ├── extract/           # CSV extraction logic
│       ├── transform/         # Data cleaning & transformation
│       └── load/              # Postgres loading logic
│   └── utils/                 # Shared utilities (logging, config, etc.)
├── scripts/
│   └── run_etl.py             # ETL pipeline launcher
├── app/
│   ├── db_utils.py            # DB connection & queries
│   └── streamlit_app.py       # Streamlit dashboard
├── data/                      # Raw CSV data input
├── logs/                      # Log files generated at runtime
├── tests/                     # Pytest test suite
└── README.md                  # Project README (this file)
```
---

## 🛠️ Code Walkthrough

### 1. `src/etl/extract/extract.py`

- **`extract_data() -> pd.DataFrame`**  
  1. Starts a timer.  
  2. Reads `data/car_sales_data.csv` via `pd.read_csv()`.  
  3. Logs row count & execution time with `log_extract_success()`.  
  4. Returns the raw DataFrame.  
  5. On error, logs and re-raises a descriptive exception.

### 2. `src/etl/transform/clean_sales.py`

Contains helper functions to clean an incoming DataFrame:

- **`drop_duplicates(df)`**  
  Removes exact duplicate rows.
- **`drop_empty(df)`**  
  Drops rows missing required fields (`Date`, `Sale_Price`).
- **`clean_dates(df)`**  
  Coerces the `Date` column to pandas `datetime`, with invalid parsing → `NaT`.
- **`fill_numeric(df)`**  
  For numeric columns (`Car_Year`, `Sale_Price`, `Commission_Rate`, `Commission_Earned`), fills missing values with the column’s median.

### 3. `src/etl/transform/transform.py`

- **Imports & Logger**  
  - Pulls in `clean_dates`, `drop_empty`, `fill_numeric`, `drop_duplicates`.  
  - Sets up a debug‐level logger writing to `logs/transforming_data.log`.
- **`load_population_monthly() -> pd.DataFrame`**  
  - Reads `data/population.csv`, parses `date`, sorts + resets index.  
  - Logs the number of rows loaded.
- **`transform_sales(df_raw) -> pd.DataFrame`**  
  1. Standardizes column names (strips whitespace, replaces spaces/`-` with `_`).  
  2. Applies the cleaning pipeline in order:  

     ```python
     df = (
       df_raw
       .pipe(clean_dates)
       .pipe(drop_empty)
       .pipe(fill_numeric)
       .pipe(drop_duplicates)
     )
     ```

  3. Extracts a `year` from the `Date` column, then drops the temp.  
  4. Renames columns to lower‐snake case:
  
     ```text
     Date → date
     Car_Make → make
     Car_Model → model
     Sale_Price → price
     …etc.
     ```

  5. Lower-cases all column names, logs final row count, and returns the clean DataFrame.

### 4. `src/etl/load/load.py`

- **`get_engine()`**  
  Wraps SQLAlchemy’s `create_engine(...)`, reading `DATABASE_URL` from environment.
- **`write_table(df, table_name: str)`**  
  Uses `df.to_sql(table_name, engine, if_exists="replace", index=False)`  
  Logs “Wrote X rows to `table_name` @ Postgres”.
- **`write_sales(df)` / `write_population(df)`**  
  Thin wrappers that call `write_table(df, "sales")` and `write_table(df, "population")`, respectively.

### 5. `src/db_utils.py`

- **`get_engine()`** (duplicate helper for app side)  
- **`get_available_years() -> List[int]`**  
  Runs a SQL query against the `sales` table:  

  ```sql
  SELECT DISTINCT EXTRACT(YEAR FROM date)::INT AS year
    FROM sales
    ORDER BY year;
  ```

  Returns a Python list of available years.
- **`load_all_sales() -> pd.DataFrame`**  
  Reads `SELECT * FROM sales`, parses `date` column, returns full DataFrame.

### 6. `src/utils/logging_utils.py`

Utility functions to standardize your logging:

- **`setup_logger(name, logfile, level)`**  
  Configures `logging` with a rotating file handler, timestamped format, etc.
- **`log_extract_success(logger, data_type, shape, elapsed, threshold)`**  
  If extract runs faster than expected, logs at INFO; if slower, warns.

### 7. `src/app/streamlit_app.py`

A Streamlit app that:

1. **Loads** all sales via `load_all_sales()`  
2. **Normalizes** columns (`date`, `year`, `month`)  
3. **Sidebar Filters**: year & make multi-select  
4. **Key Metrics Row**:  
   - Total sales count  
   - Total revenue  
   - Avg. price  
   - Top purchaser age group  
5. **Revenue by Make** (Plotly bar chart)  
6. **Sales vs Population Over Time** (dual-axis Plotly line chart)  
   - Joins `sales` to `population` monthly  
   - Strips out low-volume outliers  
7. **Fuel Type Distribution** (Plotly donut chart)  
8. **Avg. Price by Gender & Payment Method** (Altair stacked bar)  
9. **Data Explorer**: expandable table + CSV download button  


## Author

Theo Hutchings  
[theohutchings2002@gmail.com](mailto:theohutchings2002@gmail.com) 