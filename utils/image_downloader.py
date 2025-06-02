import requests
from PIL import Image
from io import BytesIO
from .drive_converter import convert_drive_link

def download_image(url):
    try:
        url = convert_drive_link(url)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("RGB")
        return img
    except:
        return Image.new("RGB", (300, 300), color=(230, 230, 230))
