import streamlit as st

def apply_global_styles():
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] {
        background-color: #f8f9fa;
        padding: 15px 10px 5px 10px;
        border-radius: 10px;
        box-shadow: 0 0 5px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
