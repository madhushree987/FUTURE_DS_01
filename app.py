import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="Business Sales Performance Analytics",
    layout="wide"
)

st.title("📊 Business Sales Performance Dashboard")

st.markdown("""
Analyze sales trends, product performance,
regional growth, and profitability insights.
""")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

df = pd.read_csv("superstore.csv", encoding='latin1')

# ------------------------------------------------
# DATA CLEANING
# ------------------------------------------------

df.drop_duplicates(inplace=True)

# Convert date column
df['Order Date'] = pd.to_datetime(df['Order Date'])

# ------------------------------------------------
# KPI SECTION
# ------------------------------------------------

total_sales = round(df['Sales'].sum(), 2)

total_profit = round(df['Profit'].sum(), 2)

total_orders = df['Order ID'].nunique()

avg_sales = round(df['Sales'].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"${total_sales}")

col2.metric("📈 Total Profit", f"${total_profit}")

col3.metric("📦 Total Orders", total_orders)

col4.metric("🛒 Average Sales", f"${avg_sales}")

st.markdown("---")

# ------------------------------------------------
# SALES TREND
# ------------------------------------------------

st.subheader("📅 Sales Trend Over Time")

sales_trend = df.groupby(
    df['Order Date'].dt.to_period('M')
)['Sales'].sum().reset_index()

sales_trend['Order Date'] = sales_trend[
    'Order Date'
].astype(str)

fig_sales = px.line(
    sales_trend,
    x='Order Date',
    y='Sales',
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig_sales, use_container_width=True)

# ------------------------------------------------
# CATEGORY ANALYSIS
# ------------------------------------------------

st.subheader("📦 Sales by Category")

category_sales = df.groupby(
    'Category'
)['Sales'].sum().reset_index()

fig_category = px.bar(
    category_sales,
    x='Category',
    y='Sales',
    color='Category',
    text='Sales',
    title="Category-wise Sales"
)

fig_category.update_traces(
    texttemplate='%{text:.2f}',
    textposition='outside'
)

st.plotly_chart(fig_category, use_container_width=True)

# ------------------------------------------------
# REGION ANALYSIS
# ------------------------------------------------

st.subheader("🌍 Regional Sales Performance")

region_sales = df.groupby(
    'Region'
)['Sales'].sum().reset_index()

fig_region = px.pie(
    region_sales,
    names='Region',
    values='Sales',
    title="Regional Sales Distribution"
)

st.plotly_chart(fig_region, use_container_width=True)

# ------------------------------------------------
# TOP PRODUCTS
# ------------------------------------------------

st.subheader("🏆 Top Selling Products")

top_products = df.groupby(
    'Product Name'
)['Sales'].sum().reset_index()

top_products = top_products.sort_values(
    by='Sales',
    ascending=False
).head(10)

fig_products = px.bar(
    top_products,
    x='Sales',
    y='Product Name',
    orientation='h',
    color='Sales',
    title="Top 10 Products"
)

st.plotly_chart(fig_products, use_container_width=True)

# ------------------------------------------------
# PROFIT ANALYSIS
# ------------------------------------------------

st.subheader("📈 Profit by Sub-Category")

subcategory_profit = df.groupby(
    'Sub-Category'
)['Profit'].sum().reset_index()

fig_profit = px.bar(
    subcategory_profit,
    x='Sub-Category',
    y='Profit',
    color='Profit',
    title="Sub-Category Profit Analysis"
)

st.plotly_chart(fig_profit, use_container_width=True)

# ------------------------------------------------
# BUSINESS INSIGHTS
# ------------------------------------------------

st.subheader("📌 Key Insights")

st.info("""
🔹 Certain product categories generate significantly higher revenue.

🔹 Some regions outperform others in total sales.

🔹 A few products contribute major share of business revenue.

🔹 Profitability varies across sub-categories.

🔹 Monthly sales trends reveal seasonal patterns.
""")

# ------------------------------------------------
# RECOMMENDATIONS
# ------------------------------------------------

st.subheader("💡 Business Recommendations")

st.success("""
✅ Focus marketing on top-performing products.

✅ Improve sales strategies in low-performing regions.

✅ Increase inventory for high-demand categories.

✅ Optimize pricing for low-profit sub-categories.

✅ Use seasonal trends for campaign planning.
""")

# ------------------------------------------------
# DATA PREVIEW
# ------------------------------------------------

st.subheader("📄 Dataset Preview")

st.dataframe(df.head())

# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.markdown("---")

st.caption(
    "Business Sales Performance Dashboard using Streamlit"
)