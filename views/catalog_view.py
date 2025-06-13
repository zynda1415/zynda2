import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import math
import pandas as pd
from config import HEADER_ALIASES
from data import load_inventory_data
from preview import customization, style, barcode_utils, pdf_Customization
from utils import pdf_export


# Set inventory alias
H = HEADER_ALIASES["Inventory"]

def catalog_module():
    st.header("📘 View Catalog")

    df = load_inventory_data()
    if df.empty:
        st.warning("No items to display.")
        return

    # === UI Controls ===
    (show_category, show_price, show_stock, show_barcode,
     layout_style, color_option, image_fit, barcode_type,
     export_layout, include_cover_page) = customization.customization_controls(df)

    style.apply_global_styles()

    col1, col2, col3, col4 = st.columns([2.5, 1.7, 1.7, 2])
    with col1:
        search = st.text_input("🔍 Search", placeholder="Name, Category, Note...")
    with col2:
        category_filter = st.selectbox("📁 Category", ["All"] + sorted(df[H["category"]].dropna().unique()))
    with col3:
        brand_filter = st.selectbox("🏷️ Brand", ["All"] + sorted(df[H["brand"]].dropna().unique()))
    with col4:
        columns_per_row = st.slider("📐 Columns", 1, 5, 3)

    # === Filter + Search ===
    filtered_df = df.copy()
    if search:
        search_lower = search.lower()
        filtered_df = filtered_df[filtered_df.apply(
            lambda row: search_lower in str(row.get(H["name"], "")).lower()
            or search_lower in str(row.get(H["category"], "")).lower()
            or search_lower in str(row.get(H["note"], "")).lower(),
            axis=1
        )]
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df[H["category"]] == category_filter]
    if brand_filter != "All":
        filtered_df = filtered_df[filtered_df[H["brand"]] == brand_filter]

    # === Display Cards ===
    render_cards(filtered_df, columns_per_row, show_category, show_price, show_stock,
                 show_barcode, color_option, image_fit, barcode_type)

    # === Export to PDF ===
    st.markdown("---")
    st.subheader("📤 Export Visual Catalog")
    if st.button("📄 Export to PDF"):
        pdf_bytes, filename = pdf_export.generate_catalog_pdf_visual(
            filtered_df, show_category, show_price, show_stock, show_barcode, barcode_type,
            color_option, export_layout, include_cover_page, logo_path=None, language='EN',
            selected_categories=[category_filter] if category_filter != "All" else None,
            selected_brands=[brand_filter] if brand_filter != "All" else None
        )
        st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name=filename)

def render_cards(df, cols, show_category, show_price, show_stock, show_barcode,
                 color_option, image_fit, barcode_type):
    if df.empty:
        st.info("No matching items.")
        return

    rows = math.ceil(len(df) / cols)
    for r in range(rows):
        card_row = st.columns(cols)
        for i in range(cols):
            idx = r * cols + i
            if idx >= len(df): break
            row = df.iloc[idx]
            with card_row[i]:
                style.render_card(
                    name=row.get(H["name"], "Unnamed"),
                    image_url=row.get(H["image"], ""),
                    price=row.get(H["price"], ""),
                    category=row.get(H["category"], ""),
                    note=row.get(H["note"], ""),
                    brand=row.get(H["brand"], ""),
                    stock=row.get(H.get("stock", ""), "N/A"),
                    code=row.get(H.get("code", ""), ""),
                    barcode=row.get(H.get("barcode", ""), ""),
                    show_category=show_category,
                    show_price=show_price,
                    show_stock=show_stock,
                    show_barcode=show_barcode,
                    color_option=color_option,
                    image_fit=image_fit,
                    barcode_type=barcode_type
                )
