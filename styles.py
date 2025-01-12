import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        .stProgress .st-bo {
            background-color: #E40019;
        }
        .stButton>button {
            background-color: #E40019;
            color: white;
        }
        .stButton>button:hover {
            background-color: #007A33;
            color: white;
        }
        .dataframe {
            font-size: 12px;
        }
        </style>
    """, unsafe_allow_html=True)

def show_logo():
    st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <h1 style="color: #E40019;">Auchan Sénégal Product Scraper</h1>
            <p style="color: #007A33;">Export products directly to Odoo format</p>
        </div>
    """, unsafe_allow_html=True)
