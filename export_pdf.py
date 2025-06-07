import io
import base64
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from PIL import Image
import requests
from . import barcode_utils

def generate_catalog_pdf_visual(df, show_category, show_price, show_stock, show_barcode, 
                               barcode_type, color_option, export_layout="Grid", include_cover_page=True):
    """Generate a visual PDF catalog"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], 
                                alignment=TA_CENTER, spaceAfter=30)
    
    # Cover page
    if include_cover_page:
        story.append(Paragraph("Inventory Catalog", title_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                              styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Total Items: {len(df)}", styles['Normal']))
        story.append(PageBreak())
    
    # Create content based on layout style
    if export_layout == "Grid":
        story.extend(_create_grid_layout(df, show_category, show_price, show_stock, 
                                       show_barcode, barcode_type, color_option, styles))
    elif export_layout == "List":
        story.extend(_create_list_layout(df, show_category, show_price, show_stock, 
                                       show_barcode, barcode_type, color_option, styles))
    else:  # Detailed
        story.extend(_create_detailed_layout(df, show_category, show_price, show_stock, 
                                           show_barcode, barcode_type, color_option, styles))
    
    # Build PDF
    doc.build(story)
    
    # Get the value of the BytesIO buffer and return it
    buffer.seek(0)
    return buffer.getvalue()

def _create_grid_layout(df, show_category, show_price, show_stock, show_barcode, barcode_type, color_option, styles):
    """Create a grid layout for the PDF"""
    story = []
    
    # Create table data
    table_data = []
    row_data = []
    
    for index, row in df.iterrows():
        cell_content = []
        
        # Item name
        cell_content.append(Paragraph(f"<b>{row['Item Name']}</b>", styles['Normal']))
        
        # Category
        if show_category:
            cell_content.append(Paragraph(f"Category: {row['Category']}", styles['Normal']))
        
        # Price
        if show_price:
            cell_content.append(Paragraph(f"Price: ${row['Sale Price']:.2f}", styles['Normal']))
        
        # Stock
        if show_stock:
            stock_qty = row['Quantity']
            _, badge_label = _get_stock_badge(stock_qty)
            cell_content.append(Paragraph(f"Stock: {stock_qty} ({badge_label})", styles['Normal']))
        
        # Combine cell content
        combined_content = [Spacer(1, 6)] + cell_content
        row_data.append(combined_content)
        
        # Create table row when we have 3 items or at the end
        if len(row_data) == 3 or index == len(df) - 1:
            table_data.append(row_data)
            row_data = []
    
    # Create table
    if table_data:
        table = Table(table_data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ]))
        story.append(table)
    
    return story

def _create_list_layout(df, show_category, show_price, show_stock, show_barcode, barcode_type, color_option, styles):
    """Create a list layout for the PDF"""
    story = []
    
    for index, row in df.iterrows():
        # Item name
        story.append(Paragraph(f"<b>{row['Item Name']}</b>", styles['Heading2']))
        
        # Category
        if show_category:
            story.append(Paragraph(f"Category: {row['Category']}", styles['Normal']))
        
        # Price
        if show_price:
            story.append(Paragraph(f"Price: ${row['Sale Price']:.2f}", styles['Normal']))
        
        # Stock
        if show_stock:
            stock_qty = row['Quantity']
            _, badge_label = _get_stock_badge(stock_qty)
            story.append(Paragraph(f"Stock: {stock_qty} ({badge_label})", styles['Normal']))
        
        story.append(Spacer(1, 12))
    
    return story

def _create_detailed_layout(df, show_category, show_price, show_stock, show_barcode, barcode_type, color_option, styles):
    """Create a detailed layout for the PDF"""
    story = []
    
    for index, row in df.iterrows():
        # Create a table for each item
        data = [
            ['Item Name', row['Item Name']],
        ]
        
        if show_category:
            data.append(['Category', row['Category']])
        
        if show_price:
            data.append(['Price', f"${row['Sale Price']:.2f}"])
        
        if show_stock:
            stock_qty = row['Quantity']
            _, badge_label = _get_stock_badge(stock_qty)
            data.append(['Stock', f"{stock_qty} ({badge_label})"])
        
        # Create table
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
    
    return story

def _get_stock_badge(stock_qty):
    """Get stock badge color and label"""
    if stock_qty == 0:
        return 'red', 'Out of Stock'
    elif stock_qty < 5:
        return 'orange', 'Low Stock'
    else:
        return 'green', 'In Stock'

def _download_image(url):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content))
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return None
