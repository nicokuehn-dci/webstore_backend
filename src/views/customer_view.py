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

# For backward compatibility
def display_cart(term, items):
    view = CustomerView(term)
    return view.display_cart(items)

def display_checkout(term, items):
    view = CustomerView(term)
    return view.display_checkout(items)
