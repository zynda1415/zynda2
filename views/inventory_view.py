import streamlit as st
import pandas as pd
import data
from utils import pdf_export

def inventory_view_module():
    st.title("📦 Inventory Management")

    df = data.load_inventory()

    # Sidebar filters
    st.sidebar.header("🔎 Filters")

    search_query = st.sidebar.text_input("Search").lower()

    # ✅ Use your real column name: 'Category'
    categories = ["All"] + sorted(df['Category'].dropna().unique())
    selected_category = st.sidebar.selectbox("Category", categories)

    suppliers = ["All"] + sorted(df['Supplier'].dropna().unique())
    selected_supplier = st.sidebar.selectbox("Supplier", suppliers)

    min_price = float(df['Sale Price'].min())
    max_price = float(df['Sale Price'].max())
    price_range = st.sidebar.slider("Sale Price Range", min_price, max_price, (min_price, max_price))

    filtered_df = df.copy()

    # Apply search filter
    if search_query:
        mask = df.apply(lambda row: search_query in str(row).lower(), axis=1)
        filtered_df = filtered_df[mask]

    # Apply category filter
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]

    # Apply supplier filter
    if selected_supplier != "All":
        filtered_df = filtered_df[filtered_df['Supplier'] == selected_supplier]

    # Apply price range filter
    filtered_df = filtered_df[
        (filtered_df['Sale Price'] >= price_range[0]) &
        (filtered_df['Sale Price'] <= price_range[1])
    ]

    st.write(f"### Inventory Items ({len(filtered_df)} items)")
    st.dataframe(filtered_df)

    # Export to PDF
    if st.button("Export to PDF"):
        pdf_bytes = pdf_export.generate_pdf_table(filtered_df)
        st.download_button("Download PDF", pdf_bytes, file_name="inventory.pdf")
