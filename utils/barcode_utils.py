# utils/barcode_utils.py
from barcode import Code128, EAN13, EAN8, UPCA
from barcode.writer import ImageWriter
import io
from PIL import Image

def generate_barcode_image(data, barcode_type='Code128'):
    if not data:
        return None
    try:
        writer = ImageWriter()
        cls = {'EAN13': EAN13, 'EAN8': EAN8, 'UPCA': UPCA}.get(barcode_type, Code128)
        barcode = cls(data, writer=writer)
        buffer = io.BytesIO()
        barcode.write(buffer)
        buffer.seek(0)
        return Image.open(buffer)
    except Exception:
        return None
