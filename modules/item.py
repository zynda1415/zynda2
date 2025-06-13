import streamlit as st
import pandas as pd
from config import HEADER_ALIASES as H
from data import load_inventory_data, save_inventory_data

def render_item_section():
    st.title("📦 Item Manager")
    df = load_inventory_data()

    tab1, tab2, tab3 = st.tabs(["📋 Preview Items", "➕ Add Item", "✏️ Edit Item"])

    with tab1:
        preview_items(df)

    with tab2:
        add_item(df)

    with tab3:
        edit_item(df)

def preview_items(df):
    st.subheader("🖼️ Preview Items")
    if df.empty:
        st.warning("No items found.")
        return

    for _, row in df.iterrows():
        with st.expander(row[H["Item Name (English)"]]):
            st.image(row.get(H["Image"], ""), width=200)
            st.markdown(f"**Brand:** {row.get(H['Brand'], 'N/A')}")
            st.markdown(f"**Category:** {row.get(H['Category 1'], 'N/A')}")
            st.markdown(f"**Sell Price:** {row.get(H['Sell Price'], 'N/A')}")
            st.markdown(f"**Code:** {row.get(H['Code'], 'N/A')}")
            st.markdown(f"**Note:** {row.get(H['Note'], 'N/A')}")

def add_item(df):
    st.subheader("➕ Add New Item")
    with st.form("add_item_form", clear_on_submit=True):
        name_en = st.text_input("Name (English)")
        name_ku = st.text_input("Name (Kurdish)")
        price = st.number_input("Sell Price", min_value=0.0, step=0.5)
        brand = st.text_input("Brand")
        category = st.text_input("Category")
        image_url = st.text_input("Image URL")
        code = st.text_input("Item Code")
        note = st.text_area("Note")

        submitted = st.form_submit_button("✅ Add Item")
        if submitted:
            new_row = {
                H["Item Name (English)"]: name_en,
                H["Item Name (Kurdish)"]: name_ku,
                H["Sell Price"]: price,
                H["Brand"]: brand,
                H["Category 1"]: category,
                H["Image"]: image_url,
                H["Code"]: code,
                H["Note"]: note
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_inventory_data(df)
            st.success("Item added successfully!")

def edit_item(df):
    st.subheader("✏️ Edit Existing Item")
    item_list = df[H["Item Name (English)"]].dropna().tolist()
    selected = st.selectbox("Select item", item_list)

    item_row = df[df[H["Item Name (English)"]] == selected]
    if item_row.empty:
        st.warning("Item not found.")
        return

    index = item_row.index[0]

    with st.form("edit_item_form"):
        name_en = st.text_input("Name (English)", value=df.at[index, H["Item Name (English)"]])
        name_ku = st.text_input("Name (Kurdish)", value=df.at[index, H["Item Name (Kurdish)"]])
        price = st.number_input("Sell Price", value=float(df.at[index, H["Sell Price"]]))
        brand = st.text_input("Brand", value=df.at[index, H["Brand"]])
        category = st.text_input("Category", value=df.at[index, H["Category 1"]])
        image_url = st.text_input("Image URL", value=df.at[index, H["Image"]])
        code = st.text_input("Item Code", value=df.at[index, H["Code"]])
        note = st.text_area("Note", value=df.at[index, H["Note"]])

        submitted = st.form_submit_button("💾 Save Changes")
        if submitted:
            df.at[index, H["Item Name (English)"]] = name_en
            df.at[index, H["Item Name (Kurdish)"]] = name_ku
            df.at[index, H["Sell Price"]] = price
            df.at[index, H["Brand"]] = brand
            df.at[index, H["Category 1"]] = category
            df.at[index, H["Image"]] = image_url
            df.at[index, H["Code"]] = code
            df.at[index, H["Note"]] = note
            save_inventory_data(df)
            st.success("Item updated successfully!")
