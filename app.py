import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from db_connection import engine
from queries import query  

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Superstore Dashboard", layout="wide")

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
# LOAD DATA
# ==============================
@st.cache_data
def load_data():
    df = pd.read_sql(query, engine)   # if needed: pd.read_sql(MAIN_QUERY, engine)
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["month_name"] = df["order_date"].dt.month_name()

    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    df["month_name"] = pd.Categorical(df["month_name"], categories=month_order, ordered=True)
    return df


df = load_data()

# ==============================
# TITLE
# ==============================
st.title("Superstore sales dashboard")
st.write("Interactive dashboard connected to PostgreSQL with KPIs, statistics, and full visual analysis.")

# ==============================
# FILTERS
# ==============================
region_options = ["All"] + sorted(df["region_name"].dropna().unique().tolist())
category_options = ["All"] + sorted(df["category_name"].dropna().unique().tolist())
period_options = ["All"] + sorted(df["year_month"].dropna().unique().tolist())

f1, f2, f3 = st.columns(3)

selected_region = f1.selectbox("Select region", region_options)
selected_category = f2.selectbox("Select category", category_options)
selected_period = f3.selectbox("Select period", period_options)

filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region_name"] == selected_region]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category_name"] == selected_category]

if selected_period != "All":
    filtered_df = filtered_df[filtered_df["year_month"] == selected_period]

# ==============================
# KPIs
# ==============================
total_sales = filtered_df["sales"].sum()
total_orders = filtered_df["order_id"].nunique()
total_customers = filtered_df["customer_id"].nunique()
avg_order_value = filtered_df.groupby("order_id")["sales"].sum().mean() if not filtered_df.empty else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total sales", f"${total_sales:,.2f}")
k2.metric("Total orders", total_orders)
k3.metric("Total customers", total_customers)
k4.metric("Average order value", f"${avg_order_value:,.2f}")

# ==============================
# DESCRIPTIVE STATISTICS
# ==============================
st.subheader("Descriptive statistics")

if not filtered_df.empty:
    stats_df = pd.DataFrame({
        "Statistic": ["Mean", "Median", "Minimum", "Maximum", "Standard deviation"],
        "Value": [
            filtered_df["sales"].mean(),
            filtered_df["sales"].median(),
            filtered_df["sales"].min(),
            filtered_df["sales"].max(),
            filtered_df["sales"].std()
        ]
    })
else:
    stats_df = pd.DataFrame({
        "Statistic": ["Mean", "Median", "Minimum", "Maximum", "Standard deviation"],
        "Value": [0, 0, 0, 0, 0]
    })

st.dataframe(stats_df, use_container_width=True)

# ==============================
# AGGREGATIONS
# ==============================
sales_by_region = filtered_df.groupby("region_name", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
sales_by_category = filtered_df.groupby("category_name", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
sales_by_subcategory = filtered_df.groupby("sub_category_name", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
sales_by_segment = filtered_df.groupby("segment", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
sales_by_month = filtered_df.groupby("year_month", as_index=False)["sales"].sum().sort_values("year_month")
sales_by_year = filtered_df.groupby("order_year", as_index=False)["sales"].sum().sort_values("order_year")
sales_by_month_name = filtered_df.groupby("month_name", as_index=False)["sales"].sum().sort_values("month_name")

top_products = (
    filtered_df.groupby("product_name", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
    .head(10)
)

top_customers = (
    filtered_df.groupby("customer_name", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
    .head(10)
)

sales_region_category = filtered_df.pivot_table(
    values="sales",
    index="region_name",
    columns="category_name",
    aggfunc="sum"
)

orders_per_region = filtered_df.groupby("region_name")["order_id"].nunique().reset_index(name="num_orders")
order_totals = filtered_df.groupby("order_id", as_index=False)["sales"].sum()

# ==============================
# VISUALIZATIONS
# ==============================
st.header("Visualizations")

# 1 and 2
c1, c2 = st.columns(2)

with c1:
    st.subheader("1. Sales by region")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=sales_by_region, x="region_name", y="sales", hue="region_name", legend=False, ax=ax)
    ax.set_title("Sales by region", pad=12, weight="bold")
    ax.set_xlabel("Region")
    ax.set_ylabel("Total sales")
    ax.tick_params(axis="x", rotation=45)
    clean_axes()
    plt.tight_layout()
    st.pyplot(fig)

with c2:
    st.subheader("2. Sales by category")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=sales_by_category, x="category_name", y="sales", hue="category_name", legend=False, ax=ax)
    ax.set_title("Sales by category", pad=12, weight="bold")
    ax.set_xlabel("Category")
    ax.set_ylabel("Total sales")
    ax.tick_params(axis="x", rotation=45)
    clean_axes()
    plt.tight_layout()
    st.pyplot(fig)

# 3 and 4
c3, c4 = st.columns(2)

with c3:
    st.subheader("3. Sales by sub-category")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=sales_by_subcategory, x="sales", y="sub_category_name", hue="sub_category_name", legend=False, ax=ax)
    ax.set_title("Sales by sub-category", pad=12, weight="bold")
    ax.set_xlabel("Total sales")
    ax.set_ylabel("Sub-category")
    clean_axes()
    plt.tight_layout()
    st.pyplot(fig)

with c4:
    st.subheader("4. Sales by segment")
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(data=sales_by_segment, x="segment", y="sales", hue="segment", legend=False, ax=ax)
    ax.set_title("Sales by segment", pad=12, weight="bold")
    ax.set_xlabel("Segment")
    ax.set_ylabel("Total sales")
    ax.tick_params(axis="x", rotation=20)
    clean_axes()
    plt.tight_layout()
    st.pyplot(fig)

# 5 and 6
c5, c6 = st.columns(2)

with c5:
    st.subheader("5. Monthly sales trend")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=sales_by_month, x="year_month", y="sales", marker="o", linewidth=2.5, ax=ax)
    ax.set_title("Monthly sales trend", pad=12, weight="bold")
    ax.set_xlabel("Year-month")
    ax.set_ylabel("Total sales")
    ax.tick_params(axis="x", rotation=45)
    clean_axes()
    plt.tight_layout()
    st.pyplot(fig)

with c6:
    st.subheader("6. Yearly sales trend")
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.lineplot(data=sales_by_year, x="order_year", y="sales", marker="o", linewidth=2.5, ax=ax)
    ax.set_title("Yearly sales trend", pad=12, weight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total sales")
    clean_axes()
    plt.tight_layout()
    st.pyplot(fig)

# 7 and 8
c7, c8 = st.columns(2)

with c7:
    st.subheader("7. Sales by month")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=sales_by_month_name, x="month_name", y="sales", hue="month_name", legend=False, ax=ax)
    ax.set_title("Sales by month", pad=12, weight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total sales")
    ax.tick_params(axis="x", rotation=45)
    clean_axes()
    plt.tight_layout()
    st.pyplot(fig)

with c8:
    st.subheader("8. Sales share by category")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        sales_by_category["sales"],
        labels=sales_by_category["category_name"],
        autopct="%1.1f%%",
        startangle=90,
        colors=sns.color_palette("viridis", len(sales_by_category)),
        wedgeprops={"edgecolor": "white", "linewidth": 1},
    )
    ax.set_title("Sales share by category", pad=12, weight="bold")
    plt.tight_layout()
    st.pyplot(fig)

# 9 and 10
c9, c10 = st.columns(2)

with c9:
    st.subheader("9. Sales share by region")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        sales_by_region["sales"],
        labels=sales_by_region["region_name"],
        autopct="%1.1f%%",
        startangle=90,
        colors=sns.color_palette("viridis", len(sales_by_region)),
        wedgeprops={"edgecolor": "white", "linewidth": 1},
    )
    centre_circle = plt.Circle((0, 0), 0.60, fc="white")
    ax.add_artist(centre_circle)
    ax.set_title("Sales share by region", pad=12, weight="bold")
    plt.tight_layout()
    st.pyplot(fig)

with c10:
    st.subheader("10. Top 10 products by sales")
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(data=top_products, x="sales", y="product_name", hue="product_name", legend=False, ax=ax)
    ax.set_title("Top 10 products by sales", pad=12, weight="bold")
    ax.set_xlabel("Total sales")
    ax.set_ylabel("Product")
    clean_axes()
    plt.tight_layout()
    st.pyplot(fig)

# 11 and 12
c11, c12 = st.columns(2)

with c11:
    st.subheader("11. Top 10 customers by sales")
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(data=top_customers, x="sales", y="customer_name", hue="customer_name", legend=False, ax=ax)
    ax.set_title("Top 10 customers by sales", pad=12, weight="bold")
    ax.set_xlabel("Total sales")
    ax.set_ylabel("Customer")
    clean_axes()
    plt.tight_layout()
    st.pyplot(fig)

with c12:
    st.subheader("12. Distribution of sales")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.histplot(filtered_df["sales"], bins=30, kde=True, ax=ax)
    ax.set_title("Distribution of sales", pad=12, weight="bold")
    ax.set_xlabel("Sales")
    ax.set_ylabel("Frequency")
    clean_axes()
    plt.tight_layout()
    st.pyplot(fig)

# 13 and 14
c13, c14 = st.columns(2)

with c13:
    st.subheader("13. Sales distribution by region")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=filtered_df, x="region_name", y="sales", hue="region_name", legend=False, ax=ax)
    ax.set_title("Sales distribution by region", pad=12, weight="bold")
    ax.set_xlabel("Region")
    ax.set_ylabel("Sales")
    ax.tick_params(axis="x", rotation=45)
    clean_axes()
    plt.tight_layout()
    st.pyplot(fig)

with c14:
    st.subheader("14. Sales distribution by category")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=filtered_df, x="category_name", y="sales", hue="category_name", legend=False, ax=ax)
    ax.set_title("Sales distribution by category", pad=12, weight="bold")
    ax.set_xlabel("Category")
    ax.set_ylabel("Sales")
    ax.tick_params(axis="x", rotation=45)
    clean_axes()
    plt.tight_layout()
    st.pyplot(fig)

# 15 and 16
c15, c16 = st.columns(2)

with c15:
    st.subheader("15. Sales heatmap by region and category")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(
        sales_region_category,
        annot=True,
        fmt=".0f",
        cmap="viridis",
        linewidths=0.5,
        linecolor="white",
        ax=ax
    )
    ax.set_title("Sales heatmap by region and category", pad=12, weight="bold")
    ax.set_xlabel("Category")
    ax.set_ylabel("Region")
    plt.tight_layout()
    st.pyplot(fig)

with c16:
    st.subheader("16. Number of orders by region")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=orders_per_region, x="region_name", y="num_orders", hue="region_name", legend=False, ax=ax)
    ax.set_title("Number of orders by region", pad=12, weight="bold")
    ax.set_xlabel("Region")
    ax.set_ylabel("Number of orders")
    ax.tick_params(axis="x", rotation=45)
    clean_axes()
    plt.tight_layout()
    st.pyplot(fig)

# 17 and 18
c17, c18 = st.columns(2)

with c17:
    st.subheader("17. Order total sales distribution")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=order_totals, x=order_totals.index, y="sales", s=70, ax=ax)
    ax.set_title("Order total sales distribution", pad=12, weight="bold")
    ax.set_xlabel("Order index")
    ax.set_ylabel("Order total sales")
    clean_axes()
    plt.tight_layout()
    st.pyplot(fig)

with c18:
    st.subheader("18. Sales distribution by segment")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.violinplot(data=filtered_df, x="segment", y="sales", hue="segment", legend=False, ax=ax)
    ax.set_title("Sales distribution by segment", pad=12, weight="bold")
    ax.set_xlabel("Segment")
    ax.set_ylabel("Sales")
    ax.tick_params(axis="x", rotation=20)
    clean_axes()
    plt.tight_layout()
    st.pyplot(fig)

# ==============================
# DATA PREVIEW
# ==============================
st.header("Filtered data preview")
st.dataframe(filtered_df.head(50), use_container_width=True)