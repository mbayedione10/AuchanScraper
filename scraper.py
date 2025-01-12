import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, List, Optional
import logging

class AuchanScraper:
    BASE_URL = "https://www.auchan.sn"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1"
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        logging.basicConfig(level=logging.INFO)

    def search_products(self, query: str) -> List[Dict]:
        """Search products by query string"""
        try:
            search_url = f"{self.BASE_URL}/recherche"
            params = {
                'controller': 'search',
                's': query
            }
            logging.info(f"Searching URL: {search_url} with params: {params}")

            response = self.session.get(search_url, params=params)
            response.raise_for_status()

            logging.info(f"Response status: {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')
            logging.info("Parsing HTML response")

            # Debug: Print the HTML structure
            logging.info(f"HTML Content Preview: {soup.prettify()[:500]}")

            products = soup.find_all('div', class_='product-description')
            logging.info(f"Found {len(products)} products")

            results = []
            for product in products:
                product_data = self._extract_product_data(product.parent)
                if product_data:
                    results.append(product_data)
                time.sleep(0.5)  # Polite delay between requests

            return results

        except Exception as e:
            logging.error(f"Error searching products: {str(e)}")
            raise e

    def _extract_product_data(self, product_element) -> Optional[Dict]:
        """Extract product data from HTML element"""
        try:
            name_elem = product_element.select_one('.product-title a')
            price_elem = product_element.select_one('.product-price-and-shipping .price')
            img_elem = product_element.select_one('.thumbnail img')

            if not all([name_elem, price_elem]):
                logging.warning("Missing required elements", 
                    extra={
                        "name_found": bool(name_elem),
                        "price_found": bool(price_elem),
                        "img_found": bool(img_elem)
                    })
                return None

            # Extract and clean price
            price_text = price_elem.text.strip()
            # Remove non-numeric characters except decimal point
            price = ''.join(c for c in price_text if c.isdigit() or c == '.')
            try:
                price = float(price)
                logging.info(f"Converted price '{price_text}' to {price}")
            except ValueError:
                logging.error(f"Failed to convert price: {price_text}")
                return None

            product_url = name_elem.get('href', '')

            product_data = {
                'name': name_elem.text.strip(),
                'default_code': product_url.split('/')[-1] if product_url else '',
                'list_price': price,  # Now guaranteed to be float
                'type': 'Biens',  # Default value as requested
                'categ_id': 'All',  # Default value as requested
                'description_sale': self._get_description(product_element),
                'active': True,
                'sale_ok': True,
                'purchase_ok': True,
                'image_1920': img_elem.get('src', '') if img_elem else '',
                'is_published': True,  # Default value as requested
                'public_categ_ids': self._get_category_hierarchy(product_element)
            }

            logging.info(f"Extracted product: {product_data['name']}")
            return product_data

        except Exception as e:
            logging.error(f"Error extracting product data: {str(e)}")
            return None

    def _get_description(self, product_element) -> str:
        """Extract product description"""
        try:
            desc_elem = product_element.select_one('.product-description')
            return desc_elem.text.strip() if desc_elem else ""
        except Exception as e:
            logging.error(f"Error getting description: {str(e)}")
            return ""

    def _get_category_hierarchy(self, product_element) -> List[str]:
        """Extract category hierarchy"""
        try:
            breadcrumb = product_element.select_one('.breadcrumb')
            if breadcrumb:
                links = breadcrumb.select('a')[1:]  # Skip home link
                return [link.text.strip() for link in links]
            return []
        except Exception as e:
            logging.error(f"Error getting category hierarchy: {str(e)}")
            return []