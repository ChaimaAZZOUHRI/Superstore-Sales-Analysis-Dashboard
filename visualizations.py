import matplotlib.pyplot as plt
import seaborn as sns

from aggregations import (
    df,
    sales_by_region,
    sales_by_category,
    sales_by_subcategory,
    sales_by_segment,
    sales_by_month,
    sales_by_year,
    sales_by_month_name,
    top_products,
    top_customers,
    sales_region_category,
    orders_per_region,
)

# ==============================
# GLOBAL STYLE
# ==============================
sns.set_theme(style="whitegrid", palette="viridis")
sns.set_context("talk")

plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["axes.edgecolor"] = "#333333"
plt.rcParams["grid.color"] = "#d9d9d9"
plt.rcParams["grid.linestyle"] = "--"
plt.rcParams["grid.alpha"] = 0.5


def clean_axes():
    sns.despine(top=True, right=True)


# ==============================
# 1. Sales by region
# ==============================
plt.figure(figsize=(8, 5))
sns.barplot(data=sales_by_region, x="region_name", y="sales", hue="region_name", legend=False)
plt.title("Sales by region", pad=12, weight="bold")
plt.xlabel("Region")
plt.ylabel("Total sales")
plt.xticks(rotation=45)
clean_axes()
plt.tight_layout()
plt.show()

# ==============================
# 2. Sales by category
# ==============================
plt.figure(figsize=(8, 5))
sns.barplot(data=sales_by_category, x="category_name", y="sales", hue="category_name", legend=False)
plt.title("Sales by category", pad=12, weight="bold")
plt.xlabel("Category")
plt.ylabel("Total sales")
plt.xticks(rotation=45)
clean_axes()
plt.tight_layout()
plt.show()

# ==============================
# 3. Sales by sub-category
# ==============================
plt.figure(figsize=(12, 7))
sns.barplot(data=sales_by_subcategory, x="sales", y="sub_category_name", hue="sub_category_name", legend=False)
plt.title("Sales by sub-category", pad=12, weight="bold")
plt.xlabel("Total sales")
plt.ylabel("Sub-category")
clean_axes()
plt.tight_layout()
plt.show()

# ==============================
# 4. Sales by segment
# ==============================
plt.figure(figsize=(7, 5))
sns.barplot(data=sales_by_segment, x="segment", y="sales", hue="segment", legend=False)
plt.title("Sales by segment", pad=12, weight="bold")
plt.xlabel("Segment")
plt.ylabel("Total sales")
plt.xticks(rotation=20)
clean_axes()
plt.tight_layout()
plt.show()

# ==============================
# 5. Monthly sales trend
# ==============================
plt.figure(figsize=(12, 5))
sns.lineplot(data=sales_by_month, x="year_month", y="sales", marker="o", linewidth=2.5)
plt.title("Monthly sales trend", pad=12, weight="bold")
plt.xlabel("Year-month")
plt.ylabel("Total sales")
plt.xticks(rotation=45)
clean_axes()
plt.tight_layout()
plt.show()

# ==============================
# 6. Yearly sales trend
# ==============================
plt.figure(figsize=(7, 5))
sns.lineplot(data=sales_by_year, x="order_year", y="sales", marker="o", linewidth=2.5)
plt.title("Yearly sales trend", pad=12, weight="bold")
plt.xlabel("Year")
plt.ylabel("Total sales")
clean_axes()
plt.tight_layout()
plt.show()

# ==============================
# 7. Sales by month name
# ==============================
plt.figure(figsize=(11, 5))
sns.barplot(data=sales_by_month_name, x="month_name", y="sales", hue="month_name", legend=False)
plt.title("Sales by month", pad=12, weight="bold")
plt.xlabel("Month")
plt.ylabel("Total sales")
plt.xticks(rotation=45)
clean_axes()
plt.tight_layout()
plt.show()

# ==============================
# 8. Pie chart by category
# ==============================
plt.figure(figsize=(8, 8))
plt.pie(
    sales_by_category["sales"],
    labels=sales_by_category["category_name"],
    autopct="%1.1f%%",
    startangle=90,
    colors=sns.color_palette("viridis", len(sales_by_category)),
    wedgeprops={"edgecolor": "white", "linewidth": 1},
)
plt.title("Sales share by category", pad=12, weight="bold")
plt.tight_layout()
plt.show()

# ==============================
# 9. Donut chart by region
# ==============================
plt.figure(figsize=(8, 8))
plt.pie(
    sales_by_region["sales"],
    labels=sales_by_region["region_name"],
    autopct="%1.1f%%",
    startangle=90,
    colors=sns.color_palette("viridis", len(sales_by_region)),
    wedgeprops={"edgecolor": "white", "linewidth": 1},
)
centre_circle = plt.Circle((0, 0), 0.60, fc="white")
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title("Sales share by region", pad=12, weight="bold")
plt.tight_layout()
plt.show()

# ==============================
# 10. Top 10 products
# ==============================
plt.figure(figsize=(12, 7))
sns.barplot(data=top_products, x="sales", y="product_name", hue="product_name", legend=False)
plt.title("Top 10 products by sales", pad=12, weight="bold")
plt.xlabel("Total sales")
plt.ylabel("Product")
clean_axes()
plt.tight_layout()
plt.show()

# ==============================
# 11. Top 10 customers
# ==============================
plt.figure(figsize=(12, 7))
sns.barplot(data=top_customers, x="sales", y="customer_name", hue="customer_name", legend=False)
plt.title("Top 10 customers by sales", pad=12, weight="bold")
plt.xlabel("Total sales")
plt.ylabel("Customer")
clean_axes()
plt.tight_layout()
plt.show()

# ==============================
# 12. Sales distribution
# ==============================
plt.figure(figsize=(9, 5))
sns.histplot(df["sales"], bins=30, kde=True)
plt.title("Distribution of sales", pad=12, weight="bold")
plt.xlabel("Sales")
plt.ylabel("Frequency")
clean_axes()
plt.tight_layout()
plt.show()

# ==============================
# 13. Boxplot by region
# ==============================
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="region_name", y="sales", hue="region_name", legend=False)
plt.title("Sales distribution by region", pad=12, weight="bold")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.xticks(rotation=45)
clean_axes()
plt.tight_layout()
plt.show()

# ==============================
# 14. Boxplot by category
# ==============================
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="category_name", y="sales", hue="category_name", legend=False)
plt.title("Sales distribution by category", pad=12, weight="bold")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.xticks(rotation=45)
clean_axes()
plt.tight_layout()
plt.show()

# ==============================
# 15. Heatmap region x category
# ==============================
plt.figure(figsize=(8, 5))
sns.heatmap(
    sales_region_category,
    annot=True,
    fmt=".0f",
    cmap="viridis",
    linewidths=0.5,
    linecolor="white"
)
plt.title("Sales heatmap by region and category", pad=12, weight="bold")
plt.xlabel("Category")
plt.ylabel("Region")
plt.tight_layout()
plt.show()

# ==============================
# 16. Number of orders by region
# ==============================
plt.figure(figsize=(8, 5))
sns.barplot(data=orders_per_region, x="region_name", y="num_orders", hue="region_name", legend=False)
plt.title("Number of orders by region", pad=12, weight="bold")
plt.xlabel("Region")
plt.ylabel("Number of orders")
plt.xticks(rotation=45)
clean_axes()
plt.tight_layout()
plt.show()

# ==============================
# 17. Order total sales scatter
# ==============================
order_totals = df.groupby("order_id", as_index=False)["sales"].sum()

plt.figure(figsize=(10, 5))
sns.scatterplot(data=order_totals, x=order_totals.index, y="sales", s=70)
plt.title("Order total sales distribution", pad=12, weight="bold")
plt.xlabel("Order index")
plt.ylabel("Order total sales")
clean_axes()
plt.tight_layout()
plt.show()

# ==============================
# 18. Violin plot by segment
# ==============================
plt.figure(figsize=(8, 5))
sns.violinplot(data=df, x="segment", y="sales", hue="segment", legend=False)
plt.title("Sales distribution by segment", pad=12, weight="bold")
plt.xlabel("Segment")
plt.ylabel("Sales")
plt.xticks(rotation=20)
clean_axes()
plt.tight_layout()
plt.show()