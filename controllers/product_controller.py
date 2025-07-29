from models.base import get_db
from models.product import Product
from models.category import Category

class ProductController:
    def __init__(self):
        self.db = get_db()
    
    def get_all_products(self):
        return self.db.query(Product).filter(Product.is_active == True).all()
    
    def get_products_by_category(self, category_id):
        return self.db.query(Product).filter(
            Product.category_id == category_id,
            Product.is_active == True
        ).all()
    
    def get_all_categories(self):
        return self.db.query(Category).all()
    
    def add_product(self, name, description, price, category_id):
        product = Product(
            name=name,
            description=description,
            price=price,
            category_id=category_id
        )
        self.db.add(product)
        self.db.commit()
        return product

