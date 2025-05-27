"""
Customer View
-----------
Functions to handle customer interface display components.
"""

from blessed import Terminal
from src.views.menu import Menu

class CustomerView:
    def __init__(self, term):
        self.term = term
    
    def display_cart(self, items):
        """Display the contents of a user's cart"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Your Cart")))
            print()
            
            if not items:
                print(self.term.center("Your cart is empty."))
                input(self.term.center("Press Enter to continue..."))
                return
            
            total = 0
            for item in items:
                print(self.term.center(f"{item.id}: {item.name} - ${item.price}"))
                total += item.price
            
            print(self.term.center(self.term.bold(f"\nTotal: ${total:.2f}")))
            input(self.term.center("Press Enter to continue..."))

    def display_checkout(self, items):
        """Display checkout screen and process order"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Checkout")))
            print()
            
            total = 0
            for item in items:
                print(self.term.center(f"{item.id}: {item.name} - ${item.price}"))
                total += item.price
            
            print(self.term.center(self.term.bold(f"\nTotal: ${total:.2f}")))
            print()
            
            print(self.term.center("Proceed with checkout? (y/n): "), end="")
            confirm = input()
            
            if confirm.lower() != "y":
                return False
            
            # In a real app, we would process payment here
            print(self.term.center("\nProcessing your order..."))
            
            print(self.term.center(self.term.green("Order completed! Thank you for your purchase.")))
            input(self.term.center("Press Enter to continue..."))
            return True

    def browse_products_by_category(self, categories, handle_product_selection):
        """Browse products with persistent category view"""
        while True:
            # Create a menu for categories
            category_options = [category['name'] for category in categories]
            category_options.append("Back to Main Menu")
            
            category_menu = Menu("Select a Category", category_options)
            cat_idx = category_menu.display()
            
            if cat_idx is None or cat_idx == len(category_options) - 1:
                return
            
            # Display products in the selected category
            category = categories[cat_idx]
            self.display_category_products(category, handle_product_selection)
    
    def display_category_products(self, category, handle_product_selection):
        """Display products in a category with return-to-category behavior"""
        while True:
            with self.term.fullscreen():
                print(self.term.clear)
                print(self.term.move_y(2) + self.term.center(self.term.bold(f"{category['name']} Products")))
                print()
                
                if not category["products"]:
                    print(self.term.center("No products available in this category"))
                    input(self.term.center("Press Enter to continue..."))
                    return
                
                product_options = [f"{p['id']}: {p['name']} - ${p['price']} (Stock: {p['stock']})" 
                                for p in category["products"]]
                product_options.append("Back to Categories")
                
                product_menu = Menu(f"{category['name']} Products", product_options)
                prod_idx = product_menu.display()
                
                if prod_idx is None or prod_idx == len(product_options) - 1:
                    return
                
                # Handle product selection (add to cart, update, delete, etc.)
                product = category["products"][prod_idx]
                action_result = handle_product_selection(product)
                
                # Stay in the same category view after operation
                if action_result:
                    with self.term.fullscreen():
                        print(self.term.clear)
                        print(self.term.move_y(2) + self.term.center(self.term.green(action_result)))
                        input(self.term.center("Press Enter to continue..."))
    
    def display_search_results(self, products, handle_product_selection, search_term):
        """Display search results with return-to-results behavior"""
        if not products:
            with self.term.fullscreen():
                print(self.term.clear)
                print(self.term.center(self.term.red(f"No products found matching '{search_term}'.")))
                input(self.term.center("Press Enter to continue..."))
            return
        
        while True:
            product_options = [f"{p['id']}: {p['name']} - ${p['price']} (Stock: {p['stock']})" 
                            for p in products]
            product_options.append("Back to Search")
            
            product_menu = Menu(f"Search Results for '{search_term}'", product_options)
            prod_idx = product_menu.display()
            
            if prod_idx is None or prod_idx == len(product_options) - 1:
                return
            
            # Handle product selection
            product = products[prod_idx]
            action_result = handle_product_selection(product)
            
            # Stay in search results after operation
            if action_result:
                with self.term.fullscreen():
                    print(self.term.clear)
                    print(self.term.move_y(2) + self.term.center(self.term.green(action_result)))
                    input(self.term.center("Press Enter to continue..."))

# For backward compatibility
def display_cart(term, items):
    view = CustomerView(term)
    return view.display_cart(items)

def display_checkout(term, items):
    view = CustomerView(term)
    return view.display_checkout(items)
