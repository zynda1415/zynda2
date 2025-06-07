from barcode import Code128
from barcode.writer import ImageWriter
import qrcode
import io
from PIL import Image

def generate_barcode_image(data, dpi=300):
    rv = io.BytesIO()
    code = Code128(data, writer=ImageWriter())
    code.write(rv, options={"dpi": dpi})
    rv.seek(0)
    return Image.open(rv)

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    return img
