from fpdf import FPDF
import io
from PIL import Image
import requests
import base64
from barcode import Code128
from barcode.writer import ImageWriter

# ========== Table-style Export ==========
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

# ========== Helper: Image Downloader ==========
def download_image(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
    except:
        return None

# ========== Helper: Barcode Generator ==========
def generate_barcode_image(data):
    try:
        barcode = Code128(data, writer=ImageWriter())
        buffer = io.BytesIO()
        barcode.write(buffer)
        buffer.seek(0)
        return Image.open(buffer)
    except:
        return None

# ========== Visual Catalog Export ==========
def generate_catalog_pdf_visual(df):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_font('DejaVu', '', 'preview/DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 8)
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    card_w, card_h = 90, 70
    x_start, y_start = 10, 10
    x, y = x_start, y_start
    spacing = 5

    for idx, row in df.iterrows():
        if x + card_w > 200:
            x = x_start
            y += card_h + spacing
            if y + card_h > 280:
                pdf.add_page()
                y = y_start

        pdf.set_xy(x, y)
        pdf.set_fill_color(240, 240, 240)
        pdf.rect(x, y, card_w, card_h, 'F')

        item_name = str(row.get('Item Name (English)', ''))
        price = str(row.get('Sell Price', ''))
        brand = str(row.get('Brand', ''))
        image_url = str(row.get('Image URL', ''))
        barcode_data = str(row.get('Barcode', ''))

        # 🔹 Item name
        pdf.set_xy(x + 2, y + 2)
        pdf.multi_cell(card_w - 4, 4, item_name, 0)

        # 🔹 Image preview
        if image_url:
            item_img = download_image(image_url)
            if item_img:
                item_img.thumbnail((card_w - 10, 25))
                buf = io.BytesIO()
                item_img.save(buf, format='PNG')
                buf.seek(0)
                pdf.image(buf, x + 2, y + 10, w=card_w - 10, h=25)

        # 🔹 Price and brand
        pdf.set_xy(x + 2, y + 36)
        pdf.cell(card_w - 4, 5, f"Price: {price}", 0, ln=1)
        pdf.cell(card_w - 4, 5, f"Brand: {brand}", 0, ln=1)

        # 🔹 Barcode
        barcode_img = generate_barcode_image(barcode_data)
        if barcode_img:
            barcode_img.thumbnail((card_w - 10, 20))
            buf = io.BytesIO()
            barcode_img.save(buf, format='PNG')
            buf.seek(0)
            pdf.image(buf, x + 2, y + 48, w=card_w - 10)

        x += card_w + spacing

    out = io.BytesIO()
    pdf.output(out)
    return out.getvalue(), 'visual_catalog.pdf'
