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

    # Search interface
    search_query = st.text_input("Enter product name or category to search", "")
    
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
                    df = processor.format_data(products)
                    
                    # Preview phase
                    update_progress(progress_bar, 0.8)
                    display_data_preview(df)
                    
                    # Export option
                    if st.button("Export to Excel"):
                        excel_data = processor.export_to_excel(df)
                        st.download_button(
                            label="Download Excel file",
                            data=excel_data,
                            file_name="auchan_products.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    update_progress(progress_bar, 1.0)
                    show_success_message(len(products))
                else:
                    st.warning("No products found for the given search query.")
                    
            except Exception as e:
                show_error_message(str(e))
        else:
            st.warning("Please enter a search query")

if __name__ == "__main__":
    main()
