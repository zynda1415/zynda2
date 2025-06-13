from fpdf import FPDF
import io
from PIL import Image
import requests
from barcode import Code128
from barcode.writer import ImageWriter
from config import HEADER_ALIASES

def download_image(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
    except:
        return None

def generate_barcode_image(data):
    try:
        barcode = Code128(data, writer=ImageWriter())
        buffer = io.BytesIO()
        barcode.write(buffer)
        buffer.seek(0)
        return Image.open(buffer)
    except:
        return None

def generate_catalog_pdf_visual(
    df,
    show_category=True,
    show_price=True,
    show_stock=True,
    show_barcode=True,
    barcode_type="Code128",
    color_option="Light",
    export_layout="Grid",
    include_cover_page=False,
    logo_path=None,
    language='EN',
    selected_categories=None,
    selected_brands=None
):
    H = HEADER_ALIASES["Inventory"]

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_font('DejaVu', '', 'preview/DejaVuSans.ttf', uni=True)
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    card_w, card_h = 90, 70
    x_start, y_start = 10, 10
    x, y = x_start, y_start
    spacing = 5

    for _, row in df.iterrows():
        if x + card_w > 200:
            x = x_start
            y += card_h + spacing
            if y + card_h > 280:
                pdf.add_page()
                y = y_start

        pdf.set_xy(x, y)
        pdf.set_fill_color(245, 245, 245)
        pdf.rect(x, y, card_w, card_h, 'F')

        item_name = str(row.get(H["name"], ''))
        price = str(row.get(H["price"], ''))
        brand = str(row.get(H["brand"], ''))
        category = str(row.get(H["category"], ''))
        stock = str(row.get(H.get("stock", ""), ''))
        image_url = row.get(H["image"], '')
        barcode_data = row.get(H.get("barcode", ""), '')

        cursor_y = y + 2
        pdf.set_font('DejaVu', '', 10)

        # Image
        if image_url:
            img = download_image(image_url)
            if img:
                img.thumbnail((card_w - 8, 25))
                buf = io.BytesIO()
                img.save(buf, format='PNG')
                buf.seek(0)
                pdf.image(buf, x + 4, cursor_y, w=card_w - 8)
                cursor_y += 26

        # Item Name
        pdf.set_xy(x + 2, cursor_y)
        pdf.multi_cell(card_w - 4, 5, item_name)
        cursor_y = pdf.get_y()

        # Price
        if show_price:
            pdf.set_xy(x + 2, cursor_y)
            pdf.cell(card_w - 4, 5, f"Price: {price}", ln=1)
            cursor_y = pdf.get_y()

        # Brand
        pdf.set_xy(x + 2, cursor_y)
        pdf.cell(card_w - 4, 5, f"Brand: {brand}", ln=1)
        cursor_y = pdf.get_y()

        # Category
        if show_category:
            pdf.set_xy(x + 2, cursor_y)
            pdf.cell(card_w - 4, 5, f"Category: {category}", ln=1)
            cursor_y = pdf.get_y()

        # Stock
        if show_stock:
            pdf.set_xy(x + 2, cursor_y)
            pdf.cell(card_w - 4, 5, f"Stock: {stock}", ln=1)
            cursor_y = pdf.get_y()

        # Barcode
        if show_barcode and barcode_data:
            barcode_img = generate_barcode_image(barcode_data)
            if barcode_img:
                barcode_img.thumbnail((card_w - 10, 20))
                buf = io.BytesIO()
                barcode_img.save(buf, format='PNG')
                buf.seek(0)
                pdf.image(buf, x + 2, y + card_h - 22, w=card_w - 10)

        x += card_w + spacing

    out = io.BytesIO()
    pdf.output(out)
    return out.getvalue(), 'visual_catalog.pdf'
