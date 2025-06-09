import streamlit as st
import pandas as pd
import data
from utils import pdf_export

def catalog_module():
    st.header("📦 Inventory Catalog Export")

    # Load data
    df = data.load_inventory()

    # ✅ Paper options
    orientation = st.selectbox("Page Orientation", ["Portrait", "Landscape"])
    paper_orientation = "P" if orientation == "Portrait" else "L"

    # ✅ Layout options
    columns_per_row = st.slider("Columns Per Row", 1, 5, 2)
    rows_per_page = st.slider("Rows Per Page", 1, 6, 3)

    # ✅ Field selection
    st.subheader("Select fields to include:")
    show_image = st.checkbox("Product Image", value=True)
    show_name = st.checkbox("Item Name", value=True)
    show_category = st.checkbox("Category", value=True)
    show_price = st.checkbox("Sale Price", value=True)
    show_stock = st.checkbox("Quantity", value=True)
    show_notes = st.checkbox("Notes", value=True)
    show_barcode = st.checkbox("Barcode", value=True)

    # ✅ Barcode type
    barcode_type = st.selectbox("Barcode Type", ["Code128", "EAN13", "EAN8", "UPCA"])

    # ✅ Cover page
    include_cover_page = st.checkbox("Include Cover Page", value=True)

    # ✅ Search filter (optional for preview)
    search = st.text_input("🔎 Search", placeholder="Search by Item Name or Category")
    if search:
        df = df[df['Item Name'].str.contains(search, case=False, na=False)]

    # ✅ Show preview
    st.write("Preview:")
    st.dataframe(df)

    # ✅ Export button
    if st.button("Generate Catalog PDF"):
        pdf_bytes, filename = pdf_export.generate_catalog_pdf_visual(
            df, 
            show_image, show_name, show_category, show_price, show_stock, 
            show_notes, show_barcode, barcode_type, 
            paper_orientation, columns_per_row, rows_per_page, include_cover_page
        )
        st.success("✅ PDF Generated Successfully!")
        st.download_button("📥 Download PDF", pdf_bytes, file_name=filename)
