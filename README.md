# ETL Pipeline Capstone Project

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

## Author

Theo Hutchings  
[theohutchings2002@gmail.com](mailto:theohutchings2002@gmail.com) 