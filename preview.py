import streamlit as st
import data
import math

def catalog_module():
    st.header("📦 Inventory Catalog")

    df = data.load_inventory()

    # Advanced Search
    search = st.text_input("🔎 Search", placeholder="Search Item Name, Category, or Notes...")
    category_filter = st.selectbox("📂 Filter by Category", ["All"] + list(df['Category'].unique()))
    sort_option = st.selectbox("↕️ Sort By", ["Item Name (A-Z)", "Price (Low-High)", "Price (High-Low)", "Stock (Low-High)", "Stock (High-Low)"])
    columns_per_row = st.slider("🖥️ Columns per row", 1, 5, 3)
    items_per_page = st.selectbox("📄 Items per page", [10, 20, 50], index=0)

    # Apply Search
    if search:
        df = df[df.apply(lambda row: search.lower() in str(row['Item Name']).lower() 
                         or search.lower() in str(row['Category']).lower()
                         or search.lower() in str(row.get('Notes', '')).lower(), axis=1)]
    
    # Apply Category Filter
    if category_filter != "All":
        df = df[df['Category'] == category_filter]

    # Apply Sorting
    if sort_option == "Item Name (A-Z)":
        df = df.sort_values(by='Item Name', ascending=True)
    elif sort_option == "Price (Low-High)":
        df = df.sort_values(by='Sale Price', ascending=True)
    elif sort_option == "Price (High-Low)":
        df = df.sort_values(by='Sale Price', ascending=False)
    elif sort_option == "Stock (Low-High)":
        df = df.sort_values(by='Quantity', ascending=True)
    elif sort_option == "Stock (High-Low)":
        df = df.sort_values(by='Quantity', ascending=False)

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
