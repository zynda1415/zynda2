# ----------- sales.py -----------
import streamlit as st
import data
import pandas as pd
from datetime import datetime

def sales_management():
    st.header("Sales Management")
    inventory_df = data.load_inventory()
    sales_df = data.load_sales()

    with st.form("sales_form"):
        item = st.selectbox("Item", options=inventory_df['Item Name'])
        qty = st.number_input("Quantity Sold", 1)
        unit_price = st.number_input("Unit Price", 0.0)
        date = st.date_input("Date", value=datetime.now())
        submitted = st.form_submit_button("Add Sale")

        if submitted:
            total_price = qty * unit_price
            new_sale = pd.DataFrame([[date.strftime("%Y-%m-%d"), item, qty, unit_price, total_price]],
                                     columns=sales_df.columns)
            sales_df = pd.concat([sales_df, new_sale], ignore_index=True)
            data.save_sales(sales_df)
            st.success("Sale recorded!")
            
            # Decrease inventory
            inventory_df.loc[inventory_df['Item Name']==item, 'Quantity'] -= qty
