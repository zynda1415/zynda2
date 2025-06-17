# utils/pdf_export.py
from fpdf import FPDF
from PIL import Image
import io
import requests

def generate_catalog_pdf_visual(df, headers):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    for _, row in df.iterrows():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt=row[headers["name"]], ln=True)
        pdf.set_font("Arial", size=10)

        # Image
        try:
            response = requests.get(row[headers["image"]])
            img = Image.open(io.BytesIO(response.content))
            img_path = "/tmp/img.jpg"
            img.save(img_path)
            pdf.image(img_path, w=40, h=40)
        except:
            pass

        # Barcode
        from utils.barcode_utils import generate_barcode_image
        barcode_img = generate_barcode_image(str(row[headers["barcode"]]))
        if barcode_img:
            bcode_path = "/tmp/bcode.png"
            barcode_img.save(bcode_path)
            pdf.image(bcode_path, w=60, h=20)

        pdf.ln(10)

    output = io.BytesIO()
    pdf.output(output)
    return output.getvalue(), "catalog.pdf"
