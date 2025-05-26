#!/usr/bin/env python3
# filepath: /home/nico-kuehn-dci/Desktop/webstore-app/menu_cli.py
"""
WebStore App - Interactive CLI Menu System
-----------------------------------------
A command-line interface for managing products and users in a web store.
Features an interactive menu system with arrow key navigation and colored UI.

Usage:
    ./menu_cli.py

Author: Nico Kuehn
Date: May 26, 2025
"""

import json
import os
import sys
import subprocess

# Check Python version
if sys.version_info < (3, 6):
    print("This script requires Python 3.6 or higher.")
    sys.exit(1)

# Check for requirements.txt and .gitignore
current_dir = os.path.dirname(os.path.abspath(__file__))
requirements_file = os.path.join(current_dir, 'requirements.txt')
gitignore_file = os.path.join(current_dir, '.gitignore')

if not os.path.exists(requirements_file):
    print("requirements.txt not found. Creating it...")
    with open(requirements_file, 'w') as f:
        f.write("blessed==1.21.0\nwcwidth==0.2.13\n")
    print("requirements.txt created successfully.")

if not os.path.exists(gitignore_file):
    print(".gitignore not found. Creating it...")
    with open(gitignore_file, 'w') as f:
        f.write("""# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
venv/
.venv/
env/
ENV/
.env

# IDE specific files
.idea/
.vscode/
*.swp

# OS specific files
.DS_Store
Thumbs.db

# Application specific
*.log
*.sqlite3
""")
    print(".gitignore created successfully.")

# Setup virtual environment if needed
venv_dir = os.path.join(current_dir, 'venv')  # Using 'venv' folder (not '.venv')
venv_bin = os.path.join(venv_dir, 'bin')
venv_python = os.path.join(venv_bin, 'python')

# Check if .venv directory was attempted (for backward compatibility)
alt_venv_dir = os.path.join(current_dir, '.venv')
if os.path.exists(alt_venv_dir) and not os.path.exists(venv_dir):
    print("Found '.venv' directory instead of 'venv'. Using the existing environment.")
    venv_dir = alt_venv_dir
    venv_bin = os.path.join(venv_dir, 'bin')
    venv_python = os.path.join(venv_bin, 'python')

if not os.path.exists(venv_dir):
    print("Creating virtual environment...")
    subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])

# Install requirements from requirements.txt
if os.path.exists(requirements_file):
    print("Installing requirements from requirements.txt...")
    try:
        subprocess.check_call([os.path.join(venv_bin, 'pip'), 'install', '-r', requirements_file])
    except Exception as e:
        print(f"Warning: Failed to install requirements: {e}")
        print("Continuing with available packages...")

# Restart script with venv Python if we're not already using it
# Add a guard to prevent endless loops
if sys.executable != venv_python and not os.environ.get('VENV_PYTHON_RUNNING'):
    os.environ['VENV_PYTHON_RUNNING'] = '1'
    try:
        # Check if the venv Python exists before trying to use it
        if os.path.exists(venv_python):
            os.execv(venv_python, [venv_python] + sys.argv)
        else:
            print(f"Warning: Virtual environment Python not found at {venv_python}")
            print("Continuing with system Python...")
    except FileNotFoundError:
        print(f"Warning: Could not find Python in virtual environment at {venv_python}")
        print("Continuing with system Python...")

from blessed import Terminal

# Define version and handle command-line arguments
VERSION = "1.0.0"

def parse_args():
    """Parse command line arguments."""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print(f"""
WebStore App - Interactive CLI Menu System v{VERSION}
Usage:
  {sys.argv[0]} [options]

Options:
  -h, --help     Show this help message and exit
  -v, --version  Show version and exit
  --init         Initialize repository with requirements.txt and .gitignore

Example:
  {sys.argv[0]}              Start the application
  {sys.argv[0]} --init       Initialize repository files
""")
            sys.exit(0)
        elif sys.argv[1] in ['-v', '--version']:
            print(f"WebStore App v{VERSION}")
            sys.exit(0)
        elif sys.argv[1] == '--init':
            print("Repository files already initialized.")
            sys.exit(0)
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print(f"Use '{sys.argv[0]} --help' for usage information.")
            sys.exit(1)

# Parse command-line arguments
parse_args()

class Product:
    def __init__(self, id, name, price, description=None, stock=0, image_url=None, specifications=None, ratings=None, tags=None):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock
        self.image_url = image_url
        self.specifications = specifications or {}
        self.ratings = ratings or {"average": 0, "count": 0}
        self.tags = tags or []

class User:
    def __init__(self, id, username, password, email=None, is_admin=False):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin

class Cart:
    def __init__(self):
        self.items = []
        
    def add_item(self, product):
        self.items.append(product)
        
    def remove_item(self, product_id):
        self.items = [item for item in self.items if item.id != product_id]
        
    def get_items(self):
        return self.items
        
    def clear(self):
        self.items = []

class Menu:
    def __init__(self, title, options):
        self.term = Terminal()
        self.title = title
        self.options = options
        self.current_option = 0
    
    def display(self):
        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
            while True:
                print(self.term.clear)
                print(self.term.move_y(2) + self.term.center(self.term.bold(self.title)))
                print()
                
                for i, option in enumerate(self.options):
                    if i == self.current_option:
                        # Orange background with black text
                        print(self.term.center(self.term.black_on_orange(f" {option} ")))
                    else:
                        print(self.term.center(f" {option} "))
                
                print()
                print(self.term.center("(Use arrow keys to navigate, Enter to select, q to quit)"))
                
                key = self.term.inkey()
                if key.name == 'KEY_UP':
                    self.current_option = (self.current_option - 1) % len(self.options)
                elif key.name == 'KEY_DOWN':
                    self.current_option = (self.current_option + 1) % len(self.options)
                elif key.name == 'KEY_ENTER':
                    return self.current_option
                elif key.lower() == 'q':
                    return None

class CLIController:
    def __init__(self):
        self.term = Terminal()
        self.users_file = os.path.join(os.path.dirname(__file__), 'users.json')
        self.products_file = os.path.join(os.path.dirname(__file__), 'products.json')
        self.users_data = self.load_json(self.users_file)
        self.products_data = self.load_json(self.products_file)
        self.current_user = None

    def load_json(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            if file_path == self.users_file:
                return {"users": [], "admins": []}
            elif file_path == self.products_file:
                return {"categories": [], "featured_products": [], "new_arrivals": [], "best_sellers": [], "on_sale": []}
            return {}
    
    def save_json(self, file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
    
    def run(self):
        while True:
            main_menu = Menu("WebStore Application", ["Register", "Login", "Exit"])
            choice = main_menu.display()
            
            if choice is None or choice == 2:  # Exit option or 'q' pressed
                break
            elif choice == 0:
                self.handle_register()
            elif choice == 1:
                self.handle_login()

    def handle_register(self):
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Register New User")))
            print()
            
            print(self.term.center("Username: "), end="")
            username = input()
            
            print(self.term.center("Password: "), end="")
            password = input()  # In a real app, use getpass to hide input
            
            print(self.term.center("Email: "), end="")
            email = input()
            
            print(self.term.center("Admin? (y/n): "), end="")
            role = input()
            is_admin = (role.lower() == "y")
            
            # Check if username already exists
            for user in self.users_data["users"]:
                if user["username"] == username:
                    print(self.term.center(self.term.red("Username already exists. Please choose another.")))
                    input(self.term.center("Press Enter to continue..."))
                    return
                    
            for admin in self.users_data["admins"]:
                if admin["username"] == username:
                    print(self.term.center(self.term.red("Username already exists. Please choose another.")))
                    input(self.term.center("Press Enter to continue..."))
                    return
            
            # Create new user
            user_id = f"user{len(self.users_data['users']) + 1}" if not is_admin else f"admin{len(self.users_data['admins']) + 1}"
            
            new_user = {
                "id": user_id,
                "username": username,
                "password": password,  # In a real app, this would be hashed
                "email": email,
                "is_admin": is_admin,
                "created_at": "2025-05-26T00:00:00Z",  # Current date (hardcoded for simplicity)
                "last_login": None
            }
            
            if is_admin:
                new_user["permissions"] = ["manage_products", "view_reports"]
                self.users_data["admins"].append(new_user)
            else:
                new_user["shipping_address"] = {}
                new_user["order_history"] = []
                self.users_data["users"].append(new_user)
            
            self.save_json(self.users_file, self.users_data)
            print(self.term.center(self.term.green(f"User {username} registered successfully!")))
            input(self.term.center("Press Enter to continue..."))

    def handle_login(self):
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Login")))
            print()
            
            print(self.term.center("Username: "), end="")
            username = input()
            
            print(self.term.center("Password: "), end="")
            password = input()  # In a real app, use getpass
            
            # Check regular users
            for user in self.users_data["users"]:
                if user["username"] == username and user["password"] == password:
                    self.current_user = User(user["id"], user["username"], user["password"], 
                                             user.get("email"), False)
                    user["last_login"] = "2025-05-26T00:00:00Z"  # Update last login
                    self.save_json(self.users_file, self.users_data)
                    print(self.term.center(self.term.green(f"Welcome, {username}!")))
                    input(self.term.center("Press Enter to continue..."))
                    self.customer_menu()
                    return
            
            # Check admin users
            for admin in self.users_data["admins"]:
                if admin["username"] == username and admin["password"] == password:
                    self.current_user = User(admin["id"], admin["username"], admin["password"], 
                                             admin.get("email"), True)
                    admin["last_login"] = "2025-05-26T00:00:00Z"  # Update last login
                    self.save_json(self.users_file, self.users_data)
                    print(self.term.center(self.term.green(f"Welcome, Admin {username}!")))
                    input(self.term.center("Press Enter to continue..."))
                    self.admin_menu()
                    return
            
            print(self.term.center(self.term.red("Invalid credentials.")))
            input(self.term.center("Press Enter to continue..."))

    def admin_menu(self):
        # Show quick help on first login
        self.show_admin_help()
        
        while True:
            admin_menu = Menu(f"Admin Menu - {self.current_user.username}", 
                            ["Add Product", "Delete Product", "List Products by Category", 
                             "Update Product", "Help", "Logout"])
            choice = admin_menu.display()
            
            if choice is None or choice == 5:  # Logout option or 'q' pressed
                self.current_user = None
                break
            elif choice == 0:
                self.add_product()
            elif choice == 1:
                self.delete_product()
            elif choice == 2:
                self.list_products_by_category()
            elif choice == 3:
                self.update_product()
            elif choice == 4:
                self.show_admin_help()
    
    def show_admin_help(self):
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Admin Help - Product Management Guide")))
            print()
            
            print(self.term.center("Here's a quick guide to managing products:"))
            print()
            
            # Add Product help
            print(self.term.bold(self.term.center("1. Adding a Product:")))
            print(self.term.center("- Product ID should be unique (e.g., 'e006' for Electronics)"))
            print(self.term.center("- Categories have specific prefixes: e=Electronics, c=Clothing, h=Home, b=Books"))
            print(self.term.center("- Example: When adding a new camera, use ID 'e006', price '499.99', stock '25'"))
            print()
            
            # Delete Product help
            print(self.term.bold(self.term.center("2. Deleting a Product:")))
            print(self.term.center("- Select a product from the list using arrow keys"))
            print(self.term.center("- Confirm deletion when prompted"))
            print(self.term.center("- Deleted products are also removed from featured lists"))
            print()
            
            # Update Product help
            print(self.term.bold(self.term.center("3. Updating a Product:")))
            print(self.term.center("- Select which field to update (Name, Price, Stock, etc.)"))
            print(self.term.center("- For tags, use comma-separated values (e.g., 'sale, premium, new')"))
            print()
            
            print(self.term.center("Press Enter to continue..."))
            input()
    
    def add_product(self):
        # First collect basic product information
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Add New Product")))
            print()
            
            # Show quick help
            print(self.term.center(self.term.yellow("Quick Tip: Use category-specific prefixes for product IDs:")))
            print(self.term.center(self.term.yellow("'e' for Electronics, 'c' for Clothing, 'h' for Home, 'b' for Books")))
            print()
            
            print(self.term.center("Product ID (e.g., e006, c006, h006, b004): "), end="")
            prod_id = input()
            
            # Check if ID already exists
            if self.find_product_by_id(prod_id):
                print(self.term.center(self.term.red(f"Error: Product ID '{prod_id}' already exists.")))
                input(self.term.center("Press Enter to continue..."))
                return
            
            print(self.term.center("Product Name: "), end="")
            name = input()
            
            print(self.term.center("Description: "), end="")
            description = input()
            
            print(self.term.center("Price (e.g., 49.99): "), end="")
            try:
                price = float(input())
            except ValueError:
                print(self.term.center(self.term.red("Invalid price. Please enter a number.")))
                input(self.term.center("Press Enter to continue..."))
                return
            
            print(self.term.center("Stock quantity: "), end="")
            try:
                stock = int(input())
            except ValueError:
                print(self.term.center(self.term.red("Invalid stock. Please enter a number.")))
                input(self.term.center("Press Enter to continue..."))
                return
        
        # Select category using Menu
        category_options = [category['name'] for category in self.products_data["categories"]]
        category_options.append("Back to Admin Menu")
        
        category_menu = Menu("Select a Category for the Product", category_options)
        cat_choice = category_menu.display()
        
        if cat_choice is None or cat_choice == len(category_options) - 1:  # Back option or 'q' pressed
            return
        
        # Create new product
        new_product = {
            "id": prod_id,
            "name": name,
            "description": description,
            "price": price,
            "stock": stock,
            "image_url": f"{name.lower().replace(' ', '_')}.jpg",
            "specifications": {},
            "ratings": {"average": 0, "count": 0},
            "tags": []
        }
        
        # Add specifications
        spec_options = ["Add a specification", "Finish adding specifications"]
        while True:
            spec_menu = Menu("Add Product Specifications", spec_options)
            spec_choice = spec_menu.display()
            
            if spec_choice is None or spec_choice == 1:  # Finish option or 'q' pressed
                break
                
            # Add a specification
            with self.term.fullscreen():
                print(self.term.clear)
                print(self.term.move_y(2) + self.term.center(self.term.bold("Add Specification")))
                print()
                
                print(self.term.center("Specification name: "), end="")
                spec_key = input()
                
                print(self.term.center(f"Value for {spec_key}: "), end="")
                spec_value = input()
                
                new_product["specifications"][spec_key] = spec_value
        
        # Add tags
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Add Product Tags")))
            print()
            
            print(self.term.center("Enter tags (comma-separated): "), end="")
            tags = input()
            if tags:
                new_product["tags"] = [tag.strip() for tag in tags.split(",")]
        
        # Add to category
        self.products_data["categories"][cat_choice]["products"].append(new_product)
        self.save_json(self.products_file, self.products_data)
        
        # Show success message
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.center(self.term.green(f"Product '{name}' added successfully!")))
            input(self.term.center("Press Enter to continue..."))
    
    def delete_product(self):
        # Get all products from all categories
        all_products = []
        for category in self.products_data["categories"]:
            for product in category["products"]:
                all_products.append({
                    "id": product["id"],
                    "name": product["name"],
                    "category": category["name"],
                    "price": product["price"],
                    "stock": product["stock"]
                })
        
        if not all_products:
            with self.term.fullscreen():
                print(self.term.clear)
                print(self.term.center(self.term.red("No products available to delete.")))
                input(self.term.center("Press Enter to continue..."))
            return
        
        # Create menu options for product deletion
        product_options = [f"{p['id']}: {p['name']} - ${p['price']} (Stock: {p['stock']}, Category: {p['category']})" 
                          for p in all_products]
        product_options.append("Back to Admin Menu")
        
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Delete Product")))
            print()
            
            # Show quick help
            print(self.term.center(self.term.yellow("Instructions:")))
            print(self.term.center(self.term.yellow("1. Use arrow keys to select a product")))
            print(self.term.center(self.term.yellow("2. Press Enter to select")))
            print(self.term.center(self.term.yellow("3. Confirm deletion on the next screen")))
            print()
        
        delete_menu = Menu("Select a Product to Delete", product_options)
        prod_idx = delete_menu.display()
        
        if prod_idx is None or prod_idx == len(product_options) - 1:  # Back option or 'q' pressed
            return
        
        # Get selected product ID
        selected_product = all_products[prod_idx]
        prod_id = selected_product["id"]
        
        # Confirm deletion
        confirm_options = ["Yes, delete this product", "No, cancel deletion"]
        confirm_menu = Menu(f"Confirm deletion of '{selected_product['name']}'?", confirm_options)
        confirm_choice = confirm_menu.display()
        
        if confirm_choice is None or confirm_choice == 1:  # Cancel option or 'q' pressed
            return
            
        # Delete the product if confirmed
        deleted = False
        for category in self.products_data["categories"]:
            for i, product in enumerate(category["products"]):
                if product["id"] == prod_id:
                    deleted_product = category["products"].pop(i)
                    deleted = True
                    break
            if deleted:
                break
        
        if deleted:
            # Also remove from featured lists
            for list_name in ["featured_products", "new_arrivals", "best_sellers", "on_sale"]:
                if prod_id in self.products_data[list_name]:
                    self.products_data[list_name].remove(prod_id)
            
            self.save_json(self.products_file, self.products_data)
            
            # Show success message
            with self.term.fullscreen():
                print(self.term.clear)
                print(self.term.center(self.term.green(f"Product '{selected_product['name']}' has been deleted successfully!")))
                input(self.term.center("Press Enter to continue..."))
    
    def list_products_by_category(self):
        # Create a menu for category selection
        category_options = [f"{category['name']} ({len(category['products'])} products)" for category in self.products_data["categories"]]
        category_options.append("All Categories")
        category_options.append("Back to Admin Menu")
        
        category_menu = Menu("Product Categories", category_options)
        cat_choice = category_menu.display()
        
        if cat_choice is None or cat_choice == len(category_options) - 1:  # Back option or 'q' pressed
            return
            
        # Display products in the selected category or all categories
        with self.term.fullscreen():
            print(self.term.clear)
            
            if cat_choice == len(category_options) - 2:  # All Categories option
                # Display all products by category
                product_list = []
                for category in self.products_data["categories"]:
                    product_list.append(f"--- {category['name']} ---")
                    for product in category["products"]:
                        product_list.append(f"{product['id']}: {product['name']} - ${product['price']} (Stock: {product['stock']})")
                    product_list.append("")  # Add empty line between categories
                
                product_list.append("Back to Categories")
                product_menu = Menu("All Products", product_list)
                product_menu.display()  # Just display the menu and return on any selection
            else:
                # Display products for a specific category
                category = self.products_data["categories"][cat_choice]
                
                if not category["products"]:
                    print(self.term.center(self.term.red("No products available in this category")))
                    input(self.term.center("Press Enter to continue..."))
                    return
                
                product_options = [f"{p['id']}: {p['name']} - ${p['price']} (Stock: {p['stock']})" 
                                for p in category["products"]]
                product_options.append("Back to Categories")
                
                product_menu = Menu(f"{category['name']} Products", product_options)
                product_menu.display()  # Just display the menu and return on any selection
    
    def update_product(self):
        # Get all products from all categories
        all_products = []
        for category in self.products_data["categories"]:
            for product in category["products"]:
                all_products.append({
                    "id": product["id"],
                    "name": product["name"],
                    "category_name": category["name"],
                    "category_index": self.products_data["categories"].index(category),
                    "product_index": category["products"].index(product),
                    "price": product["price"],
                    "stock": product["stock"]
                })
        
        if not all_products:
            with self.term.fullscreen():
                print(self.term.clear)
                print(self.term.center(self.term.red("No products available to update.")))
                input(self.term.center("Press Enter to continue..."))
            return
        
        # Create menu options for product selection
        product_options = [f"{p['id']}: {p['name']} - ${p['price']} (Stock: {p['stock']}, Category: {p['category_name']})" 
                          for p in all_products]
        product_options.append("Back to Admin Menu")
        
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Update Product")))
            print()
            
            # Show quick help
            print(self.term.center(self.term.yellow("Instructions:")))
            print(self.term.center(self.term.yellow("1. Select a product to update")))
            print(self.term.center(self.term.yellow("2. Choose which field to update (name, price, etc.)")))
            print(self.term.center(self.term.yellow("3. Enter the new value")))
            print()
            print(self.term.center(self.term.yellow("Example updates:")))
            print(self.term.center(self.term.yellow("- Price: 59.99 (numbers only)")))
            print(self.term.center(self.term.yellow("- Tags: premium, sale, new (comma-separated)")))
            print()
        
        update_menu = Menu("Select a Product to Update", product_options)
        prod_idx = update_menu.display()
        
        if prod_idx is None or prod_idx == len(product_options) - 1:  # Back option or 'q' pressed
            return
        
        # Get selected product information
        selected_product = all_products[prod_idx]
        category_index = selected_product["category_index"]
        product_index = selected_product["product_index"]
        product = self.products_data["categories"][category_index]["products"][product_index]
        
        # Menu for selecting what to update
        update_options = [
            "Name", 
            "Description", 
            "Price", 
            "Stock", 
            "Tags", 
            "Back to Product Selection"
        ]
        
        update_field_menu = Menu(f"Update Product: {product['name']}", update_options)
        update_choice = update_field_menu.display()
        
        if update_choice is None or update_choice == 5:  # Back option or 'q' pressed
            return
        
        # Update the selected field
        with self.term.fullscreen():
            print(self.term.clear)
            field_name = update_options[update_choice]
            print(self.term.move_y(2) + self.term.center(self.term.bold(f"Update {field_name}")))
            print()
            
            if update_choice == 0:  # Name
                print(self.term.center(f"Current name: {product['name']}"))
                print(self.term.center("New name: "), end="")
                new_name = input()
                product["name"] = new_name
            elif update_choice == 1:  # Description
                print(self.term.center(f"Current description: {product['description']}"))
                print(self.term.center("New description: "), end="")
                new_desc = input()
                product["description"] = new_desc
            elif update_choice == 2:  # Price
                print(self.term.center(f"Current price: ${product['price']}"))
                print(self.term.center("New price (e.g., 59.99): "), end="")
                try:
                    new_price = float(input())
                    product["price"] = new_price
                except ValueError:
                    print(self.term.center(self.term.red("Invalid price. No changes made.")))
                    input(self.term.center("Press Enter to continue..."))
                    return
            elif update_choice == 3:  # Stock
                print(self.term.center(f"Current stock: {product['stock']}"))
                print(self.term.center("New stock quantity: "), end="")
                try:
                    new_stock = int(input())
                    product["stock"] = new_stock
                except ValueError:
                    print(self.term.center(self.term.red("Invalid stock. No changes made.")))
                    input(self.term.center("Press Enter to continue..."))
                    return
            elif update_choice == 4:  # Tags
                print(self.term.center(f"Current tags: {', '.join(product['tags'])}"))
                print(self.term.center("New tags (comma-separated, e.g., premium, sale, new): "), end="")
                new_tags = input()
                product["tags"] = [tag.strip() for tag in new_tags.split(",")]
        
        # Save changes
        self.save_json(self.products_file, self.products_data)
        
        # Show success message
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.center(self.term.green(f"Product updated successfully!")))
            print(self.term.center(self.term.green(f"Field '{field_name}' has been updated.")))
            input(self.term.center("Press Enter to continue..."))

    def customer_menu(self):
        cart = Cart()
        
        while True:
            customer_menu = Menu(f"Customer Menu - {self.current_user.username}", 
                               ["Browse Products", "Search Products", "View Featured Products", 
                                "View Cart", "Add to Cart", "Remove from Cart", 
                                "Checkout", "Logout"])
            choice = customer_menu.display()
            
            if choice is None or choice == 7:  # Logout option or 'q' pressed
                self.current_user = None
                break
            elif choice == 0:
                self.browse_products(cart)
            elif choice == 1:
                self.search_products(cart)
            elif choice == 2:
                self.view_featured_products(cart)
            elif choice == 3:
                self.view_cart(cart)
            elif choice == 4:
                self.add_to_cart(cart)
            elif choice == 5:
                self.remove_from_cart(cart)
            elif choice == 6:
                self.checkout(cart)
    
    def browse_products(self, cart):
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Browse Products by Category")))
            print()
            
            # Create a menu for categories
            category_options = [category['name'] for category in self.products_data["categories"]]
            category_options.append("Back to Menu")
            
            category_menu = Menu("Select a Category", category_options)
            cat_idx = category_menu.display()
            
            if cat_idx is None or cat_idx == len(category_options) - 1:
                return
            
            # Display products in the selected category
            with self.term.fullscreen():
                print(self.term.clear)
                category = self.products_data["categories"][cat_idx]
                print(self.term.move_y(2) + self.term.center(self.term.bold(f"{category['name']} Products")))
                print()
                
                if not category["products"]:
                    print(self.term.center("No products available in this category"))
                    input(self.term.center("Press Enter to continue..."))
                    return
                
                product_options = [f"{p['id']}: {p['name']} - ${p['price']} (Stock: {p['stock']})" 
                                for p in category["products"]]
                product_options.append("Back to Categories")
                
                product_menu = Menu("Select a Product to Add to Cart", product_options)
                prod_idx = product_menu.display()
                
                if prod_idx is None or prod_idx == len(product_options) - 1:
                    return
                
                # Add selected product to cart
                product = category["products"][prod_idx]
                self.add_specific_product_to_cart(cart, product["id"])
    
    def search_products(self, cart):
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Search Products")))
            print()
            
            print(self.term.center("Enter search term: "), end="")
            search_term = input().lower()
            found_products = []
            
            for category in self.products_data["categories"]:
                for product in category["products"]:
                    if (search_term in product["name"].lower() or 
                        search_term in product["description"].lower() or
                        search_term in " ".join(product["tags"]).lower()):
                        found_products.append(product)
            
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
            self.add_specific_product_to_cart(cart, product["id"])
    
    def view_featured_products(self, cart):
        with self.term.fullscreen():
            print(self.term.clear)
            featured_ids = self.products_data["featured_products"]
            
            if not featured_ids:
                print(self.term.center(self.term.red("No featured products available.")))
                input(self.term.center("Press Enter to continue..."))
                return
            
            featured_products = []
            for featured_id in featured_ids:
                product = self.find_product_by_id(featured_id)
                if product:
                    featured_products.append(product)
            
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
            self.add_specific_product_to_cart(cart, product["id"])
    
    def find_product_by_id(self, prod_id):
        for category in self.products_data["categories"]:
            for product in category["products"]:
                if product["id"] == prod_id:
                    return product
        return None
    
    def add_specific_product_to_cart(self, cart, prod_id):
        product = self.find_product_by_id(prod_id)
        
        if not product:
            with self.term.fullscreen():
                print(self.term.clear)
                print(self.term.center(self.term.red(f"Product with ID {prod_id} not found.")))
                input(self.term.center("Press Enter to continue..."))
            return
        
        if product["stock"] <= 0:
            with self.term.fullscreen():
                print(self.term.clear)
                print(self.term.center(self.term.red("This product is out of stock.")))
                input(self.term.center("Press Enter to continue..."))
            return
        
        # Convert JSON product to Product object
        product_obj = Product(
            product["id"], 
            product["name"], 
            product["price"],
            product["description"],
            product["stock"],
            product["image_url"],
            product["specifications"],
            product["ratings"],
            product["tags"]
        )
        
        cart.add_item(product_obj)
        
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.center(self.term.green(f"{product['name']} added to your cart!")))
            input(self.term.center("Press Enter to continue..."))
    
    def add_to_cart(self, cart):
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Add to Cart")))
            print()
            
            print(self.term.center("Enter Product ID: "), end="")
            prod_id = input()
            self.add_specific_product_to_cart(cart, prod_id)
    
    def view_cart(self, cart):
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Your Cart")))
            print()
            
            items = cart.get_items()
            
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
    
    def remove_from_cart(self, cart):
        items = cart.get_items()
        
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
        cart.remove_item(prod_id)
        
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.center(self.term.green("Item removed from cart.")))
            input(self.term.center("Press Enter to continue..."))
    
    def checkout(self, cart):
        items = cart.get_items()
        
        if not items:
            with self.term.fullscreen():
                print(self.term.clear)
                print(self.term.center("Your cart is empty."))
                input(self.term.center("Press Enter to continue..."))
            return
        
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
                return
            
            # In a real app, we would process payment here
            print(self.term.center("\nProcessing your order..."))
            
            # Update stock
            for item in items:
                product = self.find_product_by_id(item.id)
                if product:
                    product["stock"] -= 1
            
            self.save_json(self.products_file, self.products_data)
            
            # Add to order history
            for user in self.users_data["users"]:
                if user["username"] == self.current_user.username:
                    order_id = f"order{len(user['order_history']) + 1}"
                    user["order_history"].append(order_id)
                    self.save_json(self.users_file, self.users_data)
                    break
            
            print(self.term.center(self.term.green("Order completed! Thank you for your purchase.")))
            cart.clear()
            input(self.term.center("Press Enter to continue..."))

# Run the application if this file is executed directly
if __name__ == "__main__":
    term = Terminal()
    print(term.clear)
    print(term.move_y(2) + term.center(term.bold(f"WebStore App v{VERSION}")))
    print(term.center("Interactive CLI Menu System"))
    print(term.center("-------------------------"))
    print()
    print(term.center("Starting application..."))
    print()
    
    # Check if git is initialized
    if not os.path.exists(os.path.join(current_dir, '.git')):
        print(term.center(term.yellow("Git repository not initialized.")))
        print(term.center(term.yellow("Run 'git init' to create a new repository.")))
        print()
    
    input(term.center("Press Enter to continue..."))
    
    controller = CLIController()
    controller.run()
