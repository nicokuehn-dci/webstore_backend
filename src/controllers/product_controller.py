"""
Product Controller
----------------
Handles product management operations.
"""

import json
import os
from src.models.product import Product

class ProductController:
    def __init__(self, term):
        self.term = term
        self.products_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'products.json')
        self.products_data = self.load_json()
    
    def load_json(self):
        """Load product data from JSON file"""
        try:
            with open(self.products_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "categories": [], 
                "featured_products": [], 
                "new_arrivals": [], 
                "best_sellers": [], 
                "on_sale": []
            }
    
    def save_json(self):
        """Save product data to JSON file"""
        with open(self.products_file, 'w') as file:
            json.dump(self.products_data, file, indent=2)
    
    def find_product_by_id(self, prod_id):
        """Find a product by its ID"""
        for category in self.products_data["categories"]:
            for product in category["products"]:
                if product["id"] == prod_id:
                    return product
        return None
    
    def add_product(self, product_info):
        """Add a new product to the store"""
        # product_info should be a dictionary with product details
        category_index = product_info.pop("category_index")
        
        # Add to category
        if 0 <= category_index < len(self.products_data["categories"]):
            self.products_data["categories"][category_index]["products"].append(product_info)
            self.save_json()
            return True
        return False
    
    def update_product(self, product_id, field_name, new_value):
        """Update a specific field of a product"""
        product = self.find_product_by_id(product_id)
        if product:
            product[field_name] = new_value
            self.save_json()
            return True
        return False
    
    def delete_product(self, product_id):
        """Delete a product by ID"""
        deleted = False
        for category in self.products_data["categories"]:
            for i, product in enumerate(category["products"]):
                if product["id"] == product_id:
                    category["products"].pop(i)
                    deleted = True
                    break
            if deleted:
                break
        
        if deleted:
            # Also remove from featured lists
            for list_name in ["featured_products", "new_arrivals", "best_sellers", "on_sale"]:
                if product_id in self.products_data[list_name]:
                    self.products_data[list_name].remove(product_id)
            self.save_json()
            return True
        return False
    
    def get_all_products(self):
        """Get all products from all categories"""
        all_products = []
        for category in self.products_data["categories"]:
            for product in category["products"]:
                all_products.append({
                    "id": product["id"],
                    "name": product["name"],
                    "category": category["name"],
                    "price": product["price"],
                    "stock": product["stock"],
                    "description": product["description"],
                    "tags": product["tags"]
                })
        return all_products
    
    def get_products_by_category(self, category_index):
        """Get products from a specific category"""
        if 0 <= category_index < len(self.products_data["categories"]):
            return self.products_data["categories"][category_index]["products"]
        return []
    
    def get_categories(self):
        """Get all product categories"""
        return self.products_data["categories"]
    
    def search_products(self, search_term):
        """Search products by name, description, or tags"""
        search_term = search_term.lower()
        found_products = []
        
        for category in self.products_data["categories"]:
            for product in category["products"]:
                if (search_term in product["id"].lower() or
                    search_term in product["name"].lower() or 
                    search_term in product["description"].lower() or
                    search_term in " ".join(product["tags"]).lower()):
                    found_products.append({
                        "id": product["id"],
                        "name": product["name"],
                        "price": product["price"],
                        "stock": product["stock"],
                        "category": category["name"],
                        "description": product["description"],
                        "tags": product["tags"]
                    })
        return found_products
    
    def get_featured_products(self, list_type="featured_products"):
        """Get featured products of a specific type"""
        featured_ids = self.products_data[list_type]
        featured_products = []
        
        for featured_id in featured_ids:
            product = self.find_product_by_id(featured_id)
            if product:
                featured_products.append(product)
        
        return featured_products
    
    def toggle_featured_status(self, product_id, list_type="featured_products"):
        """Toggle whether a product is in a featured list"""
        if product_id in self.products_data[list_type]:
            self.products_data[list_type].remove(product_id)
            self.save_json()
            return False  # Now not featured
        else:
            self.products_data[list_type].append(product_id)
            self.save_json()
            return True  # Now featured
    
    def create_product_object(self, product_data):
        """Convert product data dictionary to Product object"""
        return Product(
            product_data["id"],
            product_data["name"],
            product_data["price"],
            product_data.get("description"),
            product_data.get("stock", 0),
            product_data.get("image_url"),
            product_data.get("specifications", {}),
            product_data.get("ratings", {"average": 0, "count": 0}),
            product_data.get("tags", [])
        )
    
    def save_product_data(self):
        """Save product data to JSON file with backup creation"""
        # Create a backup of current products.json
        try:
            backup_path = os.path.join(os.path.dirname(self.products_file), 'backup', 'products.json.bak')
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            with open(self.products_file, 'r') as src_file:
                with open(backup_path, 'w') as dst_file:
                    dst_file.write(src_file.read())
        except Exception as e:
            print(f"Backup creation error: {e}")
        
        # Save the current data
        self.save_json()
        return True