import streamlit as st
import pandas as pd
import data
import preview.customization as customization
import preview.style as style
import preview.barcode_utils as barcode_utils
import utils.pdf_export as pdf_export

def catalog_module():
    st.header("📦 Inventory Catalog")
    
    try:
        df = data.load_inventory()
        if df is None or df.empty:
            st.error("No inventory data found.")
            return
        
        # Customization controls
        (show_category, show_price, show_stock, show_barcode, layout_style, 
         color_option, image_fit, barcode_type, export_layout, include_cover_page) = customization.customization_controls(df)
        
        style.apply_global_styles()
        
        col1, col2, col3, col4 = st.columns([2.5, 1.7, 1.7, 1.2])
        with col1:
            search = st.text_input("🔎 Search", placeholder="Name, Category, Notes...")
        with col2:
            category_filter = st.selectbox("📂 Category", ["All"] + list(df['Category'].unique())) if 'Category' in df.columns else "All"
        with col3:
            sort_option = st.selectbox("↕️ Sort by", ["Name", "Price (High)", "Price (Low)"])
        with col4:
            export_button = st.button("Export PDF")
        
        filtered_df = df.copy()
        if search:
            search_lower = search.lower()
            filtered_df = filtered_df[filtered_df.apply(lambda row: search_lower in str(row).lower(), axis=1)]

        if category_filter != "All" and 'Category' in df.columns:
            filtered_df = filtered_df[filtered_df['Category'] == category_filter]

        if sort_option == "Price (High)":
            filtered_df = filtered_df.sort_values(by="Sale Price", ascending=False)
        elif sort_option == "Price (Low)":
            filtered_df = filtered_df.sort_values(by="Sale Price", ascending=True)
        else:
            filtered_df = filtered_df.sort_values(by="Item Name")

        st.write(f"### Filtered Items ({len(filtered_df)} items)")

        render_cards(filtered_df, show_category, show_price, show_stock, show_barcode, color_option, image_fit, barcode_type)

        if export_button:
            pdf_bytes, filename = pdf_export.generate_catalog_pdf_visual(
                filtered_df, show_category, show_price, show_stock, show_barcode,
                barcode_type, color_option, export_layout, include_cover_page,
                logo_path=None, language='EN',
                selected_categories=None, selected_brands=None
            )
            st.download_button("Download PDF", pdf_bytes, file_name=filename)

    except Exception as e:
        st.error(f"Error: {str(e)}")

def render_cards(df, show_category, show_price, show_stock, show_barcode, color_option, image_fit, barcode_type):
    for idx, row in df.iterrows():
        st.subheader(row.get('Item Name', f"Item {idx}"))
        st.write(f"Supplier: {row.get('Supplier', 'N/A')}")
        if show_category:
            st.write(f"Category: {row.get('Category', 'N/A')}")
        if show_price:
            st.write(f"Price: ${row.get('Sale Price', 0)}")
        if show_stock:
            st.write(f"Stock: {row.get('Quantity', 0)}")
        if show_barcode and pd.notna(row.get('Barcode', None)):
            b64_barcode = barcode_utils.encode_image(row['Barcode'], barcode_type)
            st.image(b64_barcode)
        st.markdown("---")
