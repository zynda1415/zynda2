import streamlit as st
import data

def catalog_view():
    st.header("Inventory Catalog View")
    df = data.load_inventory()

    search = st.text_input("Search by Item Name")
    category_filter = st.selectbox("Filter by Category", options=["All"] + list(df['Category'].unique()))
    columns = st.slider("Columns per row", 1, 5, 3)

    filtered_df = df[df['Item Name'].str.contains(search, case=False)] if search else df
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df['Category'] == category_filter]

    for i in range(0, len(filtered_df), columns):
        cols = st.columns(columns)
        for col, row in zip(cols, filtered_df.iloc[i:i+columns].itertuples()):
            with col:
                st.image(row.Image_URL, width=150)
                st.write(row.Item_Name)
                st.write(f"Category: {row.Category}")
                st.write(f"Price: ${row.Sale_Price}")
                st.write(f"Quantity: {row.Quantity}")
