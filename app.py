# === 1. Imports ===
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === 2. Load & Prepare Data ===
@st.cache_data
def load_data():
    df = pd.read_csv('data/sales_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])  # ensure Date is datetime
    return df

df = load_data()

# === 3. Sidebar Filters ===
st.sidebar.title("Filters")

# 👉 Region filter (optional, only if your CSV has a 'Region' column)
if 'Region' in df.columns:
    regions = df['Region'].unique()
    selected_region = st.sidebar.selectbox("Choose Region", regions)
    df = df[df['Region'] == selected_region]

# 👉 Date Range Filter
start_date = st.sidebar.date_input("Start Date", df['Date'].min())
end_date = st.sidebar.date_input("End Date", df['Date'].max())
df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

# 👉 Customer Filter
customer_ids = df['CustomerID'].unique()
selected_customer = st.sidebar.selectbox("Select Customer", customer_ids)
df = df[df['CustomerID'] == selected_customer]

# === 4. Main Page Title ===
st.title("📊 Sales Insights Dashboard")

# === 5. Show Filtered Data ===
st.subheader("Filtered Sales Data")
st.dataframe(df)

# === 6. Top 5 Products by Sales ===
if 'Product' in df.columns:
    top_products = df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(5)
    st.subheader("Top 5 Products by Sales")
    st.bar_chart(top_products)

# === 7. Sales Trend Over Time ===
monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Sales'].sum().reset_index()
monthly_sales['Date'] = monthly_sales['Date'].dt.to_timestamp()

st.subheader("Monthly Sales Trend")
fig, ax = plt.subplots()
sns.lineplot(data=monthly_sales, x='Date', y='Sales', marker='o', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)
