import streamlit as st
import data
import math
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image
import io
import base64
import qrcode
from fpdf import FPDF

def catalog_module():
    st.header("📦 Inventory Catalog")

    df = data.load_inventory()

    # --- Customization Section ---
    with st.expander("⚙️ Customize Catalog View", expanded=False):
        show_category = st.checkbox("Show Category", value=True)
        show_price = st.checkbox("Show Price", value=True)
        show_stock = st.checkbox("Show Stock Badge", value=True)
        show_barcode = st.checkbox("Show Barcode", value=True)
        layout_style = st.radio("Card Layout Style", ["Detailed View", "Compact View"], index=0)

        color_option = st.selectbox("🎨 Theme Color", ["green", "blue", "purple", "orange", "red"], index=0)
        image_fit = st.radio("🖼 Image Fill Mode", ["Contain", "Cover"], index=0)
        barcode_type = st.radio("📦 Barcode Type", ["Code128", "QR"], index=0)

    # Filters
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

    # Apply filters
    if search:
        df = df[df.apply(lambda row: search.lower() in str(row['Item Name']).lower() 
                         or search.lower() in str(row['Category']).lower()
                         or search.lower() in str(row.get('Notes', '')).lower(), axis=1)]
    if category_filter != "All":
        df = df[df['Category'] == category_filter]

    # Sort
    if sort_option == "Item Name (A-Z)":
        df = df.sort_values(by='Item Name', ascending=True)
    elif sort_option == "Price (Low-High)":
        df = df.sort_values(by='Sale Price', ascending=True)
    elif sort_option == "Price (High-Low)":
        df = df.sort_values(by='Sale Price', ascending=False)
    elif sort_option == "Stock (Low-High)":
        df = df.sort_values(by='Quantity', ascending=True)
    elif sort_option == "Stock (High-Low)":
        df = df.sort_values(by='Quantity', ascending=False)

    # PDF Export Button
    if st.button("📄 Export Current Catalog to PDF"):
        pdf_bytes = generate_catalog_pdf(df, show_category, show_price, show_stock, show_barcode, color_option, barcode_type)
        st.success("✅ PDF Generated Successfully!")
        st.download_button("📥 Download Catalog PDF", pdf_bytes, file_name="catalog_export.pdf")

    # Pagination
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_data = df.iloc[start_idx:end_idx]

    object_fit_value = 'contain' if image_fit == 'Contain' else 'cover'

    # Display cards
    for i in range(0, len(page_data), columns_per_row):
        cols = st.columns(columns_per_row)
        for col, (_, row) in zip(cols, page_data.iloc[i:i+columns_per_row].iterrows()):
            with col:
                with st.container():
                    # Image block
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
                    if show_price:
                        st.markdown(f"<div style='text-align:center; font-weight:bold; color:{color_option}; font-size:16px;'>${row['Sale Price']:.2f}</div>", unsafe_allow_html=True)
                    if show_stock:
                        stock_qty = row['Quantity']
                        if stock_qty == 0:
                            badge_color = 'red'; badge_label = 'Out of Stock'
                        elif stock_qty < 5:
                            badge_color = 'orange'; badge_label = 'Low Stock'
                        else:
                            badge_color = 'green'; badge_label = 'In Stock'
                        st.markdown(
                            f"<div style='background-color:{badge_color}; color:white; text-align:center; padding:4px; border-radius:4px; font-size:12px;'>Stock: {stock_qty} ({badge_label})</div>", 
                            unsafe_allow_html=True)

                    if show_barcode:
                        code_value = str(row['Code']) if 'Code' in row else str(row['Item Name'])
                        if barcode_type == "Code128":
                            barcode_img = generate_barcode_image(code_value)
                        else:
                            barcode_img = generate_qr_code(code_value)
                        buffer = io.BytesIO(); barcode_img.save(buffer, format="PNG")
                        b64_barcode = base64.b64encode(buffer.getvalue()).decode()
                        st.markdown(f"""
                        <div style="width: 150px; height: 80px; border-radius: 6px; overflow: hidden; 
                        display: flex; align-items: center; justify-content: center; border: 1px solid #ddd; margin: auto;">
                        <img src="data:image/png;base64,{b64_barcode}" style="width: 100%; height: 100%; object-fit: contain;">
                        </div>""", unsafe_allow_html=True)

    st.write(f"Showing page {page} of {total_pages}")

# Barcode generator
def generate_barcode_image(code_value):
    barcode_io = io.BytesIO()
    options = {'module_width': 0.3,'module_height': 20,'font_size': 8,'text_distance': 1}
    Code128(code_value, writer=ImageWriter()).write(barcode_io, options)
    barcode_io.seek(0)
    return Image.open(barcode_io)

# QR code generator
def generate_qr_code(code_value):
    qr = qrcode.QRCode(box_size=2, border=1)
    qr.add_data(code_value)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# PDF generator
def generate_catalog_pdf(df, show_category, show_price, show_stock, show_barcode, color_option, barcode_type):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    headers = ["Item Name"]
    if show_category: headers.append("Category")
    if show_price: headers.append("Price")
    if show_stock: headers.append("Stock")

    col_width = pdf.w / (len(headers)+1)
    for h in headers:
        pdf.cell(col_width, 10, h, border=1)
    pdf.ln()

    for _, row in df.iterrows():
        pdf.cell(col_width, 10, str(row['Item Name']), border=1)
        if show_category:
            pdf.cell(col_width, 10, str(row['Category']), border=1)
        if show_price:
            pdf.cell(col_width, 10, f"${row['Sale Price']:.2f}", border=1)
        if show_stock:
            pdf.cell(col_width, 10, str(row['Quantity']), border=1)
        pdf.ln()

    pdf_output = io.BytesIO(pdf.output(dest='S'))
    return pdf_output
