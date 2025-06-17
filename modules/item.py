# modules/item.py
import streamlit as st
import pandas as pd
from utils.gsheet import load_sheet, write_sheet
from header_mapper import load_header_map

def inventory_module():
    st.header("📦 Inventory")

    headers = load_header_map()
    df = load_sheet("Inventory")

    # Filter/Search
    search = st.text_input("🔍 Search by name or barcode").lower()
    if search:
        df = df[df[headers["name"]].astype(str).str.lower().str.contains(search) |
                df[headers["barcode"]].astype(str).str.lower().str.contains(search)]

    # Display table
    st.dataframe(df)

    # Add/Edit Item
    with st.expander("➕ Add New Item"):
        new_item = {}
        for key in ["name", "barcode", "category", "quantity", "sell_price", "wholesale_price",
                    "last_purchase_price", "last_purchase_date", "expiry_date", "supplier", "image",
                    "notes", "free_quantity"]:
            value = st.text_input(f"{key.replace('_', ' ').title()}")
            new_item[headers[key]] = value

        if st.button("✅ Save Item"):
            df = df.append(new_item, ignore_index=True)
            write_sheet("Inventory", df)
            st.success("Item added successfully!")

