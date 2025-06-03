import streamlit as st
from your_module import add_item, edit_item, delete_item  # Replace 'your_module' by your data functions module

def render_item_section(df):
    st.subheader("Item Management")

    item_action = st.sidebar.radio("Item Actions", ["Add Item", "Edit Item", "Delete Item"])

    if item_action == "Add Item":
        st.subheader("Add New Item")
        with st.form("add_form"):
            item_name = st.text_input("Item Name")
            category = st.text_input("Category")
            quantity = st.number_input("Quantity", min_value=0, step=1)
            purchase_price = st.number_input("Purchase Price", min_value=0.0, step=0.01)
            sale_price = st.number_input("Sale Price", min_value=0.0, step=0.01)
            supplier = st.text_input("Supplier")
            notes = st.text_area("Notes")
            image_url = st.text_input("Image URL")

            submitted = st.form_submit_button("Add Item")

            if submitted:
                new_item = {
                    'Item Name': item_name,
                    'Category': category,
                    'Quantity': quantity,
                    'Purchase Price': purchase_price,
                    'Sale Price': sale_price,
                    'Supplier': supplier,
                    'Notes': notes,
                    'Image URL': image_url
                }
                add_item(new_item)
                st.success("Item added successfully!")

    elif item_action == "Edit Item":
        st.subheader("Edit Existing Item")
        if df.empty:
            st.warning("No items to edit.")
        else:
            item_to_edit = st.selectbox("Select Item to Edit", df.index, format_func=lambda x: df.loc[x, 'Item Name'])
            selected_row = df.loc[item_to_edit]

            with st.form("edit_form"):
                item_name = st.text_input("Item Name", value=selected_row['Item Name'])
                category = st.text_input("Category", value=selected_row['Category'])
                quantity = st.number_input("Quantity", min_value=0, step=1, value=int(selected_row['Quantity']))
                purchase_price = st.number_input("Purchase Price", min_value=0.0, step=0.01, value=float(selected_row['Purchase Price']))
                sale_price = st.number_input("Sale Price", min_value=0.0, step=0.01, value=float(selected_row['Sale Price']))
                supplier = st.text_input("Supplier", value=selected_row['Supplier'])
                notes = st.text_area("Notes", value=selected_row['Notes'])
                image_url = st.text_input("Image URL", value=selected_row['Image URL'])

                submitted = st.form_submit_button("Save Changes")

                if submitted:
                    updated_item = {
                        'Item Name': item_name,
                        'Category': category,
                        'Quantity': quantity,
                        'Purchase Price': purchase_price,
                        'Sale Price': sale_price,
                        'Supplier': supplier,
                        'Notes': notes,
                        'Image URL': image_url
                    }
                    edit_item(item_to_edit, updated_item)
                    st.success("Item updated successfully!")

    elif item_action == "Delete Item":
        st.subheader("Delete Item")
        if df.empty:
            st.warning("No items to delete.")
        else:
            item_to_delete = st.selectbox("Select Item to Delete", df.index, format_func=lambda x: df.loc[x, 'Item Name'])
            if st.button("Delete"):
                delete_item(item_to_delete)
                st.success("Item deleted successfully!")
