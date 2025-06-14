import streamlit as st
import pandas as pd
from config import HEADER_ALIASES
from data import load_inventory_data, save_inventory_data

H = HEADER_ALIASES["Inventory"]

def render_item_section():
    st.title("📦 Item Manager")
    df = load_inventory_data()

    tab1, tab2, tab3 = st.tabs(["📋 Preview Items", "➕ Add Item", "✏️ Edit Item"])

    with tab1:
        st.dataframe(df)

    with tab2:
        with st.form("add_item_form", clear_on_submit=True):
            name = st.text_input("Item Name")
            price = st.number_input("Price", 0.0)
            brand = st.text_input("Brand")
            submitted = st.form_submit_button("Add")
            if submitted:
                new_row = {
                    H["name"]: name,
                    H["price"]: price,
                    H["brand"]: brand
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_inventory_data(df)
                st.success("Item added.")

    with tab3:
        selected = st.selectbox("Select item to edit", df[H["name"]])
        row = df[df[H["name"]] == selected].iloc[0]
        with st.form("edit_form"):
            name = st.text_input("Item Name", row[H["name"]])
            price = st.number_input("Price", value=float(row[H["price"]]))
            brand = st.text_input("Brand", row[H["brand"]])
            save = st.form_submit_button("Update")
            if save:
                index = df[df[H["name"]] == selected].index[0]
                df.at[index, H["name"]] = name
                df.at[index, H["price"]] = price
                df.at[index, H["brand"]] = brand
                save_inventory_data(df)
                st.success("Item updated.")
