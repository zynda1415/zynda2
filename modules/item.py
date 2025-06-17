import streamlit as st
import pandas as pd
from modules.header_mapper import get_headers
from data import load_inventory_data, save_inventory_data

H = get_headers("Inventory")

def render_item_section():
    st.title("📦 Inventory Management")

    try:
        df = load_inventory_data()
    except Exception as e:
        st.error(f"Failed to load inventory data: {e}")
        return

    st.sidebar.header("🔍 Filter Items")
    brands = ["All"] + sorted(df[H["brand"]].dropna().unique())
    selected_brand = st.sidebar.selectbox("Supplier", brands)

    if selected_brand != "All":
        df = df[df[H["brand"]] == selected_brand]

    st.write(f"### Total Items: {len(df)}")
    st.dataframe(df)

    with st.expander("➕ Add New Item"):
        with st.form("add_item_form", clear_on_submit=True):
            name = st.text_input("Item Name")
            price = st.number_input("Sell Price", min_value=0.0, step=0.1)
            stock = st.number_input("Stock Quantity", min_value=0, step=1)
            brand = st.text_input("Supplier")
            category = st.text_input("Category")
            note = st.text_area("Notes")
            image_url = st.text_input("Image URL")
            barcode = st.text_input("Barcode")

            if st.form_submit_button("✅ Save Item"):
                new_item = {
                    H["name"]: name,
                    H["price"]: price,
                    H["stock"]: stock,
                    H["brand"]: brand,
                    H["category"]: category,
                    H["note"]: note,
                    H["image"]: image_url,
                    H["barcode"]: barcode,
                }
                df = pd.concat([df, pd.DataFrame([new_item])], ignore_index=True)
                save_inventory_data(df)
                st.success("✅ Item added successfully!")
