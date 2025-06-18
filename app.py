import streamlit as st
import gspread
import pandas as pd
import io # Needed for fpdf2 output if not using file paths directly

# Import modular components
from header_mapper import HeaderMapper
import item
import invoice
import clients
import returns
import purchase_history
import catalog_view # Contains render_catalog_view and generate_catalog_pdf
import map_view     # Contains render_map_view

# --- Google Sheet Connection ---
@st.cache_resource(ttl=3600)
def get_gspread_client(credentials_json):
    """
    Establishes a connection to Google Sheets using service account credentials.
    Caches the client to avoid re-authentication on every rerun.
    """
    try:
        # Load credentials from the JSON string
        return gspread.service_account_from_dict(credentials_json)
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}. Please check your credentials.")
        return None

def load_sheet_data(client, sheet_url):
    """
    Loads data from all worksheets in the specified Google Sheet.
    Returns a dictionary of DataFrames, where keys are sheet names.
    """
    data = {}
    sheet_headers = {}
    try:
        spreadsheet = client.open_by_url(sheet_url)
        for worksheet in spreadsheet.worksheets():
            records = worksheet.get_all_records()
            if records:
                df = pd.DataFrame(records)
                data[worksheet.title] = df
                sheet_headers[worksheet.title] = df.columns.tolist()
            else:
                data[worksheet.title] = pd.DataFrame() # Empty DataFrame for empty sheets
                sheet_headers[worksheet.title] = [] # No headers if sheet is empty
        return data, sheet_headers
    except Exception as e:
        st.error(f"Error loading data from Google Sheet: {e}. Make sure the sheet URL is correct and the service account has access.")
        return {}, {}

# --- Initialize Header Mapper ---
if 'header_mapper' not in st.session_state:
    st.session_state.header_mapper = HeaderMapper()

# --- Main Streamlit App ---
st.set_page_config(layout="wide", page_title="ZyndaSys Inventory & CRM")
st.title("ZyndaSys Inventory & CRM")

# Sidebar for credentials and Sheet URL
with st.sidebar:
    st.header("Configuration")
    st.write("Upload your service account JSON file and provide the Google Sheet URL.")

    uploaded_file = st.file_uploader("Upload Service Account JSON", type="json")
    google_sheet_url = st.text_input("Google Sheet URL", value="https://docs.google.com/spreadsheets/d/1hwVsrPQjJdv9c4GyI_QzujLzG3dImlUHxmOUbUdjY7M/edit?usp=sharing")

    credentials = None
    if uploaded_file is not None:
        import json
        credentials = json.load(uploaded_file)
        st.success("Credentials loaded.")

    # Connect and Load Data Button
    if st.button("Connect and Load Data"):
        if credentials and google_sheet_url:
            st.session_state.gspread_client = get_gspread_client(credentials)
            if st.session_state.gspread_client:
                st.session_state.spreadsheet_url = google_sheet_url # Store URL for sub-modules
                st.session_state.sheet_data, st.session_state.sheet_headers = load_sheet_data(
                    st.session_state.gspread_client, google_sheet_url
                )
                if st.session_state.sheet_data:
                    st.success("Data loaded successfully!")
                    # Re-initialize header mapper to pick up actual headers from loaded sheets
                    st.session_state.header_mapper = HeaderMapper()
                else:
                    st.warning("No data loaded. Check your sheet or connection.")
        else:
            st.warning("Please upload credentials and provide a Sheet URL.")

# Ensure data is loaded before displaying tabs
if "sheet_data" not in st.session_state or not st.session_state.sheet_data:
    st.info("Please connect to Google Sheets using the sidebar to proceed.")
else:
    # Get current mappings
    current_mappings = st.session_state.header_mapper.get_all_mappings()
    gspread_client = st.session_state.gspread_client
    spreadsheet_url = st.session_state.spreadsheet_url

    # Create tabs
    tab_titles = [
        "SheetConfig", "Inventory", "Clients", "Invoices", "InvoiceItems",
        "Returns", "PurchaseHistory", "Catalog View", "Map View"
    ]
    tabs = st.tabs(tab_titles)

    with tabs[0]: # SheetConfig Tab
        st.session_state.header_mapper.render_config_ui(st.session_state.sheet_headers)
        st.write("Current Mappings:")
        st.json(current_mappings)

    with tabs[1]: # Inventory Tab
        st.header("Inventory Management")
        inventory_df = item.get_inventory_df(st.session_state.sheet_data)
        item.display_inventory_data(inventory_df, current_mappings)
        st.markdown("---")
        item.add_inventory_item(gspread_client, spreadsheet_url, {}, current_mappings) # Placeholder for new item data

    with tabs[2]: # Clients Tab
        st.header("Client Management")
        clients_df = clients.get_clients_df(st.session_state.sheet_data)
        clients.display_clients_data(clients_df, current_mappings)
        st.markdown("---")
        clients.add_client(gspread_client, spreadsheet_url, {}, current_mappings) # Placeholder

    with tabs[3]: # Invoices Tab
        st.header("Invoice Management")
        invoices_df = invoice.get_invoices_df(st.session_state.sheet_data)
        invoice.display_invoices(invoices_df, current_mappings)
        st.markdown("---")
        invoice.add_invoice(gspread_client, spreadsheet_url, {}, current_mappings) # Placeholder

    with tabs[4]: # InvoiceItems Tab
        st.header("Invoice Items")
        invoice_items_df = invoice.get_invoice_items_df(st.session_state.sheet_data)
        invoice.display_invoice_items(invoice_items_df, current_mappings)
        st.markdown("---")
        invoice.add_invoice_item(gspread_client, spreadsheet_url, {}, current_mappings) # Placeholder

    with tabs[5]: # Returns Tab
        st.header("Returns Handling")
        returns_df = returns.get_returns_df(st.session_state.sheet_data)
        returns.display_returns_data(returns_df, current_mappings)
        st.markdown("---")
        returns.log_return(gspread_client, spreadsheet_url, {}, current_mappings) # Placeholder

    with tabs[6]: # PurchaseHistory Tab
        st.header("Purchase History")
        purchase_history_df = purchase_history.get_purchase_history_df(st.session_state.sheet_data)
        purchase_history.display_purchase_history_data(purchase_history_df, current_mappings)
        st.markdown("---")
        # Example of how you might call an update function
        # purchase_history.update_purchase_history(gspread_client, spreadsheet_url, "Example Item", "last_buy_price", 10.50, pd.to_datetime("today"), current_mappings)

    with tabs[7]: # Catalog View Tab
        st.header("Product Catalog")
        inventory_df = item.get_inventory_df(st.session_state.sheet_data) # Get fresh inventory data
        filtered_df = catalog_view.render_catalog_view(inventory_df, current_mappings)

        st.markdown("---")
        st.subheader("Export to PDF")
        if st.button("Generate Catalog PDF", key="main_pdf_button"):
            catalog_view.generate_catalog_pdf(filtered_df, current_mappings)


    with tabs[8]: # Map View Tab
        st.header("Client Map View")
        clients_df = clients.get_clients_df(st.session_state.sheet_data)
        map_view.render_map_view(clients_df, current_mappings)
