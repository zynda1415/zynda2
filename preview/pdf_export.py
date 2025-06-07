import io
from fpdf import FPDF
import requests
from PIL import Image
import os
from datetime import datetime
from . import barcode_utils

def generate_catalog_pdf_visual(df, show_category, show_price, show_stock, show_barcode, barcode_type, color_option, export_layout, include_cover_page, logo_path=None, language='EN', selected_categories=None, selected_brands=None):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    font_path = os.path.join(os.path.dirname(__file__), '..', 'DejaVuSans.ttf')
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font('DejaVu', '', 10)
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_creator("ZYNDA_SYSTEM")
    pdf.set_title("Visual Catalog Export")

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
    cols = 2
    card_w = 90
    card_h = 120
    margin_x = 10
    margin_y = 10
    x0 = margin_x
    y0 = margin_y
    i = 0

    for _, row in df.iterrows():
        if i % cols == 0:
            pdf.add_page()
            x0 = margin_x
            y0 = margin_y

        x = x0 + (i % cols) * (card_w + margin_x)
        y = y0

        pdf.set_xy(x, y)
        pdf.set_fill_color(245, 245, 245)
        pdf.rect(x, y, card_w, card_h, 'F')
        pdf.set_xy(x+2, y+2)

        name = row.get('Item Name', '')
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(card_w-4, 6, name, align="C")
        
        image_url = row.get('Image URL', '')
        if image_url:
            try:
                response = requests.get(image_url)
                img = Image.open(io.BytesIO(response.content)).convert("RGB")
                img_path = f"temp_img_{i}.jpg"
                img.save(img_path, dpi=(300,300))
                pdf.image(img_path, x+20, y+25, w=50, h=50)
                os.remove(img_path)
            except:
                pass

        pdf.set_font('DejaVu', '', 9)
        y_text = y + 80
        if show_category:
            pdf.set_xy(x+2, y_text)
            pdf.cell(0, 5, f"Category: {row.get('Category','')}", ln=True)
            y_text += 5
        if show_price:
            pdf.set_xy(x+2, y_text)
            pdf.cell(0, 5, f"Price: {row.get('Sale Price','')}", ln=True)
            y_text += 5
        if show_stock:
            pdf.set_xy(x+2, y_text)
            pdf.cell(0, 5, f"Stock: {row.get('Quantity','')}", ln=True)
            y_text += 5
        if show_barcode:
            barcode_path = barcode_utils.generate_barcode(row.get('Code',''), barcode_type)
            if barcode_path:
                pdf.image(barcode_path, x+25, y_text, w=40, h=15)
                os.remove(barcode_path)

        i += 1

def add_product_card(pdf, row, show_category, show_price, show_stock, show_barcode, barcode_type, color_option):
    pdf.set_font('DejaVu', '', 16)
    pdf.cell(0, 10, row.get('Item Name',''), ln=True)
    pdf.ln(3)

    image_url = row.get('Image URL','')
    if image_url:
        try:
            response = requests.get(image_url)
            img = Image.open(io.BytesIO(response.content)).convert("RGB")
            img_path = f"temp_detail.jpg"
            img.save(img_path, dpi=(300,300))
            pdf.image(img_path, x=30, w=150)
            os.remove(img_path)
        except:
            pass

    pdf.set_font('DejaVu', '', 12)
    if show_category:
        pdf.cell(0, 8, f"Category: {row.get('Category','')}", ln=True)
    if show_price:
        pdf.cell(0, 8, f"Price: {row.get('Sale Price','')}", ln=True)
    if show_stock:
        pdf.cell(0, 8, f"Stock: {row.get('Quantity','')}", ln=True)
    if show_barcode:
        barcode_path = barcode_utils.generate_barcode(row.get('Code',''), barcode_type)
        if barcode_path:
            pdf.image(barcode_path, x=80, y=pdf.get_y()+5, w=50, h=20)
            os.remove(barcode_path)
