# WebStore App Handbook

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [User Types](#user-types)
5. [Customer Guide](#customer-guide)
6. [Administrator Guide](#administrator-guide)
7. [Data Management](#data-management)
8. [Tips & Best Practices](#tips--best-practices)
9. [Troubleshooting](#troubleshooting)

## Introduction

The WebStore App is a command-line interface (CLI) application for managing an online store. It features an interactive menu system with arrow key navigation and a color-coded user interface. The application supports both customer and administrator roles, with different capabilities for each.

### Key Features
- Interactive menu navigation with arrow keys
- Color-coded interface with orange highlighting
- User authentication and role-based access
- Product management system
- Shopping cart functionality
- Data persistence using JSON files

## Installation

1. **System Requirements**
   - Python 3.6 or higher
   - Terminal with color support
   - Linux/Unix environment recommended

2. **Dependencies**
   The following packages are required:
   ```
   blessed==1.21.0
   wcwidth==0.2.13
   ```

3. **Setup**
   ```bash
   git clone <repository-url>
   cd webstore-app
   chmod +x webstore.py
   ./webstore.py
   ```
   The application will automatically:
   - Create necessary configuration files
   - Set up a virtual environment
   - Install required dependencies

## Getting Started

### First Launch
1. Run the application:
   ```bash
   ./webstore.py
   ```
2. Choose one of the following options:
   - Register: Create a new customer account
   - Login: Access your existing account
   - Exit: Close the application

### Navigation
- Use ↑/↓ arrow keys, j/k, or w/s to navigate menus
- Press Enter or Space to select an option
- Press 'q' or ESC to go back or quit a menu

## User Types

### Customers
Regular users who can:
- Browse and search products
- View product details
- Add items to cart
- Manage shopping cart
- Complete checkout process

### Administrators
Management users who can:
- Manage product inventory
- Add/update/delete products
- Configure featured products
- View reports and statistics
- Access system settings

## Customer Guide

### Product Browsing
1. Login to your customer account
2. Choose from the following options:
   - "Browse Products": View products by category
   - "Search Products": Find specific items
   - "View Featured Products": See highlighted items

### Shopping Cart Management
1. Add items:
   - Select "Add to Cart"
   - Enter the product ID
   - Confirm the addition

2. View cart:
   - Select "View Cart"
   - Review items and total

3. Remove items:
   - Select "Remove from Cart"
   - Choose the item to remove

4. Checkout:
   - Select "Checkout"
   - Confirm your purchase
   - View order confirmation

### Saving Changes
- Select "Save Changes" to ensure your cart and order data is saved
- Always save before logging out

## Administrator Guide

### Product Management

1. Adding Products:
   - Select "Product Management" > "Add New Product"
   - Enter product details:
     - ID (use prefix: e=Electronics, c=Clothing, h=Home, b=Books)
     - Name
     - Description
     - Price
     - Stock quantity
     - Category
     - Specifications
     - Tags

2. Updating Products:
   - Select "Update Product"
   - Choose the product to modify
   - Update desired fields

3. Deleting Products:
   - Select "Delete Product"
   - Choose the product to remove
   - Confirm deletion

### Featured Products Management
1. Select "Manage Featured Products"
2. Choose list type:
   - Featured Products
   - New Arrivals
   - Best Sellers
   - On Sale
3. Add or remove products from lists

### Reports & Statistics
Access sales and inventory reports through:
1. Select "Reports & Statistics"
2. Choose report type:
   - Sales Summary
   - Inventory Status
   - Customer Activity
   - Popular Products

### Settings
1. User Profiles
2. Interface Preferences
3. Security Settings
4. Backup & Restore
5. Save All Changes

## Data Management

### File Structure
The application uses three main JSON files:
1. `users.json`: Customer accounts and data
2. `admins.json`: Administrator accounts and permissions
3. `products.json`: Product inventory and categories

### Data Backup
- Automatic backups are created before saving changes
- Backup files are stored in the `backup/` directory
- Manual backups can be created through Settings

### Saving Changes
- Administrators: Use "Save All Changes" in Settings menu
- Customers: Use "Save Changes" in main menu
- Changes are automatically saved after critical operations

## Tips & Best Practices

### For Customers
1. Regularly check featured products for deals
2. Save cart changes before logging out
3. Keep track of order history
4. Use search function for quick product finding

### For Administrators
1. Use meaningful product descriptions
2. Keep inventory levels updated
3. Add relevant tags to products
4. Regularly backup data
5. Use clear product IDs with category prefixes

## Troubleshooting

### Common Issues

1. **Login Problems**
   - Verify username and password
   - Check for correct case in username
   - Ensure you're using the correct account type

2. **Display Issues**
   - Ensure terminal supports colors
   - Check terminal size is adequate
   - Verify Python version compatibility

3. **Data Not Saving**
   - Check file permissions
   - Use explicit save options
   - Verify disk space availability

### Error Messages

- "Invalid credentials": Incorrect username or password
- "Username already exists": Choose a different username
- "No products available": Category or search returned no results
- "Product ID not found": Verify the product ID

### Getting Help
- Access the help guide through:
  - Customer Menu: Help option
  - Admin Menu: Help option
- View the README.md file for technical details
- Check the construction plan for system architecture

For additional support or to report issues, please contact the system administrator.
