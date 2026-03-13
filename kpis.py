import pandas as pd
from db_connection import engine
from queries import query
df = pd.read_sql(query, engine)


total_sales = df["sales"].sum()
total_orders = df["order_id"].nunique()
total_customers = df["customer_id"].nunique()
avg_order_value = df.groupby("order_id")["sales"].sum().mean()

print(f"Total Sales: {total_sales:,.2f}")
print(f"Total Orders: {total_orders}")
print(f"Total Customers: {total_customers}")
print(f"Average Order Value: {avg_order_value:,.2f}")

