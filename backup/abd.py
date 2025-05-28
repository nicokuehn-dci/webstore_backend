# Handles user authentication and registration logic
class AuthService:
    def __init__(self):
        self.users = []

    def register(self, username, password, is_admin=False):
        if not any(user.username == username for user in self.users):
            self.users.append(User(username, password, is_admin))
            return True
        return False

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user            
        return None

# Manages product data, including adding, deleting, and listing products
class ProductService:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        if not any(p.id == product.id for p in self.products):
            self.products.append(product)
            return True
        return False

    def delete_product(self, product_id):
        self.products = [p for p in self.products if p.id != product_id]

    def list_products(self):
        return self.products.copy()

# Manages operations related to a user's shopping cart
class CartService:
    def __init__(self, cart):
        self.cart = cart

    def add_to_cart(self, product):
        self.cart.add_product(product)

    def remove_from_cart(self, product_id):
        self.cart.remove_product(product_id)

    def show_cart(self):
        return self.cart.list_items()

# calculating order summaries (subtotal, tax, discount) and printing receipts
class OrderService:
    def __init__(self, product_service):
        self.product_service = product_service
        self.tax_rate = 0.19
        self.discount_tiers = [(200, 0.2), (100, 0.1)] 

    def calculate_order_summary(self, shopping_cart):
        if not hasattr(shopping_cart, 'is_empty') or shopping_cart.is_empty():
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

        for item_in_cart_name, qty in shopping_cart.get_items():
            product = next((p for p in self.product_service.list_products() if p.name == item_in_cart_name), None)
            if product:
                item_price = product.price
                item_total = item_price * qty
                subtotal += item_total
                order_details.append({
                    'name': product.name,
                    'price': item_price,
                    'quantity': qty,
                    'item_total': item_total
                })
            else:
                print(f"Warning: Product '{item_in_cart_name}' not found in available products. Skipping.")

        tax = subtotal * self.tax_rate
        total_with_tax = subtotal + tax

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

    def print_receipt(self, summary):
        print("\n--- Receipt ---")
        
        if not summary['order_details']:
            print("Your cart was empty. No items to display.")
            print("Thank you for shopping!\n")
            return

        for item in summary['order_details']:
            print(f"{item['name']}: {item['price']:.2f} * {item['quantity']} = {item['item_total']:.2f}€")

        print(f"Subtotal: {summary['subtotal']:.2f}€")
        print(f"Tax ({int(self.tax_rate * 100)}%): {summary['tax']:.2f}€")
        print(f"Total with tax: {summary['total_with_tax']:.2f}€")
        print(f"Discount: {summary['discount']:.2f}€")
        print(f"Discount percentage: {summary['discount_percentage']}")
        print(f"Final total: {summary['final']:.2f}€")
        print("Thank you for shopping!\n")