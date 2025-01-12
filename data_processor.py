import pandas as pd
from typing import List, Dict
import io

class OdooDataProcessor:
    ODOO_COLUMNS = [
        'name', 'default_code', 'list_price', 'type', 'categ_id',
        'description_sale', 'active', 'sale_ok', 'purchase_ok',
        'image_1920', 'is_published', 'public_categ_ids'
    ]

    def format_data(self, products: List[Dict]) -> pd.DataFrame:
        """Format scraped data into Odoo-compatible DataFrame"""
        df = pd.DataFrame(products)
        
        # Ensure all required columns exist
        for col in self.ODOO_COLUMNS:
            if col not in df.columns:
                df[col] = ''
                
        # Convert boolean values to Odoo format
        bool_columns = ['active', 'sale_ok', 'purchase_ok', 'is_published']
        for col in bool_columns:
            df[col] = df[col].map({True: 1, False: 0})
            
        # Format category IDs
        df['public_categ_ids'] = df['public_categ_ids'].apply(lambda x: ','.join(x) if isinstance(x, list) else '')
        
        return df[self.ODOO_COLUMNS]

    def export_to_excel(self, df: pd.DataFrame) -> bytes:
        """Export DataFrame to Excel bytes"""
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Products')
        return output.getvalue()
