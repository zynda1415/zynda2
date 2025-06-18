import streamlit as st
import pandas as pd
from fpdf import FPDF
import barcode # From python-barcode
from barcode.writer import ImageWriter
from PIL import Image # Pillow library for image handling, needed by ImageWriter
import io
import os # For cleaning up temporary barcode files

def render_catalog_view(inventory_df, mappings):
    """
    Renders the product catalog view with filters and product cards.
    """
    st.subheader("Filters")
    # Dynamic filtering based on mapped headers
    category_col = mappings['inventory']['category']
    item_name_col = mappings['inventory']['item_name']
    barcode_col = mappings['inventory']['barcode']

    filtered_df = inventory_df.copy()

    if category_col in filtered_df.columns:
        unique_categories = filtered_df[category_col].unique().tolist()
        selected_category = st.selectbox("Filter by Category", ['All'] + unique_categories, key="catalog_category_filter")
        if selected_category != 'All':
            filtered_df = filtered_df[filtered_df[category_col] == selected_category]

    if item_name_col in filtered_df.columns:
        search_name = st.text_input("Search by Item Name", key="catalog_name_search")
        if search_name:
            filtered_df = filtered_df[filtered_df[item_name_col].str.contains(search_name, case=False, na=False)]

    st.subheader("Product Cards")
    if not filtered_df.empty:
        cols = st.columns(3) # Display 3 cards per row
        for i, row in filtered_df.iterrows():
            with cols[i % 3]:
                with st.container(border=True):
                    st.write(f"**{row.get(item_name_col, 'N/A')}**")
                    st.write(f"Category: {row.get(category_col, 'N/A')}")
                    st.write(f"Sell Price: ${row.get(mappings['inventory']['sell_price'], 'N/A'):.2f}")
                    st.write(f"Quantity: {row.get(mappings['inventory']['quantity'], 'N/A')}")

                    # Image preview
                    image_url = row.get(mappings['inventory']['image_url'])
                    if image_url:
                        st.image(image_url, caption=row.get(item_name_col, ''), width=100)
                    else:
                        st.text("No Image")

                    # Barcode generation (requires python-barcode and Pillow)
                    barcode_value = str(row.get(barcode_col))
                    if barcode_value and barcode_value != 'None' and barcode_value.strip(): # Check for non-empty string
                        try:
                            # EAN13 requires a 12-digit number (plus checksum added by the library)
                            # Or other barcode types like Code128, etc. based on your needs
                            if len(barcode_value) == 12 and barcode_value.isdigit():
                                EAN = barcode.EAN13(barcode_value, writer=ImageWriter())
                                filename = f"temp_barcode_{barcode_value}.png"
                                EAN.save(filename)
                                st.image(filename, caption="Barcode", width=150)
                                os.remove(filename) # Clean up temp file immediately
                            else:
                                st.warning(f"Barcode '{barcode_value}' is not a valid 12-digit EAN13. Displaying as text.")
                                st.code(barcode_value) # Display as text if not valid for EAN13
                        except Exception as e:
                            st.warning(f"Could not generate barcode for '{barcode_value}': {e}. Displaying as text.")
                            st.code(barcode_value) # Display as text on error
                    else:
                        st.text("No Barcode")

    else:
        st.info("No products to display based on current filters.")

    return filtered_df # Return filtered DF for PDF export

def generate_catalog_pdf(filtered_df, mappings):
    """
    Generates a PDF of the product catalog.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Product Catalog", ln=True, align="C")
    pdf.ln(10)

    # Re-extract mapped column headers for PDF
    item_name_col = mappings['inventory']['item_name']
    category_col = mappings['inventory']['category']
    sell_price_col = mappings['inventory']['sell_price']
    quantity_col = mappings['inventory']['quantity']
    barcode_col = mappings['inventory']['barcode']

    for i, row in filtered_df.iterrows():
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 10, txt=f"Item: {row.get(item_name_col, 'N/A')}", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 7, txt=f"Category: {row.get(category_col, 'N/A')}", ln=True)
        pdf.cell(0, 7, txt=f"Sell Price: ${row.get(sell_price_col, 'N/A'):.2f}", ln=True)
        pdf.cell(0, 7, txt=f"Quantity: {row.get(quantity_col, 'N/A')}", ln=True)

        barcode_value = str(row.get(barcode_col))
        if barcode_value and barcode_value != 'None' and barcode_value.strip() and len(barcode_value) == 12 and barcode_value.isdigit():
            try:
                EAN = barcode.EAN13(barcode_value, writer=ImageWriter())
                temp_barcode_path = f"temp_barcode_pdf_{barcode_value}.png"
                EAN.save(temp_barcode_path)
                
                # Check if enough space is left on the page
                if pdf.get_y() + 25 > pdf.h - pdf.b_margin: # 25 is approximate height for barcode + padding
                    pdf.add_page() # Add a new page if content will overflow
                
                # Adjust x, y, width, height for barcode image placement
                # Positioning it relative to the current y position
                pdf.image(temp_barcode_path, x=pdf.get_x() + 140, y=pdf.get_y() - 25, w=40)
                os.remove(temp_barcode_path) # Clean up temp file
            except Exception as e:
                pdf.cell(0, 7, txt=f"Barcode Generation Error: {e}", ln=True)
        else:
            pdf.cell(0, 7, txt=f"Barcode: {barcode_value if barcode_value != 'None' else 'N/A'}", ln=True)
        pdf.ln(5) # Add some space after each item

    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.download_button(
        label="Download Catalog PDF",
        data=pdf_output,
        file_name="product_catalog.pdf",
        mime="application/pdf",
        key="download_catalog_pdf"
    )
