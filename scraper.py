import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, List, Optional
import logging

class AuchanScraper:
    BASE_URL = "https://www.auchan.sn"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def search_products(self, query: str) -> List[Dict]:
        """Search products by query string"""
        try:
            search_url = f"{self.BASE_URL}/catalogsearch/result/?q={query}"
            response = self.session.get(search_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('div', class_='product-item-info')
            
            results = []
            for product in products:
                product_data = self._extract_product_data(product)
                if product_data:
                    results.append(product_data)
                time.sleep(0.5)  # Polite delay between requests
                
            return results
        except Exception as e:
            logging.error(f"Error searching products: {str(e)}")
            return []

    def _extract_product_data(self, product_element) -> Optional[Dict]:
        """Extract product data from HTML element"""
        try:
            name_elem = product_element.find('a', class_='product-item-link')
            price_elem = product_element.find('span', class_='price')
            img_elem = product_element.find('img', class_='product-image-photo')
            
            if not all([name_elem, price_elem, img_elem]):
                return None
                
            price = price_elem.text.strip()
            price = float(price.replace('FCFA', '').replace(' ', '').replace(',', ''))
            
            return {
                'name': name_elem.text.strip(),
                'default_code': name_elem.get('href', '').split('/')[-1],
                'list_price': price,
                'type': 'product',
                'categ_id': self._get_category(product_element),
                'description_sale': self._get_description(product_element),
                'active': True,
                'sale_ok': True,
                'purchase_ok': True,
                'image_1920': img_elem.get('src', ''),
                'is_published': True,
                'public_categ_ids': self._get_category_hierarchy(product_element)
            }
        except Exception as e:
            logging.error(f"Error extracting product data: {str(e)}")
            return None

    def _get_category(self, product_element) -> str:
        """Extract category information"""
        try:
            category_elem = product_element.find('div', class_='category')
            return category_elem.text.strip() if category_elem else "Uncategorized"
        except:
            return "Uncategorized"

    def _get_description(self, product_element) -> str:
        """Extract product description"""
        try:
            desc_elem = product_element.find('div', class_='description')
            return desc_elem.text.strip() if desc_elem else ""
        except:
            return ""

    def _get_category_hierarchy(self, product_element) -> List[str]:
        """Extract category hierarchy"""
        try:
            breadcrumb = product_element.find('div', class_='breadcrumbs')
            if breadcrumb:
                return [item.strip() for item in breadcrumb.text.split('/')]
            return []
        except:
            return []
