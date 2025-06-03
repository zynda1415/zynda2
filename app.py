import streamlit as st
import pandas as pd
import data
import item

st.set_page_config(page_title="Inventory Management", layout="wide")
st.title("📦 Inventory Management System")

df = data.load_data()

menu = st.sidebar.radio("Menu", ["View Inventory", "Item", "Statistics"])

if menu == "View Inventory":
    st.subheader("Inventory List")
    search = st.text_input("Search by Item Name")
    category_filter = st.selectbox("Filter by Category", ['All'] + sorted(df['Category'].dropna().unique()))

    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df['Item Name'].str.contains(search, case=False, na=False)]
    if category_filter != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == category_filter]

    st.dataframe(filtered_df, use_container_width=True)

elif menu == "Item":
    item.render_item_section(df, data.add_item, data.edit_item, data.delete_item)

elif menu == "Statistics":
    st.subheader("Inventory Statistics")
    total_items = len(df)
    total_quantity = df['Quantity'].sum() if not df.empty else 0
    total_value = (df['Quantity'] * df['Sale Price']).sum() if not df.empty else 0

    st.write(f"Total Items: {total_items}")
    st.write(f"Total Quantity: {total_quantity}")
    st.write(f"Total Inventory Value: ${total_value:,.2f}")
