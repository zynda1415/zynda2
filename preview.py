import streamlit as st
import pandas as pd

def render_preview(df):
    st.subheader("🖼 Inventory Catalog View")

    # Filtering
    search = st.text_input("Search by Item Name")
    category_filter = st.selectbox("Filter by Category", ['All'] + sorted(df['Category'].dropna().unique()))

    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df['Item Name'].str.contains(search, case=False, na=False)]
    if category_filter != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == category_filter]

    # Set number of columns (fully responsive)
    num_cols = st.slider("Columns per row", 2, 5, 3)

    # Render as grid
    for i in range(0, len(filtered_df), num_cols):
        row_items = filtered_df.iloc[i:i+num_cols]
        cols = st.columns(len(row_items))

        for idx, row in enumerate(row_items.itertuples()):
            with cols[idx]:
                st.markdown("<div style='border:1px solid #ddd; padding:10px; border-radius:10px;'>", unsafe_allow_html=True)
                
                image_url = str(row._8).strip()  # Image URL is 8th column (zero-indexed)
                if image_url and image_url.lower() != 'nan':
                    try:
                        st.image(image_url, use_container_width=True)
                    except:
                        st.write("(Invalid Image)")
                else:
                    st.write("(No Image)")

                st.write(f"**{row._1}**")  # Item Name
                st.write(f"Category: {row._2}")
                st.write(f"Quantity: {row._3}")
                st.write(f"Price: ${row._5}")
                st.markdown("</div>", unsafe_allow_html=True)
