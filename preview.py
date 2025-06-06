import streamlit as st
import data
import math

def catalog_module():
    st.header("📦 Inventory Catalog")

    df = data.load_inventory()

    # Search & Filter
    search = st.text_input("🔎 Search Items", placeholder="Enter item name...")
    category_filter = st.selectbox("📂 Filter by Category", ["All"] + list(df['Category'].unique()))
    columns_per_row = st.slider("🖥️ Columns per row", 1, 5, 3)
    items_per_page = st.selectbox("📄 Items per page", [10, 20, 50], index=0)

    # Apply filters
    if search:
        df = df[df['Item Name'].str.contains(search, case=False, na=False)]
    if category_filter != "All":
        df = df[df['Category'] == category_filter]

    # Pagination Logic
    total_items = len(df)
    total_pages = math.ceil(total_items / items_per_page)
    page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)

    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_data = df.iloc[start_idx:end_idx]

    # Display Cards
    for i in range(0, len(page_data), columns_per_row):
        cols = st.columns(columns_per_row)
        for col, (_, row) in zip(cols, page_data.iloc[i:i+columns_per_row].iterrows()):
            with col:
                with st.container():
                    st.image(row['Image URL'], width=150)
                    st.markdown(f"**{row['Item Name']}**")
                    st.write(f"📂 {row['Category']}")
                    st.write(f"💰 ${row['Sale Price']:.2f}")
                    st.write(f"📦 Stock: {row['Quantity']}")
                    
                    if row['Quantity'] < 5:
                        st.warning("⚠️ Low Stock!")

    st.write(f"Showing page {page} of {total_pages}")
