import streamlit as st
from typing import List, Dict
import pandas as pd

def create_progress_bar() -> None:
    """Create and initialize a progress bar"""
    progress_bar = st.progress(0)
    return progress_bar

def update_progress(progress_bar, value: float) -> None:
    """Update progress bar value"""
    progress_bar.progress(value)

def display_data_preview(data: pd.DataFrame) -> None:
    """Display preview of scraped data with enhanced formatting"""
    st.subheader("Aperçu des données")

    # Format price column if present
    if 'list_price' in data.columns:
        data = data.copy()
        data['list_price'] = data['list_price'].apply(lambda x: f"{x:,.2f} CFA")

    # Show total count
    st.caption(f"Total produits trouvés: {len(data)}")

    # Display the dataframe with custom styling
    st.dataframe(
        data,
        use_container_width=True,
        column_config={
            "name": "Nom du produit",
            "default_code": "Code",
            "list_price": "Prix",
            "description_sale": "Description",
            "image_1920": "URL Image"
        }
    )

def show_success_message(count: int) -> None:
    """Display success message with product count"""
    st.success(f"✅ {count} produits trouvés et traités avec succès!")

def show_error_message(error: str) -> None:
    """Display error message"""
    st.error(f"❌ Une erreur s'est produite: {error}")