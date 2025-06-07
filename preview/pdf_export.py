from fpdf import FPDF
from PIL import Image
import requests
from io import BytesIO
import barcode
from barcode.writer import ImageWriter
import os

class CatalogPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        self.set_font('DejaVu', '', 10)

    def header(self):
        self.set_font('DejaVu', '', 14)
        self.cell(0, 10, 'Inventory Catalog', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def add_catalog_item(self, item, x, y, w, h):
        self.rect(x, y, w, h)
        margin = 3
        img_w, img_h = w - 2*margin, h * 0.4

        # Draw image
        if item['Image']:
            try:
                response = requests.get(item['Image'])
                img = Image.open(BytesIO(response.content))
                img_path = f"temp_image.jpg"
                img.save(img_path)
                self.image(img_path, x + margin, y + margin, img_w, img_h)
                os.remove(img_path)
            except:
                pass

        # Write text fields
        self.set_xy(x + margin, y + margin + img_h + 2)
        self.multi_cell(img_w, 5, item['Item Name (English)'], align='C')
        self.set_x(x + margin)
        self.cell(img_w, 5, f"Category: {item['Category 1']}", ln=True, align='C')
        self.set_x(x + margin)
        self.cell(img_w, 5, f"Price: ${item['Sell Price']}", ln=True, align='C')
        self.set_x(x + margin)
        self.cell(img_w, 5, f"Stock: {item['Stock']} In Stock", ln=True, align='C')

        # Barcode
        if item['Barcode']:
            code_img = self.generate_barcode_image(item['Barcode'])
            self.image(code_img, x + w/2 - 15, y + h - 20, 30, 12)
            os.remove(code_img)

    def generate_barcode_image(self, code):
        code128 = barcode.get('code128', str(code), writer=ImageWriter())
        filename = f"barcode_{code}.png"
        code128.save(filename)
        return filename

def generate_catalog_pdf_visual(df):
    pdf = CatalogPDF()
    pdf.add_page()

    cols = 3
    spacing = 10
    item_w = (210 - (cols + 1) * spacing) / cols
    item_h = 90

    x_start = spacing
    y_start = 30
    x = x_start
    y = y_start

    for idx, row in df.iterrows():
        pdf.add_catalog_item(row, x, y, item_w, item_h)
        x += item_w + spacing
        if (idx + 1) % cols == 0:
            x = x_start
            y += item_h + spacing
            if y + item_h + spacing > 297 - 20:
                pdf.add_page()
                y = y_start

    return pdf.output(dest='S').encode('latin1')
