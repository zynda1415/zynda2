import io
import os
from PIL import Image
from barcode import Code128
from barcode.writer import ImageWriter
import qrcode

def generate_barcode(code_value, barcode_type="Code128"):
    if not code_value:
        return None

    try:
        if barcode_type == "QR":
            img = generate_qr_code(code_value)
        else:
            img = generate_barcode_image(code_value)

        temp_path = f"barcode_temp_{code_value}.png"
        img.save(temp_path, dpi=(300,300))
        return temp_path
    except:
        return None

def generate_barcode_image(code_value, dpi=300):
    barcode_io = io.BytesIO()
    options = {
        'module_width': 0.3,
        'module_height': 20,
        'font_size': 8,
        'text_distance': 1,
        'dpi': dpi
    }
    Code128(code_value, writer=ImageWriter()).write(barcode_io, options)
    barcode_io.seek(0)
    return Image.open(barcode_io)

def generate_qr_code(code_value):
    qr = qrcode.QRCode(box_size=2, border=1)
    qr.add_data(code_value)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img.convert("RGB")
