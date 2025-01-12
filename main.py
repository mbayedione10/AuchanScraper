import streamlit as st
from scraper import AuchanScraper
from data_processor import OdooDataProcessor
from utils import (
    create_progress_bar,
    update_progress,
    display_data_preview,
    show_success_message,
    show_error_message
)
from styles import apply_custom_styles, show_logo

def main():
    # Apply custom styles
    apply_custom_styles()
    show_logo()

    # Initialize components
    scraper = AuchanScraper()
    processor = OdooDataProcessor()

    # Initialize session state for DataFrame if not exists
    if 'products_df' not in st.session_state:
        st.session_state.products_df = None

    # Search interface
    search_query = st.text_input("Enter product name or category to search", "")

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Search and Scrape"):
            if search_query:
                try:
                    progress_bar = create_progress_bar()

                    # Scraping phase
                    update_progress(progress_bar, 0.2)
                    products = scraper.search_products(search_query)

                    if products:
                        # Data processing phase
                        update_progress(progress_bar, 0.6)
                        st.session_state.products_df = processor.format_data(products)

                        # Preview phase
                        update_progress(progress_bar, 0.8)
                        display_data_preview(st.session_state.products_df)

                        update_progress(progress_bar, 1.0)
                        show_success_message(len(products))
                    else:
                        st.warning("No products found for the given search query.")

                except Exception as e:
                    show_error_message(str(e))
            else:
                st.warning("Please enter a search query")

    # Export button - only show when data is available
    with col2:
        if st.session_state.products_df is not None:
            excel_data = processor.export_to_excel(st.session_state.products_df)
            st.download_button(
                label="Export to Excel",
                data=excel_data,
                file_name="auchan_products.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()