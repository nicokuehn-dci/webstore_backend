"""
Analytics Controller
------------------
Handles analytics and reporting functionality.
"""

import plotext as plt
from datetime import datetime, timedelta

from src.models.analytics import SalesAnalytics, InventoryAnalytics
from src.utils.chart_helper import setup_modern_chart, create_bar_chart, create_line_chart

class AnalyticsController:
    def __init__(self, product_controller, cart_controller):
        self.product_controller = product_controller
        self.cart_controller = cart_controller
        self.sales_analytics = SalesAnalytics()
        self.inventory_analytics = InventoryAnalytics()
        self._initialize_data()

    def _initialize_data(self):
        """Initialize analytics with existing data"""
        # Update inventory analytics
        self.update_inventory_data()
        
        # Initialize with example sales data (simulated)
        example_sales = [
            {
                'date': datetime.now().isoformat(),
                'product_id': 'p1',
                'quantity': 5,
                'price': 49.99,
                'category': 'Electronics'
            },
            {
                'date': (datetime.now() - timedelta(days=1)).isoformat(),
                'product_id': 'p2',
                'quantity': 2,
                'price': 29.99,
                'category': 'Clothing'
            },
            {
                'date': (datetime.now() - timedelta(days=2)).isoformat(),
                'product_id': 'p3',
                'quantity': 3,
                'price': 39.99,
                'category': 'Books'
            },
            {
                'date': (datetime.now() - timedelta(days=3)).isoformat(),
                'product_id': 'p4',
                'quantity': 1,
                'price': 99.99,
                'category': 'Home'
            },
            {
                'date': (datetime.now() - timedelta(days=4)).isoformat(),
                'product_id': 'p5',
                'quantity': 4,
                'price': 19.99,
                'category': 'Electronics'
            },
            {
                'date': (datetime.now() - timedelta(days=5)).isoformat(),
                'product_id': 'p1',
                'quantity': 2,
                'price': 49.99,
                'category': 'Electronics'
            },
            {
                'date': (datetime.now() - timedelta(days=6)).isoformat(),
                'product_id': 'p2',
                'quantity': 3,
                'price': 29.99,
                'category': 'Clothing'
            }
        ]
        
        # Add example sales data
        for sale in example_sales:
            self.sales_analytics.add_sale(sale)

    def update_inventory_data(self):
        """Update inventory analytics with current product data"""
        self.inventory_analytics.update_inventory(self.product_controller.get_all_products())

    def show_product_stats(self, term):
        """Display product statistics visualization"""
        stock_data = self.inventory_analytics.get_stock_levels()
        
        # Clear terminal and show title
        print(term.clear)
        print(term.move_y(2) + term.center(term.bold_white_on_black("📊 Product Stock Levels")))
        
        # Create bar chart with modern styling
        chart = create_bar_chart(
            term=term,
            title="Current Stock Levels",
            x_data=stock_data['names'],
            y_data=stock_data['stocks'],
            x_label="Products",
            y_label="Stock",
            color="orange"
        )
        chart.show()
        
        # Show low stock warnings
        low_stock = self.inventory_analytics.get_low_stock_products()
        if low_stock:
            print("\n" + term.center(term.red("⚠️ Low Stock Warnings:")))
            for product in low_stock:
                print(term.center(f"{product['name']}: {product['stock']} units remaining"))

    def show_sales_trend(self, term):
        """Display sales trend visualization"""
        sales_data = self.sales_analytics.get_daily_sales()
        
        print(term.clear)
        print(term.move_y(2) + term.center(term.bold_white_on_black("📈 Sales Trend (Last 7 Days)")))
        
        # Create line chart with modern styling
        chart = create_line_chart(
            term=term,
            title="Daily Sales Revenue",
            x_data=sales_data['dates'],
            y_data=sales_data['sales'],
            x_label="Date",
            y_label="Revenue ($)",
            color="green"
        )
        chart.show()
        
        # Show top selling products
        top_products = self.sales_analytics.get_top_products()
        if top_products:
            print("\n" + term.center(term.orange("🏆 Top Selling Products:")))
            for prod_id, quantity in top_products.items():
                product = self.product_controller.get_product_by_id(prod_id)
                if product:
                    print(term.center(f"{product.name}: {quantity} units sold"))

    def show_category_distribution(self, term):
        """Display category distribution visualization"""
        category_value = self.inventory_analytics.get_category_value()
        
        print(term.clear)
        print(term.move_y(2) + term.center(term.bold_white_on_black("🏪 Inventory Value by Category")))
        
        if category_value:
            # Create bar chart with modern styling
            chart = create_bar_chart(
                term=term,
                title="Category Distribution (by value)",
                x_data=list(category_value.keys()),
                y_data=list(category_value.values()),
                x_label="Category",
                y_label="Value ($)",
                color="cyan"
            )
            chart.show()
            
            # Show additional category details
            print("\n" + term.center(term.cyan("📊 Category Details:")))
            total = sum(category_value.values())
            for cat, value in category_value.items():
                percentage = (value / total) * 100 if total > 0 else 0
                print(term.center(f"{cat}: ${value:.2f} ({percentage:.1f}% of total)"))
        else:
            print(term.center("No category data available"))

    def get_analytics_summary(self):
        """Get a summary of key analytics metrics"""
        total_products = len(self.product_controller.get_all_products())
        low_stock = len(self.inventory_analytics.get_low_stock_products())
        sales_data = self.sales_analytics.get_daily_sales()
        total_sales = sum(sales_data['sales'])
        
        return {
            'total_products': total_products,
            'low_stock_count': low_stock,
            'total_sales_7d': total_sales,
            'categories': len(self.inventory_analytics.get_category_value())
        }
