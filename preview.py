preview_item.import streamlit as st
import pandas as pd

def render_preview(df):
    st.subheader("Inventory List")
    
    search = st.text_input("Search by Item Name")
    category_filter = st.selectbox("Filter by Category", ['All'] + sorted(df['Category'].dropna().unique()))

    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df['Item Name'].str.contains(search, case=False, na=False)]
    if category_filter != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == category_filter]

    for index, row in filtered_df.iterrows():
        with st.container():
            cols = st.columns([1, 2, 2, 2, 2])
            image_url = str(row.get('Image URL', '')).strip()
            if image_url and image_url.lower() != 'nan':
                try:
                    cols[0].image(image_url, width=80)
                except Exception:
                    cols[0].write("Invalid Image")
            else:
                cols[0].write("No Image")

            cols[1].write(f"**{row['Item Name']}**")
            cols[2].write(f"Category: {row['Category']}")
            cols[3].write(f"Quantity: {row['Quantity']}")
            cols[4].write(f"Price: ${row['Sale Price']}")
py
