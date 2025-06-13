# --- pdf_Customization.py ---
import streamlit as st

def pdf_customization_controls():
    with st.expander("🛠 Customize PDF Layout"):
        image_position = st.selectbox("🖼️ Image Position", ["Top", "Bottom", "Skip"])
        name_font_size = st.slider("🔤 Item Name Font Size", 8, 16, 10)
        stack_text = st.checkbox("📚 Stack Price & Brand", value=True)
        show_barcode_pdf = st.checkbox("🔳 Show Barcode in PDF", value=True)

    return {
        "image_position": image_position,
        "name_font_size": name_font_size,
        "stack_text": stack_text,
        "show_barcode_pdf": show_barcode_pdf
    }
