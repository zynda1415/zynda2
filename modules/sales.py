import streamlit as st
import datetime
import data

def sales_module():
    st.header("🧾 Sales Entry")

    inventory_df = data.load_inventory()
    clients_df = data.load_clients()

    item_name = st.selectbox("Select Item", inventory_df['Item Name'].unique())
    client_name = st.selectbox("Select Client", clients_df['Client name'].unique())

    today = datetime.date.today()
    sale_date = st.date_input("Sale Date", today)

    unit_price = inventory_df[inventory_df['Item Name'] == item_name]['Sale Price'].values[0]
    quantity_sold = st.number_input("Quantity Sold", min_value=1, step=1)
    
    total_price = unit_price * quantity_sold
    st.write(f"Total Price: **${total_price:,.2f}**")

    if st.button("Save Sale"):
        data.save_sale(sale_date.strftime("%Y-%m-%d"), item_name, client_name, quantity_sold, unit_price, total_price)
        st.success("✅ Sale saved successfully!")
