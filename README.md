<img width="736" height="414" alt="videoframe_15013" src="https://github.com/user-attachments/assets/a29ece32-0a18-4c5e-9a36-c44c4f6e64d1" />

**Sales Target Analysis **

An end-to-end Data Engineering and Analytics project that transforms raw retail data into a structured relational database for deep business intelligence and sales performance tracking.

**Project Overview**
This project demonstrates a complete data lifecycle:
1.  **Extraction:** Loading raw transactional data from CSV.
2.  **Transformation:** Cleaning, normalizing, and mapping data into a relational format using Python.
3.  **Loading:** Building a Star Schema in **PostgreSQL** for optimized analytical querying.
4.  **Visualization:** Connecting the structured data to **Power BI** to create an interactive sales dashboard.

**Architecture (Star Schema)**
The project organizes data into a highly efficient Star Schema to support complex analytical reporting:
* **Fact Table:** `fact_sales` (Sales amounts, quantities, and foreign keys).
* **Dimension Tables:** * `dim_customer`: Customer segments and profiles.
    * `dim_product`: Product catalog and details.
    * `dim_category`: Hierarchy of categories and sub-categories.
    * `dim_region`: Geographical sales distribution.
    * `dim_date`: Time-series intelligence (Day, Month, Quarter, Year).

**Tech Stack**
* **Language:** Python
* **Database:** PostgreSQL
* **Libraries:** Pandas, SQLAlchemy, Psycopg2
* **Visualization:** Power BI
* **Environment:** Jupyter Notebook / Python Scripts

**Project Structure**
```text
├── Data/                   # Original CSV dataset
├── Scripts/                # ETL Pipeline scripts
│   ├── load_dim_customer.py
│   ├── load_dim_product.py
│   ├── load_dim_date.py
│   ├── load_dim_region.py
│   ├── load_dim_category.py
│   └── load_fact_sales.py  # Final step: loading transactional data
├── Dashboard/              # Power BI (.pbix) file
└── README.md
```

**Setup & Installation**
Database Setup: Create a PostgreSQL database named Sales_target.db.
Configuration: Update the DB_USER and DB_PASS in the Python scripts to match your local PostgreSQL credentials.
Run ETL: Execute the scripts in the following order to maintain referential integrity:

Load all dim_ scripts.

Load load_fact_sales.py.

Visualization: Open the .pbix file in Power BI Desktop and update the data source settings to point to your PostgreSQL instance.

**Key Insights Captured**
Regional Performance: Identification of top-performing sales regions.
Category Analysis: Profitability and sales volume trends across different product lines.
Customer Segmentation: Understanding sales contribution by different customer segments.
Temporal Trends: Year-over-year and Quarter-over-quarter growth tracking.
Developed as part of a Data Analytics & Engineering Portfolio.
