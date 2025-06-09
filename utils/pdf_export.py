from fpdf import FPDF
import io
import requests
from PIL import Image
from barcode import Code128, EAN13, EAN8, UPCA
from barcode.writer import ImageWriter

# Helper function to download image from URL
def download_image(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
    except:
        return None

# Helper function to generate barcode image
def generate_barcode_image(barcode_data, barcode_type='Code128'):
    if not barcode_data:
        return None
    try:
        writer = ImageWriter()
        if barcode_type == 'EAN13':
            barcode = EAN13(barcode_data, writer=writer)
        elif barcode_type == 'EAN8':
            barcode = EAN8(barcode_data, writer=writer)
        elif barcode_type == 'UPCA':
            barcode = UPCA(barcode_data, writer=writer)
        else:
            barcode = Code128(barcode_data, writer=writer)
        barcode_io = io.BytesIO()
        barcode.write(barcode_io)
        barcode_io.seek(0)
        return Image.open(barcode_io)
    except:
        return None

# Main function to generate full visual catalog PDF
def generate_catalog_pdf_visual(df, show_category, show_price, show_stock, show_barcode, barcode_type, color_option, export_layout, include_cover_page, logo_path=None, language='EN', selected_categories=None, selected_brands=None):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_font('DejaVu', '', 'preview/DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 10)
    pdf.set_auto_page_break(auto=True, margin=10)

    if include_cover_page:
        pdf.add_page()
        pdf.set_font('DejaVu', '', 24)
        pdf.cell(0, 100, 'Inventory Catalog', ln=True, align='C')

    for index, row in df.iterrows():
        pdf.add_page()

        # Item Name
        pdf.set_font('DejaVu', '', 16)
        name = row.get('Item Name', '')
        pdf.multi_cell(0, 10, name, align='C')

        # Image Section
        image_url = row.get('Image URL', '')
        img = download_image(image_url)
        if img:
            img.thumbnail((100, 100))
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            pdf.image(img_buffer, x=55, y=50, w=100, h=100)

        pdf.ln(80)

        # Details Section
        pdf.set_font('DejaVu', '', 12)
        if show_category:
            category = str(row.get('Category', ''))
            pdf.cell(0, 10, f"Category: {category}", ln=True)
        if show_price:
            sell_price = row.get('Sale Price', '')
            pdf.cell(0, 10, f"Sale Price: {sell_price}", ln=True)
        if show_stock:
            quantity = row.get('Quantity', '')
            pdf.cell(0, 10, f"Quantity: {quantity}", ln=True)
        notes = row.get('Notes', '')
        pdf.multi_cell(0, 10, f"Notes: {notes}", ln=True)

        # Barcode Section
        if show_barcode:
            barcode_data = str(row.get('Barcode', ''))
            barcode_img = generate_barcode_image(barcode_data, barcode_type)
            if barcode_img:
                barcode_img.thumbnail((80, 30))
                barcode_buffer = io.BytesIO()
                barcode_img.save(barcode_buffer, format='PNG')
                barcode_buffer.seek(0)
                pdf.image(barcode_buffer, x=65, y=pdf.get_y()+5, w=80, h=30)
                pdf.ln(40)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    filename = "catalog_visual_export.pdf"
    return pdf_output.getvalue(), filename
