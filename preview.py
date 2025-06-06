import streamlit as st
import data

def catalog_module():
    st.header("📦 Inventory Catalog View")

    df = data.load_inventory()
    search = st.text_input("Search by Item Name")
    category_filter = st.selectbox("Filter by Category", ["All"] + list(df['Category'].unique()))
    columns_per_row = st.slider("Columns per row", 1, 5, 3)

    if search:
        df = df[df['Item Name'].str.contains(search, case=False)]
    if category_filter != "All":
        df = df[df['Category'] == category_filter]

    for i in range(0, len(df), columns_per_row):
        cols = st.columns(columns_per_row)
        for col, (_, row) in zip(cols, df.iloc[i:i+columns_per_row].iterrows()):
            with col:
                st.image(row['Image URL'], width=150)
                st.write(f"**{row['Item Name']}**")
                st.write(f"Category: {row['Category']}")
                st.write(f"Quantity: {row['Quantity']}")
                st.write(f"Price: ${row['Sale Price']}")
