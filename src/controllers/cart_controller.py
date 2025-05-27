"""
Cart Controller
-------------
Handles shopping cart operations.
"""

from src.models.cart import Cart

class CartController:
    def __init__(self, product_controller):
        self.product_controller = product_controller
        self.cart = Cart()
    
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
    
    def checkout(self):
        """Process the checkout and update inventory"""
        items = self.cart.get_items()
        
        if not items:
            return False, "Cart is empty"
        
        # Update stock for each product
        for item in items:
            product = self.product_controller.find_product_by_id(item.id)
            if product and product["stock"] > 0:
                product["stock"] -= 1
        
        # Save changes to products
        self.product_controller.save_json()
        
        # Clear the cart after successful checkout
        self.cart.clear()
        
        return True, "Order completed successfully"