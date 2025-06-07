import io
from fpdf import FPDF
import requests
from PIL import Image
import os
from datetime import datetime
from . import barcode_utils

# ✅ Corrected function header with full v2.0 parameters
def generate_catalog_pdf_visual(df, show_category, show_price, show_stock, show_barcode, barcode_type, color_option, export_layout, include_cover_page, logo_path=None, language='EN', selected_categories=None, selected_brands=None):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    font_path = os.path.join(os.path.dirname(__file__), '..', 'DejaVuSans.ttf')
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font('DejaVu', '', 10)
    pdf.set_auto_page_break(auto=True, margin=10)

    if selected_categories:
        df = df[df['Category'].isin(selected_categories)]
    if selected_brands:
        df = df[df['Brand'].isin(selected_brands)]

    if include_cover_page:
        pdf.add_page()
        if logo_path:
            try:
                pdf.image(logo_path, x=80, y=30, w=50)
            except:
                pass
        pdf.set_font('DejaVu', '', 22)
        pdf.cell(0, 90, "ZYNDA_SYSTEM CATALOG", align="C", ln=True)
        pdf.set_font('DejaVu', '', 14)
        pdf.cell(0, 10, "Generated Export", align="C", ln=True)
        pdf.ln(10)
        pdf.set_font('DejaVu', '', 10)
        pdf.multi_cell(0, 6, f"Total Items: {len(df)}")

    if export_layout == "Detailed View":
        for _, row in df.iterrows():
            pdf.add_page()
            add_product_card(pdf, row, show_category, show_price, show_stock, show_barcode, barcode_type, color_option)
    else:
        grid_export(pdf, df, show_category, show_price, show_stock, show_barcode, barcode_type, color_option)

    filename = f"catalog_export_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    output = io.BytesIO(pdf.output(dest="S"))
    return output, filename

def grid_export(pdf, df, show_category, show_price, show_stock, show_barcode, barcode_type, color_option):
    cols, rows, w, h = 2, 3, 90, 130
    for i, row in df.iterrows():
        if i % (cols*rows) == 0:
            pdf.add_page()
        col, rw = (i % (cols*rows)) % cols, (i % (cols*rows)) // cols
        x, y = 10 + col * (w + 10), 10 + rw * (h + 10)
        draw_card(pdf, row, x, y, w, h, show_category, show_price, show_stock, show_barcode, barcode_type, color_option)

def draw_card(pdf, row, x, y, w, h, show_category, show_price, show_stock, show_barcode, barcode_type, color_option):
    pdf.set_xy(x, y)
    try:
        response = requests.get(row['Image URL'], timeout=5)
        img = Image.open(io.BytesIO(response.content)).convert("RGB")
        box_w, box_h = int(w-10), int(h//2-10)
        img.thumbnail((box_w, box_h))
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG', quality=95)
        img_buffer.seek(0)
        img_w, img_h = img.size
        x_img = x + 5 + (box_w - img_w)//2
        y_img = y + 5 + (box_h - img_h)//2
        pdf.image(img_buffer, x=x_img, y=y_img, w=img_w, h=img_h)
    except:
        pass

    pdf.set_xy(x, y+h//2)
    pdf.set_font('DejaVu','', 10)
    pdf.multi_cell(w, 5, row['Item Name'], align="C")
    if show_price:
        pdf.set_text_color(*get_rgb(color_option))
        pdf.cell(w, 5, f"${row['Sale Price']:.2f}", align="C")
        pdf.set_text_color(0, 0, 0)
    if show_stock:
        stock_qty = row['Quantity']
        stock_text = f"Stock: {stock_qty} ({get_stock_label(stock_qty)})"
        pdf.cell(w, 5, stock_text, align="C")
    if show_barcode:
        add_barcode(pdf, row, barcode_type, x_offset=x+w/2-25, y_offset=y+h-30)

def add_product_card(pdf, row, show_category, show_price, show_stock, show_barcode, barcode_type, color_option):
    draw_card(pdf, row, 10, 20, 190, 250, show_category, show_price, show_stock, show_barcode, barcode_type, color_option)

def add_barcode(pdf, row, barcode_type, y_offset, x_offset=60):
    code_value = str(row['Code']) if 'Code' in row else str(row['Item Name'])
    if barcode_type == "Code128":
        barcode_img = barcode_utils.generate_barcode_image(code_value, dpi=300)
    else:
        barcode_img = barcode_utils.generate_qr_code(code_value)
    buffer = io.BytesIO()
    barcode_img.save(buffer, format="PNG")
    buffer.seek(0)
    pdf.image(buffer, x=x_offset, y=y_offset, w=50, h=20)

def get_rgb(color_name):
    colors = {"green": (0,128,0), "blue": (0,102,204), "purple": (128,0,128), "orange": (255,165,0), "red": (204,0,0)}
    return colors.get(color_name, (0,0,0))

def get_stock_label(stock_qty):
    if stock_qty == 0:
        return 'Out of Stock'
    elif stock_qty < 5:
        return 'Low Stock'
    else:
        return 'In Stock'
