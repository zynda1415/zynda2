import io
from fpdf import FPDF
import requests
from PIL import Image
from . import barcode_utils

def generate_catalog_pdf_visual(df, show_category, show_price, show_stock, show_barcode, barcode_type, color_option, export_layout, include_cover_page):
    pdf = FPDF(orientation='P', unit='mm', format='A4')

    # ✅ Corrected font path (relative to current working directory)
    import os
font_path = os.path.join(os.path.dirname(__file__), '..', 'DejaVuSans.ttf')
pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font('DejaVu', '', 10)

    pdf.set_auto_page_break(auto=True, margin=10)


    # 📝 Cover Page
    if include_cover_page:
        pdf.add_page()
        pdf.set_font('DejaVu', '', 22)
        pdf.cell(0, 60, "📦 ZYNDA_SYSTEM CATALOG", align="C", ln=True)  # ✅ Now emoji safe!
        pdf.set_font('DejaVu', '', 14)
        pdf.cell(0, 10, "Generated Visual Export", align="C", ln=True)

    if export_layout == "Detailed View":
        for _, row in df.iterrows():
            pdf.add_page()
            add_product_card(pdf, row, show_category, show_price, show_stock, show_barcode, barcode_type, color_option)
    else:
        for index, row in df.iterrows():
            if index % 2 == 0:
                pdf.add_page()
                pdf.set_y(20)
            x_pos = 10 if (index % 2 == 0) else 105
            add_product_compact(pdf, row, x_pos, show_category, show_price, show_stock, show_barcode, barcode_type, color_option)

    output = io.BytesIO(pdf.output(dest="S"))
    return output

def add_product_card(pdf, row, show_category, show_price, show_stock, show_barcode, barcode_type, color_option):
    try:
        response = requests.get(row['Image URL'], timeout=5)
        img = Image.open(io.BytesIO(response.content))
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        pdf.image(img_buffer, x=60, y=15, w=90, h=90)
    except:
        pass

    y_position = 110
    pdf.set_xy(10, y_position)
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(0, 10, f"{row['Item Name']}", ln=True, align="C")

    pdf.set_font('DejaVu', '', 12)
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
        add_barcode(pdf, row, barcode_type, y_offset=pdf.get_y()+5)

def add_product_compact(pdf, row, x_pos, show_category, show_price, show_stock, show_barcode, barcode_type, color_option):
    try:
        response = requests.get(row['Image URL'], timeout=5)
        img = Image.open(io.BytesIO(response.content))
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        pdf.image(img_buffer, x=x_pos + 20, y=20, w=50, h=50)
    except:
        pass

    pdf.set_xy(x_pos, 75)
    pdf.set_font('DejaVu', '', 11)
    pdf.multi_cell(85, 6, f"{row['Item Name']}", align="C")

    pdf.set_font('DejaVu', '', 10)
    if show_category:
        pdf.multi_cell(85, 5, f"Category: {row['Category']}", align="C")
    if show_price:
        pdf.set_text_color(*get_rgb(color_option))
        pdf.multi_cell(85, 5, f"Price: ${row['Sale Price']:.2f}", align="C")
        pdf.set_text_color(0, 0, 0)
    if show_stock:
        stock_qty = row['Quantity']
        stock_text = f"Stock: {stock_qty} ({get_stock_label(stock_qty)})"
        pdf.multi_cell(85, 5, stock_text, align="C")
    if show_barcode:
        add_barcode(pdf, row, barcode_type, x_offset=x_pos + 25, y_offset=140)

def add_barcode(pdf, row, barcode_type, y_offset, x_offset=60):
    code_value = str(row['Code']) if 'Code' in row else str(row['Item Name'])
    if barcode_type == "Code128":
        barcode_img = barcode_utils.generate_barcode_image(code_value)
    else:
        barcode_img = barcode_utils.generate_qr_code(code_value)

    buffer = io.BytesIO()
    barcode_img.save(buffer, format="PNG")
    buffer.seek(0)
    pdf.image(buffer, x=x_offset, y=y_offset, w=50, h=20)

def get_rgb(color_name):
    colors = {
        "green": (0, 128, 0),
        "blue": (0, 102, 204),
        "purple": (128, 0, 128),
        "orange": (255, 165, 0),
        "red": (204, 0, 0),
    }
    return colors.get(color_name, (0, 0, 0))

def get_stock_label(stock_qty):
    if stock_qty == 0:
        return 'Out of Stock'
    elif stock_qty < 5:
        return 'Low Stock'
    else:
        return 'In Stock'
