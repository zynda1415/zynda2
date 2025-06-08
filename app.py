import streamlit as st
from streamlit_option_menu import option_menu

# Import all modules
import modules.item as item
import modules.clients as clients
import modules.invoice as invoice
import modules.sales as sales
import modules.sales_summary as sales_summary
import modules.sales_charts as sales_charts
import modules.mapview as mapview
import views.inventory_view as inventory_view
import data
import preview.catalog_view as catalog

st.set_page_config(page_title="ZYNDA_SYSTEM Inventory Management", layout="wide")

def main():
    with st.sidebar:
        menu = option_menu("ZYNDA_SYSTEM Menu", 
            ["View Inventory", "Item", "Statistics", "Catalog View", "Map", 
             "Sales", "Sales Summary", "Sales Charts", "Clients Management", "Invoices"],
            icons=["box", "pencil-square", "bar-chart-line", "grid", "geo-alt", 
                   "cash-coin", "clipboard-data", "graph-up-arrow", "people-fill", "file-earmark-text"],
            menu_icon="grid-3x3-gap-fill", default_index=0)

    if menu == "View Inventory":
        inventory_view.inventory_view_module()

    elif menu == "Item":
        item.item_module()

    elif menu == "Statistics":
        inventory_df = data.load_inventory()
        total_items = len(inventory_df)
        total_quantity = inventory_df["Quantity"].sum()
        total_value = (inventory_df["Quantity"] * inventory_df["Sale Price"]).sum()
        st.title("📦 Inventory Statistics")
        st.write(f"Total Items: {total_items}")
        st.write(f"Total Quantity: {total_quantity}")
        st.write(f"Total Inventory Value: ${total_value:,.2f}")

    elif menu == "Catalog View":
        catalog.catalog_module()

    elif menu == "Map":
        mapview.map_module()

    elif menu == "Sales":
        sales.sales_module()

    elif menu == "Sales Summary":
        sales_summary.sales_summary_module()

    elif menu == "Sales Charts":
        sales_charts.sales_charts_module()

    elif menu == "Clients Management":
        clients.clients_module()

    elif menu == "Invoices":
        invoice.render_invoice_section()

if __name__ == "__main__":
    main()
