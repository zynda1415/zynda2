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

# Main visual catalog function
def generate_catalog_pdf_visual(
    df, show_image, show_name, show_category, show_price, show_stock, show_notes, show_barcode,
    barcode_type, paper_orientation, columns_per_row, rows_per_page, include_cover_page
):
    pdf = FPDF(orientation=paper_orientation, unit='mm', format='A4')
    pdf.add_font('DejaVu', '', 'preview/DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 9)
    pdf.set_auto_page_break(auto=True, margin=10)

    page_width = 297 if paper_orientation == "L" else 210
    page_height = 210 if paper_orientation == "L" else 297

    if include_cover_page:
        pdf.add_page()
        pdf.set_font('DejaVu', '', 26)
        pdf.cell(0, 120, '📦 Inventory Catalog', ln=True, align='C')

    cell_width = (page_width - 20) / columns_per_row
    cell_height = (page_height - 20) / rows_per_page

    counter = 0
    for index, row in df.iterrows():
        if counter % (columns_per_row * rows_per_page) == 0:
            pdf.add_page()

        x = 10 + (counter % columns_per_row) * cell_width
        y = 10 + ((counter // columns_per_row) % rows_per_page) * cell_height
        pdf.set_xy(x, y)
        pdf.set_fill_color(245, 245, 245)
        pdf.rect(x, y, cell_width - 5, cell_height - 5, 'F')

        inner_x = x + 5
        inner_y = y + 5

        if show_image:
            image_url = row.get('Image URL', '')
            img = download_image(image_url)
            if img:
                img.thumbnail((int(cell_width-20), int(cell_height/3)))
                img_buffer = io.BytesIO()
                img.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                pdf.image(img_buffer, inner_x, inner_y, w=cell_width-20)
                inner_y += img.size[1] * (cell_width-20) / img.size[0] + 5

        pdf.set_xy(inner_x, inner_y)
        pdf.set_font('DejaVu', '', 10)

        if show_name:
            name = str(row.get('Item Name', ''))
            pdf.multi_cell(cell_width-20, 5, f"🛒 {name}", align='L')

        if show_category:
            category = str(row.get('Category', ''))
            pdf.multi_cell(cell_width-20, 5, f"📂 {category}", align='L')

        if show_price:
            price = row.get('Sale Price', '')
            pdf.multi_cell(cell_width-20, 5, f"💲 {price}", align='L')

        if show_stock:
            quantity = row.get('Quantity', '')
            pdf.multi_cell(cell_width-20, 5, f"📦 {quantity}", align='L')

        if show_notes:
            notes = row.get('Notes', '')
            pdf.multi_cell(cell_width-20, 5, f"📝 {notes}", align='L')

        if show_barcode:
            barcode_data = str(row.get('Barcode', ''))
            barcode_img = generate_barcode_image(barcode_data, barcode_type)
            if barcode_img:
                barcode_img.thumbnail((int(cell_width-30), 25))
                barcode_buffer = io.BytesIO()
                barcode_img.save(barcode_buffer, format='PNG')
                barcode_buffer.seek(0)
                pdf.image(barcode_buffer, inner_x, pdf.get_y()+2, w=cell_width-30)

        counter += 1

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    filename = "catalog_visual_export.pdf"
    return pdf_output.getvalue(), filename
