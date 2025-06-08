import pandas as pd
import streamlit as st
import data

def sales_summary_module():
    st.header("📊 Sales Summary")

    sales_df = data.load_sales()

    if sales_df.empty:
        st.warning("No sales data available.")
        return

    sales_df['Total Price'] = pd.to_numeric(sales_df['Total Price'], errors='coerce')
    sales_df['Quantity Sold'] = pd.to_numeric(sales_df['Quantity Sold'], errors='coerce')

    total_revenue = sales_df['Total Price'].sum()
    total_quantity = sales_df['Quantity Sold'].sum()

    st.subheader("Overall Sales")
    st.write(f"💰 Total Revenue: **${total_revenue:,.2f}**")
    st.write(f"📦 Total Quantity Sold: **{int(total_quantity)}**")

    st.subheader("Top Selling Items")
    summary = sales_df.groupby('Item').agg({'Quantity Sold': 'sum', 'Total Price': 'sum'}).sort_values(by='Total Price', ascending=False)
    st.dataframe(summary)
