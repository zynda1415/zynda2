import io
from fpdf import FPDF
import requests
from PIL import Image

from . import barcode_utils

def generate_catalog_pdf_visual(df, show_category, show_price, show_stock, show_barcode, barcode_type, color_option):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_font("Arial", size=10)

    for _, row in df.iterrows():
        pdf.add_page()

        # Product Image (downloaded from URL)
        try:
            response = requests.get(row['Image URL'])
            img = Image.open(io.BytesIO(response.content))
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            pdf.image(img_buffer, x=60, y=15, w=90, h=90)
        except:
            pass  # ignore image loading errors

        y_position = 110
        pdf.set_xy(10, y_position)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"{row['Item Name']}", ln=True, align="C")

        pdf.set_font("Arial", "", 12)

        if show_category:
            pdf.cell(0, 8, f"Category: {row['Category']}", ln=True, align="C")
        if show_price:
            pdf.set_text_color(*get_rgb(color_option))
            pdf.cell(0, 8, f"Price: ${row['Sale Price']:.2f}", ln=True, align="C")
            pdf.set_text_color(0, 0, 0)

        if show_stock:
            stock_qty = row['Quantity']
            stock_text = f"Stock: {stock_qty} ({get_stock_label(stock_qty)})"
            pdf.cell(0, 8, stock_text, ln=True, align="C")

        if show_barcode:
            code_value = str(row['Code']) if 'Code' in row else str(row['Item Name'])
            if barcode_type == "Code128":
                barcode_img = barcode_utils.generate_barcode_image(code_value)
            else:
                barcode_img = barcode_utils.generate_qr_code(code_value)

            buffer = io.BytesIO()
            barcode_img.save(buffer, format="PNG")
            buffer.seek(0)
            pdf.image(buffer, x=60, y=pdf.get_y() + 5, w=90, h=30)

    output = io.BytesIO(pdf.output(dest="S"))
    return output


# Color mapping for price color in PDF
def get_rgb(color_name):
    colors = {
        "green": (0, 128, 0),
        "blue": (0, 102, 204),
        "purple": (128, 0, 128),
        "orange": (255, 165, 0),
        "red": (204, 0, 0),
    }
    return colors.get(color_name, (0, 0, 0))

# Stock label helper for PDF
def get_stock_label(stock_qty):
    if stock_qty == 0:
        return 'Out of Stock'
    elif stock_qty < 5:
        return 'Low Stock'
    else:
        return 'In Stock'
