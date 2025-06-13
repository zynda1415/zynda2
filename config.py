# config.py

HEADER_ALIASES = {
    "Inventory": {
        "name": "Item Name (English)",
        "barcode": "Barcode",
        "category": "Category",
        "stock": "Quantity",
        "price": "Sell Price",
        "brand": "Supplier",
        "note": "Notes",
        "image": "Image URL"
    },
    "Sales": {
        "date": "Date",
        "item": "Item",
        "client": "Client",
        "quantity": "Qty",
        "unit_price": "Unit Price",
        "total": "Total Price"
    },
    "Clients": {
        "id": "Client ID",
        "name": "Name",
        "phone": "Phone",
        "address": "Address",
        "type": "Type"
    },
    "Invoices": {
        "invoice_id": "Invoice ID",
        "client": "Client",
        "amount": "Amount",
        "due": "Due Date",
        "status": "Status"
    }
}
