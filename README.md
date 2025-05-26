# WebStore App - Interactive CLI Menu System

A command-line interface for managing products and users in a web store application. 
Features an interactive menu system with arrow key navigation and colored UI (orange background with black text).

## Features

- Interactive menu with arrow key navigation
- Orange background with black text for selected menu items
- User registration and login system
- Admin interface for product management
- Customer interface for shopping
- Product search and browsing
- Shopping cart functionality
- Checkout process

## Requirements

- Python 3.6 or higher
- Virtual environment (created automatically)
- Required packages (installed automatically):
  - blessed
  - wcwidth

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd webstore-app
   ```

2. Run the application:
   ```
   ./menu_cli.py
   ```

The application will automatically:
- Check for and create a `requirements.txt` file if needed
- Check for and create a `.gitignore` file if needed
- Set up a virtual environment if needed
- Install required packages if needed

## Usage

### Command-line options

```
./menu_cli.py [options]

Options:
  -h, --help     Show help message and exit
  -v, --version  Show version and exit
  --init         Initialize repository with requirements.txt and .gitignore
```

### User types

1. **Regular users** can:
   - Browse products by category
   - Search for products
   - Add products to cart
   - View and manage their cart
   - Checkout

2. **Admin users** can:
   - Add new products
   - Delete existing products
   - List products by category
   - Update product details

## Project Structure

```
webstore-app/
├── menu_cli.py         # Main application file
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore file
├── products.json       # Product data
└── users.json          # User data
```

## License

This project is released under the MIT License.
