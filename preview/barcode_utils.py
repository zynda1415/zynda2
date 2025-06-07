import io
import base64
from PIL import Image
from barcode import Code128
from barcode.writer import ImageWriter
import qrcode

def generate_barcode_image(code_value):
    barcode_io = io.BytesIO()
    options = {'module_width': 0.3,'module_height': 20,'font_size': 8,'text_distance': 1}
    Code128(code_value, writer=ImageWriter()).write(barcode_io, options)
    barcode_io.seek(0)
    return Image.open(barcode_io)

def generate_qr_code(code_value):
    qr = qrcode.QRCode(box_size=2, border=1)
    qr.add_data(code_value)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def encode_image_to_base64(img):
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64_img = base64.b64encode(buffer.getvalue()).decode()
    return b64_img
