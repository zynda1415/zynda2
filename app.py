
import streamlit as st
import preview
import item
import mapview
import data
import sales_charts
import sales
import sales_summary

st.set_page_config(page_title="Inventory Management System", layout="wide")

menu = st.sidebar.radio("Menu", [
    "View Inventory", "Item", "Statistics", "Catalog View", 
    "Map", "Sales", "Sales Summary", "Sales Charts"
])


if menu == "View Inventory":
    df = data.load_inventory()
    st.title("📦 Inventory Management System")
    st.dataframe(df)

elif menu == "Item":
    item.item_module()

elif menu == "Statistics":
    inventory_df = data.load_inventory()
    total_items = len(inventory_df)
    total_quantity = inventory_df["Quantity"].sum()
    total_value = (inventory_df["Quantity"] * inventory_df["Sale Price"]).sum()
    st.title("📦 Inventory Management System")
    st.subheader("Inventory Statistics")
    st.write(f"Total Items: {total_items}")
    st.write(f"Total Quantity: {total_quantity}")
    st.write(f"Total Inventory Value: ${total_value:,.2f}")

elif menu == "Catalog View":
    preview.catalog_module()

elif menu == "Map":
    mapview.map_module()

elif menu == "Sales":
    sales.sales_module()

elif menu == "Sales Charts":
    sales_charts.sales_charts_module()

elif menu == "Sales Summary":
    sales_summary.sales_summary_module()
