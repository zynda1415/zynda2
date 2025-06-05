import streamlit as st
import pandas as pd
import data

def item_management():
    st.header("Item Management")
    df = data.load_inventory()

    action = st.radio("Item Actions", ["Add Item", "Edit Item", "Delete Item"])

    if action == "Add Item":
        with st.form("add_form"):
            name = st.text_input("Item Name")
            category = st.text_input("Category")
            quantity = st.number_input("Quantity", 0)
            purchase_price = st.number_input("Purchase Price", 0.0)
            sale_price = st.number_input("Sale Price", 0.0)
            supplier = st.text_input("Supplier")
            notes = st.text_input("Notes")
            image_url = st.text_input("Image URL")
            submitted = st.form_submit_button("Add")

            if submitted:
                new_row = pd.DataFrame([[name, category, quantity, purchase_price, sale_price, supplier, notes, image_url]],
                                        columns=df.columns)
                df = pd.concat([df, new_row], ignore_index=True)
                data.save_inventory(df)
                st.success("Item Added Successfully!")

    elif action == "Edit Item":
        if df.empty:
            st.warning("No items found.")
            return

        item_to_edit = st.selectbox("Select item to edit", df['Item Name'])
        selected_row = df[df['Item Name'] == item_to_edit].iloc[0]

        with st.form("edit_form"):
            name = st.text_input("Item Name", selected_row['Item Name'])
            category = st.text_input("Category", selected_row['Category'])
            quantity = st.number_input("Quantity", 0, value=int(selected_row['Quantity']))
            purchase_price = st.number_input("Purchase Price", 0.0, value=float(selected_row['Purchase Price']))
            sale_price = st.number_input("Sale Price", 0.0, value=float(selected_row['Sale Price']))
            supplier = st.text_input("Supplier", selected_row['Supplier'])
            notes = st.text_input("Notes", selected_row['Notes'])
            image_url = st.text_input("Image URL", selected_row['Image URL'])
            submitted = st.form_submit_button("Update")

            if submitted:
                df.loc[df['Item Name'] == item_to_edit] = [
                    name, category, quantity, purchase_price, sale_price, supplier, notes, image_url
                ]
                data.save_inventory(df)
                st.success("Item updated successfully!")

    elif action == "Delete Item":
        if df.empty:
            st.warning("No items found.")
            return

        item_to_delete = st.selectbox("Select item to delete", df['Item Name'])
        if st.button("Delete"):
            df = df[df['Item Name'] != item_to_delete]
            data.save_inventory(df)
            st.success("Item deleted successfully!")
