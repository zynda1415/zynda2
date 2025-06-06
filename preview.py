import streamlit as st
import data

def catalog_module():
    st.header("📦 Inventory Catalog")

    df = data.load_inventory()

    # Search and filter
    search = st.text_input("🔎 Search Items", placeholder="Enter item name...")
    category_filter = st.selectbox("📂 Filter by Category", ["All"] + list(df['Category'].unique()))
    columns_per_row = st.slider("🖥️ Columns per row", 1, 5, 3)

    # Apply filters
    if search:
        df = df[df['Item Name'].str.contains(search, case=False, na=False)]
    if category_filter != "All":
        df = df[df['Category'] == category_filter]

    # Display cards
    for i in range(0, len(df), columns_per_row):
        cols = st.columns(columns_per_row)
        for col, (_, row) in zip(cols, df.iloc[i:i+columns_per_row].iterrows()):
            with col:
                with st.container():
                    st.image(row['Image URL'], width=150)
                    st.markdown(f"**{row['Item Name']}**")
                    st.write(f"📂 {row['Category']}")
                    st.write(f"💰 ${row['Sale Price']:.2f}")
                    st.write(f"📦 Stock: {row['Quantity']}")
                    
                    if row['Quantity'] < 5:
                        st.warning("⚠️ Low Stock!")
