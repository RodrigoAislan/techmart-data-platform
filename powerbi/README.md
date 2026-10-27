# TechMart Sales Dashboard — Power BI

## Overview

The TechMart Sales Dashboard is an interactive business intelligence report built with Power BI to analyze sales performance, product categories, brands, customer behavior, and geographic distribution.

This dashboard is the reporting layer of the **TechMart Data Engineering Platform**, an end-to-end portfolio project that demonstrates how raw e-commerce data can be extracted, stored, transformed, tested, and presented as actionable business insights.

The project integrates Python, Apache Airflow, AWS S3, Snowflake, dbt, and Power BI to demonstrate a practical data engineering and analytics workflow.

## Dashboard Preview

![TechMart Sales Dashboard](sales-dashboard.png)

## Key Performance Indicators (KPIs)

The dashboard presents four key performance indicators:

| KPI | Description |
|---|---|
| Gross Sales | Total sales value before item-level discounts. |
| Net Sales | Total sales value after item-level discounts. |
| Total Orders | Number of distinct orders represented in the dataset. |
| Units Sold | Total quantity of products sold. |

### Current Results

The dashboard currently displays approximately:

- **Gross Sales:** $3.83 million
- **Net Sales:** $3.46 million
- **Total Orders:** 208
- **Units Sold:** 2.42 thousand

These figures reflect the sample dataset used in the project and are not actual company performance figures.

## Dashboard Features

### 1. Sales by Product Category

Compares gross sales and net sales across product categories.

This analysis helps identify the categories contributing most to overall sales and compare sales before and after discounts.

### 2. Sales by Brand

Visualizes sales distribution across product brands.

This view helps identify brands with the largest sales contribution and understand how sales are distributed across the product portfolio.

### 3. Sales by Product Category — Ranking

Ranks product categories by sales value.

This visualization makes it easier to compare category performance and identify the strongest-performing product categories.

### 4. Geographic Sales Analysis

Provides a geographic breakdown of orders and net sales, including country and regional details.

This analysis helps explore where sales are concentrated and compare order volume and sales value across geographic areas.

### 5. Top 5 Customers by Sales

Identifies the five highest-value customers based on sales.

This view helps highlight customer contribution and identify customers who account for a significant share of sales.

### 6. Top Customers by City

Compares customer sales across cities.

This visualization provides additional geographic context for customer performance and helps identify cities associated with high-value customers.

## Business Questions

The dashboard is designed to help answer the following business questions:

- What are the total gross sales and net sales?
- How many distinct orders were recorded?
- How many product units were sold?
- Which product categories contribute the most to sales?
- Which brands generate the highest sales?
- Which customers contribute the most to total sales?
- How are orders and net sales distributed geographically?
- Which cities are associated with the highest-value customers?
- How do gross sales compare with net sales after item-level discounts?

## Data Model

The dashboard uses three dbt-built tables from the TechMart Snowflake data warehouse.

| Model | Type | Purpose |
|---|---|---|
| `DIM_CUSTOMERS` | Dimension | Provides customer attributes for customer and geographic analysis. |
| `DIM_PRODUCTS` | Dimension | Provides product attributes for category and brand analysis. |
| `FCT_SALES` | Fact | Contains order-item-level sales measures and related customer and product attributes. |

### Fact Table Grain

The `FCT_SALES` table has **one row per order item**.

This grain supports detailed product-level sales analysis and aggregation across customers, products, categories, and brands.

Key measures include:

- `QUANTITY`
- `UNIT_PRICE`
- `GROSS_SALES_AMOUNT`
- `NET_SALES_AMOUNT`
- `ITEM_DISCOUNT_PERCENTAGE`

Orders should be counted distinctly using `ORDER_ID`, rather than counting fact-table rows, because a single order can contain multiple items.

When aggregating sales, `GROSS_SALES_AMOUNT` and `NET_SALES_AMOUNT` are the appropriate item-level measures. Order-level totals repeated across item rows should not be summed, as this would overstate sales.

## Data Pipeline Architecture

The dashboard is the final reporting layer of the TechMart Data Engineering Platform.

The workflow follows this sequence:

1. **Data Extraction:** Python retrieves sample e-commerce data from the DummyJSON API.
2. **Workflow Orchestration:** Apache Airflow orchestrates extraction workflows.
3. **Raw Data Storage:** AWS S3 stores extracted JSON files in the raw data layer.
4. **Data Warehousing:** Snowflake stores the raw data and provides the cloud data warehouse environment.
5. **Data Transformation:** dbt transforms raw data into staging, intermediate, and mart models.
6. **Data Quality:** dbt tests validate data integrity and model assumptions.
7. **Business Intelligence:** Power BI connects to the modeled data to provide interactive reports and business insights.

## Technology Stack

| Technology | Role in the Project |
|---|---|
| Power BI | Business intelligence, KPI reporting, and data visualization |
| Snowflake | Cloud data warehousing |
| dbt Core | SQL transformations, dimensional modeling, and data quality tests |
| Python | API data extraction and ingestion |
| Apache Airflow | Workflow orchestration |
| AWS S3 | Raw data storage |
| DummyJSON API | Source of sample e-commerce data |
| Git and GitHub | Version control and project documentation |

## Data Quality and Modeling

The project uses dbt to organize transformations into distinct layers and build reusable analytical models.

The transformation workflow includes:

- Staging models for preparing source data.
- Intermediate models for enriching and combining data.
- Dimension models for customer and product analysis.
- A sales fact model at the order-item grain.
- Schema tests to validate data quality and model integrity.

These practices help produce structured, analysis-ready datasets for downstream reporting.

## Data Limitations

This project uses sample e-commerce data from the DummyJSON API rather than a live production business dataset.

The available order data does not provide a reliable order-date field for historical sales analysis. Consequently, the dashboard focuses on sales composition, product and brand performance, customer contribution, and geographic distribution rather than time-based sales trends.

The results are intended to demonstrate data engineering, data modeling, and business intelligence skills. They should not be interpreted as actual business performance.

## Skills Demonstrated

This project demonstrates practical experience with:

- End-to-end data pipeline design
- API data extraction using Python
- Workflow orchestration with Apache Airflow
- Cloud data storage with AWS S3
- Cloud data warehousing with Snowflake
- SQL transformations using dbt
- Dimensional data modeling
- Fact and dimension table design
- Data quality testing
- Git and GitHub version control
- Power BI data modeling and visualization
- KPI development and business analysis
- Translating business questions into analytical reports

## Repository

Explore the complete project, including the ingestion workflows, data transformations, and Power BI reporting layer:

[TechMart Data Engineering Platform on GitHub](https://github.com/RodrigoAislan/techmart-data-platform)

