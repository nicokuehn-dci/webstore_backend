"""
Admin View
---------
Handles admin interface display components.
"""

from blessed import Terminal
from src.views.menu import Menu

class AdminView:
    def __init__(self, term, product_controller):
        self.term = term
        self.product_controller = product_controller
    
    def show_admin_menu(self, username):
        """Main admin menu with hierarchical submenus"""
        # Show quick help on first login
        self.display_admin_help()
        
        while True:
            # Main admin menu with categorized options and emoji icons
            admin_menu = Menu(f"Admin Menu - {username}", [
                "📦 Product Management",
                "📊 Reports & Statistics",
                "🔧 Settings",
                "❓ Help",
                "🚪 Logout"
            ])
            choice = admin_menu.display()
            
            if choice is None or choice == 4:  # Logout option or 'q' pressed
                break
            elif choice == 0:  # Product Management
                self.product_management_menu()
            elif choice == 1:  # Reports & Statistics
                self.show_reports_menu()
            elif choice == 2:  # Settings
                self.settings_menu()
            elif choice == 3:  # Help
                self.display_admin_help()
    
    def product_management_menu(self):
        """Submenu for product management options"""
        while True:
            product_menu = Menu("Product Management", [
                "➕ Add New Product",
                "✏️ Update Product",
                "❌ Delete Product",
                "📋 List Products by Category",
                "🔍 Search Products",
                "🏷️ Manage Featured Products",
                "⬅️ Back to Admin Menu"
            ])
            choice = product_menu.display()
            
            if choice is None or choice == 6:  # Back option or 'q' pressed
                return
            elif choice == 0:  # Add New Product
                self.show_add_product()
            elif choice == 1:  # Update Product
                self.show_update_product()
            elif choice == 2:  # Delete Product
                self.show_delete_product()
            elif choice == 3:  # List Products by Category
                self.show_list_products()
            elif choice == 4:  # Search Products
                self.show_search_products()
            elif choice == 5:  # Manage Featured Products
                self.show_featured_products()
    
    def show_reports_menu(self):
        """Display reports and statistics menu"""
        while True:
            report_menu = Menu("Reports & Statistics", [
                "📊 Sales Summary",
                "📦 Inventory Status",
                "👤 Customer Activity",
                "⭐ Popular Products",
                "⬅️ Back to Admin Menu"
            ])
            choice = report_menu.display()
            
            if choice is None or choice == 4:  # Back option or 'q' pressed
                return
                
            # Currently all report options show the same placeholder
            self.show_reports_placeholder()
    
    def settings_menu(self):
        """Display settings menu"""
        while True:
            settings_menu = Menu("Settings", [
                "👤 User Profiles",
                "🎨 Interface Preferences",
                "🔐 Security Settings",
                "💾 Backup & Restore",
                "💾 Save All Changes",
                "⬅️ Back to Admin Menu"
            ])
            choice = settings_menu.display()
            
            if choice is None or choice == 5:  # Back option or 'q' pressed
                return
            elif choice == 4:  # Save All Changes
                self.save_all_changes()
            else:
                # Currently all other settings options show the same placeholder
                self.show_settings_placeholder()
    
    def save_all_changes(self):
        """Save all changes to JSON files"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Save All Changes")))
            print()
            
            print(self.term.center("Saving product data..."))
            self.product_controller.save_product_data()
            
            print(self.term.center(self.term.green("All changes have been saved successfully!")))
            input(self.term.center("Press Enter to continue..."))
    
    def display_admin_help(self):
        """Display help information for admin users"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Admin Help Guide")))
            print()
            
            print(self.term.center("Welcome to the WebStore Admin Panel"))
            print()
            
            # Main menu navigation
            print(self.term.bold(self.term.center("🧭 Navigation:")))
            print(self.term.center("- Use ↑/↓ arrow keys, j/k, or w/s to navigate through menu options"))
            print(self.term.center("- Press Enter or Space to select an option"))
            print(self.term.center("- Press 'q' or ESC to go back or quit a menu"))
            print()
            
            # Admin menu structure help
            print(self.term.bold(self.term.center("📋 Admin Menu Structure:")))
            print(self.term.center("- Product Management: All product-related operations"))
            print(self.term.center("- Reports & Statistics: View sales and inventory reports"))
            print(self.term.center("- Settings: Configure application settings"))
            print(self.term.center("- Help: Display this help screen"))
            print()
            
            # Product Management help
            print(self.term.bold(self.term.center("📦 Product Management:")))
            print(self.term.center("- Add Product: Create new products with unique IDs"))
            print(self.term.center("  (Use prefixes: e=Electronics, c=Clothing, h=Home, b=Books)"))
            print(self.term.center("- Update Product: Modify existing product details"))
            print(self.term.center("- Delete Product: Remove products from inventory"))
            print(self.term.center("- List Products: Browse products by category"))
            print(self.term.center("- Search Products: Find products by name, ID or tags"))
            print(self.term.center("- Featured Products: Manage special product lists"))
            print()
            
            # Tips
            print(self.term.bold(self.term.center("💡 Quick Tips:")))
            print(self.term.center("- Add meaningful product descriptions for better search results"))
            print(self.term.center("- Use comma-separated tags (e.g., 'premium, sale, new')"))
            print(self.term.center("- Keep inventory up to date by regularly checking stock levels"))
            print(self.term.center("- Feature your best products to increase visibility"))
            print(self.term.center("- All menus support keyboard navigation with various keys"))
            print()
            
            # Help message
            help_menu = Menu("Continue", ["Return to Admin Menu"])
            help_menu.display()
            
            # Help message
            help_menu = Menu("Continue", ["Return to Admin Menu"])
            help_menu.display()

    def show_reports_placeholder(self):
        """Display placeholder for reports feature"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Reports & Statistics")))
            print()
            print(self.term.center(self.term.yellow("This feature is coming soon!")))
            print(self.term.center("Future reports will include:"))
            print(self.term.center("- Sales reports"))
            print(self.term.center("- Inventory status"))
            print(self.term.center("- Customer activity"))
            print(self.term.center("- Popular products"))
            input(self.term.center("\nPress Enter to return to Reports Menu..."))

    def show_settings_placeholder(self):
        """Display placeholder for settings feature"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Settings")))
            print()
            print(self.term.center(self.term.yellow("This feature is coming soon!")))
            print(self.term.center("Future settings will include:"))
            print(self.term.center("- User profile settings"))
            print(self.term.center("- Application preferences"))
            print(self.term.center("- Theme customization"))
            print(self.term.center("- Backup and restore"))
            input(self.term.center("\nPress Enter to return to Settings Menu..."))
    
    # Product management methods (placeholders for now)
    def show_add_product(self):
        """Show add product form"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.center(self.term.yellow("Add Product functionality will be implemented soon.")))
            input(self.term.center("\nPress Enter to return..."))
    
    def show_update_product(self):
        """Show update product form"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.center(self.term.yellow("Update Product functionality will be implemented soon.")))
            input(self.term.center("\nPress Enter to return..."))
    
    def show_delete_product(self):
        """Show delete product form"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.center(self.term.yellow("Delete Product functionality will be implemented soon.")))
            input(self.term.center("\nPress Enter to return..."))
    
    def show_list_products(self):
        """Show list products form"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.center(self.term.yellow("List Products functionality will be implemented soon.")))
            input(self.term.center("\nPress Enter to return..."))
    
    def show_search_products(self):
        """Show search products form"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.center(self.term.yellow("Search Products functionality will be implemented soon.")))
            input(self.term.center("\nPress Enter to return..."))
    
    def show_featured_products(self):
        """Show featured products form"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.center(self.term.yellow("Featured Products functionality will be implemented soon.")))
            input(self.term.center("\nPress Enter to return..."))
