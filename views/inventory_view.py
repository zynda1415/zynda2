import streamlit as st
import pandas as pd
import data
from fpdf import FPDF
import io

def inventory_view_module():
    st.title("📦 Inventory Management")

    # Load inventory from your Google Sheet
    df = data.load_inventory()

    # =============================
    # Professional Filters Section
    # =============================

    st.sidebar.header("🔎 Filters")

    # Search box (multi-field search)
    search_query = st.sidebar.text_input("Search (name, notes...)").lower()

    # Category filter
    categories = ["All"] + sorted(df['Category 1'].dropna().unique())
    selected_category = st.sidebar.selectbox("Category", categories)

    # Brand filter
    brands = ["All"] + sorted(df['Brand'].dropna().unique())
    selected_brand = st.sidebar.selectbox("Brand", brands)

    # Price Range filter
    min_price = float(df['Sell Price'].min())
    max_price = float(df['Sell Price'].max())
    price_range = st.sidebar.slider("Sell Price Range", min_price, max_price, (min_price, max_price))

    # Stock Availability
    stock_filter = st.sidebar.radio("Stock Availability", ["All", "In Stock", "Out of Stock"])

    # Apply filters
    filtered_df = df.copy()

    if search_query:
        mask = df.apply(lambda row: search_query in str(row).lower(), axis=1)
        filtered_df = filtered_df[mask]

    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['Category 1'] == selected_category]

    if selected_brand != "All":
        filtered_df = filtered_df[filtered_df['Brand'] == selected_brand]

    filtered_df = filtered_df[
        (filtered_df['Sell Price'] >= price_range[0]) &
        (filtered_df['Sell Price'] <= price_range[1])
    ]

    if stock_filter == "In Stock":
        filtered_df = filtered_df[filtered_df['Stock'] > 0]
    elif stock_filter == "Out of Stock":
        filtered_df = filtered_df[filtered_df['Stock'] <= 0]

    st.write(f"### Inventory List ({len(filtered_df)} items)")
    st.dataframe(filtered_df)

    # =============================
    # Export to PDF
    # =============================
    if st.button("Export to PDF"):
        pdf_bytes = generate_pdf_table(filtered_df)
        st.download_button("Download PDF", pdf_bytes, file_name="inventory.pdf")


# ==================================
# PDF Export Logic (Table Style)
# ==================================

def generate_pdf_table(df):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 10)
    pdf.add_page()

    # Table headers
    headers = ["Item Name (EN)", "Sell Price", "Stock", "Brand", "Category", "Note"]
    col_widths = [60, 30, 20, 40, 40, 60]

    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, border=1)

    pdf.ln()

    # Table rows
    for index, row in df.iterrows():
        values = [
            str(row['Item Name (English)']),
            f"{row['Sell Price']}",
            f"{row['Stock']}",
            str(row['Brand']),
            str(row['Category 1']),
            str(row['Note'])
        ]

        for i, value in enumerate(values):
            pdf.cell(col_widths[i], 10, value, border=1)

        pdf.ln()

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    return pdf_output.getvalue()
