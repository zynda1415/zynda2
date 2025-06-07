import io
from fpdf import FPDF

def generate_catalog_pdf(df, show_category, show_price, show_stock):
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
