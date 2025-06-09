from fpdf import FPDF
import io
import requests
from PIL import Image
from barcode import Code128, EAN13, EAN8, UPCA
from barcode.writer import ImageWriter

# Download image from URL
def download_image(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
    except:
        return None

# Generate barcode image
def generate_barcode_image(barcode_data, barcode_type='Code128'):
    if not barcode_data:
        return None
    try:
        writer = ImageWriter()
        barcode_cls = {"EAN13": EAN13, "EAN8": EAN8, "UPCA": UPCA}.get(barcode_type, Code128)
        barcode = barcode_cls(barcode_data, writer=writer)
        barcode_io = io.BytesIO()
        barcode.write(barcode_io)
        barcode_io.seek(0)
        return Image.open(barcode_io)
    except:
        return None

# Master generator function
def generate_catalog_pdf_visual(df, fields, layout, cover_page):
    orientation = layout["orientation"]
    columns = layout["columns"]
    rows = layout["rows"]
    barcode_type = layout["barcode_type"]

    pdf = FPDF(orientation=orientation, unit='mm', format='A4')
    pdf.add_font('DejaVu', '', 'preview/DejaVuSans.ttf', uni=True)
    pdf.set_auto_page_break(auto=True, margin=10)

    page_w, page_h = (297, 210) if orientation == "L" else (210, 297)
    box_w = (page_w - 20) / columns
    box_h = (page_h - 20) / rows

    if cover_page:
        pdf.add_page()
        pdf.set_font('DejaVu', '', 28)
        pdf.cell(0, 120, '📦 Inventory Catalog', ln=True, align='C')

    for idx, row in df.iterrows():
        if idx % (columns * rows) == 0:
            pdf.add_page()

        col = (idx % columns)
        rw = (idx // columns) % rows
        x, y = 10 + col * box_w, 10 + rw * box_h

        pdf.set_xy(x, y)
        pdf.set_fill_color(245, 245, 245)
        pdf.rect(x, y, box_w-5, box_h-5, 'F')
        x_inner, y_inner = x + 5, y + 5

        pdf.set_font('DejaVu', '', 10)

        # Image
        if fields["image"]:
            img = download_image(row.get('Image URL', ''))
            if img:
                img.thumbnail((int(box_w-20), int(box_h/3)))
                img_io = io.BytesIO()
                img.save(img_io, format='PNG')
                img_io.seek(0)
                pdf.image(img_io, x_inner, y_inner, w=box_w-20)
                y_inner += img.size[1] * (box_w-20) / img.size[0] + 5

        # Text fields
        text_fields = [
            ("Item Name", fields["name"], row.get("Item Name", '')),
            ("Category", fields["category"], row.get("Category", '')),
            ("Sale Price", fields["price"], f"${row.get('Sale Price', '')}"),
            ("Quantity", fields["stock"], row.get("Quantity", '')),
            ("Notes", fields["notes"], row.get("Notes", ''))
        ]

        for label, show, value in text_fields:
            if show:
                pdf.set_xy(x_inner, y_inner)
                pdf.multi_cell(box_w-20, 5, f"{label}: {value}")
                y_inner = pdf.get_y()

        # Barcode
        if fields["barcode"]:
            barcode_data = str(row.get('Barcode', ''))
            barcode_img = generate_barcode_image(barcode_data, barcode_type)
            if barcode_img:
                barcode_img.thumbnail((int(box_w-30), 25))
                barcode_io = io.BytesIO()
                barcode_img.save(barcode_io, format='PNG')
                barcode_io.seek(0)
                pdf.image(barcode_io, x_inner, y_inner+2, w=box_w-30)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    filename = "catalog_visual_export.pdf"
    return pdf_output.getvalue(), filename
