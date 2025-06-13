import streamlit as st
import pandas as pd
import data
from utils import pdf_export

def inventory_view_module():
    st.title("📦 Inventory Management")

    # 🔄 Load data
    df = data.load_inventory()

    # 🛡 Clean/prepare columns
    if 'Sell Price' in df.columns:
        df['Sell Price'] = pd.to_numeric(df['Sell Price'], errors='coerce').fillna(0)
    else:
        df['Sell Price'] = 0.0

    if 'Supplier' not in df.columns:
        df['Supplier'] = "Unknown"

    st.sidebar.header("🔎 Filters")

    # 🔍 Search + Filters
    search_query = st.sidebar.text_input("Search").lower()

    categories = ["All"] + sorted(df['Category'].dropna().unique()) if 'Category' in df.columns else ["All"]
    selected_category = st.sidebar.selectbox("Category", categories)

    suppliers = ["All"] + sorted(df['Supplier'].dropna().unique())
    selected_supplier = st.sidebar.selectbox("Supplier", suppliers)

    min_price = df['Sell Price'].min()
    max_price = df['Sell Price'].max()
    price_range = st.sidebar.slider("Sell Price Range", float(min_price), float(max_price), (float(min_price), float(max_price)))

    # 🧠 Apply filters
    filtered_df = df.copy()

    if search_query:
        mask = filtered_df.apply(lambda row: search_query in str(row).lower(), axis=1)
        filtered_df = filtered_df[mask]

    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]

    if selected_supplier != "All":
        filtered_df = filtered_df[filtered_df['Supplier'] == selected_supplier]

    filtered_df = filtered_df[
        (filtered_df['Sell Price'] >= price_range[0]) &
        (filtered_df['Sell Price'] <= price_range[1])
    ]

    # 📊 Display data
    st.write(f"### Inventory Items ({len(filtered_df)} items)")
    st.dataframe(filtered_df)

    # 📄 Export to PDF
    if st.button("Export to PDF"):
        pdf_bytes = pdf_export.generate_pdf_table(filtered_df)
        st.download_button("Download PDF", pdf_bytes, file_name="inventory.pdf")
