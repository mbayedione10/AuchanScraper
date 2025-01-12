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

    # Initialize session state
    if 'products_df' not in st.session_state:
        st.session_state.products_df = None

    # Sidebar configuration
    with st.sidebar:
        st.subheader("Options de recherche")
        search_query = st.text_input("Rechercher un produit", "")

        st.subheader("Filtres")
        min_price = st.number_input("Prix minimum (CFA)", 0, 1000000, 0)
        max_price = st.number_input("Prix maximum (CFA)", 0, 1000000, 1000000)

        st.subheader("Champs à exporter")
        export_fields = st.multiselect(
            "Sélectionner les champs",
            ['name', 'default_code', 'list_price', 'description_sale', 'image_1920'],
            ['name', 'default_code', 'list_price']
        )

    # Main content area with tabs
    tab1, tab2 = st.tabs(["Recherche", "Résultats"])

    with tab1:
        if st.button("Rechercher et Scraper", type="primary"):
            if search_query:
                try:
                    progress_bar = create_progress_bar()

                    # Scraping phase
                    update_progress(progress_bar, 0.2)
                    products = scraper.search_products(search_query)

                    if products:
                        # Filter products by price
                        filtered_products = [
                            p for p in products 
                            if min_price <= p['list_price'] <= max_price
                        ]

                        # Data processing phase
                        update_progress(progress_bar, 0.6)
                        df = processor.format_data(filtered_products)

                        # Keep only selected fields
                        st.session_state.products_df = df[export_fields]

                        # Switch to results tab
                        st.session_state.active_tab = "Résultats"

                        update_progress(progress_bar, 1.0)
                        show_success_message(len(filtered_products))
                    else:
                        st.warning("Aucun produit trouvé pour cette recherche.")

                except Exception as e:
                    show_error_message(str(e))
            else:
                st.warning("Veuillez entrer un terme de recherche")

    with tab2:
        if st.session_state.products_df is not None:
            # Preview data
            display_data_preview(st.session_state.products_df)

            # Export button
            col1, col2 = st.columns([4, 1])
            with col2:
                excel_data = processor.export_to_excel(st.session_state.products_df)
                st.download_button(
                    label="Exporter (Excel)",
                    data=excel_data,
                    file_name="auchan_products.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary"
                )

if __name__ == "__main__":
    main()