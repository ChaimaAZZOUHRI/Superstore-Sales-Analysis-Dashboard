import pandas as pd
from db_connection import engine
from queries import query

df = pd.read_sql(query, engine)

# Preview data
print(df.head())
print(df.shape)
print(df.columns)
print(df.info())


# CLEANING


# Remove duplicates
df = df.drop_duplicates()

# Convert date column
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# Remove rows with missing important values
df = df.dropna(subset=["sales", "order_date"])

# Create useful columns
df["order_year"] = df["order_date"].dt.year
df["order_month"] = df["order_date"].dt.month

# Show result
print("\nAfter cleaning:")
print(df.shape)

# Save cleaned dataset
df.to_csv("clean_data.csv", index=False)

print(df.isna().sum())