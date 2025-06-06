import streamlit as st
import data
import pandas as pd
from fpdf import FPDF
import tempfile
import os

def export_pdf_module():
    st.header("📄 Export Reports to PDF")

    options = ["Inventory", "Sales Summary"]
    report_type = st.selectbox("Select Report Type", options)

    if report_type == "Inventory":
        df = data.load_inventory()
        filename = "inventory_report.pdf"
        pdf_bytes = generate_pdf(df)
        st.success("PDF Generated Successfully!")
        st.download_button("Download Inventory PDF", pdf_bytes, file_name=filename)

    elif report_type == "Sales Summary":
        sales_df = data.load_sales()
        sales_df['Total Price'] = pd.to_numeric(sales_df['Total Price'], errors='coerce')
        sales_df['Quantity Sold'] = pd.to_numeric(sales_df['Quantity Sold'], errors='coerce')

        summary = sales_df.groupby('Item').agg({'Quantity Sold': 'sum', 'Total Price': 'sum'}).reset_index()
        filename = "sales_summary_report.pdf"
        pdf_bytes = generate_pdf(summary)
        st.success("PDF Generated Successfully!")
        st.download_button("Download Sales Summary PDF", pdf_bytes, file_name=filename)

def generate_pdf(df):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        temp_filename = tmp_file.name
    
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        # Calculate column width
        col_width = pdf.w / (len(df.columns) + 1)

        # Add headers
        for col in df.columns:
            pdf.cell(col_width, 10, str(col), border=1)
        pdf.ln()

        # Add data rows
        for i, row in df.iterrows():
            for item in row:
                pdf.cell(col_width, 10, str(item), border=1)
            pdf.ln()

        # Output to temporary file
        pdf.output(temp_filename)
        
        # Read the file and return bytes
        with open(temp_filename, 'rb') as f:
            pdf_bytes = f.read()
            
        return pdf_bytes
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)
