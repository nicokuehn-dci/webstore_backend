"""
Product Model
-----------
Defines the Product class for the WebStore application.
"""

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
