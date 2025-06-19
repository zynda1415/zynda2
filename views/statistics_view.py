import streamlit as st
import data

def statistics_module():
    inventory_df = data.load_inventory()
    total_items = len(inventory_df)
    total_quantity = inventory_df["Quantity"].sum()
    total_value = (inventory_df["Quantity"] * inventory_df["Sale Price"]).sum()

    st.title("📦 Inventory Statistics")
    st.write(f"Total Items: {total_items}")
    st.write(f"Total Quantity: {total_quantity}")
    st.write(f"Total Inventory Value: ${total_value:,.2f}")
