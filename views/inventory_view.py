import streamlit as st
import pandas as pd
import data
from utils import pdf_export

def inventory_view_module():
    st.title("📦 Inventory Management")

    df = data.load_inventory()

    st.sidebar.header("🔎 Filters")
    search_query = st.sidebar.text_input("Search").lower()

    categories = ["All"] + sorted(df['Category 1'].dropna().unique())
    selected_category = st.sidebar.selectbox("Category", categories)

    brands = ["All"] + sorted(df['Brand'].dropna().unique())
    selected_brand = st.sidebar.selectbox("Brand", brands)

    min_price = float(df['Sell Price'].min())
    max_price = float(df['Sell Price'].max())
    price_range = st.sidebar.slider("Sell Price Range", min_price, max_price, (min_price, max_price))

    filtered_df = df.copy()

    if search_query:
        mask = df.apply(lambda row: search_query in str(row).lower(), axis=1)
        filtered_df = filtered_df[mask]

    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['Category 1'] == selected_category]

    if selected_brand != "All":
        filtered_df = filtered_df[filtered_df['Brand'] == selected_brand]

    filtered_df = filtered_df[
        (filtered_df['Sell Price'] >= price_range[0]) &
        (filtered_df['Sell Price'] <= price_range[1])
    ]

    st.write(f"### Inventory List ({len(filtered_df)} items)")
    st.dataframe(filtered_df)

    if st.button("Export to PDF"):
        pdf_bytes = pdf_export.generate_pdf_table(filtered_df)
        st.download_button("Download PDF", pdf_bytes, file_name="inventory.pdf")
