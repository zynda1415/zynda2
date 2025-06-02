import re

def convert_drive_link(url):
    pattern = r"https://drive\\.google\\.com/file/d/(.*?)/"
    match = re.search(pattern, url)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=view&id={file_id}"
    return url
