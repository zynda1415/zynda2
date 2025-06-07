import streamlit as st
from streamlit_option_menu import option_menu

# Modularized preview system
try:
    import preview.catalog_view as catalog
except ImportError as e:
    st.error(f"Error importing catalog module: {e}")
    catalog = None

# Existing modules
try:
    import item
    import mapview
    import data
    import sales
    import sales_summary
    import sales_charts
    import export_pdf
    import clients
except ImportError as e:
    st.error(f"Error importing modules: {e}")

st.set_page_config(page_title="ZYNDA_SYSTEM Inventory Management", layout="wide")

# Sidebar Menu using option_menu
with st.sidebar:
    menu = option_menu(
        "ZYNDA_SYSTEM Menu", 
        [
            "View Inventory", "Item", "Statistics", "Catalog View", "Map", 
            "Sales", "Sales Summary", "Sales Charts", "Export PDF", "Clients Management"
        ],
        icons=[
            "box", "pencil-square", "bar-chart-line", "grid", "geo-alt", 
            "cash-coin", "clipboard-data", "graph-up-arrow", "file-earmark-pdf", "people-fill"
        ],
        menu_icon="grid-3x3-gap-fill", 
        default_index=0
    )

# Page Routing
if menu == "View Inventory":
    try:
        df = data.load_inventory()
        st.title("📦 Inventory Management System")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error loading inventory: {e}")

elif menu == "Item":
    try:
        item.item_module()
    except Exception as e:
        st.error(f"Error loading item module: {e}")

elif menu == "Statistics":
    try:
        inventory_df = data.load_inventory()
        total_items = len(inventory_df)
        total_quantity = inventory_df["Quantity"].sum()
        total_value = (inventory_df["Quantity"] * inventory_df["Sale Price"]).sum()
        st.title("📊 Inventory Statistics")
        
        # Create columns for better layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Items", total_items)
        with col2:
            st.metric("Total Quantity", f"{total_quantity:,}")
        with col3:
            st.metric("Total Value", f"${total_value:,.2f}")
            
    except Exception as e:
        st.error(f"Error loading statistics: {e}")

elif menu == "Catalog View":
    if catalog is not None:
        try:
            catalog.catalog_module()
        except Exception as e:
            st.error(f"Error loading catalog view: {e}")
            st.write("Please check the following:")
            st.write("1. Ensure all required modules are properly installed")
            st.write("2. Check that the preview folder contains all necessary files")
            st.write("3. Verify that the data module is working correctly")
    else:
        st.error("Catalog module could not be imported. Please check your file structure.")

elif menu == "Map":
    try:
        mapview.map_module()
    except Exception as e:
        st.error(f"Error loading map module: {e}")

elif menu == "Sales":
    try:
        sales.sales_module()
    except Exception as e:
        st.error(f"Error loading sales module: {e}")

elif menu == "Sales Summary":
    try:
        sales_summary.sales_summary_module()
    except Exception as e:
        st.error(f"Error loading sales summary module: {e}")

elif menu == "Sales Charts":
    try:
        sales_charts.sales_charts_module()
    except Exception as e:
        st.error(f"Error loading sales charts module: {e}")

elif menu == "Export PDF":
    try:
        export_pdf.export_pdf_module()
    except Exception as e:
        st.error(f"Error loading export PDF module: {e}")

elif menu == "Clients Management":
    try:
        clients.clients_module()
    except Exception as e:
        st.error(f"Error loading clients module: {e}")

# Add footer
st.sidebar.markdown("---")
st.sidebar.markdown("**ZYNDA_SYSTEM** v1.0")
st.sidebar.markdown("Inventory Management System")
