"""
Analytics Model
-------------
Handles data structures and calculations for analytics and reporting.
"""

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

class SalesAnalytics:
    def __init__(self):
        self.sales_data = []
        self.product_stats = {}
        self.category_stats = {}
        self.revenue_data = []

    def add_sale(self, sale):
        """Add a sale record to analytics"""
        self.sales_data.append({
            'date': sale.get('date', datetime.now().isoformat()),
            'product_id': sale.get('product_id'),
            'quantity': sale.get('quantity', 1),
            'price': sale.get('price', 0),
            'category': sale.get('category', 'Uncategorized')
        })
        self._update_stats()

    def _update_stats(self):
        """Update internal statistics"""
        df = pd.DataFrame(self.sales_data)
        if not df.empty:
            # Product statistics
            self.product_stats = df.groupby('product_id').agg({
                'quantity': 'sum',
                'price': 'mean'
            }).to_dict('index')

            # Category statistics
            self.category_stats = df.groupby('category')['quantity'].sum().to_dict()

            # Revenue data
            df['revenue'] = df['quantity'] * df['price']
            df['date'] = pd.to_datetime(df['date'])
            self.revenue_data = df.groupby(df['date'].dt.date)['revenue'].sum().to_dict()

    def get_daily_sales(self, days=7):
        """Get daily sales for the last n days"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days-1)
        dates = [start_date + timedelta(days=x) for x in range(days)]
        
        sales = [self.revenue_data.get(date, 0) for date in dates]
        return {
            'dates': [d.strftime('%d/%m/%Y') for d in dates],
            'sales': sales
        }

    def get_category_distribution(self):
        """Get product distribution by category"""
        return self.category_stats

    def get_product_stats(self):
        """Get detailed product statistics"""
        return self.product_stats

    def get_top_products(self, limit=5):
        """Get top selling products"""
        df = pd.DataFrame(self.sales_data)
        if df.empty:
            return []
        return df.groupby('product_id')['quantity'].sum().nlargest(limit).to_dict()

class InventoryAnalytics:
    def __init__(self):
        self.inventory_data = []

    def update_inventory(self, products):
        """Update inventory analytics data"""
        self.inventory_data = [{
            'id': p['id'],
            'name': p['name'],
            'stock': p['stock'],
            'price': p['price'],
            'category': p.get('category', 'Uncategorized')
        } for p in products]

    def get_stock_levels(self):
        """Get current stock levels"""
        df = pd.DataFrame(self.inventory_data)
        if df.empty:
            return {'names': [], 'stocks': []}
        return {
            'names': df['name'].tolist(),
            'stocks': df['stock'].tolist()
        }

    def get_low_stock_products(self, threshold=5):
        """Get products with low stock"""
        df = pd.DataFrame(self.inventory_data)
        if df.empty:
            return []
        return df[df['stock'] <= threshold].to_dict('records')

    def get_category_value(self):
        """Get inventory value by category"""
        df = pd.DataFrame(self.inventory_data)
        if df.empty:
            return {}
        df['value'] = df['stock'] * df['price']
        return df.groupby('category')['value'].sum().to_dict()
