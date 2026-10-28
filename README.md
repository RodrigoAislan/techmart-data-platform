# TechMart — End-to-End Data Engineering Platform

## Overview

TechMart is an end-to-end data engineering portfolio project that demonstrates how to extract data from a public e-commerce API, orchestrate ingestion, store raw data in AWS S3, transform data with Snowflake and dbt, and deliver business insights through Power BI.

The project focuses on data pipeline orchestration, cloud data storage, SQL transformations, dimensional modeling, data quality testing, and CI automation.

## Architecture

```text
DummyJSON E-commerce API
          |
          v
Python Ingestion Scripts
          |
          v
Apache Airflow
          |
          v
AWS S3 — Raw JSON Data
          |
          v
Snowflake — RAW
          |
          v
dbt — STAGING
          |
          v
dbt — INTERMEDIATE
          |
          v
dbt — MARTS
          |
          v
Power BI Dashboard
```

GitHub Actions provides CI checks for Python syntax and dbt project parsing.

## Technology Stack

- **Languages:** Python, SQL
- **Orchestration:** Apache Airflow
- **Cloud storage:** AWS S3
- **Data warehouse:** Snowflake
- **Transformation and testing:** dbt Core
- **Visualization:** Power BI
- **Version control:** Git and GitHub
- **CI:** GitHub Actions
- **API:** DummyJSON

## Data Models

The analytics layer includes:

- `DIM_CUSTOMERS` — customer attributes.
- `DIM_PRODUCTS` — product attributes.
- `FCT_SALES` — sales at the order-item grain.

The sales fact table supports analysis by product, customer, category, and geography.

## Dashboard

The Power BI dashboard presents sales KPIs, product-category comparisons, brand analysis, customer rankings, and geographic insights.

![TechMart Power BI Dashboard](powerbi/sales-dashboard.png)

See [Power BI documentation](powerbi/README.md) for dashboard details and model information.

## Repository Structure

```text
.
├── .github/workflows/   # GitHub Actions CI
├── dags/                # Airflow DAGs
├── ingestion/           # Python extraction scripts
├── techmart_dbt/        # dbt models, macros, and tests
├── powerbi/             # Dashboard and documentation
├── docs/                # Project documentation
├── infrastructure/      # Infrastructure-related files
├── config/              # Configuration files
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12
- Docker Desktop and Docker Compose
- An AWS account with appropriate S3 permissions
- A Snowflake account and suitable role permissions
- Power BI Desktop to open the dashboard

### Setup

1. Clone the repository.
2. Configure AWS credentials using your own AWS profile.
3. Configure the dbt Snowflake profile in `~/.dbt/profiles.yml`.
4. Install the Python and dbt dependencies.
5. Start Airflow using the project's Docker Compose configuration.
6. Run the ingestion DAGs and verify the raw files in S3.
7. Run dbt models and tests against your configured Snowflake environment.
8. Open the Power BI file and refresh it using the appropriate data connection.

Refer to the project documentation and configuration files for the exact commands and environment-specific settings.

## Data Quality and CI

The project includes dbt data tests and a GitHub Actions workflow that validates Python syntax and parses the dbt project.

CI parsing does not execute the transformations or validate live warehouse data.

## Limitations

The project uses sample e-commerce data from DummyJSON. It is intended to demonstrate data engineering concepts and does not represent a live production business or continuously updated commercial dataset.

## Author

Data Engineering portfolio project demonstrating Python, SQL, AWS, Snowflake, Airflow, dbt, Power BI, and GitHub Actions.

