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

# Card-style catalog PDF generator
def generate_catalog_pdf_visual(df, fields, layout, cover_page):
    orientation = layout["orientation"]
    pdf = FPDF(orientation=orientation, unit='mm', format='A4')
    pdf.add_font('DejaVu', '', 'preview/DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVu", size=10)
    pdf.set_auto_page_break(auto=True, margin=10)

    # Layout config
    card_w, card_h = 60, 85
    margin_x, margin_y = 10, 10
    space_x, space_y = 5, 10
    cols = layout["columns"]
    rows = layout["rows"]
    barcode_type = layout["barcode_type"]

    if cover_page:
        pdf.add_page()
        pdf.set_font("DejaVu", size=28)
        pdf.cell(0, 120, '📦 Inventory Catalog', ln=True, align='C')

    count = 0
    pdf.add_page()

    for idx, row in df.iterrows():
        if count % (cols * rows) == 0 and count != 0:
            pdf.add_page()
            count = 0

        col = count % cols
        rw = count // cols
        x = margin_x + col * (card_w + space_x)
        y = margin_y + rw * (card_h + space_y)
        x_inner = x + 5
        y_cursor = y + 5

        # Card background
        pdf.set_fill_color(245, 245, 245)
        pdf.rect(x, y, card_w, card_h, 'F')

        # Product Image
        if fields["image"]:
            img = download_image(row.get("Image URL", ""))
            if img:
                img.thumbnail((card_w - 10, 30))
                img_io = io.BytesIO()
                img.save(img_io, format="PNG")
                img_io.seek(0)
                pdf.image(img_io, x_inner, y_cursor, w=card_w - 10)
                y_cursor += img.size[1] * (card_w - 10) / img.size[0] + 3

        # Item Name
        if fields["name"]:
            pdf.set_xy(x + 3, y_cursor)
            pdf.set_font("DejaVu", size=9, style='B')
            pdf.multi_cell(card_w - 6, 5, row.get("Item Name", ""), align="C")
            y_cursor = pdf.get_y()

        # Category
        if fields["category"]:
            pdf.set_font("DejaVu", size=8)
            pdf.set_xy(x + 3, y_cursor)
            pdf.multi_cell(card_w - 6, 5, f"Category: {row.get('Category', '')}", align="C")
            y_cursor = pdf.get_y()

        # Sale Price
        if fields["price"]:
            pdf.set_text_color(0, 128, 0)
            pdf.set_font("DejaVu", size=9, style='B')
            pdf.set_xy(x + 3, y_cursor)
            pdf.multi_cell(card_w - 6, 5, f"${row.get('Sale Price', '')}", align="C")
            y_cursor = pdf.get_y()
            pdf.set_text_color(0, 0, 0)

        # Quantity (Stock Badge)
        if fields["stock"]:
            stock = int(row.get("Quantity", 0))
            badge = f"Stock: {stock}" if stock > 0 else "Out of Stock"
            pdf.set_fill_color(0, 200, 0) if stock > 0 else pdf.set_fill_color(200, 0, 0)
            pdf.set_font("DejaVu", size=8)
            pdf.set_xy(x + 8, y_cursor)
            pdf.cell(card_w - 16, 6, badge, align="C", fill=True)
            y_cursor += 7

        # Notes
        if fields["notes"]:
            pdf.set_font("DejaVu", size=8)
            pdf.set_xy(x + 3, y_cursor)
            pdf.multi_cell(card_w - 6, 4, row.get("Notes", ""), align="C")
            y_cursor = pdf.get_y()

        # Barcode
        if fields["barcode"]:
            barcode_img = generate_barcode_image(str(row.get("Barcode", "")), barcode_type)
            if barcode_img:
                barcode_img.thumbnail((card_w - 10, 20))
                barcode_io = io.BytesIO()
                barcode_img.save(barcode_io, format="PNG")
                barcode_io.seek(0)
                pdf.image(barcode_io, x + 5, y + card_h - 20, w=card_w - 10)

        count += 1

    output = io.BytesIO()
    pdf.output(output)
    return output.getvalue(), "catalog_visual_export.pdf"
