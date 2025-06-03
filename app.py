import streamlit as st
import pandas as pd
import gspread
import json
from google.oauth2.service_account import Credentials
import item  # new file we created

# Your connect_gsheets(), load_data(), save_data() etc...

st.set_page_config(page_title="Inventory Management", layout="wide")
st.title("📦 Inventory Management System")

df = load_data()

menu = st.sidebar.radio("Menu", ["View Inventory", "Item", "Statistics"])

if menu == "View Inventory":
    # your inventory table code

elif menu == "Statistics":
    show_statistics()

elif menu == "Item":  # << this is still correct!
    item.render_item_section(df)
