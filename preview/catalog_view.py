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
            st.error("No inventory data found. Please check your data source.")
            return
            
        # Debug: Show column names
        st.write("**Debug - Available columns:**", list(df.columns))
        
        # Customization controls
        (show_category, show_price, show_stock, show_barcode, layout_style, 
         color_option, image_fit, barcode_type, export_layout, include_cover_page) = customization.customization_controls(df)
        
        style.apply_global_styles()
        
        # Create filter controls
        col1, col2, col3, col4, col5, col6 = st.columns([2.5, 1.7, 1.7, 1.2, 1.2, 1.2])
        
        with col1:
            search = st.text_input("🔎 Search", placeholder="Name, Category, Notes...")
        
        with col2:
            # Check if Category column exists
            if 'Category' in df.columns:
                category_filter = st.selectbox("📂 Category", ["All"] + list(df['Category'].unique()))
            else:
                category_filter = "All"
                st.write("No Category column found")
        
        with col3:
            # Check which price column exists
            price_column = None
            for col in ['Sale Price', 'Price', 'Unit Price']:
                if col in df.columns:
                    price_column = col
                    break
            
            if price_column:
                sort_option = st.selectbox("↕️ Sort by", ["Name", "Price (High)", "Price (Low)"])
            else:
                sort_option = st.selectbox("↕️ Sort by", ["Name"])
        
        with col4:
            export_button = st.button("Export PDF")
        
        # Apply filtering
        filtered_df = df.copy()
        
        if search:
            search_lower = search.lower()
            filtered_df = filtered_df[filtered_df.apply(lambda row: search_lower in str(row).lower(), axis=1)]
        
        if category_filter != "All" and 'Category' in df.columns:
            filtered_df = filtered_df[filtered_df['Category'] == category_filter]
        
        # Apply sorting
        if price_column and sort_option in ["Price (High)", "Price (Low)"]:
            if sort_option == "Price (High)":
                filtered_df = filtered_df.sort_values(by=price_column, ascending=False)
            elif sort_option == "Price (Low)":
                filtered_df = filtered_df.sort_values(by=price_column, ascending=True)
        else:
            # Sort by name or first column
            name_column = None
            for col in ['Item Name', 'Name', 'Product Name']:
                if col in df.columns:
                    name_column = col
                    break
            if name_column:
                filtered_df = filtered_df.sort_values(by=name_column)
        
        st.write(f"### Filtered Items ({len(filtered_df)} items)")
        
        # Render the catalog cards
        render_cards(filtered_df, show_category, show_price, show_stock, show_barcode, color_option, image_fit, barcode_type)
        
        # Handle PDF export
        if export_button:
            try:
                pdf_bytes, filename = pdf_export.generate_catalog_pdf_visual(
                    filtered_df,
                    show_category, show_price, show_stock, show_barcode,
                    barcode_type, color_option, export_layout, include_cover_page,
                    logo_path=None, language='EN',
                    selected_categories=None, selected_brands=None
                )
                st.download_button("Download PDF", pdf_bytes, file_name=filename)
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
                
    except Exception as e:
        st.error(f"Error loading catalog: {str(e)}")
        st.write("Please check your data.py file and ensure it returns a valid DataFrame.")

def render_cards(df, show_category, show_price, show_stock, show_barcode, color_option, image_fit, barcode_type):
    """
    Render inventory items as cards
    """
    for idx, row in df.iterrows():
        try:
            # Determine the name column
            name_column = None
            for col in ['Item Name', 'Name', 'Product Name', 'Item']:
                if col in df.columns:
                    name_column = col
                    break
            
            if name_column:
                st.subheader(row[name_column])
            else:
                st.subheader(f"Item {idx}")
            
            # Show supplier if available
            supplier_column = None
            for col in ['Supplier', 'Vendor', 'Brand']:
                if col in df.columns:
                    supplier_column = col
                    break
            
            if supplier_column and pd.notna(row[supplier_column]):
                st.write(f"Supplier: {row[supplier_column]}")
            
            # Show category if requested and available
            if show_category and 'Category' in df.columns and pd.notna(row['Category']):
                st.write(f"Category: {row['Category']}")
            
            # Show price if requested and available
            if show_price:
                price_column = None
                for col in ['Sale Price', 'Price', 'Unit Price']:
                    if col in df.columns:
                        price_column = col
                        break
                
                if price_column and pd.notna(row[price_column]):
                    st.write(f"Price: ${row[price_column]}")
            
            # Show stock if requested and available
            if show_stock:
                stock_column = None
                for col in ['Quantity', 'Stock', 'Qty', 'Inventory']:
                    if col in df.columns:
                        stock_column = col
                        break
                
                if stock_column and pd.notna(row[stock_column]):
                    st.write(f"Stock: {row[stock_column]}")
            
            # Show barcode if requested and available
            if show_barcode:
                barcode_column = None
                for col in ['Barcode', 'SKU', 'Code', 'Product Code']:
                    if col in df.columns:
                        barcode_column = col
                        break
                
                if barcode_column and pd.notna(row[barcode_column]) and str(row[barcode_column]).strip():
                    try:
                        b64_barcode = barcode_utils.encode_image(row[barcode_column], barcode_type)
                        st.image(b64_barcode)
                    except Exception as e:
                        st.write(f"Barcode: {row[barcode_column]} (Could not generate image)")
                else:
                    st.write("No barcode available")
            
            st.markdown("---")
            
        except Exception as e:
            st.error(f"Error rendering item {idx}: {str(e)}")
            st.markdown("---")
