import pandas as pd
from db_connection import engine
from queries import query

import pandas as pd
from db_connection import engine
from queries import query

# Load data from PostgreSQL
df = pd.read_sql(query, engine)

# Create date-based columns
df["order_date"] = pd.to_datetime(df["order_date"])
df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
df["month_name"] = df["order_date"].dt.month_name()

month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

sales_by_region = df.groupby("region_name", as_index=False)["sales"].sum().sort_values("sales", ascending=False)

sales_by_category = df.groupby("category_name", as_index=False)["sales"].sum().sort_values("sales", ascending=False)

sales_by_subcategory = df.groupby("sub_category_name", as_index=False)["sales"].sum().sort_values("sales", ascending=False)

sales_by_segment = df.groupby("segment", as_index=False)["sales"].sum().sort_values("sales", ascending=False)

sales_by_month = df.groupby("year_month", as_index=False)["sales"].sum().sort_values("year_month")

sales_by_year = df.groupby("order_year", as_index=False)["sales"].sum().sort_values("order_year")

sales_by_month_name = (
    df.groupby("month_name", as_index=False)["sales"]
    .sum()
)

sales_by_month_name["month_name"] = pd.Categorical(
    sales_by_month_name["month_name"],
    categories=month_order,
    ordered=True
)

sales_by_month_name = sales_by_month_name.sort_values("month_name")

top_products = (
    df.groupby("product_name", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
    .head(10)
)

top_customers = (
    df.groupby("customer_name", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
    .head(10)
)

sales_region_category = df.pivot_table(
    values="sales",
    index="region_name",
    columns="category_name",
    aggfunc="sum"
)

orders_per_region = df.groupby("region_name")["order_id"].nunique().reset_index(name="num_orders")


print(sales_by_region)
print(sales_by_subcategory.head())
print(sales_by_segment.head())
print(sales_by_month.head())
print(sales_by_year.head())
print(sales_by_month_name.head())
print(sales_by_category)
print(sales_by_month.head())
print(top_products.head())
print(top_customers.head())
print(sales_region_category)
print(orders_per_region)

