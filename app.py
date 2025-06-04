import streamlit as st
import pandas as pd
import data
import item
import preview

st.set_page_config(page_title="Inventory Management", layout="wide")
st.title("📦 Inventory Management System")

df = data.load_data()

menu = st.sidebar.radio("Menu", ["View Inventory", "Item", "Statistics", "Catalog View", "Map"])

# View Inventory Tab
if menu == "View Inventory":
    preview.render_preview(df)

# Item Management Tab
elif menu == "Item":
    item.render_item_section(df, data.add_item, data.edit_item, data.delete_item)

# Statistics Tab
elif menu == "Statistics":
    st.subheader("Inventory Statistics")
    total_items = len(df)
    total_quantity = df['Quantity'].sum() if not df.empty else 0
    total_value = (df['Quantity'] * df['Sale Price']).sum() if not df.empty else 0

    st.write(f"Total Items: {total_items}")
    st.write(f"Total Quantity: {total_quantity}")
    st.write(f"Total Inventory Value: ${total_value:,.2f}")

# Catalog View Tab
elif menu == "Catalog View":
    preview.render_preview(df)

# Map Tab
elif menu == "Map":
    st.subheader("📍 Inventory Map View")

    if 'Latitude' in df.columns and 'Longitude' in df.columns:
        # Only show map if coordinates exist
        map_data = df[['Latitude', 'Longitude']].dropna()
        if not map_data.empty:
            st.map(map_data)
        else:
            st.warning("Latitude/Longitude columns exist, but no data found.")
    else:
        st.warning("No Latitude/Longitude columns found in your sheet.")
