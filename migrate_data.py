#!/usr/bin/env python3
"""
Migration Script
--------------
This script migrates user data from the old format (users.json with both users and admins)
to the new format (separate users.json and admins.json files).

Usage:
    ./migrate_data.py
"""

import json
import os
import sys

def migrate_user_data():
    """Migrate users and admins to separate files"""
    print("Starting user data migration...")
    
    # Paths
    users_file = os.path.join(os.path.dirname(__file__), 'users.json')
    admins_file = os.path.join(os.path.dirname(__file__), 'admins.json')
    
    # Check if migration is needed
    if os.path.exists(admins_file):
        print(f"Admins file {admins_file} already exists. No migration needed.")
        return
    
    # Load old users.json
    try:
        with open(users_file, 'r') as file:
            old_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Could not load {users_file} or file is empty.")
        return
    
    # Check if old format (contains both users and admins)
    if "users" in old_data and "admins" in old_data:
        print(f"Found old format with users and admins in {users_file}")
        
        # Extract admins to new file
        admins_data = {"admins": old_data["admins"]}
        
        # Keep only users in users file
        users_data = {"users": old_data["users"]}
        
        # Save new files
        try:
            with open(admins_file, 'w') as file:
                json.dump(admins_data, file, indent=2)
            print(f"Created {admins_file} with {len(admins_data['admins'])} admins")
            
            with open(users_file, 'w') as file:
                json.dump(users_data, file, indent=2)
            print(f"Updated {users_file} with {len(users_data['users'])} users")
            
            print("Migration completed successfully.")
        except Exception as e:
            print(f"Error during migration: {str(e)}")
    else:
        print(f"File {users_file} already uses new format or has unexpected structure.")
        
        # If no admins file exists, create default
        if not os.path.exists(admins_file):
            default_admins = {
                "admins": [
                    {
                        "id": "admin1",
                        "username": "admin",
                        "password": "admin123",
                        "email": "admin@webstore.com",
                        "is_admin": True,
                        "permissions": ["manage_products", "view_reports"],
                        "created_at": "2025-05-26T00:00:00Z",
                        "last_login": None
                    }
                ]
            }
            
            try:
                with open(admins_file, 'w') as file:
                    json.dump(default_admins, file, indent=2)
                print(f"Created {admins_file} with default admin account")
            except Exception as e:
                print(f"Error creating default admin file: {str(e)}")

if __name__ == "__main__":
    migrate_user_data()
