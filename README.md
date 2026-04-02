# Superstore Sales Analysis Dashboard

A portfolio project that demonstrates how to build an **interactive business intelligence dashboard** with **Python, PostgreSQL, SQLAlchemy, and Streamlit**.  
The application connects to a relational database, retrieves sales data through SQL joins, performs data preparation and aggregation, and delivers interactive analytics through KPIs, descriptive statistics, and visualizations.

---

## Project summary

This project was designed to transform Superstore sales data into a clean and interactive analytics experience.  
Instead of working only with raw SQL queries or static notebooks, this dashboard provides a simple interface for exploring sales performance by **region**, **category**, and **time period**.

It highlights both **data engineering** and **data analysis** skills by combining:

- relational database querying
- Python-based data processing
- statistical summaries
- business KPI reporting
- interactive dashboard design


---

## Key features

### Interactive filters
Users can filter the dashboard by:

- Region
- Category
- Period (year-month)

### KPI section
The dashboard automatically updates the following metrics based on selected filters:

- Total sales
- Total orders
- Total customers
- Average order value

### Descriptive statistics
The project calculates summary statistics for the sales variable:

- Mean
- Median
- Minimum
- Maximum
- Standard deviation

### Visual analytics
The dashboard includes multiple charts to explore business performance, including:

- Sales by region
- Sales by category
- Sales by sub-category
- Sales by segment
- Monthly sales trend
- Yearly sales trend
- Sales by month
- Sales share by category
- Sales share by region
- Top 10 products by sales
- Top 10 customers by sales
- Sales distribution
- Sales distribution by region
- Sales distribution by category
- Sales heatmap by region and category
- Number of orders by region
- Order total sales distribution
- Sales distribution by segment

### Data preview
A filtered table preview is displayed to help users inspect the underlying data used in the analysis.

---

## Tech stack

- **Python**
- **PostgreSQL**
- **SQLAlchemy**
- **Pandas**
- **Streamlit**
- **Matplotlib**
- **Seaborn**
- **psycopg2**

---

## Project architecture

This repository is organized into modular scripts, with each file covering one part of the workflow:

```bash
Superstore-Sales-Analysis-Dashboard/
│
├── app.py                # Main Streamlit dashboard
├── db_connection.py      # PostgreSQL connection setup
├── queries.py            # Main SQL query joining normalized tables
├── load_data.py          # Data loading and cleaning
├── kpis.py               # KPI calculations
├── stats_desc.py         # Descriptive statistics
├── aggregations.py       # Grouped analysis and summaries
├── visualizations.py     # Standalone plotting logic
├── test_tables.py        # Database structure check
├── clean_data.csv        # Dataset file
