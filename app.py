import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Business Sales Dashboard", page_icon="📊", layout="wide")
st.title("📊 B2B Sales Performance Dashboard")
st.markdown("_Built by a Data Analyst for interactive business reporting._")

# 2. Load the Data
# The @st.cache_data decorator keeps the app fast by not reloading data on every click
@st.cache_data
def load_data():
    df = pd.read_csv("business_sales_data.csv")
    # Clean data types
    df["Date"] = pd.to_datetime(df["Date"])
    df["Profit Margin %"] = (df["Profit"] / df["Sales Amount"]) * 100
    return df

df = load_data()

# 3. Create "Slicers" (Sidebar Filters)
st.sidebar.header("Filter Data")
region_filter = st.sidebar.multiselect("Select Region", options=df["Region"].unique(), default=df["Region"].unique())
category_filter = st.sidebar.multiselect("Select Category", options=df["Product Category"].unique(), default=df["Product Category"].unique())

# Apply filters to the dataframe
filtered_df = df[(df["Region"].isin(region_filter)) & (df["Product Category"].isin(category_filter))]

# 4. Calculate KPIs
total_sales = filtered_df["Sales Amount"].sum()
total_profit = filtered_df["Profit"].sum()
avg_margin = filtered_df["Profit Margin %"].mean()
total_units = filtered_df["Quantity Sold"].sum()

# Display KPIs in columns
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Avg Profit Margin", f"{avg_margin:.1f}%")
col4.metric("Units Sold", f"{total_units:,}")

st.markdown("---")

# 5. Charts (The visual part of the dashboard)
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Monthly Sales Trend")
    # Group by month for the line chart
    monthly_sales = filtered_df.groupby(filtered_df["Date"].dt.to_period("M"))["Sales Amount"].sum().reset_index()
    monthly_sales["Date"] = monthly_sales["Date"].dt.to_timestamp()
    fig_trend = px.line(monthly_sales, x="Date", y="Sales Amount", markers=True, color_discrete_sequence=["#005A9C"])
    st.plotly_chart(fig_trend, use_container_width=True)

with col_chart2:
    st.subheader("Sales by Region")
    region_sales = filtered_df.groupby("Region")["Sales Amount"].sum().reset_index()
    fig_region = px.bar(region_sales, x="Region", y="Sales Amount", color="Region", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_region, use_container_width=True)

st.markdown("---")

# Bottom Row: Top Products & Raw Data
col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    st.subheader("Top 5 Products by Sales")
    top_products = filtered_df.groupby("Product Name")["Sales Amount"].sum().nlargest(5).reset_index()
    fig_products = px.bar(top_products, x="Sales Amount", y="Product Name", orientation="h", color_discrete_sequence=["#2ca02c"])
    st.plotly_chart(fig_products, use_container_width=True)

with col_chart4:
    st.subheader("Sales by Category")
    fig_pie = px.pie(filtered_df, names="Product Category", values="Sales Amount", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)