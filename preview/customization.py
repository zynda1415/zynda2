import streamlit as st

def customization_controls(df):
    with st.expander("⚙️ Customize Catalog View", expanded=False):
        show_category = st.checkbox("Show Category", value=True)
        show_price = st.checkbox("Show Price", value=True)
        show_stock = st.checkbox("Show Stock Badge", value=True)
        show_barcode = st.checkbox("Show Barcode", value=True)
        layout_style = st.radio("Card Layout Style", ["Detailed View", "Compact View"], index=0)
        color_option = st.selectbox("🎨 Theme Color", ["green", "blue", "purple", "orange", "red"], index=0)
        image_fit = st.radio("🖼 Image Fill Mode", ["Contain", "Cover"], index=0)
        barcode_type = st.radio("📦 Barcode Type", ["Code128", "QR"], index=0)

        # 🔥 Batch 4 New Options:
        export_layout = st.radio("🖨️ PDF Layout Style", ["Detailed View", "Compact View"], index=0)
        include_cover_page = st.checkbox("📄 Include Cover Page", value=True)

    return (
        show_category, show_price, show_stock, show_barcode, layout_style, 
        color_option, image_fit, barcode_type, export_layout, include_cover_page
    )
