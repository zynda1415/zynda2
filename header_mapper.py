import streamlit as st

class HeaderMapper:
    """
    Manages the mapping between logical field keys and actual Google Sheet column headers.
    """
    def __init__(self):
        # Define default logical field keys for each section
        self.logical_fields = {
            "inventory": {
                "item_name": "Item Name",
                "barcode": "Barcode",
                "category": "Category",
                "quantity": "Quantity",
                "sell_price": "Sell Price",
                "wholesale_price": "Wholesale Price",
                "last_purchase_price": "Last Purchase Price",
                "last_purchase_date": "Last Purchase Date",
                "expiry_date": "Expiry Date",
                "supplier": "Supplier",
                "image_url": "Image URL",
                "notes": "Notes",
                "free_quantity": "Free Quantity"
            },
            "clients": {
                "client_id": "Client ID",
                "name": "Name",
                "phone": "Phone",
                "address": "Address",
                "type": "Type",
                "latitude": "Latitude",
                "longitude": "Longitude"
            },
            "invoices": {
                "invoice_id": "Invoice ID",
                "client": "Client",
                "amount": "Amount",
                "due_date": "Due Date",
                "status": "Status",
                "type": "Type"
            },
            "invoice_items": {
                "invoice_id": "Invoice ID",
                "item_name": "Item Name",
                "quantity": "Quantity",
                "unit_price": "Unit Price",
                "total_price": "Total_Price",
                "free_quantity": "Free Quantity"
            },
            "returns": {
                "return_id": "Return ID",
                "invoice_id": "Invoice ID",
                "item_name": "Item Name",
                "quantity": "Quantity",
                "return_date": "Return Date",
                "reason": "Reason"
            },
            "purchase_history": {
                "item_name": "Item Name",
                "last_buy_price": "Last Buy Price",
                "last_sell_price": "Last Sell Price",
                "last_wholesale_price": "Last Wholesale Price",
                "last_transaction_date": "Last Transaction Date"
            }
        }
        # Initialize session state for mappings if not already present
        if "header_mappings" not in st.session_state:
            st.session_state.header_mappings = self.logical_fields

    def get_mapping(self, section, logical_key):
        """
        Retrieves the actual column header for a given logical key and section.
        """
        return st.session_state.header_mappings.get(section, {}).get(logical_key, logical_key)

    def set_mapping(self, section, logical_key, actual_header):
        """
        Sets the mapping for a given logical key and section.
        """
        if section not in st.session_state.header_mappings:
            st.session_state.header_mappings[section] = {}
        st.session_state.header_mappings[section][logical_key] = actual_header

    def render_config_ui(self, sheet_headers):
        """
        Renders the Streamlit UI for configuring header mappings.
        sheet_headers: A dictionary where keys are sheet names and values are lists of column headers.
        """
        st.header("Sheet Configuration")
        st.info("Map your logical field keys to actual Google Sheet column headers.")

        for section, fields in self.logical_fields.items():
            st.subheader(f"{section.replace('_', ' ').title()} Sheet Mapping")
            if section in sheet_headers:
                available_headers = [''] + sheet_headers[section]  # Add empty option
            else:
                available_headers = [''] # No headers available for this section yet

            for logical_key, default_header in fields.items():
                current_mapping = st.session_state.header_mappings.get(section, {}).get(logical_key, default_header)
                selected_header = st.selectbox(
                    f"Logical Field: **{logical_key.replace('_', ' ').title()}**",
                    options=available_headers,
                    index=available_headers.index(current_mapping) if current_mapping in available_headers else 0,
                    key=f"{section}_{logical_key}_mapping"
                )
                self.set_mapping(section, logical_key, selected_header)
            st.markdown("---")

    def get_all_mappings(self):
        """
        Returns all current header mappings.
        """
        return st.session_state.header_mappings
