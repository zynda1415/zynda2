import streamlit as st
import data

def render_catalog_view():
    st.title("🖼 Inventory Catalog v2")

    df = data.load_data()

    if df.empty:
        st.warning("No items found.")
        return

    # Rename columns to clean names for easier processing
    df = df.rename(columns={
        "Item Name": "Name",
        "Image URL": "Image",
        "Sale Price": "Price",
        "Quantity": "Quantity",
        "Barcode": "Barcode",
        "Brand": "Brand",
        "Category": "Category"
    })

    # Filtering UI
    with st.expander("🔎 Filters", expanded=True):
        search = st.text_input("Search by Name or Barcode")
        brand_filter = st.selectbox("Select Brand", ["All"] + sorted(df["Brand"].dropna().unique().tolist()))
        category_filter = st.selectbox("Select Category", ["All"] + sorted(df["Category"].dropna().unique().tolist()))

    # Filtering logic
    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[
            filtered_df["Name"].str.contains(search, case=False, na=False) |
            filtered_df["Barcode"].astype(str).str.contains(search, na=False)
        ]

    if brand_filter != "All":
        filtered_df = filtered_df[filtered_df["Brand"] == brand_filter]

    if category_filter != "All":
        filtered_df = filtered_df[filtered_df["Category"] == category_filter]

    # Responsive grid
    num_cols = st.slider("🖼 Items per row", 2, 5, 4)
    items_per_page = num_cols * 2

    total_pages = (len(filtered_df) + items_per_page - 1) // items_per_page
    page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)

    start = (page - 1) * items_per_page
    end = start + items_per_page

    paginated_df = filtered_df.iloc[start:end]

    for i in range(0, len(paginated_df), num_cols):
        row_items = paginated_df.iloc[i:i+num_cols]
        cols = st.columns(len(row_items))

        for idx, item in enumerate(row_items.itertuples()):
            with cols[idx]:
                st.markdown("<div style='border:1px solid #DDD; padding:10px; border-radius:10px;'>", unsafe_allow_html=True)
                try:
                    st.image(item.Image, use_column_width=True)
                except:
                    st.write("(No Image)")

                st.write(f"**Name:** {item.Name}")
                st.write(f"**Barcode:** {item.Barcode}")
                st.write(f"**Price:** ${item.Price}")
                st.write(f"**Quantity:** {item.Quantity}")
                st.write(f"**Brand:** {item.Brand}")
                st.write(f"**Category:** {item.Category}")
                st.markdown("</div>", unsafe_allow_html=True)
