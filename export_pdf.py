import streamlit as st
import data
import pandas as pd
from fpdf import FPDF
from datetime import datetime

class SimplePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_font("Arial", size=10)
        self.set_auto_page_break(auto=True, margin=15)

    def add_title(self, title):
        self.set_font("Arial", 'B', 16)
        self.cell(0, 10, title, ln=True, align='C')
        self.ln(10)

    def add_table(self, df):
        col_width = self.w / (len(df.columns) + 1)
        self.set_font("Arial", 'B', 10)
        for col in df.columns:
            self.cell(col_width, 10, str(col), border=1)
        self.ln()

        self.set_font("Arial", '', 10)
        for _, row in df.iterrows():
            for item in row:
                self.cell(col_width, 10, str(item), border=1)
            self.ln()

def export_pdf_module():
    st.header("🪶 Lightweight PDF Export")
    
    report_options = ["Inventory Report", "Sales Summary"]
    report_type = st.selectbox("Select Report Type", report_options)

    if st.button("Generate PDF"):
        if report_type == "Inventory Report":
            df = data.load_inventory()
            filename = "inventory_report.pdf"
            pdf_bytes = generate_pdf(df, "Inventory Report")
            st.download_button("Download Inventory PDF", pdf_bytes, file_name=filename, mime="application/pdf")
            
        elif report_type == "Sales Summary":
            df = data.load_sales()
            df['Total Price'] = pd.to_numeric(df['Total Price'], errors='coerce')
            df['Quantity Sold'] = pd.to_numeric(df['Quantity Sold'], errors='coerce')
            summary = df.groupby('Item').agg({'Quantity Sold': 'sum', 'Total Price': 'sum'}).reset_index()
            filename = "sales_summary_report.pdf"
            pdf_bytes = generate_pdf(summary, "Sales Summary Report")
            st.download_button("Download Sales Summary PDF", pdf_bytes, file_name=filename, mime="application/pdf")

def generate_pdf(df, title):
    pdf = SimplePDF()
    pdf.add_page()
    pdf.add_title(title)
    pdf.add_table(df)
    
    return pdf.output(dest='S').encode('latin-1')
