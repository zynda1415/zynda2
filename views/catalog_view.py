# views/catalog_view.py
import streamlit as st
from PIL import Image
import requests
import io
from header_mapper import load_header_map
from utils.gsheet import load_sheet
from utils import barcode_utils, pdf_export

def catalog_module():
    st.header("📘 Product Catalog")

    headers = load_header_map()
    df = load_sheet("Inventory")

    search = st.text_input("🔍 Search by name/category").lower()
    if search:
        df = df[df[headers["name"]].str.lower().str.contains(search) |
                df[headers["category"]].str.lower().str.contains(search)]

    st.markdown("### 🖼️ Product Cards")
    cols = st.columns(3)

    for i, (_, row) in enumerate(df.iterrows()):
        with cols[i % 3]:
            st.subheader(row[headers["name"]])
            try:
                img = Image.open(requests.get(row[headers["image"]], stream=True).raw)
                st.image(img, use_column_width=True)
            except:
                st.image("https://via.placeholder.com/150", use_column_width=True)
            st.write(f"💵 {row[headers['sell_price']]}")
            st.write(f"📦 Stock: {row[headers['quantity']]}")
            barcode_img = barcode_utils.generate_barcode_image(str(row[headers["barcode"]]))
            if barcode_img:
                st.image(barcode_img, caption="Barcode")

    if st.button("📥 Export to PDF"):
        pdf_bytes, filename = pdf_export.generate_catalog_pdf_visual(df, headers)
        st.download_button("Download PDF", data=pdf_bytes, file_name=filename)
