# Fixed version of generate_catalog_pdf_visual function
def generate_catalog_pdf_visual(df):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_font('DejaVu', '', 'preview/DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 8)
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    card_w, card_h = 90, 70
    x_start, y_start = 10, 10
    x, y = x_start, y_start
    spacing = 5

    for idx, row in df.iterrows():
        if x + card_w > 200:
            x = x_start
            y += card_h + spacing
            if y + card_h > 280:
                pdf.add_page()
                y = y_start

        pdf.set_xy(x, y)
        pdf.set_fill_color(240, 240, 240)
        pdf.rect(x, y, card_w, card_h, 'F')

        # 🔹 FIXED: Use correct column names
        item_name = str(row.get('Item Name', ''))  # This should match your data
        price = str(row.get('Sale Price', ''))     # Changed from 'Sell Price'
        category = str(row.get('Category', ''))    # Changed from 'Brand'
        image_url = str(row.get('Image URL', ''))
        barcode_data = str(row.get('Barcode', ''))

        # 🔹 Item name
        pdf.set_xy(x + 2, y + 2)
        pdf.multi_cell(card_w - 4, 4, item_name, 0)

        # 🔹 Image preview
        if image_url and image_url != 'nan':
            item_img = download_image(image_url)
            if item_img:
                item_img.thumbnail((card_w - 10, 25))
                buf = io.BytesIO()
                item_img.save(buf, format='PNG')
                buf.seek(0)
                pdf.image(buf, x + 2, y + 10, w=card_w - 10, h=25)

        # 🔹 Price and category
        pdf.set_xy(x + 2, y + 36)
        pdf.cell(card_w - 4, 5, f"Price: ${price}", 0, ln=1)
        pdf.cell(card_w - 4, 5, f"Category: {category}", 0, ln=1)

        # 🔹 Barcode
        if barcode_data and barcode_data != 'nan':
            barcode_img = generate_barcode_image(barcode_data)
            if barcode_img:
                barcode_img.thumbnail((card_w - 10, 20))
                buf = io.BytesIO()
                barcode_img.save(buf, format='PNG')
                buf.seek(0)
                pdf.image(buf, x + 2, y + 48, w=card_w - 10)

        x += card_w + spacing

    out = io.BytesIO()
    pdf.output(out)
    return out.getvalue(), 'visual_catalog.pdf'
