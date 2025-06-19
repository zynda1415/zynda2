import io
import base64
from PIL import Image
import barcode
from barcode.writer import ImageWriter
import qrcode

def generate_barcode_image(code_value):
    code128 = barcode.get('code128', str(code_value), writer=ImageWriter())
    buffer = io.BytesIO()
    code128.write(buffer, options={"write_text": False})
    buffer.seek(0)
    return Image.open(buffer)

def encode_image(code_value, barcode_type="Code128"):
    img = generate_barcode_image(code_value)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
