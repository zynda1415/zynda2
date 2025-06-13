# --- catalog_view.py ---
import streamlit as st
import math
import data
import preview.customization as customization
import preview.style as style
import preview.barcode_utils as barcode_utils
import utils.pdf_export as pdf_export
import base64
import io
from preview.pdf_Customization import pdf_customization_controls
from PIL import Image

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
        df = df[df.apply(lambda row: search.lower() in str(row['Item Name']).lower() 
                         or search.lower() in str(row['Category']).lower()
                         or search.lower() in str(row.get('Notes', '')).lower(), axis=1)]
    if category_filter != "All":
        df = df[df['Category'] == category_filter]

    df = apply_sort(df, sort_option)

    if st.button("📄 Export Visual Catalog to PDF"):
        # Patch keys for PDF compatibility
        df = df.rename(columns={"Sale Price": "Sell Price", "Supplier": "Brand"})
        pdf_bytes, filename = pdf_export.generate_catalog_pdf_visual(df)
        st.success("PDF Generated Successfully!")
        st.download_button("Download PDF", data=pdf_bytes, file_name=filename)

    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_data = df.iloc[start_idx:end_idx]

    render_cards(page_data, columns_per_row, show_category, show_price, show_stock, show_barcode,
                 color_option, image_fit, barcode_type)

def apply_sort(df, sort_option):
    if sort_option == "Item Name (A-Z)":
        return df.sort_values(by='Item Name', ascending=True)
    elif sort_option == "Price (Low-High)":
        return df.sort_values(by='Sale Price', ascending=True)
    elif sort_option == "Price (High-Low)":
        return df.sort_values(by='Sale Price', ascending=False)
    elif sort_option == "Stock (Low-High)":
        return df.sort_values(by='Quantity', ascending=True)
    elif sort_option == "Stock (High-Low)":
        return df.sort_values(by='Quantity', ascending=False)
    return df

def render_cards(df, columns_per_row, show_category, show_price, show_stock, show_barcode, color_option, image_fit, barcode_type):
    object_fit_value = 'contain' if image_fit == 'Contain' else 'cover'
    for i in range(0, len(df), columns_per_row):
        cols = st.columns(columns_per_row)
        for col, (_, row) in zip(cols, df.iloc[i:i+columns_per_row].iterrows()):
            with col:
                with st.container():
                    st.markdown(f"""
                    <div style="
                        width: 200px; height: 200px; border-radius: 10px; overflow: hidden; 
                        display: flex; align-items: center; justify-content: center;
                        border: 1px solid #ddd; margin: auto;">
                        <img src="{row['Image URL']}" style="width: 100%; height: 100%; object-fit: {object_fit_value};">
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"<div style='text-align:center; font-weight:700; font-size:18px;'>{row['Item Name']}</div>", unsafe_allow_html=True)

                    if show_category:
                        st.markdown(f"<div style='text-align:center; font-size:14px; color:gray;'>Category: {row['Category']}</div>", unsafe_allow_html=True)
                    if show_price and 'Sale Price' in row:
                        st.markdown(f"<div style='text-align:center; font-weight:bold; color:{color_option}; font-size:16px;'>${row['Sale Price']:.2f}</div>", unsafe_allow_html=True)

                    if show_stock:
                        stock_qty = row['Quantity']
                        badge_color, badge_label = get_stock_badge(stock_qty)
                        st.markdown(
                            f"<div style='background-color:{badge_color}; color:white; text-align:center; padding:4px; border-radius:4px; font-size:12px;'>Stock: {stock_qty} ({badge_label})</div>", 
                            unsafe_allow_html=True)

                    if show_barcode and 'Barcode' in df.columns:
                        b64_barcode = barcode_utils.encode_image(row['Barcode'], barcode_type)
                        st.markdown(f"""
                        <div style="
                            width: 220px; height: 80px; border-radius: 8px; overflow: hidden; 
                            display: flex; align-items: center; justify-content: center; 
                            border: 1px solid #ddd; margin: auto; margin-top:10px;">
                            <img src="data:image/png;base64,{b64_barcode}" 
                                 style="width:100%; height:100%; object-fit:cover;">
                        </div>
                        """, unsafe_allow_html=True)

def get_stock_badge(stock_qty):
    if stock_qty == 0:
        return 'red', 'Out of Stock'
    elif stock_qty < 5:
        return 'orange', 'Low Stock'
    else:
        return 'green', 'In Stock'
