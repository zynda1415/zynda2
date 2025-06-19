import streamlit as st
import data

def item_module():
    st.header("Item Management")

    action = st.radio("Choose Action", ["Add Item", "Edit Item", "Delete Item"])

    if action == "Add Item":
        st.subheader("Add New Item")

        name = st.text_input("Item Name")
        category = st.text_input("Category")
        quantity = st.number_input("Quantity", min_value=0)
        purchase_price = st.number_input("Purchase Price", min_value=0.0)
        sale_price = st.number_input("Sale Price", min_value=0.0)
        supplier = st.text_input("Supplier")
        notes = st.text_area("Notes")
        image_url = st.text_input("Image URL")

        if st.button("Add Item"):
            ws = data.sheet.worksheet("Inventory")
            ws.append_row([name, category, quantity, purchase_price, sale_price, supplier, notes, image_url])
            st.success("Item added successfully!")

    elif action == "Edit Item":
        st.subheader("Edit Item (Not Implemented Yet)")

    elif action == "Delete Item":
        st.subheader("Delete Item (Not Implemented Yet)")
