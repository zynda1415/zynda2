from fpdf import FPDF
import io

def generate_pdf_table(df):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_font('DejaVu', '', 'preview/DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 10)
    pdf.add_page()

    headers = ["Item Name (English)", "Sell Price", "Stock", "Brand", "Category", "Note"]
    col_widths = [60, 30, 20, 40, 40, 60]

    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, border=1)
    pdf.ln()

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
