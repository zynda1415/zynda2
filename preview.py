import streamlit as st
import data
import math
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image
import io

def catalog_module():
    st.header("📦 Inventory Catalog with Barcodes")

    df = data.load_inventory()

    search = st.text_input("🔎 Search", placeholder="Search Item Name, Category, or Notes...")
    category_filter = st.selectbox("📂 Filter by Category", ["All"] + list(df['Category'].unique()))
    sort_option = st.selectbox("↕️ Sort By", ["Item Name (A-Z)", "Price (Low-High)", "Price (High-Low)", "Stock (Low-High)", "Stock (High-Low)"])
    columns_per_row = st.slider("🖥️ Columns per row", 1, 5, 3)
    items_per_page = st.selectbox("📄 Items per page", [10, 20, 50], index=0)

    if search:
        df = df[df.apply(lambda row: search.lower() in str(row['Item Name']).lower() 
                         or search.lower() in str(row['Category']).lower()
                         or search.lower() in str(row.get('Notes', '')).lower(), axis=1)]
    
    if category_filter != "All":
        df = df[df['Category'] == category_filter]

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

    total_items = len(df)
    total_pages = math.ceil(total_items / items_per_page)
    page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)

    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_data = df.iloc[start_idx:end_idx]

    for i in range(0, len(page_data), columns_per_row):
        cols = st.columns(columns_per_row)
        for col, (_, row) in zip(cols, page_data.iloc[i:i+columns_per_row].iterrows()):
            with col:
                with st.container():
                    st.image(row['Image URL'], width=150)
                    
                    st.markdown(f"<h4 style='text-align:center'>{row['Item Name']}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align:center; color: gray'>Category: {row['Category']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align:center; font-weight:bold; color:green;'>${row['Sale Price']:.2f}</p>", unsafe_allow_html=True)

                    stock_qty = row['Quantity']
                    if stock_qty == 0:
                        color = 'red'
                        label = 'Out of Stock'
                    elif stock_qty < 5:
                        color = 'orange'
                        label = 'Low Stock'
                    else:
                        color = 'green'
                        label = 'In Stock'
                    
                    st.markdown(
                        f"<div style='background-color:{color}; color:white; text-align:center; padding:4px; border-radius:6px;'>"
                        f"Stock: {stock_qty} ({label})</div>", 
                        unsafe_allow_html=True
                    )

                    # Render barcode (assume you have column 'Code')
                    code_value = str(row['Code']) if 'Code' in row else str(row['Item Name'])
                    barcode_img = generate_barcode_image(code_value)
                    st.image(barcode_img, caption=f"Barcode: {code_value}")

def generate_barcode_image(code_value):
    barcode_io = io.BytesIO()
    Code128(code_value, writer=ImageWriter()).write(barcode_io)
    barcode_io.seek(0)
    img = Image.open(barcode_io)
    return img
