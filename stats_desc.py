import pandas as pd
from db_connection import engine
from queries import query

df = pd.read_sql(query, engine)

print("Mean sales:", df["sales"].mean())
print("Median sales:", df["sales"].median())
print("Min sales:", df["sales"].min())
print("Max sales:", df["sales"].max())
print("Std sales:", df["sales"].std())


print("\n===== Descriptive Statistics =====")
print(df["sales"].describe())