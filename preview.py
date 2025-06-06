import streamlit as st
import data
import math
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image
import io

def catalog_module():
    st.header("📦 Inventory Catalog")

    df = data.load_inventory()

    # Inject custom CSS for professional filter bar layout
    st.markdown("""
    <style>
    .filter-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: space-between;
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
    }
    .filter-item {
        flex: 1 1 150px;
        min-width: 150px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Start filter container
    st.markdown("<div class='filter-container'>", unsafe_allow_html=True)

    # Each filter inside same flex box
    with st.container():
        with st.markdown("<div class='filter-item'>", unsafe_allow_html=True):
            search = st.text_input("🔎 Search", placeholder="Name, Category, Notes...")
            st.markdown("</div>", unsafe_allow_html=True)

        with st.markdown("<div class='filter-item'>", unsafe_allow_html=True):
            category_filter = st.selectbox("📂 Category", ["All"] + list(df['Category'].unique()))
            st.markdown("</div>", unsafe_allow_html=True)

        with st.markdown("<div class='filter-item'>", unsafe_allow_html=True):
            sort_option = st.selectbox("↕️ Sort", ["Item Name (A-Z)", "Price (Low-High)", "Price (High-Low)", "Stock (Low-High)", "Stock (High-Low)"])
            st.markdown("</div>", unsafe_allow_html=True)

        with st.markdown("<div class='filter-item'>", unsafe_allow_html=True):
            columns_per_row = st.selectbox("🖥️ Columns", [1, 2, 3, 4, 5], index=2)
            st.markdown("</div>", unsafe_allow_html=True)

        with st.markdown("<div class='filter-item'>", unsafe_allow_html=True):
            items_per_page = st.selectbox("📄 Items/Page", [10, 20, 50], index=0)
            st.markdown("</div>", unsafe_allow_html=True)

        with st.markdown("<div class='filter-item'>", unsafe_allow_html=True):
            total_items = len(df)
            total_pages = math.ceil(total_items / items_per_page)
            page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
            st.markdown("</div>", unsafe_allow_html=True)

    # End filter container
    st.markdown("</div>", unsafe_allow_html=True)

    # Apply filters
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

    # Pagination
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_data = df.iloc[start_idx:end_idx]

    # Display cards
    for i in range(0, len(page_data), columns_per_row):
        cols = st.columns(columns_per_row)
        for col, (_, row) in zip(cols, page_data.iloc[i:i+columns_per_row].iterrows()):
            with col:
                with st.container():
                    # Fixed height image container
                    st.markdown("<div style='height:200px; display:flex; align-items:center; justify-content:center;'>", unsafe_allow_html=True)
                    st.image(row['Image URL'], width=180)
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown(f"<div style='text-align:center; font-weight:700; font-size:18px;'>{row['Item Name']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align:center; font-size:14px; color:gray;'>Category: {row['Category']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align:center; font-weight:bold; color:green; font-size:16px;'>${row['Sale Price']:.2f}</div>", unsafe_allow_html=True)

                    # Stock badge
                    stock_qty = row['Quantity']
                    if stock_qty == 0:
                        badge_color = 'red'
                        badge_label = 'Out of Stock'
                    elif stock_qty < 5:
                        badge_color = 'orange'
                        badge_label = 'Low Stock'
                    else:
                        badge_color = 'green'
                        badge_label = 'In Stock'

                    st.markdown(
                        f"<div style='background-color:{badge_color}; color:white; text-align:center; "
                        f"padding:4px; border-radius:4px; font-size:12px;'>Stock: {stock_qty} ({badge_label})</div>", 
                        unsafe_allow_html=True
                    )

                    # Barcode
                    code_value = str(row['Code']) if 'Code' in row else str(row['Item Name'])
                    barcode_img = generate_barcode_image(code_value)
                    st.image(barcode_img, width=150)

    st.write(f"Showing page {page} of {total_pages}")

# Barcode function
def generate_barcode_image(code_value):
    barcode_io = io.BytesIO()
    options = {
        'module_width': 0.3,
        'module_height': 20,
        'font_size': 8,
        'text_distance': 1,
    }
    Code128(code_value, writer=ImageWriter()).write(barcode_io, options)
    barcode_io.seek(0)
    img = Image.open(barcode_io)
    return img
