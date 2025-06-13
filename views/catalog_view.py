# --- catalog_view.py ---
import streamlit as st
import math
import data
import preview.customization as customization
import preview.style as style
import preview.barcode_utils as barcode_utils
import utils.pdf_export as pdf_export
from preview.pdf_Customization import pdf_customization_controls
from PIL import Image
import base64
import io
import pandas as pd

def decode_base64_to_image(b64_data):
    img_data = base64.b64decode(b64_data)
    img = Image.open(io.BytesIO(img_data))
    return img

def catalog_module():
    st.header("📦 Inventory Catalog")

    df = data.load_inventory()

    (show_category, show_price, show_stock, show_barcode, layout_style, 
     color_option, image_fit, barcode_type, export_layout, include_cover_page) = customization.customization_controls(df)

    style.apply_global_styles()

    col1, col2, col3, col4, col5, col6 = st.columns([2.5, 1.7, 1.7, 1.2, 1.2, 1.2])
    with col1:
        search = st.text_input("🔎 Search", placeholder="Name, Category, Notes...")
    with col2:
        category_filter = st.selectbox("📂 Category", ["All"] + list(df['Category'].unique()))
    with col3:
        sort_option = st.selectbox("↕️ Sort", ["Item Name (A-Z)", "Price (Low-High)", "Price (High-Low)", "Stock (Low-High)", "Stock (High-Low)"])
    with col4:
        columns_per_row = st.selectbox("🖥️ Columns", [1, 2, 3, 4, 5], index=2)
    with col5:
        items_per_page = st.selectbox("📄 Items/Page", [10, 20, 50], index=0)
    with col6:
        total_items = len(df)
        total_pages = math.ceil(total_items / items_per_page)
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)

    if search:
        df = df[df.apply(lambda row: search.lower() in str(row['Item Name (English)']).lower() 
                         or search.lower() in str(row['Category']).lower()
                         or search.lower() in str(row.get('Notes', '')).lower(), axis=1)]
    if category_filter != "All":
        df = df[df['Category'] == category_filter]

    df = apply_sort(df, sort_option)

    if st.button("📄 Export Visual Catalog to PDF"):
        try:
            pdf_df = df.copy()

            # fix headers
            if 'Supplier' in pdf_df.columns and 'Brand' not in pdf_df.columns:
                pdf_df['Brand'] = pdf_df['Supplier']
            if 'Quantity' in pdf_df.columns and 'Stock' not in pdf_df.columns:
                pdf_df['Stock'] = pdf_df['Quantity']
            if 'Category' in pdf_df.columns and 'Category 1' not in pdf_df.columns:
                pdf_df['Category 1'] = pdf_df['Category']
            if 'Notes' in pdf_df.columns and 'Note' not in pdf_df.columns:
                pdf_df['Note'] = pdf_df['Notes']

            required_columns = {
                'Item Name (English)': 'Unknown Item',
                'Sell Price': 0.0,
                'Stock': 0,
                'Brand': 'Unknown Brand',
                'Category 1': 'Uncategorized',
                'Note': '',
                'Image URL': '',
                'Barcode': ''
            }

            for col, default_val in required_columns.items():
                if col not in pdf_df.columns:
                    pdf_df[col] = default_val

            pdf_options = pdf_customization_controls()

            pdf_bytes, filename = pdf_export.generate_catalog_pdf_visual(
                pdf_df,
                image_position=pdf_options["image_position"],
                name_font_size=pdf_options["name_font_size"],
                stack_text=pdf_options["stack_text"],
                show_barcode=pdf_options["show_barcode_pdf"]
            )

            st.success("PDF Generated Successfully!")
            st.download_button("Download PDF", data=pdf_bytes, file_name=filename)

        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
            st.write("DataFrame columns available:", list(df.columns))

    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_data = df.iloc[start_idx:end_idx]

    render_cards(page_data, columns_per_row, show_category, show_price, show_stock, show_barcode,
                 color_option, image_fit, barcode_type)

def apply_sort(df, sort_option):
    if sort_option == "Item Name (A-Z)":
        return df.sort_values(by='Item Name (English)', ascending=True)
    elif sort_option == "Price (Low-High)":
        return df.sort_values(by='Sell Price', ascending=True)
    elif sort_option == "Price (High-Low)":
        return df.sort_values(by='Sell Price', ascending=False)
    elif sort_option == "Stock (Low-High)":
        return df.sort_values(by='Quantity', ascending=True)
    elif sort_option == "Stock (High-Low)":
        return df.sort_values(by='Quantity', ascending=False)
    return df
