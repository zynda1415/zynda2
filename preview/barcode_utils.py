import base64
import io
from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter

def encode_image(barcode_data, barcode_type='code128'):
    """
    Generate a barcode image and return it as a base64 encoded string
    """
    try:
        if not barcode_data or str(barcode_data).strip() == '':
            return create_placeholder_barcode()
        
        # Clean the barcode data
        barcode_data = str(barcode_data).strip()
        
        # Get the barcode class
        if barcode_type.lower() == 'code128':
            barcode_class = barcode.get_barcode_class('code128')
        elif barcode_type.lower() == 'ean13' and len(barcode_data) >= 12:
            barcode_class = barcode.get_barcode_class('ean13')
            # Ensure EAN13 format
            if len(barcode_data) == 12:
                barcode_data = barcode_data
            else:
                barcode_data = barcode_data[:12]
        else:
            # Default to Code128
            barcode_class = barcode.get_barcode_class('code128')
        
        # Create barcode instance
        barcode_instance = barcode_class(barcode_data, writer=ImageWriter())
        
        # Generate barcode image
        buffer = io.BytesIO()
        barcode_instance.write(buffer)
        buffer.seek(0)
        
        # Convert to base64
        barcode_base64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{barcode_base64}"
        
    except Exception as e:
        print(f"Error generating barcode: {e}")
        return create_placeholder_barcode()

def create_placeholder_barcode():
    """
    Create a placeholder barcode image when generation fails
    """
    try:
        # Create a simple placeholder image
        img = Image.new('RGB', (200, 100), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to use a font, fallback to default if not available
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        # Draw placeholder text
        draw.text((50, 40), "No Barcode", fill='black', font=font)
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        barcode_base64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{barcode_base64}"
        
    except Exception as e:
        print(f"Error creating placeholder barcode: {e}")
        # Return a minimal SVG as fallback
        svg_content = '''<svg width="200" height="100" xmlns="http://www.w3.org/2000/svg">
            <rect width="200" height="100" fill="white" stroke="black"/>
            <text x="70" y="55" font-family="Arial" font-size="14" fill="black">No Barcode</text>
        </svg>'''
        svg_base64 = base64.b64encode(svg_content.encode()).decode()
        return f"data:image/svg+xml;base64,{svg_base64}"
