import io
from fpdf import FPDF
import requests
from PIL import Image
import os
from . import barcode_utils

def generate_catalog_pdf_visual(df, show_category, show_price, show_stock, show_barcode, barcode_type, color_option, export_layout, include_cover_page, logo_path=None, language='EN'):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    font_path = os.path.join(os.path.dirname(__file__), '..', 'DejaVuSans.ttf')
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font('DejaVu', '', 10)
    pdf.set_auto_page_break(auto=True, margin=10)

    if include_cover_page:
        pdf.add_page()
        if logo_path:
            try:
                pdf.image(logo_path, x=80, y=30, w=50)
            except:
                pass
        pdf.set_font('DejaVu', '', 24)
        pdf.cell(0, 100, translate("ZYNDA_SYSTEM CATALOG", language), align="C", ln=True)
        pdf.set_font('DejaVu', '', 14)
        pdf.cell(0, 10, translate("Generated Export", language), align="C", ln=True)

    if export_layout == "Detailed View":
        for _, row in df.iterrows():
            pdf.add_page()
            add_product_card(pdf, row, show_category, show_price, show_stock, show_barcode, barcode_type, color_option, language)
    else:
        grid_export(pdf, df, show_category, show_price, show_stock, show_barcode, barcode_type, color_option, language)

    output = io.BytesIO(pdf.output(dest="S"))
    return output

def grid_export(pdf, df, show_category, show_price, show_stock, show_barcode, barcode_type, color_option, language):
    cols, rows, w, h = 2, 3, 90, 130
    for i, row in df.iterrows():
        if i % (cols*rows) == 0:
            pdf.add_page()
        col, rw = (i % (cols*rows)) % cols, (i % (cols*rows)) // cols
        x, y = 10 + col * (w + 10), 10 + rw * (h + 10)
        draw_card(pdf, row, x, y, w, h, show_category, show_price, show_stock, show_barcode, barcode_type, color_option, language)

def draw_card(pdf, row, x, y, w, h, show_category, show_price, show_stock, show_barcode, barcode_type, color_option, language):
    pdf.set_xy(x, y)
    try:
        response = requests.get(row['Image URL'], timeout=5)
        img = Image.open(io.BytesIO(response.content)).convert("RGB")
        img = img.resize((int(w-10), int(h//2-10)))
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG', quality=90)
        img_buffer.seek(0)
        pdf.image(img_buffer, x+5, y+5, w-10, h//2-10)
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
        stock_text = translate("Stock", language) + f": {stock_qty} ({get_stock_label(stock_qty, language)})"
        pdf.cell(w, 5, stock_text, align="C")
    if show_barcode:
        add_barcode(pdf, row, barcode_type, x_offset=x+w/2-25, y_offset=y+h-30)

def add_product_card(pdf, row, show_category, show_price, show_stock, show_barcode, barcode_type, color_option, language):
    draw_card(pdf, row, 10, 20, 190, 250, show_category, show_price, show_stock, show_barcode, barcode_type, color_option, language)

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
    colors = {"green": (0,128,0), "blue": (0,102,204), "purple": (128,0,128), "orange": (255,165,0), "red": (204,0,0)}
    return colors.get(color_name, (0,0,0))

def get_stock_label(stock_qty, lang):
    if stock_qty == 0:
        return translate("Out of Stock", lang)
    elif stock_qty < 5:
        return translate("Low Stock", lang)
    else:
        return translate("In Stock", lang)

def translate(text, lang):
    translations = {
        'Stock': {'EN': 'Stock', 'AR': 'المخزون', 'KU': 'کیشتۆک'},
        'Out of Stock': {'EN': 'Out of Stock', 'AR': 'نفاد', 'KU': 'بێتۆفی'},
        'Low Stock': {'EN': 'Low Stock', 'AR': 'مخزون قليل', 'KU': 'كمی کیشتۆک'},
        'In Stock': {'EN': 'In Stock', 'AR': 'متوفر', 'KU': 'لە کیشتۆکدا'},
        'ZYNDA_SYSTEM CATALOG': {'EN': 'ZYNDA_SYSTEM CATALOG', 'AR': 'كتالوج نظام ZYNDA', 'KU': 'کاتەلۆڵگی ZYNDA_SYSTEM'},
        'Generated Export': {'EN': 'Generated Export', 'AR': 'تصدير منشأ', 'KU': 'تەرشکەراو هانەرد'},
    }
    return translations.get(text, {}).get(lang, text)
