import streamlit as st
import pandas as pd
import os

# File path to store inventory data
DATA_FILE = 'inventory.csv'

# Initialize CSV if not exists
def init_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["Item Name", "Category", "Quantity", "Purchase Price", "Sale Price", "Supplier", "Notes"])
        df.to_csv(DATA_FILE, index=False)

# Load data from CSV
def load_data():
    return pd.read_csv(DATA_FILE)

# Save data to CSV
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Add new item
def add_item(item):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([item])], ignore_index=True)
    save_data(df)

# Delete item by index
def delete_item(index):
    df = load_data()
    df = df.drop(index)
    df.reset_index(drop=True, inplace=True)
    save_data(df)

# Update item by index
def update_item(index, updated_item):
    df = load_data()
    df.loc[index] = updated_item
    save_data(df)

# Filter data based on search query
def filter_data(df, query):
    if query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    return df

# Initialize the CSV file on first run
init_data_file()

# Streamlit UI
st.title("📦 Inventory Management System")

menu = ["Add Item", "View Inventory", "Edit/Delete Item", "Statistics"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Item":
    st.subheader("Add New Item")
    
    with st.form("Add Form"):
        item_name = st.text_input("Item Name")
        category = st.text_input("Category")
        quantity = st.number_input("Quantity", min_value=0, step=1)
        purchase_price = st.number_input("Purchase Price", min_value=0.0, step=0.01)
        sale_price = st.number_input("Sale Price", min_value=0.0, step=0.01)
        supplier = st.text_input("Supplier")
        notes = st.text_area("Notes")
        submit = st.form_submit_button("Add Item")
        
        if submit:
            item = {
                "Item Name": item_name,
                "Category": category,
                "Quantity": quantity,
                "Purchase Price": purchase_price,
                "Sale Price": sale_price,
                "Supplier": supplier,
                "Notes": notes
            }
            add_item(item)
            st.success("Item added successfully!")

elif choice == "View Inventory":
    st.subheader("Inventory List")
    df = load_data()
    
    search_query = st.text_input("Search")
    filtered_df = filter_data(df, search_query)
    st.dataframe(filtered_df)

elif choice == "Edit/Delete Item":
    st.subheader("Edit or Delete Items")
    df = load_data()
    st.write("Select an item to edit or delete:")
    
    for index, row in df.iterrows():
        with st.expander(f"{row['Item Name']} ({row['Category']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Delete", key=f"del_{index}"):
                    delete_item(index)
                    st.warning("Item deleted!")
                    st.experimental_rerun()
            
            with col2:
                if st.button("Edit", key=f"edit_{index}"):
                    with st.form(f"edit_form_{index}"):
                        item_name = st.text_input("Item Name", value=row["Item Name"])
                        category = st.text_input("Category", value=row["Category"])
                        quantity = st.number_input("Quantity", min_value=0, value=int(row["Quantity"]))
                        purchase_price = st.number_input("Purchase Price", min_value=0.0, value=float(row["Purchase Price"]))
                        sale_price = st.number_input("Sale Price", min_value=0.0, value=float(row["Sale Price"]))
                        supplier = st.text_input("Supplier", value=row["Supplier"])
                        notes = st.text_area("Notes", value=row["Notes"])
                        submit = st.form_submit_button("Update")
                        
                        if submit:
                            updated_item = {
                                "Item Name": item_name,
                                "Category": category,
                                "Quantity": quantity,
                                "Purchase Price": purchase_price,
                                "Sale Price": sale_price,
                                "Supplier": supplier,
                                "Notes": notes
                            }
                            update_item(index, updated_item)
                            st.success("Item updated!")
                            st.experimental_rerun()

elif choice == "Statistics":
    st.subheader("Inventory Statistics")
    df = load_data()
    total_items = df.shape[0]
    total_quantity = df["Quantity"].sum()
    total_value = (df["Quantity"] * df["Purchase Price"]).sum()
    potential_revenue = (df["Quantity"] * df["Sale Price"]).sum()
    
    st.metric("Total Items", total_items)
    st.metric("Total Quantity", total_quantity)
    st.metric("Total Purchase Value", f"${total_value:,.2f}")
    st.metric("Potential Revenue", f"${potential_revenue:,.2f}")
