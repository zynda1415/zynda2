import io
import base64
from PIL import Image
import barcode
from barcode.writer import ImageWriter
import qrcode

# Generate Code128 barcode image
def generate_barcode_image(code_value):
    code128 = barcode.get('code128', str(code_value), writer=ImageWriter())
    buffer = io.BytesIO()
    code128.write(buffer, options={"write_text": False})
    buffer.seek(0)
    return Image.open(buffer)

# Generate QR Code image (optional alternative)
def generate_qr_code(code_value):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(str(code_value))
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return Image.open(buffer)

# Encode image to base64 for Streamlit display
def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    base64_str = base64.b64encode(img_bytes).decode("utf-8")
    return base64_str

# Handle full encoding depending on barcode type
def encode_image(code_value, barcode_type="Code128"):
    try:
        if barcode_type == "Code128":
            img = generate_barcode_image(code_value)
        else:
            img = generate_qr_code(code_value)
        return encode_image_to_base64(img)
    except Exception as e:
        print(f"Barcode generation failed: {str(e)}")
        return None
