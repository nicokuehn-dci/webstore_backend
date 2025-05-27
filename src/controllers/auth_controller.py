"""
Authentication Controller
-----------------------
Handles user authentication, registration, and session management.
"""

import json
import os

from src.models.user import User
from src.views.menu import Menu

class AuthController:
    def __init__(self, term):
        self.term = term
        self.users_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'users.json')
        self.admins_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'admins.json')
        self.users_data = self.load_users_json()
        self.admins_data = self.load_admins_json()
        self.current_user = None

    def load_users_json(self):
        """Load user data from JSON file"""
        try:
            with open(self.users_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"users": []}

    def load_admins_json(self):
        """Load admin data from JSON file"""
        try:
            with open(self.admins_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Create default admin list if file doesn't exist
            default_data = {
                "admins": [
                    {
                        "id": "admin1",
                        "username": "admin",
                        "password": "admin123",  # In a real app, this would be hashed
                        "email": "admin@webstore.com",
                        "is_admin": True,
                        "permissions": ["manage_products", "view_reports"],
                        "created_at": "2025-05-26T00:00:00Z",
                        "last_login": None
                    }
                ]
            }
            self.save_admins_json(default_data)
            return default_data

    def save_users_json(self, data):
        """Save user data to JSON file"""
        with open(self.users_file, 'w') as file:
            json.dump(data, file, indent=2)
    
    def save_admins_json(self, data):
        """Save admin data to JSON file"""
        with open(self.admins_file, 'w') as file:
            json.dump(data, file, indent=2)

    def register_user(self):
        """Register a new user (customer only, no admin registration)"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Register New User")))
            print()
            
            username = Menu.get_centered_input(self.term, "Username:")
            password = Menu.get_centered_input(self.term, "Password:")  # In a real app, use getpass to hide input
            email = Menu.get_centered_input(self.term, "Email:")
            
            # Check if username already exists in users
            for user in self.users_data["users"]:
                if user["username"] == username:
                    print(self.term.center(self.term.red("Username already exists. Please choose another.")))
                    input(self.term.center("Press Enter to continue..."))
                    return None
            
            # Check if username exists in admins
            for admin in self.admins_data["admins"]:
                if admin["username"] == username:
                    print(self.term.center(self.term.red("Username already exists. Please choose another.")))
                    input(self.term.center("Press Enter to continue..."))
                    return None
            
            # Create new user (always as a regular user, not admin)
            user_id = f"user{len(self.users_data['users']) + 1}"
            
            new_user = {
                "id": user_id,
                "username": username,
                "password": password,  # In a real app, this would be hashed
                "email": email,
                "is_admin": False,
                "created_at": "2025-05-26T00:00:00Z",  # Current date (hardcoded for simplicity)
                "last_login": None,
                "shipping_address": {},
                "order_history": []
            }
            
            self.users_data["users"].append(new_user)
            self.save_users_json(self.users_data)
            
            print(self.term.center(self.term.green(f"User {username} registered successfully!")))
            input(self.term.center("Press Enter to continue..."))
            
            # Return a User object
            return User(new_user["id"], new_user["username"], new_user["password"], 
                       new_user["email"], new_user["is_admin"])

    def login(self):
        """Authenticate a user or admin"""
        with self.term.fullscreen():
            print(self.term.clear)
            print(self.term.move_y(2) + self.term.center(self.term.bold("Login")))
            print()
            
            username = Menu.get_centered_input(self.term, "Username:")
            password = Menu.get_centered_input(self.term, "Password:")  # In a real app, use getpass
            
            # Check regular users
            for user in self.users_data["users"]:
                if user["username"] == username and user["password"] == password:
                    user_obj = User(user["id"], user["username"], user["password"], 
                                   user.get("email"), False)
                    
                    # Update last login
                    user["last_login"] = "2025-05-26T00:00:00Z"
                    self.save_users_json(self.users_data)
                    
                    print(self.term.center(self.term.green(f"Welcome, {username}!")))
                    input(self.term.center("Press Enter to continue..."))
                    return user_obj
            
            # Check admin users
            for admin in self.admins_data["admins"]:
                if admin["username"] == username and admin["password"] == password:
                    admin_obj = User(admin["id"], admin["username"], admin["password"], 
                                    admin.get("email"), True)
                    
                    # Update last login
                    admin["last_login"] = "2025-05-26T00:00:00Z"
                    self.save_admins_json(self.admins_data)
                    
                    print(self.term.center(self.term.green(f"Welcome, Admin {username}!")))
                    input(self.term.center("Press Enter to continue..."))
                    return admin_obj
            
            print(self.term.center(self.term.red("Invalid credentials.")))
            input(self.term.center("Press Enter to continue..."))
            return None

    def logout(self):
        """Log out the current user"""
        self.current_user = None