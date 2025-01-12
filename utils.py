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
    """Display preview of scraped data"""
    st.subheader("Data Preview")
    st.dataframe(data.head(10))

def show_success_message(count: int) -> None:
    """Display success message with product count"""
    st.success(f"Successfully scraped {count} products!")

def show_error_message(error: str) -> None:
    """Display error message"""
    st.error(f"An error occurred: {error}")
