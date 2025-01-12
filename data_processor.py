import pandas as pd
from typing import List, Dict
import io
from datetime import datetime

class OdooDataProcessor:
    ODOO_COLUMNS = [
        'name', 'default_code', 'list_price', 'type', 'categ_id',
        'description_sale', 'active', 'sale_ok', 'purchase_ok',
        'image_1920', 'is_published', 'public_categ_ids', 'create_date'
    ]

    def format_data(self, products: List[Dict]) -> pd.DataFrame:
        """Format scraped data into Odoo-compatible DataFrame"""
        # Create DataFrame from products
        df = pd.DataFrame(products)

        # Add create_date field
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df['create_date'] = current_date

        # Ensure all required columns exist
        for col in self.ODOO_COLUMNS:
            if col not in df.columns:
                df[col] = ''

        # Convert boolean values to integers (Odoo format)
        bool_columns = ['active', 'sale_ok', 'purchase_ok', 'is_published']
        for col in bool_columns:
            df[col] = 1  # Set all to True by default

        # Format category IDs
        if 'public_categ_ids' in df.columns:
            df['public_categ_ids'] = df['public_categ_ids'].apply(
                lambda x: ','.join(x) if isinstance(x, list) else str(x)
            )

        # Format prices to 2 decimal places
        if 'list_price' in df.columns:
            df['list_price'] = df['list_price'].round(2)

        # Reorder columns to match ODOO_COLUMNS
        return df[self.ODOO_COLUMNS]

    def export_to_excel(self, df: pd.DataFrame) -> bytes:
        """Export DataFrame to Excel bytes with proper formatting"""
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Products')

            # Get the workbook and the worksheet
            workbook = writer.book
            worksheet = writer.sheets['Products']

            # Auto-adjust columns width
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

            # Format headers
            for cell in worksheet[1]:
                cell.style = 'Headline 3'

        return output.getvalue()