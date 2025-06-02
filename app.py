import streamlit as st
import pandas as pd
import os

# CSV file to store inventory data
CSV_FILE = 'inventory.csv'

# Define inventory columns
COLUMNS = ['Item Name', 'Category', 'Quantity', 'Purchase Price', 'Sale Price', 'Supplier', 'Notes']

# Load data from CSV
@st.cache_data(ttl=60)
def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_FILE, index=False)
    return df

# Save data to CSV
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Define your add_item, edit_item, delete_item, show_statistics here (same as previous code)

# Now load the data after defining functions:
df = load_data()

# Now build the sidebar menu safely
menu = st.sidebar.radio("Menu", ["View Inventory", "Item", "Statistics"])
