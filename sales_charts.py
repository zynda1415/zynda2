import streamlit as st
import data
import pandas as pd
import altair as alt

def sales_charts_module():
    st.header("📈 Sales Charts")

    sales_df = data.load_sales()

    if sales_df.empty:
        st.warning("No sales data available.")
        return

    # Ensure correct data types
    sales_df['Total Price'] = pd.to_numeric(sales_df['Total Price'], errors='coerce')
    sales_df['Quantity Sold'] = pd.to_numeric(sales_df['Quantity Sold'], errors='coerce')
    sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')

    # Sales per item bar chart
    st.subheader("Top Selling Items")
    item_summary = sales_df.groupby('Item').agg({'Total Price': 'sum'}).reset_index()
    chart = alt.Chart(item_summary).mark_bar().encode(
        x=alt.X('Item', sort='-y'),
        y='Total Price',
        tooltip=['Item', 'Total Price']
    ).properties(width=700, height=400)
    st.altair_chart(chart)

    # Sales over time line chart
    st.subheader("Sales Over Time")
    date_summary = sales_df.groupby('Date').agg({'Total Price': 'sum'}).reset_index()
    line_chart = alt.Chart(date_summary).mark_line(point=True).encode(
        x='Date',
        y='Total Price',
        tooltip=['Date', 'Total Price']
    ).properties(width=700, height=400)
    st.altair_chart(line_chart)
