import streamlit as st
from streamlit_option_menu import option_menu

import dataimport views.sheet_info_view as sheet_info_view

# Views
import views.inventory_view as inventory_view
import views.statistics_view as statistics_view
import views.catalog_view as catalog

# Modules
import modules.item as item
import modules.clients as clients
import modules.invoice as invoice
import modules.sales as sales
import modules.sales_summary as sales_summary
import modules.sales_charts as sales_charts
import modules.mapview as mapview

st.set_page_config(page_title="ZYNDA_SYSTEM Inventory Management", layout="wide")

def main():
    with st.sidebar:
        menu = option_menu("ZYNDA_SYSTEM Menu", 
            ["View Inventory", "Item", "Statistics", "Catalog View", "Map", 
             "Sales", "Sales Summary", "Sales Charts", "Clients Management", "Invoices", "Sheet Info"],
            icons=["box", "pencil-square", "bar-chart-line", "grid", "geo-alt", 
                   "cash-coin", "clipboard-data", "graph-up-arrow", "people-fill", "file-earmark-text"],
            menu_icon="grid-3x3-gap-fill", default_index=0)

    if menu == "View Inventory":
        inventory_view.inventory_view_module()

    elif menu == "Item":
        item.item_module()

    elif menu == "Statistics":
        statistics_view.statistics_module()

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
        
    elif menu == "Sheet Info":
        sheet_info_view.sheet_info_module()


if __name__ == "__main__":
    main()
