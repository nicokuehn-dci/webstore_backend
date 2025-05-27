"""
Cart Controller
-------------
Handles shopping cart operations.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.models.cart import Cart

class CartController:
    def __init__(self, product_controller):
        self.product_controller = product_controller
        self.cart = Cart()
        # Add tax rate and discount tiers
        self.tax_rate = 0.19  # 19% tax rate
        self.discount_tiers = [(200, 0.2), (100, 0.1)]  # (threshold, discount_rate)
    
    def add_to_cart(self, product_id):
        """Add a product to the cart"""
        product_data = self.product_controller.find_product_by_id(product_id)
        
        if not product_data:
            return False, "Product not found"
        
        if product_data["stock"] <= 0:
            return False, "Product out of stock"
        
        # Convert JSON product to Product object
        product_obj = self.product_controller.create_product_object(product_data)
        self.cart.add_item(product_obj)
        
        return True, f"{product_data['name']} added to cart"
    
    def remove_from_cart(self, product_id):
        """Remove a product from the cart"""
        initial_count = len(self.cart.items)
        self.cart.remove_item(product_id)
        
        # Check if an item was actually removed
        if len(self.cart.items) < initial_count:
            return True, "Item removed from cart"
        else:
            return False, "Product not found in cart"
    
    def get_cart_items(self):
        """Get all items in the cart"""
        return self.cart.get_items()
    
    def get_cart_total(self):
        """Calculate the total price of items in the cart"""
        total = 0
        for item in self.cart.get_items():
            total += item.price
        return total
    
    def clear_cart(self):
        """Empty the cart"""
        self.cart.clear()
    
    def get_order_summary(self):
        """Calculate detailed order summary including tax and potential discounts"""
        items = self.get_cart_items()
        
        if not items:
            return {
                'subtotal': 0.0,
                'tax': 0.0,
                'total_with_tax': 0.0,
                'discount': 0.0,
                'discount_percentage': "0%",
                'final': 0.0,
                'order_details': []
            }

        order_details = []
        subtotal = 0.0

        for item in items:
            item_price = item.price
            item_total = item_price  # Currently one item per entry
            subtotal += item_total
            order_details.append({
                'name': item.name,
                'price': item_price,
                'quantity': 1,
                'item_total': item_total
            })

        tax = subtotal * self.tax_rate
        total_with_tax = subtotal + tax

        # Calculate discount if applicable
        discount = 0
        discount_percentage = "0%"
        for threshold, rate in self.discount_tiers:
            if total_with_tax >= threshold:
                discount = total_with_tax * rate
                discount_percentage = f"{int(rate * 100)}%"
                break

        final_total = total_with_tax - discount

        return {
            'subtotal': subtotal,
            'tax': tax,
            'total_with_tax': total_with_tax,
            'discount': discount,
            'discount_percentage': discount_percentage,
            'final': final_total,
            'order_details': order_details
        }

    def print_receipt(self):
        """Print a detailed receipt of the current cart"""
        summary = self.get_order_summary()
        print("\n--- Receipt ---")
        
        if not summary['order_details']:
            print("Your cart is empty. No items to display.")
            print("Thank you for shopping!\n")
            return

        for item in summary['order_details']:
            print(f"{item['name']}: {item['price']:.2f} * {item['quantity']} = {item['item_total']:.2f}€")

        print(f"Subtotal: {summary['subtotal']:.2f}€")
        print(f"Tax ({int(self.tax_rate * 100)}%): {summary['tax']:.2f}€")
        print(f"Total with tax: {summary['total_with_tax']:.2f}€")
        
        if summary['discount'] > 0:
            print(f"Discount: {summary['discount']:.2f}€")
            print(f"Discount percentage: {summary['discount_percentage']}")
            
        print(f"Final total: {summary['final']:.2f}€")
        print("Thank you for shopping!\n")

    def checkout(self):
        """Process the checkout and update inventory"""
        items = self.cart.get_items()
        
        if not items:
            return False, "Cart is empty"
        
        # Get order summary before clearing cart
        summary = self.get_order_summary()
        
        # Update stock for each product
        for item in items:
            product = self.product_controller.find_product_by_id(item.id)
            if product and product["stock"] > 0:
                product["stock"] -= 1
        
        # Save changes to products
        self.product_controller.save_json()
        
        # Print receipt
        self.print_receipt()
        
        # Clear the cart after successful checkout
        self.cart.clear()
        
        return True, f"Order completed successfully. Total amount: €{summary['final']:.2f}"
    


