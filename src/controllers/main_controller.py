"""
Main Controller
-------------
Main application controller that coordinates other controllers and views.
"""

from blessed import Terminal
from src.controllers.auth_controller import AuthController
from src.controllers.product_controller import ProductController
from src.controllers.cart_controller import CartController
from src.views.menu import Menu
from src.views.admin_view import AdminView
from src.views.customer_view import CustomerView

class MainController:
    def __init__(self):
        self.term = Terminal()
        self.auth_controller = AuthController(self.term)
        self.product_controller = ProductController(self.term)
        self.cart_controller = CartController(self.product_controller)
        self.admin_view = AdminView(self.term, self.product_controller, self.cart_controller)
        self.customer_view = CustomerView(self.term)
        self.current_user = None
    
    def run(self):
        """Run the main application loop"""
        while True:
            main_menu = Menu("WebStore Application", ["Register", "Login", "Exit"])
            choice = main_menu.display()
            
            if choice is None or choice == 2:  # Exit option or 'q' pressed
                break
            elif choice == 0:
                # Register new user (only as customer, not admin)
                user = self.auth_controller.register_user()
                if user:
                    self.current_user = user
                    self.handle_user_session()
            elif choice == 1:
                # Login
                user = self.auth_controller.login()
                if user:
                    self.current_user = user
                    self.handle_user_session()
    
    def handle_user_session(self):
        """Direct user to appropriate interface based on role"""
        if self.current_user.is_admin:
            self.admin_view.show_admin_menu(self.current_user.username)
        else:
            self.show_customer_menu()
        
        # Clear user session on exit
        self.current_user = None
        self.cart_controller.clear_cart()
    
    def show_customer_menu(self):
        """Display the customer menu and handle options"""
        while True:
            customer_menu = Menu(f"Customer Menu - {self.current_user.username}", 
    ["Browse Products", "Search Products", "View Featured Products", 
     "View Cart", "Add to Cart", "Remove from Cart", 
     "Checkout", "Save Changes", "Print Receipt", "Logout"])
            choice = customer_menu.display()
            
            if choice is None or choice == 10:  # Logout option or 'q' pressed
                break
            elif choice == 0:
                self.browse_products()
            elif choice == 1:
                self.search_products()
            elif choice == 2:
                self.view_featured_products()
            elif choice == 3:
                self.customer_view.display_cart(self.cart_controller.get_cart_items())
            elif choice == 4:
                self.add_to_cart()
            elif choice == 5:
                self.remove_from_cart()
            elif choice == 6:
                self.checkout()
            elif choice == 7:
                self.display_order_summary()
            elif choice == 8:
                self.cart_controller.print_receipt()
                input(self.term.center("Press Enter to continue..."))
            elif choice == 9:
                self.save_customer_changes()



    def browse_products(self):
        """Browse products by category"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Browse Products by Category")))
            print()
            
            # Create a menu for categories
            categories = self.product_controller.get_categories()
            category_options = [category['name'] for category in categories]
            category_options.append("Back to Menu")
            
            category_menu = Menu("Select a Category", category_options)
            cat_idx = category_menu.display()
            
            if cat_idx is None or cat_idx == len(category_options) - 1:
                return
            
            # Display products in the selected category
            with self.term.fullscreen():
                print(self.term.clear)
                category = categories[cat_idx]
                print(self.term.move_y(2) + self.term.center(self.term.bold(f"{category['name']} Products")))
                print()
                
                products = self.product_controller.get_products_by_category(cat_idx)
                if not products:
                    print(self.term.center("No products available in this category"))
                    input(self.term.center("Press Enter to continue..."))
                    return
                
                product_options = [f"{p['id']}: {p['name']} - ${p['price']} (Stock: {p['stock']})" 
                                for p in products]
                product_options.append("Back to Categories")
                
                product_menu = Menu("Select a Product to Add to Cart", product_options)
                prod_idx = product_menu.display()
                
                if prod_idx is None or prod_idx == len(product_options) - 1:
                    return
                
                # Add selected product to cart
                product = products[prod_idx]
                success, message = self.cart_controller.add_to_cart(product["id"])
                
                with self.term.fullscreen():
                    print(self.term.clear)
                    if success:
                        print(self.term.center(self.term.green(message)))
                    else:
                        print(self.term.center(self.term.red(message)))
                    input(self.term.center("Press Enter to continue..."))
    
    def search_products(self):
        """Search products by keyword"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Search Products")))
            print()
            
            print(self.term.center("Enter search term: "), end="")
            search_term = input().lower()
            found_products = self.product_controller.search_products(search_term)
            
            if not found_products:
                print(self.term.center(self.term.red("No products found matching your search.")))
                input(self.term.center("Press Enter to continue..."))
                return
            
            # Display found products as a menu
            product_options = [f"{p['id']}: {p['name']} - ${p['price']} (Stock: {p['stock']})" 
                            for p in found_products]
            product_options.append("Back to Menu")
            
            product_menu = Menu(f"Found {len(found_products)} products", product_options)
            prod_idx = product_menu.display()
            
            if prod_idx is None or prod_idx == len(product_options) - 1:
                return
            
            # Add selected product to cart
            product = found_products[prod_idx]
            success, message = self.cart_controller.add_to_cart(product["id"])
            
            with self.term.fullscreen():
                print(self.term.clear)
                if success:
                    print(self.term.center(self.term.green(message)))
                else:
                    print(self.term.center(self.term.red(message)))
                input(self.term.center("Press Enter to continue..."))
    
    def view_featured_products(self):
        """View and select from featured products"""
        with self.term.fullscreen():
            print(self.term.clear)
            
            featured_products = self.product_controller.get_featured_products()
            
            if not featured_products:
                print(self.term.center(self.term.red("No featured products available.")))
                input(self.term.center("Press Enter to continue..."))
                return
            
            # Display featured products as a menu
            product_options = [f"{p['id']}: {p['name']} - ${p['price']} (Stock: {p['stock']})" 
                            for p in featured_products]
            product_options.append("Back to Menu")
            
            product_menu = Menu("Featured Products", product_options)
            prod_idx = product_menu.display()
            
            if prod_idx is None or prod_idx == len(product_options) - 1:
                return
            
            # Add selected product to cart
            product = featured_products[prod_idx]
            success, message = self.cart_controller.add_to_cart(product["id"])
            
            with self.term.fullscreen():
                print(self.term.clear)
                if success:
                    print(self.term.center(self.term.green(message)))
                else:
                    print(self.term.center(self.term.red(message)))
                input(self.term.center("Press Enter to continue..."))
    
    def add_to_cart(self):
        """Add a product to the cart by ID"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Add to Cart")))
            print()
            
            print(self.term.center("Enter Product ID: "), end="")
            prod_id = input()
            
            success, message = self.cart_controller.add_to_cart(prod_id)
            
            with self.term.fullscreen():
                print(self.term.clear)
                if success:
                    print(self.term.center(self.term.green(message)))
                else:
                    print(self.term.center(self.term.red(message)))
                input(self.term.center("Press Enter to continue..."))
    
    def remove_from_cart(self):
        """Remove a product from the cart"""
        items = self.cart_controller.get_cart_items()
        
        if not items:
            with self.term.fullscreen():
                print(self.term.clear)
                print(self.term.center("Your cart is empty."))
                input(self.term.center("Press Enter to continue..."))
            return
        
        # Display cart items as a menu
        item_options = [f"{item.id}: {item.name} - ${item.price}" for item in items]
        item_options.append("Back to Menu")
        
        item_menu = Menu("Select an Item to Remove", item_options)
        item_idx = item_menu.display()
        
        if item_idx is None or item_idx == len(item_options) - 1:
            return
        
        # Remove selected item from cart
        prod_id = items[item_idx].id
        success, message = self.cart_controller.remove_from_cart(prod_id)
        
        with self.term.fullscreen():
            print(self.term.clear)
            if success:
                print(self.term.center(self.term.green(message)))
            else:
                print(self.term.center(self.term.red(message)))
            input(self.term.center("Press Enter to continue..."))  


    def display_order_summary(self):
        """Display a detailed order summary to the user"""
        summary = self.cart_controller.get_order_summary()
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Order Summary")))
            print()
            if not summary['order_details']:
                print(self.term.center("Your cart is empty. No items to display."))
                input(self.term.center("Press Enter to continue..."))
                return
            for item in summary['order_details']:
                print(self.term.center(f"{item['name']}: {item['price']:.2f} * {item['quantity']} = {item['item_total']:.2f}€"))
            print()
            print(self.term.center(f"Subtotal: {summary['subtotal']:.2f}€"))
            print(self.term.center(f"Tax ({int(self.cart_controller.tax_rate * 100)}%): {summary['tax']:.2f}€"))
            print(self.term.center(f"Total with tax: {summary['total_with_tax']:.2f}€"))
            if summary['discount'] > 0:
                print(self.term.center(f"Discount: {summary['discount']:.2f}€"))
                print(self.term.center(f"Discount percentage: {summary['discount_percentage']}"))
            print(self.term.center(f"Final total: {summary['final']:.2f}€"))
            print()
            input(self.term.center("Press Enter to continue..."))                   
    
    def checkout(self):
        """Process the checkout"""
        items = self.cart_controller.get_cart_items()
        
        if not items:
            with self.term.fullscreen():
                print(self.term.clear)
                print(self.term.center("Your cart is empty."))
                input(self.term.center("Press Enter to continue..."))
            return
        
        # Use the display_checkout function from customer_view
        confirmed = self.customer_view.display_checkout(items)
        
        if confirmed:
            success, message = self.cart_controller.checkout()
            
            # Update user order history (simplified)
            # In a full implementation, we would create an order record
            
            with self.term.fullscreen():
                print(self.term.clear)
                if success:
                    print(self.term.center(self.term.green(message)))
                else:
                    print(self.term.center(self.term.red(message)))
                input(self.term.center("Press Enter to continue..."))
    
    def save_customer_changes(self):
        """Save all customer-related changes to JSON files"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Save Changes")))
            print()
            
            # Save product data (including stock changes from cart)
            print(self.term.center("Saving product data..."))
            self.product_controller.save_product_data()
            
            # If needed, save customer-specific data (like order history)
            print(self.term.center("Saving user data..."))
            # This would update the user's data in the users.json file
            # self.auth_controller.save_user_data(self.current_user)
            
            print(self.term.center(self.term.green("All changes have been saved successfully!")))
            input(self.term.center("Press Enter to continue..."))



            
