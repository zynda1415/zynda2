# utils/barcode_utils.py
from barcode import Code128, EAN13, EAN8, UPCA
from barcode.writer import ImageWriter
import io
from PIL import Image

def generate_barcode_image(barcode_data, barcode_type='Code128'):
    if not barcode_data:
        return None
    try:
        writer = ImageWriter()
        barcode_cls = {
            "EAN13": EAN13,
            "EAN8": EAN8,
            "UPCA": UPCA
        }.get(barcode_type, Code128)

        barcode = barcode_cls(barcode_data, writer=writer)
        barcode_io = io.BytesIO()
        barcode.write(barcode_io)
        barcode_io.seek(0)
        return Image.open(barcode_io)
    except Exception as e:
        return None
