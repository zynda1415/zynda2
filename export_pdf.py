import streamlit as st
import data
import pandas as pd
from fpdf import FPDF
from datetime import datetime, date
import tempfile
import os

class ProfessionalPDF(FPDF):
    def __init__(self, company_name="Your Company", company_address="", company_phone="", company_email=""):
        super().__init__()
        self.company_name = company_name
        self.company_address = company_address
        self.company_phone = company_phone
        self.company_email = company_email
        
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.company_name, 0, 1, 'C')
        if self.company_address:
            self.set_font('Arial', '', 10)
            self.cell(0, 5, self.company_address, 0, 1, 'C')
        contact_info = []
        if self.company_phone:
            contact_info.append(f"Phone: {self.company_phone}")
        if self.company_email:
            contact_info.append(f"Email: {self.company_email}")
        if contact_info:
            self.cell(0, 5, " | ".join(contact_info), 0, 1, 'C')
        self.ln(5)
        self.set_draw_color(128, 128, 128)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_draw_color(128, 128, 128)
        self.line(10, self.get_y()-5, 200, self.get_y()-5)
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Page {self.page_no()}', 0, 0, 'C')

    def add_title(self, title, subtitle=""):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        if subtitle:
            self.set_font('Arial', '', 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 5, subtitle, 0, 1, 'L')
            self.set_text_color(0, 0, 0)
        self.ln(5)

    def add_professional_table(self, df, title="Data Table"):
        self.add_title(title)
        if df.empty:
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, 'No data available', 0, 1, 'C')
            return
        available_width = self.w - 20
        col_count = len(df.columns)
        col_width = available_width / col_count
        self.set_font('Arial', 'B', 9)
        self.set_fill_color(70, 130, 180)
        self.set_text_color(255, 255, 255)
        for col in df.columns:
            self.cell(col_width, 8, str(col), 1, 0, 'C', True)
        self.ln()
        self.set_font('Arial', '', 8)
        self.set_text_color(0, 0, 0)
        for i, (_, row) in enumerate(df.iterrows()):
            self.set_fill_color(245, 245, 245) if i % 2 == 0 else self.set_fill_color(255, 255, 255)
            for item in row:
                text = str(item)
                self.cell(col_width, 6, text, 1, 0, 'C', True)
            self.ln()

def export_pdf_module():
    st.header("📄 PDF Export Without Emojis")
    report_options = ["Inventory Report", "Sales Summary"]
    report_type = st.selectbox("Select Report Type", report_options)

    if st.button("Generate PDF"):
        if report_type == "Inventory Report":
            df = data.load_inventory()
            filename = "inventory_report.pdf"
            pdf_bytes = generate_pdf(df, report_type)
            st.download_button("Download PDF", data=pdf_bytes, file_name=filename, mime="application/pdf")
        elif report_type == "Sales Summary":
            df = data.load_sales()
            df['Total Price'] = pd.to_numeric(df['Total Price'], errors='coerce')
            df['Quantity Sold'] = pd.to_numeric(df['Quantity Sold'], errors='coerce')
            summary = df.groupby('Item').agg({'Quantity Sold': 'sum', 'Total Price': 'sum'}).reset_index()
            filename = "sales_summary_report.pdf"
            pdf_bytes = generate_pdf(summary, report_type)
            st.download_button("Download PDF", data=pdf_bytes, file_name=filename, mime="application/pdf")

def generate_pdf(df, title="Report"):
    pdf = ProfessionalPDF(company_name="ZYNDA_SYSTEM")
    pdf.add_page()
    pdf.add_title(title)
    pdf.add_professional_table(df, title="Report Table")
    return pdf_to_bytes(pdf)

def pdf_to_bytes(pdf):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        temp_filename = tmp_file.name
    try:
        pdf.output(temp_filename)
        with open(temp_filename, 'rb') as f:
            pdf_bytes = f.read()
        return pdf_bytes
    finally:
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)
