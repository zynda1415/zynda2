import streamlit as st
import pandas as pd
import data
from utils import pdf_export

def catalog_module():
    st.header("📦 Professional Catalog Export")

    df = data.load_inventory()

    # Layout Options
    orientation = st.radio("Page Orientation", ["Portrait", "Landscape"])
    columns = st.slider("Columns per Row", 1, 5, 2)
    rows = st.slider("Rows per Page", 1, 5, 3)
    barcode_type = st.selectbox("Barcode Type", ["Code128", "EAN13", "EAN8", "UPCA"])
    cover_page = st.checkbox("Include Cover Page", True)

    # Fields selection
    st.subheader("Fields to Include")
    fields = {
        "image": st.checkbox("Product Image", True),
        "name": st.checkbox("Item Name", True),
        "category": st.checkbox("Category", True),
        "price": st.checkbox("Sale Price", True),
        "stock": st.checkbox("Quantity", True),
        "notes": st.checkbox("Notes", True),
        "barcode": st.checkbox("Barcode", True),
    }

    # Search filter
    search = st.text_input("🔎 Search", placeholder="Filter by name...")
    if search:
        df = df[df['Item Name'].str.contains(search, case=False, na=False)]

    st.dataframe(df)

    if st.button("Generate Catalog PDF"):
        layout = {
            "orientation": "P" if orientation == "Portrait" else "L",
            "columns": columns,
            "rows": rows,
            "barcode_type": barcode_type
        }
        pdf_bytes, filename = pdf_export.generate_catalog_pdf_visual(df, fields, layout, cover_page)
        st.success("✅ PDF Ready!")
        st.download_button("📥 Download PDF", pdf_bytes, file_name=filename)
