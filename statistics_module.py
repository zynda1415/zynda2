import streamlit as st
import data

def show_statistics():
    st.header("Inventory Statistics")
    df = data.load_inventory()
    total_items = len(df)
    total_quantity = df['Quantity'].sum()
    total_value = (df['Quantity'] * df['Sale Price']).sum()

    st.write(f"Total Items: {total_items}")
    st.write(f"Total Quantity: {total_quantity}")
    st.write(f"Total Inventory Value: ${total_value:,.2f}")
