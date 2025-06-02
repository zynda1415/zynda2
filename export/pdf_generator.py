from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from io import BytesIO
from ..utils.image_downloader import download_image

def generate_catalog_pdf(df, filename="catalog.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []

    for idx, row in df.iterrows():
        img_url = row.get("Image URL", "")
        img = download_image(img_url)
        img.thumbnail((200, 200))
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        rl_img = RLImage(img_buffer, width=150, height=150)

        data = [
            ["Item Name:", row.get("Item Name", "")],
            ["Category:", row.get("Category", "")],
            ["Price:", f"${row.get('Sale Price', 0)}"],
            ["Quantity:", row.get("Quantity", "")],
            ["Barcode:", row.get("Barcode", "N/A")],
        ]
        table = Table(data, colWidths=[80, 300])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.grey)
        ]))

        story.append(rl_img)
        story.append(Spacer(1, 12))
        story.append(table)
        story.append(Spacer(1, 24))

    doc.build(story)
    return filename
