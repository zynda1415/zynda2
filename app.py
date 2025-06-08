import streamlit as st
import item
import client
import invoice
import inventory_view  # ✅ NEW Inventory View Module

def main():
    st.sidebar.title("ZYNDA2 SYSTEM")

    menu = [
        "Dashboard",
        "Inventory View",
        "Manage Items",
        "Clients",
        "Invoices",
        "Settings"
    ]
    
    page = st.sidebar.radio("Go to", menu)

    if page == "Dashboard":
        st.title("📊 ZYNDA2 Dashboard")
        st.write("Welcome to your inventory & accounting system.")

    elif page == "Inventory View":
        inventory_view.inventory_view_module()  # ✅ New Module Called Here

    elif page == "Manage Items":
        item.render_item_section()

    elif page == "Clients":
        client.render_client_section()

    elif page == "Invoices":
        invoice.render_invoice_section()

    elif page == "Settings":
        st.title("⚙️ Settings")
        st.write("System configuration coming soon.")

if __name__ == "__main__":
    main()
