# 🏠 Walmart Data Engineering Pipeline with Airflow, Databricks & dbt

## 📋 Overview
![Walmart Data Engineering Pipeline](walmart_dbt_project/Walmart%20Project.png)

This project demonstrates an end-to-end modern data engineering pipeline built using **Apache Airflow, Databricks, and dbt**. The pipeline orchestrates CDC ingestion from Databricks source tables, runs dbt transformations across technical and business layers, and loads analytics-ready datasets.

Rather than focusing only on SQL transformations, this project emphasizes production-friendly orchestration, modular dbt project structure, incremental data loading, and SCD-style snapshot tracking.

### Key Highlights

- Built a multi-stage data pipeline orchestrated by Airflow.
- Integrated Databricks source tables with dbt models.
- Organized transformations into technical and business layers.
- Created reusable dbt models and ephemeral transformations for maintainability.
- Used dbt snapshots for historical dimension tracking.
- Implemented source freshness checks and automated testing via Airflow tasks.

---

# 🏗️ Architecture

```
Databricks Source Tables
    │
    ▼
Bronze / Source Layer
    │
    ▼
Silver Layer
    │   ├── silver_t (technical)
    │   └── silver_b (business)
    │
    ▼
Gold Layer
    │   ├── One Big Table (obt_b)
    │   ├── Fact Table (fact_orders)
    │   └── Ephemeral Models
    │
    ▼
Snapshots / Dimensions
```

---

# 🛠️ Technology Stack

| Category | Technologies |
|-----------|--------------|
| Orchestration | Apache Airflow |
| Data Platform | Databricks |
| Transformation | dbt Core |
| Language | SQL, Jinja, Python |
| Scheduling | Airflow DAGs |
| Version Control | Git |
| Historical Tracking | dbt Snapshots |

# 📊 Data Model

The project follows a layered architecture with source ingestion, technical/business transformations, and analytics-ready gold outputs.

## 🥉 Bronze / Source Layer

The Bronze layer uses Databricks source tables with minimal transformation and serves as the raw input for dbt.

Models / Tables:
- `orders`
- `customers`
- `products`
- `order_items`
- `stores`
- `employees`

**Features**
- Source definitions stored in `models/source/sources.yml`
- Incremental ingestion by Databricks CDC process
- Source freshness validation in Airflow

---

## 🥈 Silver Layer

The Silver layer standardizes and enriches the Bronze data with technical and business transformations.

Models:
- `silver_t.customers_t`
- `silver_t.employees_t`
- `silver_t.order_items_t`
- `silver_t.orders_t`
- `silver_t.products_t`
- `silver_t.stores_t`
- `silver_b.obt_b`

**Transformations**
- Technical data modeling for core domain tables
- Business logic applied in the `silver_b` layer
- Reusable ephemeral models in `models/gold/ephemeral`

---

## 🥇 Gold Layer

The Gold layer contains analytics-ready outputs and denormalized data for downstream consumption.

Models:
- `models/gold/obt_b.sql`
- `models/gold/fact/fact_orders.sql`
- `models/gold/ephemeral/eph_customers.sql`
- `models/gold/ephemeral/eph_employees.sql`
- `models/gold/ephemeral/eph_orders.sql`
- `models/gold/ephemeral/eph_products.sql`
- `models/gold/ephemeral/eph_stores.sql`

The Gold layer supports reporting and downstream consumption via consolidated fact and ephemeral datasets.

---

## 📸 Slowly Changing Dimensions (SCD Style)

Historical changes are tracked using dbt snapshots.

Dimensions:
- `dim_customers`
- `dim_employees`
- `dim_orders`
- `dim_products`
- `dim_stores`

These snapshots preserve history while supporting point-in-time analysis.

---

# 📁 Project Structure

```text
airflow_dbt_project/
│
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
├── dags/
│   └── orchestrate.py
├── config/
│   └── airflow.cfg
├── walmart_project/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── README.md
│   ├── models/
│   │   ├── gold/
│   │   │   ├── fact/
│   │   │   │   └── fact_orders.sql
│   │   │   ├── ephemeral/
│   │   │   │   ├── eph_customers.sql
│   │   │   │   ├── eph_employees.sql
│   │   │   │   ├── eph_orders.sql
│   │   │   │   ├── eph_products.sql
│   │   │   │   └── eph_stores.sql
│   │   │   └── obt_b.sql
│   │   ├── silver_b/
│   │   │   └── obt_b.sql
│   │   ├── silver_t/
│   │   │   ├── customers_t.sql
│   │   │   ├── employees_t.sql
│   │   │   ├── order_items_t.sql
│   │   │   ├── orders_t.sql
│   │   │   ├── products_t.sql
│   │   │   ├── stores_t.sql
│   │   │   └── properties.yml
│   │   └── source/
│   │       └── sources.yml
│   ├── macros/
│   │   └── custom_schema.sql
│   ├── snapshots/
│   │   ├── dim_customers.yml
│   │   ├── dim_employees.yml
│   │   ├── dim_orders.yml
│   │   ├── dim_products.yml
│   │   └── dim_stores.yml
│   └── tests/
│       └── test_obt.sql
```

### Folder Overview

| Folder | Purpose |
|---------|---------|
| **dags/** | Airflow DAGs and orchestration logic |
| **models/** | dbt transformation models |
| **macros/** | Reusable dbt macros and Jinja helpers |
| **snapshots/** | dbt snapshots for historical tracking |
| **tests/** | Custom dbt tests |
| **config/** | Airflow configuration |
| **walmart_project/** | dbt project root |

---

## 🚀 Orchestration Flow

The Airflow DAG defined in `dags/orchestrate.py` runs this flow:

1. `ingest_cdc` triggers Databricks CDC ingestion.
2. `clean_target` clears dbt target and logs.
3. `source_freshness` runs `dbt source freshness`.
4. `silver_technical` runs dbt models in `silver_t`.
5. `silver_technical_tests` runs tests for `silver_t`.
6. `silver_business` runs dbt models in `silver_b`.
7. `silver_business_tests` runs tests for `silver_b`.
8. `gold_ephermeral` builds ephemeral gold models.
9. `gold_dimensions` runs `dbt snapshot`.
10. `gold_facts` runs gold fact models.
