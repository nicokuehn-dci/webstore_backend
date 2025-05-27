"""
User Model
---------
Defines the User class for the WebStore application.
"""

class User:
    def __init__(self, id, username, password, email=None, is_admin=False):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin
