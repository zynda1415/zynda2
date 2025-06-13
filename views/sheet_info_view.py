import streamlit as st
import pandas as pd
import data
from utils import pdf_export
from config import HEADER_ALIASES as H

def inventory_view_module():
    st.title("📦 Inventory Management")

    col = H["Inventory"]
    df = data.load_inventory()

    df[col["price"]] = pd.to_numeric(df[col["price"]], errors='coerce').fillna(0)
    df[col["brand"]] = df[col["brand"]].astype(str)

    st.sidebar.header("🔎 Filters")

    search_query = st.sidebar.text_input("Search").lower()
    categories = ["All"] + sorted(df[col["category"]].dropna().unique())
    selected_category = st.sidebar.selectbox("Category", categories)

    suppliers = ["All"] + sorted(df[col["brand"]].dropna().unique())
    selected_supplier = st.sidebar.selectbox("Supplier", suppliers)

    min_price = df[col["price"]].min()
    max_price = df[col["price"]].max()
    price_range = st.sidebar.slider("Sell Price Range", float(min_price), float(max_price), (float(min_price), float(max_price)))

    filtered_df = df.copy()

    if search_query:
        mask = df.apply(lambda row: search_query in str(row).lower(), axis=1)
        filtered_df = filtered_df[mask]

    if selected_category != "All":
        filtered_df = filtered_df[filtered_df[col["category"]] == selected_category]

    if selected_supplier != "All":
        filtered_df = filtered_df[filtered_df[col["brand"]] == selected_supplier]

    filtered_df = filtered_df[
        (filtered_df[col["price"]] >= price_range[0]) &
        (filtered_df[col["price"]] <= price_range[1])
    ]

    st.write(f"### Inventory Items ({len(filtered_df)} items)")
    st.dataframe(filtered_df)

    if st.button("Export to PDF"):
        pdf_bytes = pdf_export.generate_pdf_table(filtered_df)
        st.download_button("Download PDF", pdf_bytes, file_name="inventory.pdf")
